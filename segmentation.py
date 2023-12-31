# -*- coding: utf-8 -*-
"""Segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ae7Zat7YScvswk3e_Hx-GLiXw7700doI
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from keras.models import Model
from keras.layers import Dense, Input
from keras.optimizers import Adam
from keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import plotly.express as px
from keras.layers import Dense, Input

# Load the data
data = pd.read_csv('data.csv', encoding='ISO-8859-1')

data.head()

data.shape

data.isna().sum()

# Group data by StockCode and sum the Quantity for each
grouped_data = data.groupby('StockCode')['Quantity'].sum().reset_index()

# Plot the data
fig = px.bar(grouped_data, x='StockCode', y='Quantity', title='Quantity per StockCode')
fig.show()

# Count the number of invoices per country
country_counts = data['Country'].value_counts().reset_index()

# Rename the columns to something more descriptive
country_counts.columns = ['Country', 'Number of Invoices']

# Plot the data
fig = px.bar(country_counts, x='Country', y='Number of Invoices',
             title='Number of Invoices per Country',
             labels={'Country':'Country', 'Number of Invoices':'Number of Invoices'},
             color='Number of Invoices')
fig.show()

# Plot the data
fig = px.histogram(data, x="UnitPrice", nbins=50, title='Distribution of Unit Price')
fig.show()

# Define price categories
bins = [0, 10, 50, 100, np.inf]
names = ['<10', '10-50', '50-100', '100+']

data['PriceRange'] = pd.cut(data['UnitPrice'], bins, labels=names)

# Plot the data
fig = px.pie(data, names='PriceRange', title='Distribution of Price Ranges')
fig.show()

# Plot the data
fig = px.histogram(data, x="Quantity", nbins=50, title='Distribution of Quantity')
fig.show()

# Plot the data
fig = px.histogram(data, x="Quantity", nbins=50, title='Distribution of Quantity')
fig.show()

data.columns
data.head()
df_product_quan=data.groupby("StockCode").agg({"Quantity":"sum"}).sort_values(by="Quantity",ascending=False).reset_index().head(15)
df_product_quan

fig=px.histogram(data_frame=df_product_quan,x="StockCode",y="Quantity",
                 template="plotly_white",color_discrete_sequence=px.colors.sequential.Aggrnyl,
                 title="Distribution of Product StockCode")
fig.update_xaxes(tickangle = 45)
fig.update_layout(yaxis_title="Quantity",
                  xaxis_title="StockCode")

# Ensure InvoiceDate is in the correct datetime format
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# Group data by date and count the number of invoices per date
grouped_data = data.groupby(data['InvoiceDate'].dt.date)['InvoiceNo'].nunique().reset_index()

# Plot the data
fig = px.line(grouped_data, x='InvoiceDate', y='InvoiceNo', title='Number of Invoices over Time')
fig.show()

# Plot the data
fig = px.scatter(data, x="Quantity", y="UnitPrice", title='Scatter plot: Quantity vs. Unit Price')

# Show the plot
fig.show()

# Count the number of invoices per country
country_counts = data['Country'].value_counts().reset_index()

# Rename the columns to something more descriptive
country_counts.columns = ['Country', 'Number of Invoices']

# Plot the data
fig = px.choropleth(country_counts, locations='Country', color='Number of Invoices',
                    locationmode='country names', # Depends on the country format in your data
                    title='Number of Invoices per Country',
                    color_continuous_scale=px.colors.sequential.Plasma)
fig.show()

# Create a bar plot
fig = px.bar(data, x='Country', y='UnitPrice',
             title='Distribution of UnitPrice for each Country')
fig.show()

# Create a box plot
fig = px.box(data, x='Country', y='UnitPrice',
             title='Distribution of UnitPrice for each Country')
fig.show()

# Drop 'Description' column
data = data.drop('Description', axis=1)

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from keras.models import Model
from keras.layers import Dense, Input
from keras.optimizers import Adam
from keras.models import load_model

# Handle missing values
data = data.dropna()

# Perform label encoding for categorical columns
le = LabelEncoder()
categorical_columns = ['InvoiceNo', 'StockCode', 'InvoiceDate', 'CustomerID', 'Country']
for column in categorical_columns:
    data[column] = le.fit_transform(data[column])

# Normalize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Define the autoencoder
input_layer = Input(shape=(data.shape[1],))
encoded = Dense(50, activation='relu')(input_layer)
encoded = Dense(20, activation='relu')(encoded)
decoded = Dense(50, activation='relu')(encoded)
output_layer = Dense(data.shape[1], activation='linear')(decoded)

autoencoder = Model(input_layer, output_layer)
autoencoder.compile(optimizer=Adam(0.0001), loss='mean_squared_error')

# Define model path
model_path = 'autoencoder_model.h5'

# Check if the model already exists
if os.path.exists(model_path):
    # Load the model from the file
    autoencoder = load_model(model_path)
    print("Model loaded successfully.")
else:
    # Train the autoencoder
    autoencoder.fit(data_scaled, data_scaled, epochs=100, batch_size=32, shuffle=True, validation_split=0.2)
    # Save model for future use
    autoencoder.save(model_path)
    print("Model trained and saved successfully.")

# Use the encoder part to transform the data to lower dimensional space
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.layers[1].output)
data_compressed = encoder.predict(data_scaled)

# Perform clustering
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(data_compressed)

# Output the cluster assignments
print(clusters)

cluster_counts = np.bincount(clusters)
print(f"Cluster frequencies: {cluster_counts}")

encoder.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

encoder.save('encoder_model.h5')

# evaluate the autoencoder
train_mse = autoencoder.evaluate(data_scaled, data_scaled, verbose=0)
print(f'Train MSE: {train_mse}')