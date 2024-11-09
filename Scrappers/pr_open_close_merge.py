import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('consolidated_pr_trend.csv')  # Replace with your actual file path

# Fill NaN values with 0
data.fillna(0, inplace=True)

# Aggregate duplicate entries by summing up PRs for each (Repository, Year) pair
data = data.groupby(['Repository', 'Year'], as_index=False).sum()

# Pivot data for each PR type
open_pr_data = data.pivot(index="Repository", columns="Year", values="OpenPRsPerYear").fillna(0)
closed_pr_data = data.pivot(index="Repository", columns="Year", values="ClosedPRsPerYear").fillna(0)
merged_pr_data = data.pivot(index="Repository", columns="Year", values="MergedPRsPerYear").fillna(0)

# Plot heatmap for Open PRs
plt.figure(figsize=(12, 8))
sns.heatmap(open_pr_data, cmap="YlGnBu", linewidths=.5, linecolor='gray')
plt.title("Open PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()

# Plot heatmap for Closed PRs
plt.figure(figsize=(12, 8))
sns.heatmap(closed_pr_data, cmap="YlGnBu", linewidths=.5, linecolor='gray')
plt.title("Closed PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()

# Plot heatmap for Merged PRs
plt.figure(figsize=(12, 8))
sns.heatmap(merged_pr_data, cmap="YlGnBu", linewidths=.5, linecolor='gray')
plt.title("Merged PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()
