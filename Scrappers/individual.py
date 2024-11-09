from github import Github
from datetime import datetime

# Replace with your GitHub personal access token
ACCESS_TOKEN = ''

# Replace with the repository owner and name (e.g., 'owner/repo')
REPO_NAME = 'sakshiudeshi/Aequitas'

# Initialize Github object
g = Github(ACCESS_TOKEN)
repo = g.get_repo(REPO_NAME)

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
merged_prs_count = repo.get_pulls(state='closed').totalCount - len([pr for pr in repo.get_pulls(state='closed') if pr.merged_at is None])

# 7. Number of commits by developers
total_commits = repo.get_commits().totalCount

# 8. Maximum days of the repository without a commit
commits = repo.get_commits()
commit_dates = [commit.commit.author.date for commit in commits]
max_days_without_commit = max((commit_dates[i] - commit_dates[i + 1]).days for i in range(len(commit_dates) - 1))

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
owner_projects = g.get_user(owner.login).get_projects().totalCount

# 12. Number of commits from the project owner
owner_commits = repo.get_commits(author=owner.login).totalCount

# Display the results
print(f'1. Number of forks: {num_forks}')
print(f'2. Total number of issues opened by devs: {open_issues_count}')
print(f'3. Number of issues closed by devs: {closed_issues_count}')
print(f'4. Number of open pull requests: {open_prs_count}')
print(f'5. Number of closed pull requests: {closed_prs_count}')
print(f'6. Number of merged pull requests: {merged_prs_count}')
print(f'7. Number of commits by devs: {total_commits}')
print(f'8. Max days without commit: {max_days_without_commit}')
print(f'9. Number of commits by the most active developer: {max_commits_by_dev}')
print(f'10. Total number of contributors: {total_contributors}')
print(f'11. Number of projects by project owner: {owner_projects}')
print(f'12. Number of commits from the project owner: {owner_commits}')
