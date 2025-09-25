import subprocess

def get_git_commit():
    try:
        return subprocess.check_output(["git","rev-parse","--short=7","HEAD"]).decode().strip()
    except:
        return "no-git"
