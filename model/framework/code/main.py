# imports
import os
import csv
import sys
import subprocess
from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
print(root)

# in this model, the file mole_antimicrobial_prediction.py takes care of everything

cmd = [
    "python",
    "mole_antimicrobial_prediction.py",
    os.path.join(root, "..", input_file),  # input file
    os.path.join(root, "..", output_file),  # output file
    "--smiles_input",  # flag to indicate SMILES input
    "--smiles_colname", "input",  # column name for SMILES
    "--mole_model", "../../checkpoints",  # path to the folder with the Mole models for compound representation
    "--strain_categories", "../../checkpoints/maier_screening_results.tsv.gz",  # path to the TSV file with the strain categories
    "--xgboost_model", "../../checkpoints/MolE-XGBoost-08.03.2024_14.20.pkl"  # path to the XGBoost model
]

subprocess.run(cmd, cwd=root)