import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file with only two columns(id and score)
df = pd.read_csv('../newport.csv', header=None)

# Extract scores from the second column
scores = df.iloc[:, 1]

# Calculate the mean of the scores
mean_score = scores.mean()

# Create bins for the bar graph
bins = range(0, 110, 10)

# Create a histogram with the accumulated scores
plt.hist(scores, bins=bins, edgecolor='black', cumulative=True)
plt.xlabel('Score Ranges')
plt.ylabel('Accumulated People')
plt.title('Accumulated Distribution')
plt.axvline(x=mean_score, color='r', linestyle='--', label=f'Mean Score: {mean_score}')
plt.legend()
plt.show()

# Create a histogram for the regular distribution
plt.hist(scores, bins=bins, edgecolor='black')
plt.xlabel('Score Ranges')
plt.ylabel('Number of People')
plt.title('Score Distribution')
plt.axvline(x=mean_score, color='r', linestyle='--', label=f'Mean Score: {mean_score}')
plt.legend()
plt.show()
