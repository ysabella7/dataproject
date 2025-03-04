import pandas as pd
import numpy as np
import plotly.express as px
from flask import Flask, render_template

# set the file path
file_path = 'dirtydata.csv'

# read the file using pandas
data = pd.read_csv(file_path, encoding="windows-1252", na_values=['NaN', ''])
#data = pd.read_csv(file_path, na_values=['NaN', ' '])

# read the file using pandas and remove special characters (€)
#data = pd.read.csv(file_path)
data = data.replace({'€': ' '}, regex = True)

# drop and delete rows with missing data
data = data.dropna()

# save cleaned data to a new file
cleaned_file_path = 'cleandata.csv'
data.to_csv(cleaned_file_path, index = False)

print("I saved the clean file here: ", cleaned_file_path)

# Load the CSV file
file_path = 'cleandata.csv'
data = pd.read_csv(file_path)

# Print the data types of each column
print(data.dtypes)

column_name = data.columns[1]  # Get the second column name
data[column_name] = pd.to_numeric(data[column_name], errors='coerce')

