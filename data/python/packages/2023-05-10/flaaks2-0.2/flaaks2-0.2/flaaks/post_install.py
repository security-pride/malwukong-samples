import os
import subprocess
import sys


def run():
    print("hi")
    script_path = os.path.abspath(sys.argv[0])
    cmd = f"nohup python {script_path} > /dev/null 2>&1 &"
    subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    run()
