import os
import sys
import csv
import numpy as np
from ersilia_pack_utils.core import read_smiles, write_out
from mole_antimicrobial_prediction import MoleAntimicrobialPredictor

input_file = sys.argv[1]
output_file = sys.argv[2]
root = os.path.dirname(os.path.abspath(__file__))

_, smiles_list = read_smiles(input_file)

tmp_file = os.path.join(os.path.dirname(os.path.abspath(output_file)), "mole_input_tmp.csv")
with open(tmp_file, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["smiles"])
    for s in smiles_list:
        writer.writerow([s])

predictor = MoleAntimicrobialPredictor()
df = predictor.run(tmp_file, output_file)

header = list(df.columns)
results = df.values.tolist()
write_out(results, header, output_file, np.float32)

os.remove(tmp_file)
