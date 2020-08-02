import streamlit as st
import pandas as pd
import numpy as np
import ast

st.title('Report classification helper')

@st.cache
def load_data():
    data = pd.read_csv('0. Data/classification_dataset_hashtag_sample.csv', sep=";")
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
dataset = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Data Loaded in cache successfully!")

def create_markdown_text(report, surline_information):

    try : 
        # Initialization and parameters
        shift = 0
        start_tag = '<span style="background-color: #FFFF00">'
        end_tag = '</span>'

        # Creating a dataset of the elements to surline
        df_surline_batch = pd.DataFrame(columns=['word','coordinates'])

        for surline_info in ast.literal_eval(surline_information):
            words = surline_info[0]
            index = surline_info[1]
            for i in range(len(words)):
                df_surline_batch = df_surline_batch.append({'word':words[i], 'coordinates':index[i]}, ignore_index=True)
        df_surline_batch.sort_values(by="coordinates", inplace=True) # for surlining in order of position

        # Updating the report

        for i in range(df_surline_batch.shape[0]):
            word = df_surline_batch['word'].iloc[i]
            index = df_surline_batch['coordinates'].iloc[i]

            report = report[:index + shift] + start_tag + word + end_tag + report[len(report[:index + shift] + word):]
            
            shift += len(start_tag) + len(end_tag)
        return report

    except:
        return report

def extract_info(filepath_filter, dataset):
    filtered_dataset = dataset[dataset.index == filepath_filter]

    report = filtered_dataset['report'].iloc[0]
    hashtags = filtered_dataset['hashtag'].iloc[0]
    crisis_type = filtered_dataset['crisis_type'].iloc[0]
    surline_data = filtered_dataset['surline_data'].iloc[0]

    return report, hashtags, crisis_type, surline_data


# Listing all the index names
filepaths = dataset.index

# Creating the index selector
st.subheader('Select index')
filepath_filter = st.selectbox('filepath',filepaths)

report, hashtags, crisis_type, surline_data = extract_info(filepath_filter, dataset)

md_text = create_markdown_text(report, surline_data)

# Display of the elements

st.subheader('crisis type')
st.write(crisis_type)

st.subheader('hashtags')
st.write(hashtags)

st.subheader('Report')
st.markdown(md_text, unsafe_allow_html=True)