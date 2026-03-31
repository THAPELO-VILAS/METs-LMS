
# METs Academy Python (Pandas) Training

import pandas as pd

# Load dataset
df = pd.read_excel('METs_Academy_Sales_Dataset.xlsx')

# Data Cleaning
df = df.drop_duplicates()
df['Sales'] = df['Sales'].fillna(df['Sales'].mean())
df = df[df['Cost'] > 0]

# Transformation
df['Profit'] = df['Sales'] - df['Cost']
df['Month'] = pd.to_datetime(df['Order_Date']).dt.month

# Analysis
print("Total Sales:", df['Sales'].sum())
print("Sales by Region:")
print(df.groupby('Region')['Sales'].sum())

# Top Products
print(df.groupby('Product')['Profit'].sum().sort_values(ascending=False))
