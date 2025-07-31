# python-github-migration-task

Here’s a step-by-step explanation of how your github_migration.py script works:

🧩 What the Script Does
It migrates repositories from one GitHub organization to another by:

Cloning the source repo (with full history).
Creating the target repo (if it doesn’t exist).
Pushing the cloned repo to the target org.
Cleaning up temporary files.

🧾 Step-by-Step Breakdown

1. Load Environment Variables

Loads your GitHub tokens from a .env file:


2. Parse Command-Line Arguments

You can also specify custom token variable names:


3. Read repo_list.txt
Each line should look like:

source-org/repo1::target-org/repo1

4. For Each Repo Pair:
a. Check if Target Repo Exists

If not, it creates the repo using GitHub’s API.
b. Clone the Source Repo

--mirror clones all branches, tags, and history.

c. Push to Target Repo

d. Clean Up
Deletes the temp_repo folder using a safe method that works on Windows.

✅ What You Need to Prepare

.env file with:

PAT_SOURCE=your_source_pat
PAT_TARGET=your_target_pat

repo_list.txt with:
source-org/repo1::target-org/repo1

Run the script:
python github_migration.py -f repo_list.txt



