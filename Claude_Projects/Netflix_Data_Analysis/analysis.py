import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# Set output directory
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Global styling
BKG_COLOR = '#0B0B0B'
TEXT_COLOR = '#FFFFFF'
RED_DARK = '#B20710'
RED_MAIN = '#E50914'
RED_BRIGHT = '#FF4C4C'

def set_dark_style():
    plt.rcParams['figure.facecolor'] = BKG_COLOR
    plt.rcParams['axes.facecolor'] = BKG_COLOR
    plt.rcParams['text.color'] = TEXT_COLOR
    plt.rcParams['axes.labelcolor'] = TEXT_COLOR
    plt.rcParams['xtick.color'] = TEXT_COLOR
    plt.rcParams['ytick.color'] = TEXT_COLOR
    plt.rcParams['axes.edgecolor'] = '#B3B3B3'
    plt.rcParams['grid.color'] = 'none'

# 1. Data Loading and Cleaning
df = pd.read_csv('cleaned_netflix_titles.csv')

initial_rows = df.shape[0]
initial_cols = df.shape[1]

# Check missing values
missing_values = df.isnull().sum()

# Drop missing rows
df_cleaned = df.dropna().copy()

final_rows = df_cleaned.shape[0]
final_cols = df_cleaned.shape[1]

# Dataset info
dataset_info = df_cleaned.describe(include='all').to_string()
column_names = df_cleaned.columns.tolist()

with open('data_info.txt', 'w') as f:
    f.write(f"Initial rows and columns: {initial_rows}, {initial_cols}\n")
    f.write("\nMissing values per column:\n")
    f.write(missing_values.to_string())
    f.write(f"\n\nFinal rows and columns after cleaning: {final_rows}, {final_cols}\n")
    f.write("\nDataset Information:\n")
    f.write(dataset_info)
    f.write("\n\nColumn Names:\n")
    f.write(", ".join(column_names))

print("Data cleaning complete. Info saved to data_info.txt")

# Visualization functions
def apply_red_shades(counts):
    # High values -> #B20710, Medium -> #E50914, Low -> #FF4C4C
    colors = []
    max_val = counts.max()
    min_val = counts.min()

    for val in counts:
        if val >= 0.8 * max_val:
            colors.append(RED_DARK)
        elif val >= 0.4 * max_val:
            colors.append(RED_MAIN)
        else:
            colors.append(RED_BRIGHT)
    return colors

# 2. Top 10 Genres
set_dark_style()
plt.figure(figsize=(10, 6))
genre_counts = df_cleaned['listed_in'].value_counts().head(10)
colors = apply_red_shades(genre_counts)
bars = plt.barh(genre_counts.index, genre_counts.values, color=colors)
plt.title('Top 10 Genres', color=TEXT_COLOR)
plt.xlabel('Count', color=TEXT_COLOR)
plt.gca().invert_yaxis()
plt.grid(False)

# Add labels
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{int(width)}',
             va='center', ha='left', color=TEXT_COLOR)

plt.tight_layout()
plt.savefig(f'{output_dir}/Top 10 Genres.png')
plt.close()

# 3. Distribution of Titles by Type
set_dark_style()
plt.figure(figsize=(8, 6))
type_counts = df_cleaned['type'].value_counts().sort_values(ascending=False)
bars = plt.bar(type_counts.index, type_counts.values, color=RED_MAIN)
plt.title('Distribution of Titles by Type', color=TEXT_COLOR)
plt.ylabel('Count', color=TEXT_COLOR)
plt.grid(False)

# Add labels on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.1, f'{int(height)}',
             va='bottom', ha='center', color=TEXT_COLOR)

plt.tight_layout()
plt.savefig(f'{output_dir}/Distribution of Titles by Type.png')
plt.close()

# 4. Number of Titles Released Each Year
set_dark_style()
plt.figure(figsize=(12, 6))
year_counts = df_cleaned['release_year'].value_counts().sort_index(ascending=False)
# We want top years or just distribution? CLAUDE.md says "Number of Titles Released Each Year"
# Usually, we show all or the most frequent. Let's show the distribution.
# To avoid overcrowding, let's take the top 30 years or use a bar chart.
top_years = year_counts.sort_values(ascending=False).head(30)
bars = plt.bar(top_years.index.astype(str), top_years.values, color=RED_MAIN)
plt.title('Number of Titles Released Each Year', color=TEXT_COLOR)
plt.ylabel('Count', color=TEXT_COLOR)
plt.grid(False)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.1, f'{int(height)}',
             va='bottom', ha='center', color=TEXT_COLOR, fontsize=8)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}/Number of Titles Released Each Year.png')
plt.close()

# 5. Top 10 Countries with the Most Titles
set_dark_style()
plt.figure(figsize=(10, 6))
country_counts = df_cleaned['country'].value_counts().head(10)
colors = apply_red_shades(country_counts)
bars = plt.barh(country_counts.index, country_counts.values, color=colors)
plt.title('Top 10 Countries with the Most Titles', color=TEXT_COLOR)
plt.xlabel('Number of Titles', color=TEXT_COLOR)
plt.gca().invert_yaxis()
plt.grid(False)

for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{int(width)}',
             va='center', ha='left', color=TEXT_COLOR)

plt.tight_layout()
plt.savefig(f'{output_dir}/Top 10 Countries with the Most Titles.png')
plt.close()

# 6. Top 10 Directors
set_dark_style()
plt.figure(figsize=(10, 6))
directors = df_cleaned['director'].dropna().str.split(', ').explode()
director_counts = directors.value_counts().head(10)
colors = apply_red_shades(director_counts)
bars = plt.barh(director_counts.index, director_counts.values, color=colors)
plt.title('Top 10 Directors', color=TEXT_COLOR)
plt.xlabel('Count', color=TEXT_COLOR)
plt.gca().invert_yaxis()
plt.grid(False)

for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{int(width)}',
             va='center', ha='left', color=TEXT_COLOR)

plt.tight_layout()
plt.savefig(f'{output_dir}/Top 10 Directors.png')
plt.close()

# 7. Distribution of Movie Durations
set_dark_style()
plt.figure(figsize=(10, 6))
# Extract minutes from duration
movies_df = df_cleaned[df_cleaned['type'] == 'Movie'].copy()
movies_df['duration_min'] = movies_df['duration'].str.extract(r'(\d+)').astype(float)

sns.histplot(movies_df['duration_min'], color=RED_MAIN, kde=True,
             line_kws={'color': RED_BRIGHT}, stat='count')
plt.title('Distribution of Movie Durations', color=TEXT_COLOR)
plt.xlabel('Duration (minutes)', color=TEXT_COLOR)
plt.ylabel('Count', color=TEXT_COLOR)
plt.grid(False)

# Adding labels on top of bars is tricky for histplot, let's try to get the patches
ax = plt.gca()
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        plt.text(p.get_x() + p.get_width()/2, height + 0.1, f'{int(height)}',
                 va='bottom', ha='center', color=TEXT_COLOR, fontsize=8)

plt.tight_layout()
plt.savefig(f'{output_dir}/Distribution of Movie Durations.png')
plt.close()

# 8. Dashboard HTML
images = [
    "Top 10 Genres.png",
    "Distribution of Titles by Type.png",
    "Number of Titles Released Each Year.png",
    "Top 10 Countries with the Most Titles.png",
    "Top 10 Directors.png",
    "Distribution of Movie Durations.png"
]

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netflix Data Intelligence Dashboard</title>
    <style>
        body {{
            background-color: black;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: {RED_MAIN};
            text-align: center;
            margin-bottom: 40px;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            width: 100%;
            max-width: 1200px;
        }}
        .chart-container {{
            background-color: #1a1a1a;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }}
        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .chart-title {{
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #ccc;
        }}
    </style>
</head>
<body>
    <h1>Netflix Data Intelligence Dashboard</h1>
    <div class="dashboard-grid">
"""

for img in images:
    html_content += f"""
        <div class="chart-container">
            <div class="chart-title">{img.replace('.png', '')}</div>
            <img src="{img}" alt="{img}">
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open(f'{output_dir}/dashboard.html', 'w') as f:
    f.write(html_content)

print("Dashboard HTML created.")
