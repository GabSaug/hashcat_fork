import subprocess
import shutil
import os
from os.path import join, basename, realpath
from tqdm import tqdm
import json
import argparse

import sys
sys.path.append('/home/gabriel/codemerger/scripts/benchmark/')
from compare_functions_features import compareFunctionsFeatures
from create_payload_after_random_insert import createNewAsm


parser=argparse.ArgumentParser()
parser.add_argument("payloadAsm", help="Payload asm file")
parser.add_argument("payloadFunction", help="Payload function name ")
parser.add_argument("targetAsm", help="target asm file")
parser.add_argument("targetFunction", help="target function name ")
parser.add_argument("insertion_method", help="Method for code insertion", choices={"none", "random", "simple_liveliness", "clever_liveliness", "dead_branch"})
parser.add_argument("output", help="name of the ouput file, without extension")
args=parser.parse_args()

def runCmd(cmd):
    cmd_list = [e for e in cmd.split(" ") if len(e) > 0]
    return subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# === vars

pAsm, pFun, tAsm, tFun = args.payloadAsm, args.payloadFunction, args.targetAsm, args.targetFunction
diff_table = "diffTable/{}_diffTable.pickle".format(args.output)

# ========== Get diff table

if compareFunctionsFeatures(pAsm, pFun, tAsm, tFun, diff_table) != 0:
    print("Error comparing function features {} {} {} {}".format(pAsm, pFun, tAsm, tFun))
    exit(1)

# ========== Create new asm file (p2)

outputAsm = "asm/{}-2.s".format(args.output)
# Do the asm instruction insertion and write the new asm file
if createNewAsm(pAsm, pFun, diff_table, args.insertion_method, outputAsm) != 0:
    print("Error creating new Asm file {}".format(outputAsm))
    exit(1)
