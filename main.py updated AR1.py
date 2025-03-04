import pandas as pd
import numpy as np
import plotly.express as px
from flask import Flask, render_template

## BR 1 ##
# set the file path
file_path = 'dirtydata.csv'

# read the file using pandas
data = pd.read_csv(file_path, encoding="windows-1252", na_values=['NaN', ''])
# if encoding is not working, use encoding='utf-8'

# read the file using pandas and remove special characters (€)
#data = pd.read.csv(file_path)
data = data.replace({'€': ' '}, regex = True)

# drop and delete rows with missing data
data = data.dropna()

# fill this in
numeric_cols = ['......']
for col in numeric_cols:
  data[col] = pd.to_numeric(data[col], errors='coerce')

# save cleaned data to a new file
cleaned_file_path = 'cleandata.csv'
data.to_csv(cleaned_file_path, index = False)

print("I saved the clean file here:", cleaned_file_path)


## BR 2 ##
# define non numeric columns 
non_numeric_cols = ['Year']

# create a dictionary for statistics
stats_dictionary = {}

for col in data.columns: # go through each column but skip first column
  if col not in non_numeric_cols:
    stats_data = data[col]
    # populate stats_dictionary with stats on each column 
    stats_dictionary[col] = {
      'Mean': stats_data.mean(),
      'Median': stats_data.median(),
      'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
      'Range': stats_data.max() - stats_data.min()
    }

# to view the dictionary 
# print(stats_dictionary)

# convert stats to DataFrame so it looks nicer when printed
stats_df = pd.DataFrame(stats_dictionary).transpose()
print(stats_df)

range_value = stats_df.loc["...name of column...", "Range"]
print("My range is: ", range_value)

# change these values later
if range_value > 281:
  #print("That range is fantastic! I'd recommend you leave it as it is.")
  recommendation = ("That range is fantastic! I'd recommend you leave it as it is.")

elif range_value < 281 and range_value > 5: 
  #print("That range is fine. I'd recommend you increase it.")
  recommendation = ("That range is fine. I'd recommend you increase it.")
  
else:
  #print("Your data is all the same.")
  recommendation = ("That range is fine. I'd recommend you increase it.")

# graphs using plotly
bar_chart = px.bar(
    data,
    x = data.columns[0],
    y = data.columns[1],
    title="Bar Chart: Column 0 vs Column 1",
    labels={data.columns[0]: "Year", data.columns[1]: "Values"}
    )

# graph 2: line chart (Column 0 vs Columns 1, 2, 3, and 4)
data_long = data.melt(
    id_vars=[data. columns [0]],
    value_vars=[data.columns[1], data.columns[2], data.columns[3], data.columns[4]]
    name="Variable",
    value_name="Value"
    )

line_chart = px. line(
    data_long, 
    x = data.columns [0],
    y = "Value",
    color="Variable",
    title="Line Chart: Column 0 vs Columns 1, 2, 3, and 4"),
    labels={data.columns[0]: "Year", "Value": "Values", "Variable": "Categories"}
)
line_chart_html = line_chart.to_html(full_html=False, include_plotlyjs="cdn")

# graph 3: scatter plot (column 3 vs column 4)
scatter_plot = px.scatter(
    data,
    x = data.columns[2],
    y = data.columns[3],
    title="Scatter Plot: Column 3 vs Column 4",
    labels={data.columns[3]: "Values"}
)
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

# comment out for BR3 once they are in the webpage
bar_chart.show()
line_chart.show()
scatter_plot.show()

## BR 3 ##
app = Flask(__name__)

# routes
@app.route('/')
def index():
    return render_template(
        'index.html'
        bar_chart=bar_chart_html,
        line_chart=line_chart_html,
        scatter_chart=scatter_plot_html
        )

@app.route('/recommendations')
def recommendations():
  return render_template('recommendations.html', recommendation = recommendation)

@app.route('/suggestions')
def suggestions():
  return render_template('suggestions.html')
                    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)


