#'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'
import requests
import pandas as pd
from datetime import datetime

# Your GitHub token here
GITHUB_TOKEN = ''

# GitHub GraphQL endpoint
url = 'https://api.github.com/graphql'

# Set up headers with authentication token
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Read repository list from a text file
with open('testdata', 'r') as file:
    repo_list = [line.strip() for line in file if line.strip()]

# Output DataFrames to store consolidated data
star_trend_all = pd.DataFrame()
pr_trend_all = pd.DataFrame()

# Function to paginate through all stargazer data
def fetch_stargazers(owner, name):
    stargazers = []
    cursor = None
    while True:
        query = """
        {
          repository(owner: "%s", name: "%s") {
            stargazers(first: 100, after: %s, orderBy: {field: STARRED_AT, direction: ASC}) {
              edges {
                starredAt
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
        }
        """ % (owner, name, f'"{cursor}"' if cursor else 'null')

        response = requests.post(url, json={'query': query}, headers=headers)
        data = response.json()

        if 'errors' in data:
            print(f"Error fetching stargazers for {owner}/{name}:", data['errors'])
            break

        stargazer_edges = data['data']['repository']['stargazers']['edges']
        stargazers.extend([edge['starredAt'] for edge in stargazer_edges])

        page_info = data['data']['repository']['stargazers']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']

    return stargazers

# Function to paginate through all pull request data
def fetch_pull_requests(owner, name):
    pull_requests = []
    cursor = None
    while True:
        query = """
        {
          repository(owner: "%s", name: "%s") {
            pullRequests(first: 100, after: %s, states: [OPEN, MERGED, CLOSED], orderBy: {field: CREATED_AT, direction: ASC}) {
              edges {
                node {
                  createdAt
                  closedAt
                  mergedAt
                  state
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
        }
        """ % (owner, name, f'"{cursor}"' if cursor else 'null')

        response = requests.post(url, json={'query': query}, headers=headers)
        data = response.json()

        if 'errors' in data:
            print(f"Error fetching pull requests for {owner}/{name}:", data['errors'])
            break

        pr_edges = data['data']['repository']['pullRequests']['edges']
        pull_requests.extend([
            {
                'CreatedAt': pr['node']['createdAt'],
                'ClosedAt': pr['node']['closedAt'],
                'MergedAt': pr['node']['mergedAt'],
                'State': pr['node']['state']
            }
            for pr in pr_edges
        ])

        page_info = data['data']['repository']['pullRequests']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']

    return pull_requests

# Loop through each repository in the list
for repo in repo_list:
    owner, name = repo.split('/')
    print(f"Processing repository: {owner}/{name}")

    # Fetch stargazers
    star_dates = fetch_stargazers(owner, name)
    if star_dates:
        star_df = pd.DataFrame({'StarredAt': pd.to_datetime(star_dates)})
        star_df['Year'] = star_df['StarredAt'].dt.to_period('Y')
        star_trend = star_df.groupby('Year').size().reset_index(name='StarsPerYear')
        star_trend['Repository'] = f"{owner}/{name}"
        star_trend_all = pd.concat([star_trend_all, star_trend], ignore_index=True)

    # Fetch pull requests
    pr_data = fetch_pull_requests(owner, name)
    if pr_data:
        pr_df = pd.DataFrame(pr_data)
        pr_df['CreatedAt'] = pd.to_datetime(pr_df['CreatedAt'])
        pr_df['Year'] = pr_df['CreatedAt'].dt.to_period('Y')
        pr_df['Repository'] = f"{owner}/{name}"

        # Group by year and state to count PRs in each state per year
        open_pr_trend = pr_df[pr_df['State'] == 'OPEN'].groupby(['Year', 'Repository']).size().reset_index(name='OpenPRsPerYear')
        closed_pr_trend = pr_df[pr_df['State'] == 'CLOSED'].groupby(['Year', 'Repository']).size().reset_index(name='ClosedPRsPerYear')
        merged_pr_trend = pr_df[pr_df['State'] == 'MERGED'].groupby(['Year', 'Repository']).size().reset_index(name='MergedPRsPerYear')

        # Combine PR trends
        pr_trend_combined = open_pr_trend.merge(closed_pr_trend, on=['Year', 'Repository'], how='outer').merge(merged_pr_trend, on=['Year', 'Repository'], how='outer')
        pr_trend_all = pd.concat([pr_trend_all, pr_trend_combined], ignore_index=True)

# Save consolidated results to CSV
star_trend_all.to_csv('consolidated_star_trend.csv', index=False)
pr_trend_all.to_csv('consolidated_pr_trend.csv', index=False)

print("Consolidated star trends and pull request trends saved to CSV files.")
