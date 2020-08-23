import streamlit as st
import pandas as pd
import numpy as np
import re
import ast

st.title('Patient epilepsy classification')

@st.cache
def load_data():
    data = pd.read_csv('data/structured_reports/Sample_annotated_report_database.csv', encoding="iso-8859-1")
    return data

@st.cache
def load_classified_reports():
    data = pd.read_csv('data/classified_reports/classified_report_database.csv', encoding="iso-8859-1")
    return data

@st.cache
def load_tags_list():
    data = pd.read_csv('data/parameters/tags_list.csv', encoding="iso-8859-1")
    tags_list = data['tags'].tolist()
    return tags_list

@st.cache
def load_epilepsy_types_list():
    data = pd.read_csv('data/parameters/epilepsy_types.csv', encoding="iso-8859-1")
    epilepsy_type_list = data['epilepsy_types'].tolist()
    return epilepsy_type_list

# Create a text element and let the reader know the data is loading.
data_load_state = st.info('Loading data...')
dataset = load_data()
classified_dataset = load_classified_reports()
tags_list = load_tags_list()
epilepsy_type_list = load_epilepsy_types_list()

# Notify the reader that the data was successfully loaded.
data_load_state.success("Data Loaded in cache successfully!")

def create_highlighted_markdown_text(report, highlighted_information):
    #try :
    # Initialization and parameters
    shift = 0
    if pd.isnull(highlighted_information):
        report = re.sub("\n", "<br>", report)
        return report

    # Creating a dataset of the elements to highlight
    df_highlighted_batch = pd.DataFrame(columns=['word','coordinates'])

    for highlighted_info in ast.literal_eval(highlighted_information):
        words = highlighted_info[0]
        index = highlighted_info[1]
        for i in range(len(words)):
            df_highlighted_batch = df_highlighted_batch.append({'word':words[i], 'coordinates':index[i]}, ignore_index=True)
    df_highlighted_batch.sort_values(by="coordinates", inplace=True) # for highlighting in order of position

    # Updating the report
    for i in range(df_highlighted_batch.shape[0]):
        word = df_highlighted_batch['word'].iloc[i]
        index = df_highlighted_batch['coordinates'].iloc[i]

        decorate_word = html_decorate_text(word, background_color="#FFFF00")
        report = report[:index + shift] + decorate_word + report[len(report[:index + shift] + word):]

        shift += len(decorate_word) - len(word)

    # Keep newline in the markdown report
    report = re.sub("\n", "<br>", report)
    return report

    #except:

    #    return report

def html_decorate_text(text, background_color = "#DDDDDD", font_weight = "500"):
    return '<span style="background-color: '+ background_color +'; font-weight: '+ font_weight +';">'+ text +'</span>'

def html_decorate_tag_list(tag_list):
    if pd.isnull(tag_list):
        return tag_list
    else:
        tag_list_content = str(tag_list).split(",")
        tag_list_content = [html_decorate_text(content) for content in tag_list_content]
        tag_list_content = ", ".join(tag_list_content)
        return tag_list_content

def extract_info(selected_patient, dataset):
    single_patient_df = dataset[dataset["Patient_name"] == selected_patient]
    single_patient_df = single_patient_df[["Patient_name", "Exam_name", "Nb_Seizures", "Patient_report", "Exam_duration", "Tags", "Seizure_type", "Highlighted_data"]]
    single_patient_df = single_patient_df.groupby("Exam_name").agg({"Patient_name": "first",
                                                                    "Nb_Seizures": "sum",
                                                                    "Patient_report" :"first",
                                                                    "Exam_duration":"sum",
                                                                    "Tags" : "first",
                                                                    "Seizure_type" : "first",
                                                                    "Highlighted_data" : "first"})

    single_patient_df = single_patient_df.sort_values(["Nb_Seizures", "Exam_name"], ascending = (False, True))
    return single_patient_df

def default_value_listing(defaut_values_df):
    
    # Dealing with Seizure_type and Tags colums
    default_list = []
    columns = ['Seizure_type', 'Tags']

    for col in columns:
        element = defaut_values_df[col].iloc[0]
        if pd.isnull(element):
            element = None
        else:
            try:
                element = element.split(', ')
            except:
                element = list(element)    
        default_list.append(element)

    # Adding free notes
    element = defaut_values_df['Free_Notes'].iloc[0]
    if pd.isnull(element):
        element = ''
    default_list.append(element)

    return [element for element in default_list]      

def extract_defaut_values(selected_patient, classified_dataset):
    defaut_values_df = classified_dataset[classified_dataset["Patient_name"] == selected_patient]
    default_epilepsy_type, default_tags, default_free_notes = default_value_listing(defaut_values_df)
    return default_epilepsy_type, default_tags, default_free_notes

# Creating the patient index selector in side menu
st.sidebar.subheader('Select Patient ID')
unique_patient_ids = set(dataset["Patient_name"])
selected_patient = st.sidebar.selectbox('Patient ID', sorted(list(unique_patient_ids)))
single_patient_df = extract_info(selected_patient, dataset)

# Type of epilepsy
st.sidebar.subheader('Classification: ')
default_epilepsy_type, default_tags, default_free_notes = extract_defaut_values(selected_patient, classified_dataset)
epilepsy_type_input = st.sidebar.multiselect('Epilepsy type input', epilepsy_type_list, default=default_epilepsy_type)
keywords_input = st.sidebar.multiselect('Keywords input', tags_list, default=default_tags)
free_notes = st.sidebar.text_area('Free notes', value=default_free_notes)


# Render report list + meta informations
for index, row in single_patient_df.iterrows():
    st.header('Report #' + index)

    # Display of the informative elements
    st.subheader("Seizure during the exam:")
    st.write(html_decorate_text("YES", background_color="#66CD00") if row["Nb_Seizures"] > 0 else html_decorate_text("NO", background_color="#FF7F7F"), unsafe_allow_html=True)

    st.subheader('Tags')
    st.write(html_decorate_tag_list(row["Tags"]), unsafe_allow_html=True)
    
    st.subheader('Suggestion of seizure type')
    st.write(html_decorate_tag_list(row["Seizure_type"]), unsafe_allow_html=True)

    #Display highlighted repport
    md_report = create_highlighted_markdown_text(row["Patient_report"], row["Highlighted_data"])
    st.markdown(md_report, unsafe_allow_html=True)