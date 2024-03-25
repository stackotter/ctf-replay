import argparse
import dotenv
import fsspec
import os

dotenv.load_dotenv()

# Not required, but you'll probably hit rate limits pretty quickly without them
git_username = os.environ.get("GIT_USERNAME")
git_token = os.environ.get("GIT_TOKEN")

parser = argparse.ArgumentParser("manager")
parser.add_argument("ctf", type=str)
parser.add_argument("year", type=str)
parser.add_argument("--category", type=str, default=None)
parser.add_argument("--challenge", type=str, default=None)
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
    print(challenge_path)
    os.makedirs(challenge_path, exist_ok=True)
    fs.get(fs.ls(challenge_path), challenge_path, recursive=True)

try:
    os.remove("latest")
except Exception:
    pass
os.symlink(path, "latest")
