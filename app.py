import streamlit as st
import pandas as pd
import numpy as np

st.title('Report classification helper')

@st.cache
def load_data():
    data = pd.read_csv('0. Data/classification_dataset_hashtag_sample.csv', sep=';')
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Data Loaded in cache successfully!")

filepaths = data.index

st.subheader('Select index')
filepath_filter = st.selectbox('filepath',filepaths)

# Filters
filtered_data = data[data.index == filepath_filter]
filtererd_report = filtered_data['report'].iloc[0]
filtererd_hashtags = filtered_data['hashtag'].iloc[0]
filtererd_crisis_type = filtered_data['crisis_type'].iloc[0]

st.subheader('crisis type')
st.write(filtererd_crisis_type)

st.subheader('hashtags')
st.write(filtererd_hashtags)

st.subheader('Report')
st.write(filtererd_report)