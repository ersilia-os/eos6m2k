import os
import re
import pickle
import torch
import numpy as np
import pandas as pd
from scipy.stats.mstats import gmean
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
from pathlib import Path

chkpt_root = Path(__file__).parent.parent.parent

class MoleAntimicrobialPredictor:
    def __init__(
        self,
        smiles_input=True,
        smiles_colname="input",
        chemid_colname="chem_id",
        xgboost_model=os.path.join(chkpt_root, "checkpoints/MolE-XGBoost-08.03.2024_14.20.pkl"),
        mole_model=os.path.join(chkpt_root, "checkpoints"),
        aggregate_scores=False,
        app_threshold=0.04374140128493309,
        min_nkill=10,
        strain_categories=os.path.join(chkpt_root, "checkpoints/maier_screening_results.tsv.gz"),
        gram_information=os.path.join(chkpt_root, "checkpoints/strain_info_SF2.xlsx"),
        device="auto",
    ):
        self.smiles_input = smiles_input
        self.smiles_colname = smiles_colname
        self.chemid_colname = chemid_colname
        self.xgboost_model = xgboost_model
        self.mole_model = mole_model
        self.aggregate_scores = aggregate_scores
        self.app_threshold = app_threshold
        self.min_nkill = min_nkill
        self.strain_categories = strain_categories
        self.gram_information = gram_information
        if device == "auto" and smiles_input:
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device


    def _read_representation(self, input_filepath):
        if self.smiles_input:
            from mole_representation import process_representation
            return process_representation(
                dataset_path=input_filepath,
                smile_column_str=self.smiles_colname,
                id_column_str=self.chemid_colname,
                pretrained_dir=self.mole_model,
                device=self.device,
            )
        else:
            return pd.read_csv(input_filepath, sep='\t', index_col=0)

    def _prep_ohe(self, categories):
        ohe = OneHotEncoder(sparse=False)
        ohe.fit(pd.DataFrame(categories))
        return pd.DataFrame(ohe.transform(pd.DataFrame(categories)), columns=categories, index=categories)

    def _add_strains(self, chemfeats_df, screen_path):
        maier_screen = pd.read_csv(screen_path, sep='\t', index_col=0)
        ohe_df = self._prep_ohe(maier_screen.columns)
        chemfe = chemfeats_df.reset_index().rename(columns={"index": "chem_id"})
        chemfe["chem_id"] = chemfe["chem_id"].astype(str)
        sohe = ohe_df.reset_index().rename(columns={"index": "strain_name"})
        xpred = chemfe.merge(sohe, how="cross")
        xpred["ids"] = xpred["chem_id"].str.cat(xpred["strain_name"], sep=" --- ")
        xpred = xpred.set_index("ids").drop(columns=["chem_id", "strain_name"])
        assert xpred.shape[0] == (chemfeats_df.shape[0] * ohe_df.shape[0])
        assert xpred.shape[1] == (chemfeats_df.shape[1] + ohe_df.shape[1])
        return xpred

    def _load_xgb_model(self, xgb_path):
        with open(xgb_path, "rb") as file:
            return pickle.load(file)

    def _gram_stain(self, label_df, strain_info_df):
        df_label = label_df.copy()
        df_label["nt_number"] = df_label["strain_name"].apply(lambda x: re.search(".*?\((NT\d+)\)", x).group(1))
        gram_dict = strain_info_df[["Gram stain"]].to_dict()["Gram stain"]
        df_label["gram_stain"] = df_label["nt_number"].apply(gram_dict.get)
        return df_label

    def _antimicrobial_potential(self, score_df, strain_filepath):
        maier_strains = pd.read_excel(
            strain_filepath,
            skiprows=[0,1,43,44,45,46,47,48,49,50,51,52,53,54],
            index_col="NT data base",
        )
        score_df["pred_id"] = score_df['ids']
        score_df["chem_id"] = score_df["pred_id"].str.split(" --- ", expand=True)[0]
        score_df["strain_name"] = score_df["pred_id"].str.split(" --- ", expand=True)[1]
        pred_df = self._gram_stain(score_df, maier_strains)
        # apscore_total = pred_df.groupby("chem_id")["1"].apply(gmean).to_frame().rename(columns={"1": "apscore_total"})
        apscore_total = pred_df.groupby("chem_id")["antimicrobial_predictive_probability"].apply(gmean).to_frame().rename(columns={"antimicrobial_predictive_probability": "apscore_total"})
        apscore_total["apscore_total"] = np.log2(apscore_total["apscore_total"])
        apscore_gram = pred_df.groupby(["chem_id", "gram_stain"])["antimicrobial_predictive_probability"].apply(gmean).unstack().rename(columns={"negative": "apscore_gnegative","positive": "apscore_gpositive"})
        apscore_gram["apscore_gnegative"] = np.log2(apscore_gram["apscore_gnegative"])
        apscore_gram["apscore_gpositive"] = np.log2(apscore_gram["apscore_gpositive"])
        # inhibted_total = pred_df.groupby("chem_id")["growth_inhibition"].sum().to_frame().rename(columns={"growth_inhibition": "ginhib_total"})
        # inhibted_gram = pred_df.groupby(["chem_id", "gram_stain"])["growth_inhibition"].sum().unstack().rename(columns={"negative": "ginhib_gnegative","positive": "ginhib_gpositive"})
        # return apscore_total.join(apscore_gram).join(inhibted_total).join(inhibted_gram)
        return apscore_total.join(apscore_gram)

    def predict(self, input_filepath):
        udl_representation = self._read_representation(input_filepath)
        smiles = udl_representation.index.tolist()
        X_input = self._add_strains(udl_representation, self.strain_categories)
        model_abx = self._load_xgb_model(self.xgboost_model)
        y_pred = model_abx.predict_proba(X_input)
        pred_df = pd.DataFrame(y_pred, columns=["0","1"], index=X_input.index)
        pred_df = pred_df.drop(columns=["0"]).rename(columns={"1": "antimicrobial_predictive_probability"})
        # pred_df["growth_inhibition"] = pred_df["1"].apply(lambda x: 1 if x >= args.app_threshold else 0)
        pred_df_ = pd.DataFrame(pred_df).reset_index()
        agg_df = self._antimicrobial_potential(pred_df_, self.gram_information)
        # agg_df["broad_spectrum"] = agg_df["ginhib_total"].apply(lambda x: 1 if x >= args.min_nkill else 0)
        agg_df = agg_df.to_dict(orient="index")
        probs = {}
        features = set()
        for i, j in zip(pred_df.index, pred_df["antimicrobial_predictive_probability"]):
            smi, feat = i.split(" --- ")
            feat = feat.lower().replace(" ", "_").replace("(", "").replace(")", "")
            features.add(feat)
            if smi not in probs:
                probs[smi] = {}
            probs[smi][feat] = j
        rows = []
        features = sorted(features)
        for smi in smiles:
            p = [probs[smi][feat] for feat in features]
            p_global = [agg_df[smi]["apscore_total"], agg_df[smi]["apscore_gpositive"], agg_df[smi]["apscore_gnegative"]]
            rows.append([smi] + p_global + p)
        df = pd.DataFrame(rows, columns=["smiles"] + ["apscore_total", "apscore_gpositive", "apscore_gnegative"] + features).drop(columns=["smiles"])
        return df

    def run(self, input_filepath, output_filepath):
        df = self.predict(input_filepath)
        df.to_csv(output_filepath, sep=',', index=False)
        return output_filepath