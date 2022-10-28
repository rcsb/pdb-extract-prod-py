#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-10-01
# Updates:
# =============================================================================
"""
config enviroment variables for unit, integration, and functional tests. This
way the variables are set within program, and stay local to the program run
without impacting the global enviroment.

For deployment, these variables are set globally in setup.sh or setup.csh

"""
import os


def config(top_dir):
    top_dir = os.path.abspath(top_dir)
    os.environ["PDB_EXTRACT_PY"] = top_dir
    print("set %s=%s" % ("PDB_EXTRACT_PY", os.environ["PDB_EXTRACT_PY"]))
    os.environ["RCSBROOT"] = os.path.join(top_dir, "packages/maxit-v11.100-prod-src")
    print("set %s=%s" % ("RCSBROOT", os.environ["RCSBROOT"]))

    if os.getenv("PYTHONPATH"):
        l_path = os.getenv("PYTHONPATH").split(':')
        if top_dir not in l_path:
            os.environ["PYTHONPATH"] = "%s:%s" % (top_dir, os.getenv("PYTHONPATH"))
    else:
        os.environ["PYTHONPATH"] = top_dir
    print("set %s=%s" % ("PYTHONPATH", os.environ["PYTHONPATH"]))


def main():
    top_dir = ".."
    config(top_dir)


if __name__ == "__main__":
    main()
