# imports
import os
import sys
from mole_antimicrobial_prediction import MoleAntimicrobialPredictor

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
print(root)

predictor = MoleAntimicrobialPredictor()
predictor.run(input_file, output_file)