# imports
import os
import sys
import csv
import traceback
import numpy as np
from ersilia_pack_utils.core import read_smiles, write_out
from mole_antimicrobial_prediction import MoleAntimicrobialPredictor

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# --- TEMP DIAGNOSTIC: log exactly what the serve passes and what happens ---
def _diag(msg):
    try:
        with open("/tmp/main_diag.log", "a") as _d:
            _d.write(msg + "\n")
    except Exception:
        pass

_diag("==== main.py invoked ====")
_diag("argv: %r" % (sys.argv,))
try:
    _diag("INPUT FILE (%s):\n%s" % (input_file, open(input_file).read()))
except Exception as _e:
    _diag("could not read input_file: %r" % _e)

try:
    # Read SMILES robustly from the Ersilia-provided input (handles any column layout)
    _, smiles_list = read_smiles(input_file)
    _diag("read_smiles -> %d smiles: %r" % (len(smiles_list), smiles_list[:3]))

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
    _diag("df shape: %s; head row: %r" % (df.shape, df.iloc[0].tolist()[:5] if len(df) else "EMPTY"))

    # Write output through the Ersilia standard writer (consumed by the serving layer)
    header = list(df.columns)
    results = df.values.tolist()
    write_out(results, header, output_file, np.float32)

    # Remove tmp file
    os.remove(tmp_file)
    _diag("==== main.py completed OK ====")
except Exception:
    _diag("EXCEPTION:\n" + traceback.format_exc())
    raise
