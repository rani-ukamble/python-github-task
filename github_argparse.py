## to run this script=>
## python github_argparse.py -r repolist.txt -st PAT_SOURCE

import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def create_repo(org, name, private=False, visibility='public', auto_init=True, token=None):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json'
    }
    payload = {
        'name': name,
        'private': private,
        'visibility': visibility,
        'auto_init': auto_init
    }
    response = requests.post(
        f'https://api.github.com/orgs/{org}/repos',
        headers=headers,
        json=payload
    )
    if response.status_code == 201:
        print(f"Created: {org}/{name}")
    else:
        print(f"Failed: {org}/{name} - {response.status_code} - {response.text}")

def process_repo_file(repo_file, token):
    if not os.path.exists(repo_file):
        print(f"File not found: {repo_file}")
        return

    with open(repo_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '/' in line:
                org, repo = line.split('/')
                create_repo(org, repo, token=token)
            else:
                print(f"Skipping invalid line: {line}") 

    print(repo_file, org, repo, token)




def main():
    parser = argparse.ArgumentParser(description="...Process POST migration validation for repositories...")
    parser.add_argument('-r', '--repo_file', type=str, required=True, help="Path to the file containing list of repositories")
    parser.add_argument('-o', '--output_folder', type=str, default='./output', help="Path to the folder where the migration summary will be saved (default: './output').")
    parser.add_argument('-st', '--source_token_env', type=str, required=True, help="Environment variable name for Source GitHub personal access token")

    args = parser.parse_args()

    # Get token from environment
    source_token = os.getenv(args.source_token_env)
    if not source_token:
        raise ValueError(f"Environment variable '{args.source_token_env}' not found or empty.")

    # Ensure output folder exists
    os.makedirs(args.output_folder, exist_ok=True)

    # Process the repo list
    process_repo_file(args.repo_file, source_token)





if __name__ == "__main__":
    main()
