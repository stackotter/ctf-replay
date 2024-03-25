import argparse
import fsspec
import os

from pathlib import Path

parser = argparse.ArgumentParser("manager")
parser.add_argument("ctf", type=str)
parser.add_argument("year", type=str)
parser.add_argument("category", type=str)
parser.add_argument("challenge", type=str)
args = parser.parse_args()

path = f"ctfs/{args.ctf}/{args.year}/{args.category}/{args.challenge}"
destination = Path.cwd() / path
destination.mkdir(exist_ok=True, parents=True)
fs = fsspec.filesystem("github", org="sajjadium", repo="ctf-archives")
fs.get(fs.ls(path), destination.as_posix(), recursive=True)
os.symlink(path, "latest")
