import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('consolidated_star_trend.csv')  # Replace with your actual file path

# Aggregate duplicate entries by summing up the stars for each (Repository, Year) pair
data = data.groupby(['Repository', 'Year'], as_index=False).sum()

# Define the full range of years and unique repositories
all_years = np.arange(2019, 2025)  # Ensuring it covers 2016 to 2024 inclusively, based on your provided data
all_repos = data['Repository'].unique()

# Create a DataFrame with all combinations of Repository and Year
complete_index = pd.MultiIndex.from_product([all_repos, all_years], names=["Repository", "Year"])
complete_data = pd.DataFrame(index=complete_index).reset_index()

# Merge the complete DataFrame with the original data, filling missing values with 0 for StarsPerYear
data_complete = pd.merge(complete_data, data, on=["Repository", "Year"], how="left").fillna(0)

# Pivot the data for heatmap plotting
heatmap_data = data_complete.pivot(index="Repository", columns="Year", values="StarsPerYear")

# Check if all expected repositories and years are present in the final dataset
print("Final data used for heatmap:\n", heatmap_data)

# Plot heatmap
plt.figure(figsize=(15, 12))
sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5, linecolor='gray', annot=True, fmt=".0f")
#plt.title("Number of Stars Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()


#################################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('consolidated_pr_trend.csv')  # Replace with your actual file path

# Check for duplicates in the original data
duplicates = data[data.duplicated(subset=["Repository", "Year"], keep=False)]
if not duplicates.empty:
    print("Found duplicate entries:\n", duplicates)

# Aggregate duplicate entries by summing PR counts (modify this as needed, e.g., .mean() for averaging)
data = data.groupby(["Repository", "Year"], as_index=False).sum()

# Define the full range of years and unique repositories
all_years = np.arange(data['Year'].min(), data['Year'].max() + 1)
all_repos = data['Repository'].unique()

# Create a DataFrame with all combinations of Repository and Year
complete_index = pd.MultiIndex.from_product([all_repos, all_years], names=["Repository", "Year"])
complete_data = pd.DataFrame(index=complete_index).reset_index()

# Merge this complete DataFrame with the original data, filling missing values with 0
data_complete = pd.merge(complete_data, data, on=["Repository", "Year"], how="left").fillna(0)

# Pivot for each type of PR data
open_pr_data = data_complete.pivot(index="Repository", columns="Year", values="OpenPRsPerYear")
closed_pr_data = data_complete.pivot(index="Repository", columns="Year", values="ClosedPRsPerYear")
merged_pr_data = data_complete.pivot(index="Repository", columns="Year", values="MergedPRsPerYear")

# Plot separate heatmap for Open PRs
plt.figure(figsize=(14, 10))
sns.heatmap(open_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray')
#plt.title("Open PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()

# Plot separate heatmap for Closed PRs
plt.figure(figsize=(14, 10))
sns.heatmap(closed_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray')
#plt.title("Closed PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()

# Plot separate heatmap for Merged PRs
plt.figure(figsize=(14, 10))
sns.heatmap(merged_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray')
#plt.title("Merged PRs Per Year for Each Repository")
plt.xlabel("Year")
plt.ylabel("Repository")
plt.show()
###############################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('consolidated_pr_trend.csv')  # Replace with your actual file path

# Filter data to include only years from 2019 onward
data = data[data['Year'] >= 2019]

# Check for duplicates in the filtered data
duplicates = data[data.duplicated(subset=["Repository", "Year"], keep=False)]
if not duplicates.empty:
    print("Found duplicate entries:\n", duplicates)

# Aggregate duplicate entries by summing PR counts
data = data.groupby(["Repository", "Year"], as_index=False).sum()

# Define the full range of years and unique repositories
all_years = np.arange(2019, data['Year'].max() + 1)
all_repos = data['Repository'].unique()

# Create a DataFrame with all combinations of Repository and Year
complete_index = pd.MultiIndex.from_product([all_repos, all_years], names=["Repository", "Year"])
complete_data = pd.DataFrame(index=complete_index).reset_index()

# Merge this complete DataFrame with the filtered data, filling missing values with 0
data_complete = pd.merge(complete_data, data, on=["Repository", "Year"], how="left").fillna(0)

# Pivot for each type of PR data
open_pr_data = data_complete.pivot(index="Repository", columns="Year", values="OpenPRsPerYear")
closed_pr_data = data_complete.pivot(index="Repository", columns="Year", values="ClosedPRsPerYear")
merged_pr_data = data_complete.pivot(index="Repository", columns="Year", values="MergedPRsPerYear")

# Plot heatmaps side by side in a single figure with smaller text size
fig, axes = plt.subplots(1, 3, figsize=(20, 10))

# Set font sizes for heatmap annotations, labels, and tick labels
heatmap_font_size = 8
label_font_size = 8
title_font_size = 8
tick_label_size = 8  # Size for repository names and years on the axes

# Open PRs heatmap with repository names
sns.heatmap(open_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray',
            ax=axes[0], annot_kws={"size": heatmap_font_size})
axes[0].set_title("Open PRs Per Year", fontsize=title_font_size)
axes[0].set_xlabel("Year", fontsize=label_font_size)
axes[0].set_ylabel("Repository", fontsize=label_font_size)
axes[0].tick_params(axis='x', labelsize=tick_label_size)
axes[0].tick_params(axis='y', labelsize=tick_label_size)

# Closed PRs heatmap without repository names
sns.heatmap(closed_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray',
            ax=axes[1], annot_kws={"size": heatmap_font_size})
axes[1].set_title("Closed PRs Per Year", fontsize=title_font_size)
axes[1].set_xlabel("Year", fontsize=label_font_size)
axes[1].set_ylabel("")  # Remove y-axis label
axes[1].tick_params(axis='x', labelsize=tick_label_size)
axes[1].tick_params(axis='y', left=False, labelleft=False)  # Hide y-axis tick labels

# Merged PRs heatmap without repository names
sns.heatmap(merged_pr_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, linecolor='gray',
            ax=axes[2], annot_kws={"size": heatmap_font_size})
axes[2].set_title("Merged PRs Per Year", fontsize=title_font_size)
axes[2].set_xlabel("Year", fontsize=label_font_size)
axes[2].set_ylabel("")  # Remove y-axis label
axes[2].tick_params(axis='x', labelsize=tick_label_size)
axes[2].tick_params(axis='y', left=False, labelleft=False)  # Hide y-axis tick labels

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
