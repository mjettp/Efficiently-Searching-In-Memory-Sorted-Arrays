# This file containes a helper function gives the appropriate configuration
# file to the benchmarking framework and saves the results.
# This file also run the experiments that produce the figures of our paper.

from os import path, remove
import sys
import subprocess
from subprocess import call, check_output, DEVNULL


def run(tsvname):
    print("Running experiment : " + tsvname)
    if not path.exists("../searchbench"):
        print(
            "Please make sure searchbench is compiled. You can compile this by running make on the parent directory.")
        sys.exit()

    if not path.exists("experiments_configurations/" + tsvname):
        print("The configuration file does not exist: "+tsvname)
        sys.exit()

    resultFile = "experiments_results/" + tsvname + ".results"
    if path.exists(resultFile):
        print(
            "This tsv has been already executed and the results have been saved.")
        print(
                    "If you want to rerun the experiments please delete the file: " + tsvname + ".results")
    else:
        with open(resultFile, "w") as log_file:
            subprocess.run(["python3", "./getTimesReproducibility.py",
                            "./reproduce_experiments/experiments_configurations/" + tsvname],
                           stdout=log_file, stderr=DEVNULL, cwd="../")

def run_metadata(tsvname):
    print("Running experiment : " + tsvname)
    if not path.exists("../searchbench"):
        print(
            "Please make sure searchbench is compiled. You can compile this by running make on the parent directory.")
        sys.exit()

    if not path.exists("experiments_configurations/" + tsvname):
        print("The configuration file does not exist: "+tsvname)
        sys.exit()

    resultFile = "experiments_results/" + tsvname + ".results"
    if path.exists(resultFile):
        print(
            "This tsv has been already executed and the results have been saved.")
        print(
                "If you want to rerun the experiments please delete the file: " + tsvname + ".results")
    else:
        with open("experiments_configurations/uniq_" + tsvname, "w") as log_file:
            subprocess.run(["uniq", "./reproduce_experiments/experiments_configurations/" + tsvname],
                            stdout=log_file, stderr=DEVNULL, cwd="../")

        with open(resultFile, "w") as log_file:
            subprocess.run(["./searchbench", "./reproduce_experiments/experiments_configurations/uniq_" + tsvname],
                           stdout=log_file, stderr=DEVNULL, cwd="../")


##########################

run("fig2.tsv")
run("fig5.tsv")
run("fig6_8.tsv")
run("fig6_32.tsv")
run("fig6_128.tsv")
run("fig7.tsv")
run("fig8_1.tsv")
run("fig8_2.tsv")
run("fig8_3.tsv")
run("fig8_4.tsv")

run("fig9_05_fal.tsv")
run("fig9_105_fal.tsv")
run("fig9_125_fal.tsv")
run("fig9_15_fal.tsv")
run("fig9_05_cfal.tsv")
run("fig9_105_cfal.tsv")
run("fig9_125_cfal.tsv")
run("fig9_15_cfal.tsv")

run("fig10.tsv")
run("fig11.tsv")
run("fig12_times.tsv")
run("section56_SIP_UAR.tsv")
run("section56_SIP_FB.tsv")

run("section56_TIP_05_fal.tsv")
run("section56_TIP_105_fal.tsv")
run("section56_TIP_125_fal.tsv")
run("section56_TIP_15_fal.tsv")
run("section56_TIP_05_cfal.tsv")
run("section56_TIP_105_cfal.tsv")
run("section56_TIP_125_cfal.tsv")
run("section56_TIP_15_cfal.tsv")
run("section56_TIP_Freq.tsv")
run_metadata("fig12.tsv")
