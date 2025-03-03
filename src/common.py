import yaml
import sys
import os
import subprocess
import questionary
import os
import shutil
import requests 
import xmltodict
from difflib import SequenceMatcher
from typing import TypedDict

REAL_REPO = ""
REPOS_LOCATION = "/var/db/repos"
REPO_LOC = ""
ROOT = "sudo"

try:
    with open(os.path.expanduser("~/.config/gpo-steal/config.yaml"), "r") as f:
        cfg = yaml.safe_load(f.read())
        REAL_REPO = cfg["repo"]
        REPO_LOC = cfg["repo_location"]
        ROOT = cfg["elevation"]
except FileNotFoundError:
    print("no configuration found, should be in ~/.config/gpo-steal/config.yaml")
    exit(1)

FULL_REPOS_LOCATION = os.path.join(REPOS_LOCATION, REAL_REPO)
REPO_CFG_LOC = os.path.join(REPO_LOC, "repos.yaml")
TRACKED_CFG_LOC = os.path.join(REPO_LOC, "tracked.yaml")

os.system(f"mkdir -p {REPO_LOC}")

class repo_pair(TypedDict):
    url: str
    name: str

repos = {}
tracked = {}

try:
    with open(REPO_CFG_LOC, "r") as f:
        repos = yaml.safe_load(f.read()) or repos
except:
    pass

try:
    with open(TRACKED_CFG_LOC, "r") as f:
        tracked = yaml.safe_load(f.read()) or tracked
except:
    pass

def save() -> None:
    with open(REPO_CFG_LOC, "w") as f:
        yaml.dump(repos, f)

    with open(TRACKED_CFG_LOC, "w") as f:
        yaml.dump(tracked, f)

def eexec(cmd) -> None:
    run = f"{ROOT} sh -c '{cmd}'"
    print(run)
    os.system(run)
