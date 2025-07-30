import requests

import os
from dotenv import load_dotenv

load_dotenv()
PAT_SOURCE = os.getenv("PAT_SOURCE")
PAT_TARGET = os.getenv("PAT_TARGET") 

# Organization names
SOURCE_ORG = 'Source-orgn'
TARGET_ORG = 'Target-orgn'

# Headers for GitHub API
headers_source = {
    'Authorization': f'token {PAT_SOURCE}',
    'Accept': 'application/vnd.github+json'
}

# Repositories to create in source org
repos = [
    {'name': 'public-repo', 'private': False, 'visibility': 'public'},
    {'name': 'private-repo', 'private': True, 'visibility': 'private'},
    {'name': 'internal-repo', 'private': True, 'visibility': 'internal'}
]

# Create repositories
def create_repos():
    for repo in repos:
        payload = {
            'name': repo['name'],
            'private': repo['private'],
            'visibility': repo['visibility'],
            'auto_init': True
        }
        response = requests.post(
            f'https://api.github.com/orgs/{SOURCE_ORG}/repos',
            headers=headers_source,
            json=payload
        )
        if response.status_code == 201:
            print(f"Created: {repo['name']}")
        else:
            print(f"Failed: {repo['name']} - {response.status_code} - {response.text}")


def invite_user_to_org(username):
    # Step 1: Get the user's GitHub ID
    user_resp = requests.get(f"https://api.github.com/users/{username}", headers=headers_source)
    if user_resp.status_code != 200:
        print(f"Failed to fetch user ID for '{username}': {user_resp.status_code} - {user_resp.text}")
        return

    user_id = user_resp.json().get("id")

    # Step 2: Send the invitation using the user ID
    url = f'https://api.github.com/orgs/{SOURCE_ORG}/invitations'
    payload = {
        'invitee_id': user_id,
        'role': 'direct_member'
    }
    response = requests.post(url, headers=headers_source, json=payload)
    if response.status_code in [201, 204]:
        print(f"Invited user '{username}' to org.")
    else:
        print(f"Failed to invite user '{username}': {response.status_code} - {response.text}")





# Create team and add user
def create_team_and_add_user(team_name, username):
    team_payload = {'name': team_name, 'privacy': 'closed'}
    team_response = requests.post(f'https://api.github.com/orgs/{SOURCE_ORG}/teams', headers=headers_source, json=team_payload)
    if team_response.status_code == 201:
        print(f"Team '{team_name}' created.")
        team_slug = team_response.json()['slug']
        add_user_response = requests.put(
            f'https://api.github.com/orgs/{SOURCE_ORG}/teams/{team_slug}/memberships/{username}',
            headers=headers_source
        )
        if add_user_response.status_code in [200, 201]:
            print(f"User '{username}' added to team '{team_name}'.")
        else:
            print(f"Failed to add user to team: {add_user_response.status_code} - {add_user_response.text}")
    else:
        print(f"Failed to create team: {team_response.status_code} - {team_response.text}")





# create_repos()
# invite_user_to_org('jAnushka26')  # Replace with actual GitHub username
create_team_and_add_user('python-git-team', 'jAnushka26')
