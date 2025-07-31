# To migrate repositories from one GitHub organization to another (rather than transferring), you typically:

# Clone the source repository.
# Push it to a new repository in the target organization.
# Optionally, migrate issues, PRs, and other metadata using GitHub APIs or third-party tools.

import os
import subprocess
import argparse
from dotenv import load_dotenv
import shutil
import stat
import requests

load_dotenv()

def build_git_url(org_repo, token):
    return f"https://{token}@github.com/{org_repo}.git"

def on_rm_error(func, path, exc_info):
    # Remove readonly and try again
    os.chmod(path, stat.S_IWRITE)
    func(path)

def ensure_target_repo_exists(target_repo, target_token):
    org, repo = target_repo.split("/", 1)
    url = f"https://api.github.com/repos/{org}/{repo}"
    headers = {
        "Authorization": f"token {target_token}",
        "Accept": "application/vnd.github+json"
    }
    # Check if repo exists
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return  # Repo exists
    # Create repo
    url = f"https://api.github.com/orgs/{org}/repos"
    data = {"name": repo, "private": True}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code not in (201, 202):
        raise Exception(f"Failed to create target repo {target_repo}: {resp.text}")
    print(f"Created target repo: {target_repo}")

def migrate_repo(source_org_repo, target_org_repo, source_token, target_token, temp_dir="temp_repo"):
    source_url = build_git_url(source_org_repo, source_token)
    target_url = build_git_url(target_org_repo, target_token)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, onerror=on_rm_error)

    print(f"Cloning from {source_org_repo}...")
    subprocess.run(["git", "clone", "--mirror", source_url, temp_dir], check=True)

    print(f"Pushing to {target_org_repo}...")
    os.chdir(temp_dir)
    subprocess.run(["git", "remote", "set-url", "origin", target_url], check=True)
    subprocess.run(["git", "push", "--mirror"], check=True)
    os.chdir("..")
    shutil.rmtree(temp_dir, onerror=on_rm_error)
    print(f"Migration complete: {source_org_repo} → {target_org_repo}\n")

def main():
    parser = argparse.ArgumentParser(description="Migrate GitHub repositories from one org to another using a repo list file.")
    parser.add_argument("-f", "--file", required=True, help="Path to repo list file (format: org/repo::org/repo per line)")
    parser.add_argument("-st", "--source_token_env", type=str, default="PAT_SOURCE", help="Env var for source GitHub PAT (default: PAT_SOURCE)")
    parser.add_argument("-tt", "--target_token_env", type=str, default="PAT_TARGET", help="Env var for target GitHub PAT (default: PAT_TARGET)")
    args = parser.parse_args()

    source_token = os.getenv(args.source_token_env)
    target_token = os.getenv(args.target_token_env)
    if not source_token:
        raise ValueError(f"Set your source GitHub token in the {args.source_token_env} environment variable.")
    if not target_token:
        raise ValueError(f"Set your target GitHub token in the {args.target_token_env} environment variable.")

    with open(args.file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "::" not in line:
                continue
            source_repo, target_repo = line.split("::")
            try:
                ensure_target_repo_exists(target_repo, target_token)
                migrate_repo(source_repo, target_repo, source_token, target_token)
            except subprocess.CalledProcessError as e:
                print(f"Error migrating {source_repo}: {e}")
            except Exception as e:
                print(f"Error ensuring target repo {target_repo}: {e}")

    print("Migration and argument parsing completed successfully.")

if __name__ == "__main__":
    main()

# # To run this script => python github_migration.py -f repo_list.txt 

