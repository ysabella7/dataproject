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

# Print to check conversion
print(data.dtypes)  # Verify data types
print(data.head())   # Check the first few rows

# Save back to CSV
data.to_csv('cleandata_fixed.csv', index=False)

'''
# load the CSV file
df = pd.read_csv("cleandata.csv")

# select only the last three columns (ignore the first numeric column)
data = df.iloc[:, 1:]  # This selects all rows but only columns 2, 3, and 4

# calculate mean, median, mode, and range
mean_values = data.mean()
median_values = data.median()
mode_values = data.mode().iloc[0]  # mode() can return multiple values, take the first
range_values = data.max() - data.min()

# print the results
print("Mean:\n", mean_values)
print("\nMedian:\n", median_values)
print("\nMode:\n", mode_values)
print("\nRange:\n", range_values)
'''
