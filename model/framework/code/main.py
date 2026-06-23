# imports
import os
import sys
import csv
import numpy as np
from ersilia_pack_utils.core import read_smiles, write_out
from mole_antimicrobial_prediction import MoleAntimicrobialPredictor

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# Read SMILES robustly from the Ersilia-provided input (handles any column layout)
_, smiles_list = read_smiles(input_file)

# Write an intermediate file in the format the predictor expects: the predictor's
# reader is tab-separated and keys on a "smiles" column.
tmp_file = os.path.join(os.path.dirname(os.path.abspath(output_file)), "mole_input_tmp.csv")
with open(tmp_file, "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["smiles"])
    for s in smiles_list:
        writer.writerow([s])

# make predictions
predictor = MoleAntimicrobialPredictor()
df = predictor.run(tmp_file, output_file)

# Write output through the Ersilia standard writer (consumed by the serving layer)
header = list(df.columns)
results = df.values.tolist()
write_out(results, header, output_file, np.float32)

# Remove tmp file
os.remove(tmp_file)
