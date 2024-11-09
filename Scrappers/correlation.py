import pandas as pd
import numpy as np

# Load your classified data file
file_path = 'classified_data.csv'  # Replace with the correct path to your file
df = pd.read_csv(file_path)

# Convert the target classification to numeric if it's categorical (e.g., 'maintained' or 'unmaintained')
df['Classification'] = df['Classification'].astype('category').cat.codes

# Calculate the correlation between each feature and the target
correlations = df.corr()['Classification'].drop('Classification').sort_values(ascending=False)

# Convert the correlations to a DataFrame for easy viewing and save to CSV
correlation_df = pd.DataFrame(correlations).reset_index()
correlation_df.columns = ['Feature', 'Correlation with Classification']
correlation_df.to_csv('feature_correlation_output.csv', index=False)

# Display the feature with highest and lowest correlation for quick summary
print("Feature with highest correlation:", correlation_df.iloc[0]['Feature'])
print("Feature with lowest correlation:", correlation_df.iloc[-1]['Feature'])
print("Correlations have been saved to feature_correlation_output.csv")
