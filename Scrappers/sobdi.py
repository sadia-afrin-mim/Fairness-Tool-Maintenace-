import pandas as pd
from github import Github
from datetime import datetime
import csv
import os

# Replace with your GitHub personal access token
ACCESS_TOKEN = ''

# Initialize Github object
g = Github(ACCESS_TOKEN)

# Input file containing repository names (one per line)
input_file = 'ESEM - Dataset.csv'

# Output CSV file path
output_csv = 'repository_info_output.csv'

# Define the CSV headers
csv_headers = ['Repository', 'Forks', 'Total Issues', 'Closed Issues', 'Open PRs', 'Closed PRs', 'Merged PRs',
               'Total Commits', 'Max Days Without Commit', 'Most Active Dev Commits', 'Contributors',
               'Owner Projects', 'Owner Commits']

# Create the output CSV file if it doesn't exist
if not os.path.exists(output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()


# Function to gather information for a single repository
def get_repo_info(repo_name):
    try:
        repo = g.get_repo(repo_name)

        # 1. Number of forks
        num_forks = repo.forks_count

        # 2. Total number of issues opened by devs
        open_issues_count = repo.get_issues(state='all').totalCount

        # 3. Number of issues closed by devs
        closed_issues_count = repo.get_issues(state='closed').totalCount

        # 4. Number of open pull requests
        open_prs_count = repo.get_pulls(state='open').totalCount

        # 5. Number of closed pull requests
        closed_prs_count = repo.get_pulls(state='closed').totalCount

        # 6. Number of merged pull requests
        merged_prs_count = closed_prs_count - len([pr for pr in repo.get_pulls(state='closed') if pr.merged_at is None])

        # 7. Number of commits by developers
        total_commits = repo.get_commits().totalCount

        # 8. Maximum days of the repository without a commit
        commits = repo.get_commits()
        commit_dates = [commit.commit.author.date for commit in commits]
        max_days_without_commit = max(
            (commit_dates[i] - commit_dates[i + 1]).days for i in range(len(commit_dates) - 1))

        # 9. Number of commits by the developer who committed the most
        commit_authors = {}
        for commit in repo.get_commits():
            author = commit.commit.author.name
            if author not in commit_authors:
                commit_authors[author] = 1
            else:
                commit_authors[author] += 1
        max_commits_by_dev = max(commit_authors.values())

        # 10. Total number of contributors
        total_contributors = repo.get_contributors().totalCount

        # 11. Number of projects created by the project owner
        owner = repo.owner
        if owner.type == 'Organization':
            owner_projects = g.get_organization(owner.login).get_projects().totalCount
        else:
            owner_projects = g.get_user(owner.login).get_projects().totalCount

        # 12. Number of commits from the project owner
        owner_commits = repo.get_commits(author=owner.login).totalCount

        # Return the information as a dictionary
        return {
            'Repository': repo_name,
            'Forks': num_forks,
            'Total Issues': open_issues_count,
            'Closed Issues': closed_issues_count,
            'Open PRs': open_prs_count,
            'Closed PRs': closed_prs_count,
            'Merged PRs': merged_prs_count,
            'Total Commits': total_commits,
            'Max Days Without Commit': max_days_without_commit,
            'Most Active Dev Commits': max_commits_by_dev,
            'Contributors': total_contributors,
            'Owner Projects': owner_projects,
            'Owner Commits': owner_commits
        }

    except Exception as e:
        print(f"Error processing {repo_name}: {e}")
        return None


# Read repository names from the input file and process them
if os.path.exists(input_file):
    with open(input_file, mode='r') as file:
        repo_names = [line.strip() for line in file.readlines()]

    for repo_name in repo_names:
        if repo_name:
            # Fetch the repository information
            info = get_repo_info(repo_name)

            if info:
                # Write the result to the output CSV file
                with open(output_csv, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=csv_headers)
                    writer.writerow(info)

                print(f"{repo_name} : done and saved to file")
            else:
                print(f"Could not retrieve information for {repo_name}")
else:
    print(f"Input file {input_file} does not exist. Please provide a valid input file.")

print(f"All available repository information has been saved to {output_csv}")
