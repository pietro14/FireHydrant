#!/usr/bin/env python
"""Text filing dataset info returned by dasgoclient queries
"""
import json
import shlex
import subprocess
import sys
import time

OUTPUT_FILE = "/publicweb/w/wsi/public/lpcdm/backgroundsummary.txt"

DATASET_GRP = dict(
    ttWJets=[
        "/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM"
    ],
    singleTop=[
        "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v1/AODSIM",
        "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v1/AODSIM",
    ],
    WJets=[
        "/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
        "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM",
    ],
)


# https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def main():

    sys.stdout = open(OUTPUT_FILE, "w")
    print("Generated at {}".format(time.ctime()))
    print("=" * 100, end="\n\n")
    fmt = "{:135}{:>10}{:>10}{:>10}  {}"
    print(fmt.format("Dataset", "#Events", "#Files", "size", "sites"))
    for categ, datasets in DATASET_GRP.items():

        print("+++ ", categ, " +++")
        print("-" * 160)
        for ds in datasets:
            nFiles, nEvents, fileSize = (-1, -1, -1)
            sites = []
            try:
                dasquery = 'dasgoclient -query="summary dataset={}" -json'.format(ds)
                dasres = subprocess.check_output(shlex.split((dasquery)))
                dasres = json.loads(dasres)[0]

                dasquery_site = 'dasgoclient -query="site dataset={}"'.format(ds)
                dasres_site = subprocess.check_output(shlex.split((dasquery_site)))

                nFiles = dasres["summary"][0]["num_file"]
                nEvents = dasres["summary"][0]["num_event"]
                fileSize = dasres["summary"][0]["file_size"]
                sites = [s.decode() for s in dasres_site.split()]
            except Exception:
                ds += " **"
            print(fmt.format(ds, nEvents, nFiles, sizeof_fmt(fileSize), sites))
        print("-" * 160)
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    print("Write summary at ", OUTPUT_FILE)
    print("Please visit")
    print("\thttp://home.fnal.gov/~wsi/public/lpcdm/backgroundsummary.txt")


if __name__ == "__main__":
    main()
