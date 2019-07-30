#!/usr/bin/env python
"""Text filing dataset info returned by dasgoclient queries
"""
import json
import shlex
import subprocess
import sys
import time

OUTPUT_FILE = "/publicweb/w/wsi/public/lpcdm/backgroundsummary.txt"
DATASET_GRP = json.load(open("backgroundlist.json"))


# https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def main():

    with open(OUTPUT_FILE, "w") as outf:
        outf.write("Generated at {}\n".format(time.ctime()))
        outf.write("=" * 100 + "\n\n")
        fmt = "{:145}{:>10}{:>10}{:>10}  {}"
        outf.write(fmt.format("Dataset", "#Events", "#Files", "size", "sites(disk only)") + "\n")

        starttime = time.time()
        starttimec = time.time()

        print('**', time.asctime())
        for categ, datasets in DATASET_GRP.items():

            outf.write(f"+++ {categ} +++\n")
            print('{:25}'.format(f"+++ {categ} +++ [{len(datasets)}]"), end="\t")
            outf.write("-" * 160 + "\n")
            for ds in datasets:
                nFiles, nEvents, fileSize = (-1, -1, -1)
                sites = []
                try:
                    dasquery = 'dasgoclient -query="summary dataset={}" -json'.format(ds)
                    dasres = subprocess.check_output(shlex.split((dasquery)))
                    dasres = json.loads(dasres)[0]

                    dasquery_site = 'dasgoclient -query="site dataset={}" -json'.format(ds)
                    dasres_site = subprocess.check_output(shlex.split((dasquery_site)))
                    dasres_site = json.loads(dasres_site.decode())

                    nFiles = dasres["summary"][0]["num_file"]
                    nEvents = dasres["summary"][0]["num_event"]
                    fileSize = dasres["summary"][0]["file_size"]
                    sites = []
                    for siteinfo in dasres_site:
                        _service = siteinfo["das"]["services"][0]
                        _sitename = siteinfo["site"][0]["name"]
                        if _sitename.startswith("T0"):
                            continue
                        if _sitename.startswith("T1") and not _sitename.endswith("Disk"):
                            continue
                        if _sitename not in sites:
                            sites.append(_sitename)
                        if _service.startswith("combined"):
                            if (
                                siteinfo["site"][0]["block_completion"] != "100.00%"
                                or siteinfo["site"][0]["block_fraction"] != "100.00%"
                                or siteinfo["site"][0]["dataset_fraction"] != "100.00%"
                                or siteinfo["site"][0]["replica_fraction"] != "100.00%"
                            ):
                                if _sitename in sites:
                                    sites.remove(_sitename)

                except Exception:
                    ds += " **"
                outf.write(fmt.format(ds, nEvents, nFiles, sizeof_fmt(fileSize), sites) + "\n")
            outf.write("-" * 160 + "\n")
            print("--> took {:.3f}s".format(time.time() - starttimec))
            starttimec = time.time()

    print('_'*45)
    print("--> took {:.3f}s".format(time.time() - starttime))
    print("Write summary at ", OUTPUT_FILE)
    print("Please visit")
    print("\thttp://home.fnal.gov/~wsi/public/lpcdm/backgroundsummary.txt")


if __name__ == "__main__":
    main()
