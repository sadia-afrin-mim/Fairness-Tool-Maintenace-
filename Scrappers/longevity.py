import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from CSV file
data = pd.read_csv('lonevity.csv')  # Replace with your actual file path

# Set up the figure and plot each variable in separate violin plots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Violin plot for Longevity
sns.violinplot(x='Status', y='Longevity', data=data, ax=axes[0])
axes[0].set_title('Longevity by Project Status')
axes[0].set_xlabel('Status')
axes[0].set_ylabel('Longevity')

# Violin plot for Last Commit Since
sns.violinplot(x='Status', y='Last commit since', data=data, ax=axes[1])
axes[1].set_title('Last Commit Since by Project Status')
axes[1].set_xlabel('Status')
axes[1].set_ylabel('Last Commit Since (years)')

# Adjust layout and display the plots
plt.tight_layout()
plt.show()
