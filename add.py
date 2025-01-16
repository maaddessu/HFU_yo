import streamlit as st
import pandas as pd
import numpy as np

# Title
st.title("My Dashboard")

# Slider for selecting the number of data points
num_points = st.slider("Select number of data points", min_value=10, max_value=100, value=50)

# Create a DataFrame with random data
data = pd.DataFrame({
    'x': np.arange(num_points),
    'y': np.random.rand(num_points)  # Use np.random.rand() for random numbers
})

# Line chart
st.line_chart(data.set_index('x'))

# Checkbox to show raw data
if st.checkbox("Show raw data"):
    st.write(data)
