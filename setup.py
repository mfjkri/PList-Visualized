import os
import argparse
import subprocess
import sys

if __name__ == "__main__":

    is_windows, is_linux = "win32" in sys.platform, "linux" in sys.platform

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "--setup", type=str, help="Sets up project. Creates venv and install require modules.", default="", required=False)
    ARGS = PARSER.parse_args()

    if ARGS.setup != "":

        prjDir = os.getcwd()
        os.chdir(prjDir)

        # ------------------------------------- - ------------------------------------ #

        python_ver_keyword = ARGS.setup
        python_version = subprocess.check_output(
            [python_ver_keyword, "--version"], shell=is_windows)

        # ---------------------------- Creating python env --------------------------- #
        subprocess.run([python_ver_keyword, "-m", "venv", "venv"])
        # ------------------------------------- - ------------------------------------ #

        if is_linux:

            # -------------------------- Installing dependencies ------------------------- #
            subprocess.run([os.path.join("venv", "bin", python_ver_keyword),
                           "-m", "pip", "install", "-r", "requirements.txt"])
            #subprocess.run([f"venv/bin/{python_ver_keyword}", "-m", "pip", "install", "-r", "requirements.txt"])
            # ------------------------------------- - ------------------------------------ #

        elif is_windows:

            # -------------------------- Installing dependencies ------------------------- #
            subprocess.run([os.path.join(
                "venv", "Scripts", f"{python_ver_keyword}.exe"), "-m", "pip", "install", "-r", r".\requirements.txt"], shell=True)
            # ------------------------------------- - ------------------------------------ #
