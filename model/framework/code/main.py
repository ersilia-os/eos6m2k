import sys as _sys, time as _t
open("/tmp/main_diag.log","a").write("MAIN_INVOKED %s argv=%r\n" % (_t.strftime("%H:%M:%S"), _sys.argv))
try:
    import os, sys, csv
    import numpy as np
    from ersilia_pack_utils.core import read_smiles, write_out
    from mole_antimicrobial_prediction import MoleAntimicrobialPredictor
    open("/tmp/main_diag.log","a").write("imports OK %s\n" % _t.strftime("%H:%M:%S"))
except Exception:
    import traceback as _tb
    open("/tmp/main_diag.log","a").write("IMPORT EXC:\n"+_tb.format_exc())
    raise
input_file = sys.argv[1]; output_file = sys.argv[2]
try:
    _, smiles_list = read_smiles(input_file)
    open("/tmp/main_diag.log","a").write("smiles=%d %r\n" % (len(smiles_list), smiles_list[:2]))
    tmp_file = os.path.join(os.path.dirname(os.path.abspath(output_file)), "mole_input_tmp.csv")
    with open(tmp_file, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["smiles"])
        for s in smiles_list: w.writerow([s])
    predictor = MoleAntimicrobialPredictor()
    df = predictor.run(tmp_file, output_file)
    open("/tmp/main_diag.log","a").write("df=%s\n" % str(df.shape))
    write_out(df.values.tolist(), list(df.columns), output_file, np.float32)
    os.remove(tmp_file)
    open("/tmp/main_diag.log","a").write("DONE OK\n")
except Exception:
    import traceback as _tb2
    open("/tmp/main_diag.log","a").write("RUN EXC:\n"+_tb2.format_exc())
    raise
