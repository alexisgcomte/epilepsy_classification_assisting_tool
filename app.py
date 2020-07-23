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
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Data Loaded in cache successfully!")

def create_markdown(index, data):
    list_of_colors = []
    report = data['report'].iloc[index]
    surline_data = data['surline_data'].iloc[index]
    surline_data_list = ast.literal_eval(surline_data)
    start_tag = '<span style="background-color: #FFFF00">'
    end_tag = '</span>'
    shift = 0



filepaths = data.index

st.subheader('Select index')
filepath_filter = st.selectbox('filepath',filepaths)

# Filters
filtered_data = data[data.index == filepath_filter]
filtererd_report = filtered_data['report'].iloc[0]
filtererd_hashtags = filtered_data['hashtag'].iloc[0]
filtererd_crisis_type = filtered_data['crisis_type'].iloc[0]
rich_text = '<span style="background-color: #ff5733">LENGTH OF THE RECORDING</span>: 22  ***minutes*** and 53 <em>seconds</em> CLINICAL HISTORY: The patient is a 27-year-old man with past medical history of cognitive delay, mitochondrial disorder, seizure disorder. The patient was brought to the emergency room with multiple witnessed seizures. MEDICATIONS: Ativan, Dilantin, clonazepam, chlorpromazine, amlodipine. INTRODUCTION: Digital video EEG is performed in the lab/bedside using standard 10-20 system of electrode placement with one channel of EKG. Hyperventilation and photic stimulation are performed. DESCRIPTION OF THE RECORD: During maximal wakefulness there are periods of fragmented moderate amplitude 9 Hz alpha activity with preserved anterior-to-posterior frequency amplitude gradient. The majority of the background, however, consists of low amplitude fast activity admixed with polymorphic frequently sharply contoured central theta and delta activity. Additionally, up to 20 second runs of sharply contoured frontocentral theta activity without spatial or temporal evolution are captured. These runs are not ictal in etiology. Occasional moderate amplitude isolated diffuse frontally predominant sharply contoured slow waves without clear spike waves or sharp waves are captured. A good example of such waveform occurs at 09:59:50 a.m. On a single occasion at 10:01:20 a.m., such discharge is correlated with a brief generalized body jerk. There is a continuous diffuse EKG artifact. No hyperventilation or photic stimulation are captured. There is no normal sleep architecture captured. FINDINGS: 1. Mild diffuse slowing. 2. Runs of non-evolving frontocentral theta activity. 3. Isolated diffuse frontally predominant slow waves that on a single occasion correlates with the generalized body jerks. IMPRESSION: This is a very abnormal EEG due to mild diffuse slowing, runs of sharply contoured bifrontocentral activity and occasional diffuse waveforms without clearly formed sharp waveforms that on a single occasion are associated with brief generalized body jerks. This EEG supports a bihemispheric diffuse disturbance of cerebral dysfunction. No clear electrographic seizures are captured.'
#rich_text = '<span style="background-color: #FFFF00">This text is highlighted in yellow.</span>'
st.subheader('crisis type')
st.write(filtererd_crisis_type)

st.subheader('hashtags')
st.write(filtererd_hashtags)

st.subheader('Report')
st.write(filtererd_report)

st.subheader('test rich text')
st.markdown(rich_text, unsafe_allow_html=True)