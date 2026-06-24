import sys as _sys
try:
    open("/tmp/main_diag.log", "a").write("MAIN_INVOKED argv=%r\n" % (_sys.argv,))
except Exception:
    pass

# imports (wrapped to catch import-time crashes during serve)
try:
    import os
    import sys
    import csv
    import traceback
    import numpy as np
    open("/tmp/main_diag.log", "a").write("stdlib+numpy OK\n")
    from ersilia_pack_utils.core import read_smiles, write_out
    open("/tmp/main_diag.log", "a").write("ersilia_pack_utils OK\n")
    from mole_antimicrobial_prediction import MoleAntimicrobialPredictor
    open("/tmp/main_diag.log", "a").write("MoleAntimicrobialPredictor import OK\n")
except Exception:
    import traceback as _tb
    open("/tmp/main_diag.log", "a").write("IMPORT EXCEPTION:\n" + _tb.format_exc())
    raise

input_file = sys.argv[1]
output_file = sys.argv[2]
root = os.path.dirname(os.path.abspath(__file__))

try:
    open("/tmp/main_diag.log", "a").write("INPUT FILE (%s):\n%s\n" % (input_file, open(input_file).read()))
    _, smiles_list = read_smiles(input_file)
    open("/tmp/main_diag.log", "a").write("read_smiles -> %d : %r\n" % (len(smiles_list), smiles_list[:3]))

    tmp_file = os.path.join(os.path.dirname(os.path.abspath(output_file)), "mole_input_tmp.csv")
    with open(tmp_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["smiles"])
        for s in smiles_list:
            writer.writerow([s])

    predictor = MoleAntimicrobialPredictor()
    df = predictor.run(tmp_file, output_file)
    open("/tmp/main_diag.log", "a").write("df shape=%s head=%r\n" % (df.shape, df.iloc[0].tolist()[:5] if len(df) else "EMPTY"))

    header = list(df.columns)
    results = df.values.tolist()
    write_out(results, header, output_file, np.float32)
    os.remove(tmp_file)
    open("/tmp/main_diag.log", "a").write("DONE OK\n")
except Exception:
    open("/tmp/main_diag.log", "a").write("RUN EXCEPTION:\n" + traceback.format_exc())
    raise
