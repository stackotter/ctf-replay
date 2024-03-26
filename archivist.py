#!/usr/bin/env python3
import argparse
import dotenv
import fsspec
import os
from shutil import rmtree

GREEN = '\033[32m'
RESET = '\033[0m'
YELLOW = '\033[93m'
LIGHTBLUE = '\033[94m'

dotenv.load_dotenv()

# Not required, but you'll probably hit rate limits pretty quickly without them
git_username = os.environ.get("GIT_USERNAME")
git_token = os.environ.get("GIT_TOKEN")

parser = argparse.ArgumentParser("archivist.py")
parser.add_argument("ctf", type=str)
parser.add_argument("year", type=str)
parser.add_argument("--category", type=str, default=None)
parser.add_argument("--challenge", type=str, default=None)
parser.add_argument("-m", "--mode", type=str, default="overwrite", choices=["overwrite", "skip", "duplicate"], help="overwrite(default): overwrite existing files,\nskip: skip existing files,\nduplicate: rename existing files")
args = parser.parse_args()

fs = fsspec.filesystem(
    "github", org="sajjadium", repo="ctf-archives",
    username=git_username,
    token=git_token
)

path = f"ctfs/{args.ctf}/{args.year}"
challenge_paths = []
if args.category is None:
    category_paths = fs.ls(path)
    for category_path in category_paths:
        challenge_paths += fs.ls(category_path)
else:
    category_path = f"{path}/{args.category}"
    path = category_path
    if args.challenge is None:
        challenge_paths = fs.ls(category_path)
    else:
        challenge_path = f"{category_path}/{args.challenge}"
        challenge_paths = [challenge_path]
        path = challenge_path

for challenge_path in challenge_paths:
    if args.mode == "skip" and os.path.exists(challenge_path):
            print(f"{LIGHTBLUE}[skip]{RESET} " + challenge_path)
            continue
    elif args.mode == "duplicate" and os.path.exists(challenge_path):
            if os.path.exists(challenge_path + "_copy"):
                rmtree(challenge_path + "_copy")
            os.rename(challenge_path, challenge_path + "_copy")
            print(f"{YELLOW}[duplicate]{RESET} " + challenge_path + "_copy")

    os.makedirs(challenge_path, exist_ok=True)
    fs.get(fs.ls(challenge_path), challenge_path, recursive=True)
    print(f"{GREEN}[download]{RESET} " + challenge_path)

try:
    os.remove("latest")
except Exception:
    pass
os.symlink(path, "latest")
