
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the dataset
df = pd.read_csv("/Users/13454/Desktop/Results_21Mar2022.csv")

# 2. Select relevant environmental impact columns
env_columns = [
    "mean_ghgs", "mean_land", "mean_watuse",
    "mean_bio", "mean_acid", "mean_eut", "mean_watscar"
]
df_cleaned = df.dropna(subset=["diet_group"])

# 3. Group by diet type and calculate the mean for each variable
df_grouped = df_cleaned.groupby("diet_group")[env_columns].mean()

# 4. Ensure diet types are ordered consistently
ordered_diets = ["vegan", "veggie", "fish", "meat50", "meat", "meat100"]
df_grouped = df_grouped.loc[ordered_diets]

# 5. Normalize the data for radar chart comparison (min-max scaling)
data_norm = (df_grouped - df_grouped.min()) / (df_grouped.max() - df_grouped.min())

# 6. Set up radar chart axis and labels
labels = [
    "GHG Emissions", "Land Use", "Water Use",
    "Biodiversity", "Acidification", "Eutrophication", "Water Scarcity"
]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]  # close the loop

# 7. Plot the radar chart
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

for diet in data_norm.index:
    values = data_norm.loc[diet].tolist()
    values += values[:1]
    ax.plot(angles, values, label=diet)
    ax.fill(angles, values, alpha=0.1)

# 8. Customize the appearance
ax.set_title("Environmental Impact by Diet Type (All 6 Types, Normalized)", size=14)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=10)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.05))

# 9. Save the chart and show
plt.tight_layout()
plt.savefig("CW2_RadarChart_6DietTypes.png")
plt.show()
