#!/usr/bin/env python3
import argparse
import dotenv
import fsspec
import os
from shutil import rmtree
import colorama
from colorama import Fore

colorama.init()

dotenv.load_dotenv()

# Not required, but you'll probably hit rate limits pretty quickly without them
git_username = os.environ.get("GIT_USERNAME")
git_token = os.environ.get("GIT_TOKEN")

parser = argparse.ArgumentParser("archivist.py", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("ctf", type=str)
parser.add_argument("year", type=str)
parser.add_argument("--category", type=str, default=None)
parser.add_argument("--challenge", type=str, default=None)
parser.add_argument("-m", "--mode", type=str, default="skip", 
                    choices=["skip","overwrite", "backup", "prompt"], 
                    help='''
                            skip(default): skip existing files, 
                            overwrite: overwrite existing files, 
                            backup: backup existing files, 
                            prompt: prompt for each file
                         ''')

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

def skip_file(path):
    print(f"{Fore.LIGHTBLUE_EX}[skip]{Fore.RESET} " + path)

def backup_file(path):
    if os.path.exists(path + "_backup"):
        rmtree(path + "_backup")
    os.rename(path, path + "_backup")
    print(f"{Fore.YELLOW}[backup]{Fore.RESET} " + path + "_backup") 

def prompt_file(path):
    while True:
        response = input(f"{Fore.CYAN}[prompt]{Fore.RESET} {path} exists. (o/s/b): ").strip()
        if response == "s":
            skip_file(path)
            return 1
        elif response == "b":
            backup_file(path)
            return 0
        elif response == "o":
            return 0
        print("Please enter 'o', 's', or 'b'. (overwrite/skip/backup)")

for challenge_path in challenge_paths:
    if args.mode == "prompt" and os.path.exists(challenge_path):
        if prompt_file(challenge_path):
            continue
    elif args.mode == "skip" and os.path.exists(challenge_path):
        skip_file(challenge_path)
        continue
    elif args.mode == "backup" and os.path.exists(challenge_path):
        backup_file(challenge_path)

    os.makedirs(challenge_path, exist_ok=True)
    fs.get(fs.ls(challenge_path), challenge_path, recursive=True)
    print(f"{Fore.GREEN}[download]{Fore.RESET} " + challenge_path)

try:
    os.remove("latest")
except Exception:
    pass
os.symlink(path, "latest")



    
