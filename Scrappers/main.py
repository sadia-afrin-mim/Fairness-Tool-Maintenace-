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

# Plot heatmap with bold font for repository names and values
plt.figure(figsize=(15, 12))
sns.heatmap(
    heatmap_data,
    cmap="YlGnBu",
    linewidths=0.5,
    linecolor='gray',
    annot=True,
    fmt=".0f",
    annot_kws={"fontweight": "bold"}
)
plt.xlabel("Year")
plt.ylabel("Repository")

# Make repository names bold
plt.yticks(fontweight="bold")

plt.show()
