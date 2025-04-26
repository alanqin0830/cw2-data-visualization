import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. Load the dataset
df = pd.read_csv("/Users/13454/Desktop/Results_21Mar2022.csv")  

# 2. Select relevant environmental impact columns
env_columns = [col for col in df.columns if col.startswith("mean_")]
df_cleaned = df.dropna(subset=["diet_group"])

# 3. Group by diet type and calculate the mean for each variable
df_grouped = df_cleaned.groupby("diet_group")[env_columns].mean()

# 4. Ensure diet types are ordered consistently
ordered_diets = ["vegan", "veggie", "fish", "meat50", "meat", "meat100"]
df_grouped = df_grouped.loc[ordered_diets]

# 5. Normalize the data for radar chart comparison (min-max scaling)
data_norm = (df_grouped - df_grouped.min()) / (df_grouped.max() - df_grouped.min())
data_norm = data_norm * 0.95 + 0.05  # Adjusted normalization for better visibility

# 6. Select 15 indicators (top 15 columns) for detailed radar chart
selected_columns = data_norm.columns[:15]
data = data_norm[selected_columns]
labels = [col.replace("mean_", "").replace("_", " ").title() for col in selected_columns]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
labels += labels[:1]  # close the radar chart

# 7. Create interactive radar chart
fig = go.Figure()

# Define color mapping for each diet group
color_map = {
    "vegan": "gold",
    "veggie": "lightgreen",
    "fish": "dodgerblue",
    "meat50": "orange",
    "meat": "red",
    "meat100": "darkred"
}

# Add traces for each diet group
for diet in data.index:
    values = data.loc[diet].tolist() + [data.loc[diet].tolist()[0]]
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        mode='lines+markers',
        name=diet,
        line=dict(color=color_map[diet], width=2.5 if diet == "vegan" else 1.5),
        marker=dict(size=6),
        hovertemplate=f"<b>{diet}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>"
    ))

# 8. Customize chart layout
fig.update_layout(
    title="Environmental Impact by Diet Type – Detailed Radar Chart (15 Indicators)",
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            showticklabels=True,
            tickfont_size=10
        ),
        angularaxis=dict(
            rotation=90,
            direction="clockwise"
        )
    ),
    template="plotly_dark",
    legend_title_text="Diet Group",
    autosize=True
)

# 9. Show the chart
fig.show()

# 10. (Optional) Save the interactive radar chart as an HTML file
fig.write_html("CW2_RadarChart_Interactive_15Indicators.html")


