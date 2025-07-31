## to run this script=>
## python github_migration.py -r repo_list.txt -st PAT_SOURCE_CLASSIC


from dotenv import load_dotenv
import requests
import os
import argparse
from dotenv import load_dotenv 

load_dotenv()

def transfer_repo(source_org, repo_name, target_org, target_repo_name, headers):
    url = f"https://api.github.com/repos/{source_org}/{repo_name}/transfer"
    payload = {
        "new_owner": target_org,
        "new_name": target_repo_name
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (202, 201):
        print(f"Transfer started: {source_org}/{repo_name} -> {target_org}/{target_repo_name}")
    else:
        print(f"Failed to transfer {source_org}/{repo_name}: {resp.status_code} {resp.text}")

def process_repo_list(repo_list_file, headers):
    if not os.path.exists(repo_list_file):
        print(f"File not found: {repo_list_file}")
        return

    with open(repo_list_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or "::" not in line:
                print(f"Skipping invalid line: {line}")
                continue
            src, tgt = line.split("::")
            if "/" not in src or "/" not in tgt:
                print(f"Skipping invalid line: {line}")
                continue
            source_org, repo_name = src.split("/", 1)
            target_org, target_repo_name = tgt.split("/", 1)
            print(f"Transferring {source_org}/{repo_name} -> {target_org}/{target_repo_name} ...")
            transfer_repo(source_org, repo_name, target_org, target_repo_name, headers)

def main():
    parser = argparse.ArgumentParser(description="Transfer repositories as specified in a repo list file.")
    parser.add_argument('-r', '--repo_list', type=str, required=True, help="Path to the repo list file") 
    parser.add_argument('-st', '--source_token_env', type=str, required=True, help="Environment variable name for Source GitHub personal access token")
    
    args = parser.parse_args()

    source_token = os.getenv(args.source_token_env)
    if not source_token:
        raise ValueError(f"Set your GitHub token in the {args.source_token_env} environment variable.")

    headers = {
        "Authorization": f"token {source_token}",
        "Accept": "application/vnd.github+json"
    }

    process_repo_list(args.repo_list, headers)

if __name__ == "__main__":
    main()