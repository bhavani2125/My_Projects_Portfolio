# Netflix Titles Dashboard — Claude Code Context
> You are a Professional Data Analyzer and here you are analyzing the Netflix data.
> Please find the number of rows and columns in the file using pandas.
> Please check the data have any missing values.
> Please drop those missing rows using pandas. 
> After cleaning the Data Please display the number of rows and columns using Pandas.
> Extract dataset information using pandas.
> Extract all column names in the file  using pandas
> save all above information in data_info.txt file.


# set up

- CSV is in 'C:\Users\bhava\OneDrive\Desktop\Python_Projects\Netflix_Data_Analysis\cleaned_netflix_titles.csv'
- Install packages: pandas matplotlib numpy seaborn 
- Columns:'show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
       'release_year', 'rating', 'duration', 'listed_in', 'description'
- Use ALL rows

# Apply the following exact color styling:

GLOBAL:

Use THREE red shades:

High values → #B20710 (dark red)
Medium values → #E50914 (main Netflix red)
Low values → #FF4C4C (bright red)

Do NOT use a single red for all bars.

RULES:

Do NOT use white, blue, or gray for data bars
Only use red shades for all data
Remove bar borders
Use gradients only within red palette
Keep design minimal and consistent


### 1. `output/Top 10 Genres.png`
- Plot a horizontal bar chart with counts on the x-axis and genres on the y-axis.
- Select ONLY the top 10 most frequent genres.
- Do NOT split genres.
- Treat each row as a single combined category.
- Align data labels horizontally On the right end of each bar.
- All bar charts must be sorted in DESCENDING order
- Highest values should appear at the TOP (for horizontal charts)
- Add small spacing from bar (padding).
- Do NOT place labels randomly inside the chart.
- Use font color:#FFFFFF.
- Remove the grid lines.

### 2. `output/Distribution of Titles by Type`
- plot a bar chart with type on the x-axis and count on the y-axis.
- count the each categeory and plot the bar chart.
- Use "Distribution of Titles by Type" as title for the chart.
- Add data labels (numbers) at the top of the each bar.
- Do NOT place labels randomly inside the chart.
- Use font color:#FFFFFF.
- Remove the grid lines.

### 3. `output/Number of Titles Released Each Year`
- plot the bar chart with year on the x-axis and count on the y-axis.
- Extract year from Release year.
- Use "Number of Titles Released Each Year" as title for the chart.
- Add data labels (numbers) at the top of the each bar.
- Do NOT place labels randomly inside the chart.
- Use font color:#FFFFFF.
- Remove the grid lines.

### 4. `output/Top 10 Countries with the Most Titles`
- Plot bar chart with Number of Titles on x-axis and Country on the y-axis.
- Select only top 10. 
- Use "Top 10 Countries with the Most Titles" as title for the chart.
- All bar charts must be sorted in DESCENDING order
- Highest values should appear at the TOP (for horizontal charts)
- Align data labels horizontally On the right end of each bar.
- Add small spacing from bar (padding).
- Do NOT place labels randomly inside the chart.
- Use font color:#FFFFFF.
- Remove the grid lines.

### 5. `output/Top 10 Directors`

- split the directors and get the top 10 directors with individual bar.
- Plot bar polt with count on X-axis and Director on y-axis.
- Get the lables for bars.
- Add small spacing from bar (padding).
- All bar charts must be sorted in DESCENDING order
- Highest values should appear at the TOP (for horizontal charts)
- Align data labels horizontally On the right end of each bar.
- Do NOT place labels randomly inside the chart.
- Use font color:#FFFFFF.
- Remove the grid lines.

### 6. `output/Distribution of Movie Durations`

- Extract minutes data from the Duration.
- plot the histplot with Duration(minutes) on x-axis and count on y-axis.
- Use COUNT as the statistic (do NOT normalize or scale).
- Add a smooth KDE curve on top.

* IMPORTANT:

- Do NOT change bin size when applying styling
- Do NOT change the underlying distribution
- Do NOT use stacking or grouping (no hue)
- Do NOT alter the shape of the histogram

* COLOR STYLING:

- Bars: #E50914
- KDE curve: #FF4C4C
- Background: #0B0B0B
- Text: #FFFFFF
- Axis: #B3B3B3

* VISUAL RULE:

- Styling changes must NOT affect the data distribution or shape
- Add data labels (numbers) at the top of the each bar.
- Remove grid lines.

### 7. `output/dashboard.html`

Apply dark theme return intelligence dashboard (single self-contained HTML file):
- Background color: black
- Axes background: black
- Text color: white
- Grid: subtle or off
- write HTML file in "output/dashboard.html" file


## Rules
1. First read the csv file
2. Install packages silently (`pip install -q`)
3. Use ALL data










