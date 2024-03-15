import matplotlib.pyplot as plt
import numpy as np

# Data for group x and y
data_x = {
    '1': 33,
    '2': 30,
    '3': 14,
    '4': 18,
    '5': 5
}
data_y = {
    '1': 71,
    '2': 71,
    '3': 87,
    '4': 83,
    '5': 96
}

# Extract classes and percentages for group x and y
classes = list(data_x.keys())
percentages_x = list(data_x.values())
percentages_y = list(data_y.values())

# Create the plot
plt.figure(figsize=(8, 6))

# Plot bars for group x
plt.bar(np.arange(len(classes)) - 0.2, percentages_x, width=0.4, color='salmon', label='Group X - Not Morisien')

# Plot bars for group y
plt.bar(np.arange(len(classes)) + 0.2, percentages_y, width=0.4, color='skyblue', label='Group Y - Morisien')

# Calculate and display proportions
for i, class_name in enumerate(classes):
    prop_x = percentages_x[i] / (percentages_x[i] + percentages_y[i]) * 100
    prop_y = percentages_y[i] / (percentages_x[i] + percentages_y[i]) * 100
    plt.text(i - 0.2, percentages_x[i] + 2, f'{prop_x:.1f}%', ha='center', color='black')
    plt.text(i + 0.2, percentages_y[i] + 2, f'{prop_y:.1f}%', ha='center', color='black')


plt.xlabel('Rarity Classes (Number of Occurences in Collected Data)')
plt.ylabel('Number of Observations')
plt.title('Comparison of proportions between Group X and Group Y')

# Show legend
plt.legend()

# Show plot
plt.xticks(np.arange(len(classes)), classes)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()