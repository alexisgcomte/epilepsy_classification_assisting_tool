import streamlit as st
import pandas as pd
import numpy as np
import re
import ast
import glob
from datetime import datetime

# FUNCTION DEFINITIONS

def create_highlighted_markdown_text(report, highlighted_information, neutral_tags_list):
    #try :
    # Initialization and parameters
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
    #for i in range(df_highlighted_batch.shape[0]):
     #   word = df_highlighted_batch['word'].iloc[i]
      #  index = df_highlighted_batch['coordinates'].iloc[i]

     #   decorate_word = html_decorate_text(word, background_color="#FFFF00")
     #   report = report[:index + shift] + decorate_word + report[len(report[:index + shift] + word):]
     #   shift += len(decorate_word) - len(word)
    #n = df_highlighted_batch.shape[0]
    #for i in range(n):
    #    word = df_highlighted_batch['word'].iloc[n-i-1]
    #    index = df_highlighted_batch['coordinates'].iloc[n-i-1]
    #    decorate_word = html_decorate_text(word, background_color="#FFFF00")
    #    report = report[:index] + decorate_word + report[len(report[:index] + word):]

    # changing for regex
    word_list =  df_highlighted_batch['word'].unique()
    word_list.sort()    
    # To prevent double <>
    for word in word_list:
        decorate_word = html_decorate_text(word, background_color="#FFFF00")
        report = re.sub(' '+word+' ', ' '+decorate_word+' ', report) 


    # Keep newline in the markdown report
    report = re.sub("\n", "<br>", report)
    report = bolded_tagged_sentenced(report)
    report = neutral_tags_addition(report, neutral_tags_list)
    return report

def html_decorate_text(text, background_color = "#DDDDDD", font_weight = "500"):
    return '<span style="background-color: '+ background_color +'; font-weight: '+ font_weight +';">'+ text +'</span>'

def bolded_tagged_sentenced(report):
    bolded_report = ''
    for sentence in str(report).split('.'):
        if re.search('<span style=', sentence):
            sentence = str('**') + sentence + str('**.') 
        else:
            sentence = sentence + '.'
        bolded_report += sentence
    return bolded_report

def neutral_tags_addition(report, neutral_tags_list):
    updated_report = report
    for neutral_tags in neutral_tags_list:
        search = neutral_tags
        updated_report = re.sub(search, html_decorate_text(neutral_tags, background_color='#00ecff'), updated_report)
     
        #search = '(\w*)?({})\w*'.format(neutral_tags)
        #updated_report = re.sub(neutral_tags, html_decorate_text(neutral_tags, background_color='#00ecff'), updated_report)

      # with capital letter
        #maj_neutral_tags = str(neutral_tags[:1].upper()+neutral_tags[1:])
        #search = maj_neutral_tags
        #search = '\w*({})\w*'.format(maj_neutral_tags)
        #updated_report = re.sub(search, html_decorate_text(neutral_tags, background_color='#00ecff'), updated_report)
    return updated_report

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

def defaut_value_listing(defaut_values_df):
    # Loading previously input datas
    # Dealing with Seizure_type and Tags colums
    default_list = []
    columns = ['Seizure_type', 'Tags', 'Laterality', 'thesaurus']

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
    # Extract previously input fields
    defaut_values_df = classified_dataset[classified_dataset["Patient_name"] == str(selected_patient)]
    default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes = defaut_value_listing(defaut_values_df)
    return default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes

def update_classified_dataset(selected_patient, classified_dataset, epilepsy_type_input, keywords_input, laterality_input, free_notes_input):
    # Update the classification CSV with input values
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Seizure_type'] = re.sub(r"([\]\'\[])",'',str(epilepsy_type_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Tags'] = re.sub(r"([\]\'\[])",'',str(keywords_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Laterality'] = re.sub(r"([\]\'\[])",'',str(laterality_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'thesaurus'] = re.sub(r"([\]\\[])",'',str(thesaurus_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Free_Notes'] = free_notes_input
    return classified_dataset

def update_last_patient_classified(last_patient_classified_df, selected_patient):
    # Update the number of the last patient classified
    last_patient_classified_df['last_patient_classified'].iloc[0] = sorted_list[sorted_list.index(selected_patient)]
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)

def update_last_patient_classified_next(last_patient_classified_df, selected_patient):
    # Modify last_patient_classied for the next before loading
    if selected_patient == sorted_list[-1]:
        updated_patient = sorted_list[sorted_list.index(selected_patient)]
        st.sidebar.info('Last report completed!')
    else:
        updated_patient = sorted_list[sorted_list.index(selected_patient) + 1]
    last_patient_classified_df['last_patient_classified'].iloc[0] = updated_patient
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)
    return updated_patient

def update_last_patient_classified_previous(last_patient_classified_df, selected_patient):
    # Modify last_patient_classied for the previous before loading
    if selected_patient == sorted_list[0]:
        updated_patient = sorted_list[sorted_list.index(selected_patient)]
        st.sidebar.info('First report :)')
    else:
        updated_patient = sorted_list[sorted_list.index(selected_patient) -1]
    last_patient_classified_df['last_patient_classified'].iloc[0] = updated_patient
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)
    return updated_patient
###
# TO UPDATE
###
def completion_status(thesaurus_input):
    # Return 1 of Epilepsy type is incomplete, else 0
    status = 1
    thesaurus_input = re.sub(r"([\]\'\[])",'',str(thesaurus_input))

    if (len(thesaurus_input) == 0 or str(thesaurus_input) == 'None'):
        status = 0
    return status

# LOADING THE DATAS

@st.cache
def update_save_path():
    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    save_path = ('data/classified_reports/classified_report_database - {}.csv').format(now)
    return save_path

@st.cache
def load_data():
    #data = pd.read_csv('data/structured_reports/Sample_annotated_report_database.csv', encoding="iso-8859-1")
    data = pd.read_csv('data/structured_reports/Annotated_reports_database_tagged_v0.2 tag utf-8.csv', encoding='utf8', sep=";")
    return data

#@st.cache(allow_output_mutation=True)
def load_classified_reports(save_path):
    files = [f for f in glob.glob('data/classified_reports' + "**/*.csv", recursive=True)]
    files.sort()
    last_report_path = files[-1]
    data = pd.read_csv(last_report_path, encoding="iso-8859-1")
    data.to_csv(save_path, index=False)
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

@st.cache
def load_laterality_list():
    data = pd.read_csv('data/parameters/laterality_list.csv', encoding="iso-8859-1")
    laterality_list = data['laterality'].tolist()
    return laterality_list

@st.cache
def load_neutral_tags_list():
    data = pd.read_csv('data/parameters/neutral_tags_list.csv', encoding="iso-8859-1")
    neutral_tags_list = data['neutral_tags'].tolist()
    return neutral_tags_list

@st.cache
def load_thesaurus_list():
    data = pd.read_csv('data/parameters/thesaurus_list.csv', encoding="iso-8859-1")
    thesaurus_list = data['thesaurus'].tolist()
    return thesaurus_list

#@st.cache(allow_output_mutation=True)
def last_patient_classified():
    last_patient_classified_df = pd.read_csv('data/parameters/last_patient_classified.csv', encoding="iso-8859-1")
    last_patient_classified = last_patient_classified_df['last_patient_classified'].iloc[0]
    return last_patient_classified_df, last_patient_classified

# Create a text element and let the reader know the data is loading.
data_load_state = st.sidebar.info('Loading data...')
save_path = update_save_path()
dataset = load_data()
classified_dataset = load_classified_reports(save_path)
tags_list = load_tags_list()
epilepsy_type_list = load_epilepsy_types_list()
laterality_list = load_laterality_list()
neutral_tags_list = load_neutral_tags_list()
thesaurus_list = load_thesaurus_list()

# Notify the reader that the data was successfully loaded.
data_load_state.success("Data Loaded in cache successfully!")

# SIDEBAR WINDOWS

unique_patient_ids = set(dataset["Patient_name"])
sorted_list = sorted(list(unique_patient_ids))

last_patient_classified_df, last_patient_classified = last_patient_classified()
selected_patient = last_patient_classified

# Patient ID navigation

st.sidebar.subheader('Patient ID navigation:')
if st.sidebar.button('Next'):
    selected_patient = update_last_patient_classified_next(last_patient_classified_df, selected_patient)

if st.sidebar.button('Previous'):
    selected_patient = update_last_patient_classified_previous(last_patient_classified_df, selected_patient)

selected_patient = st.sidebar.selectbox('Manual Selection  ', sorted_list, index=sorted_list.index(selected_patient))
single_patient_df = extract_info(selected_patient, dataset)
show_only_epilepsy = st.sidebar.checkbox('Show only epilepsy reports', value=0)
if show_only_epilepsy == 1:
    single_patient_df = single_patient_df[single_patient_df["Nb_Seizures"] > 0]


# Manual classification part

default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes = extract_defaut_values(selected_patient, classified_dataset)

st.sidebar.subheader('Information:')
epilepsy_type_input = st.sidebar.multiselect('Epilepsy type input', epilepsy_type_list, default=default_epilepsy_type)
keywords_input = st.sidebar.multiselect('Keywords input', tags_list, default=default_tags)
laterality_input = st.sidebar.multiselect('Laterality input', laterality_list, default=default_laterality)
free_notes_input = st.sidebar.text_area('Free notes', value=default_free_notes)



st.sidebar.subheader('Classification:')

def index_thesaurus_list(default_thesaurus):
    if default_thesaurus is None:
        return thesaurus_list[0]
    else:
        return re.sub(r"([\]\'\[])",'',str(default_thesaurus))

thesaurus_input = st.sidebar.selectbox('Epilepsy Classification ', thesaurus_list, index=thesaurus_list.index(index_thesaurus_list(default_thesaurus)))

status = completion_status(default_thesaurus)

if st.sidebar.button('Save'):
    classified_dataset = update_classified_dataset(selected_patient, classified_dataset, epilepsy_type_input, keywords_input, laterality_input, free_notes_input)
    classified_dataset.to_csv(save_path, index=False)
    update_last_patient_classified(last_patient_classified_df, selected_patient)
    # Checking if report is now completed
    status = completion_status(thesaurus_input)

    data_save_state = st.sidebar.info('Saving data...')
    data_save_state.success("Classification saved!")

# MAIN WINDOW

st.title('Patient epilepsy classification')
st.subheader('Current patient ID is: {}'.format(selected_patient))

if status == 1:
    st.subheader('Status: {}'.format('Classification completed'))
    st.image('data/icons/correct.jpg', width = 150)
else:
    st.subheader('Status: {}'.format('Classification in progress'))
    st.image('data/icons/incorrect.jpg', width = 150)

# Render report list + meta informations

# Filtering filters with reports


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
    md_report = create_highlighted_markdown_text(row["Patient_report"], row["Highlighted_data"], neutral_tags_list)
    st.markdown(md_report, unsafe_allow_html=True)