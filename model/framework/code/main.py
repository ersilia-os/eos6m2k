# imports
import os
import sys
import csv
from mole_antimicrobial_prediction import MoleAntimicrobialPredictor

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
tmp_file = input_file.replace(".csv", '_tmp.csv')

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# read smiles and create tmp file
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [r[0] for r in reader]

with open(tmp_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["input"])
    for s in smiles_list:
        writer.writerow([s])

# make predictions
predictor = MoleAntimicrobialPredictor()
df = predictor.run(input_file, output_file)

# Change output format
df.to_csv(output_file, sep=',', index=False)

# Remove tmp file
os.remove(tmp_file)