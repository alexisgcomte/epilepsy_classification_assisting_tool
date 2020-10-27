import streamlit as st
import pandas as pd
from datetime import datetime
from modules.navigation import SessionState
from modules.decorate.decorate import (
    html_decorate_text,
    tags_underlining,
    bolded_tagged_sentenced,
    html_decorate_tag_list
)
from modules.levenstein_research.levenstein_research  import levenshtein_extraction
from modules.in_out.in_out import load_language
from mutimodule_functions import create_highlighted_markdown_text
import re

state = SessionState.get(key=0)

# FUNCTION DEFINITIONS


def crisis_type_correspondance(target_tags_list, correspondance_dataset):
    crisis_type_list = []

    for target in target_tags_list:
        try:
            crisis_type = correspondance_dataset[correspondance_dataset
            ['symptome-en-simple'] == target]['type_of_crisis'].iloc[0]
            if crisis_type not in crisis_type_list:
                crisis_type_list.append(crisis_type)
        except:
            pass
    crisis_type_list = [crisis_type for crisis_type in crisis_type_list if str(crisis_type) != 'nan']
    return crisis_type_list


def extract_info(selected_patient, dataset):
    single_patient_df = dataset[dataset["Patient_name"] == selected_patient]
    single_patient_df = single_patient_df[["Patient_name",
                                           "Exam_name",
                                           "Nb_Seizures",
                                           "Patient_report",
                                           "Exam_duration",
                                           "Tags",
                                           "Seizure_type",
                                           "Highlighted_data"]]

    single_patient_df = single_patient_df.groupby("Exam_name").agg({"Patient_name": "first",
                                                                    "Nb_Seizures": "sum",
                                                                    "Patient_report" :"first",
                                                                    "Exam_duration":"sum",
                                                                    "Tags" : "first",
                                                                    "Seizure_type" : "first",
                                                                    "Highlighted_data" : "first"})

    single_patient_df = single_patient_df.sort_values(["Nb_Seizures",
                                                       "Exam_name"],
                                                       ascending = (False, True))
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
        element = ' '
    default_list.append(element)

    return [element for element in default_list]


def extract_defaut_values(selected_patient, classified_dataset):
    # Extract previously input fields
    defaut_values_df = classified_dataset[classified_dataset["Patient_name"] == selected_patient]
    default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes = defaut_value_listing(defaut_values_df)
    return default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes

def update_classified_dataset(selected_patient, classified_dataset, epilepsy_type_input, keywords_input, laterality_input, thesaurus_input, free_notes_input):
    # Update the classification CSV with input values
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Seizure_type'] = re.sub(r"([\]\'\[])", '', str(epilepsy_type_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Tags'] = re.sub(r"([\]\'\[])", '', str(keywords_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Laterality'] = re.sub(r"([\]\'\[])", '', str(laterality_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'Free_Notes'] = free_notes_input
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'thesaurus'] = re.sub(r"([\]\\[])", '', str(thesaurus_input))
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'classified'] = 1
    return classified_dataset

def update_last_patient_classified(last_patient_classified_df, selected_patient):
    # Update the number of the last patient classified
    last_patient_classified_df['last_patient_classified'].iloc[0] = sorted_list[sorted_list.index(selected_patient)]
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)

def update_last_patient_classified_next(last_patient_classified_df, selected_patient, sorted_list):
    # Modify last_patient_classied for the next before loading
    if selected_patient == sorted_list[-1]:
        updated_patient = sorted_list[sorted_list.index(selected_patient)]
        st.sidebar.info('Last report completed!')
    else:
        updated_patient = sorted_list[sorted_list.index(selected_patient) + 1]
    last_patient_classified_df['last_patient_classified'].iloc[0] = updated_patient
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)
    return updated_patient

def update_last_patient_classified_previous(last_patient_classified_df, selected_patient, sorted_list):
    # Modify last_patient_classied for the previous before loading
    if selected_patient == sorted_list[0]:
        updated_patient = sorted_list[sorted_list.index(selected_patient)]
        st.sidebar.info('First report :)')
    else:
        updated_patient = sorted_list[sorted_list.index(selected_patient) -1]
    last_patient_classified_df['last_patient_classified'].iloc[0] = updated_patient
    last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)
    return updated_patient

def completion_status(classified_dataset, selected_patient):
    if classified_dataset[classified_dataset['Patient_name'] == selected_patient]['classified'].iloc[0] == 1:
        return 1
    else:
        return 0

# LOADING THE DATAS

@st.cache
def update_save_path():
    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    save_path = ('data/classified_reports/classified_report_database - {}.csv').format(now)
    return save_path

@st.cache
def load_data():
    #data = pd.read_csv('data/structured_reports/Sample_annotated_report_database.csv', encoding='utf-8')
    data = pd.read_csv('data/structured_reports/Annotated_reports_database_tagged_v0.2 + tags utf8.csv', encoding='utf8', sep=";")
    return data

@st.cache
def load_classified_reports_first(save_path):
    data = pd.read_csv('data/classified_reports/classified_report_database.csv', encoding='UTF-8', sep=';')
    data.to_csv(save_path, index=False, encoding='UTF-8', sep=';')

#@st.cache(allow_output_mutation=True)
def load_classified_reports():
    data = pd.read_csv('data/classified_reports/classified_report_database.csv', encoding='UTF-8', sep=';')
    return data

@st.cache
def load_tags_list():
    data = pd.read_csv('data/parameters/tags_list.csv', encoding="utf-8")
    tags_list = data['tags'].tolist()
    return tags_list

@st.cache
def load_epilepsy_types_list():
    data = pd.read_csv('data/parameters/epilepsy_types.csv', encoding="utf-8")
    epilepsy_type_list = data['epilepsy_types'].tolist()
    return epilepsy_type_list

@st.cache
def load_laterality_list():
    data = pd.read_csv('data/parameters/laterality_list.csv', encoding="utf-8")
    laterality_list = data['laterality'].tolist()
    return laterality_list

@st.cache
def load_neutral_tags_list():
    data = pd.read_csv('data/parameters/neutral_tags_list.csv', encoding="utf-8")
    neutral_tags_list = data['neutral_tags'].tolist()
    return neutral_tags_list

@st.cache
def load_thesaurus_list():
    data = pd.read_csv('data/parameters/thesaurus_list.csv', encoding="utf-8")
    thesaurus_list = data['thesaurus'].tolist()
    return thesaurus_list

@st.cache
def simplified_key_words():
    correspondance_dataset = pd.read_csv('data/parameters/simplified_key_words.csv', encoding="utf-8")
    target_tags_list = correspondance_dataset['symptome-en-simple'].tolist()
    return target_tags_list, correspondance_dataset

#@st.cache(allow_output_mutation=True)
def last_patient_classified():
    last_patient_classified_df = pd.read_csv('data/parameters/last_patient_classified.csv', encoding="utf-8")
    last_patient_classified = last_patient_classified_df['last_patient_classified'].iloc[0]
    return last_patient_classified_df, last_patient_classified


def sorted_list_definition(dataset, seizure_only_filter):
    agg_dataset = dataset[['Patient_name','Nb_Seizures']].groupby(by='Patient_name').sum()
    agg_dataset = agg_dataset[agg_dataset['Nb_Seizures'] >= seizure_only_filter]
    sorted_list = sorted(list(set(agg_dataset.index)))
    return sorted_list


# Language implmentation
selectbox_language = st.sidebar.selectbox('', ['EN','FR'])
dict_lang = load_language(selectbox_language.lower())

data_load_state = st.sidebar.info(dict_lang['message']['loading'])
# Create a text element and let the reader know the data is loading.

save_path = update_save_path()
dataset = load_data()
classified_dataset = load_classified_reports_first(save_path)
classified_dataset = load_classified_reports()
tags_list = load_tags_list()
epilepsy_type_list = load_epilepsy_types_list()
laterality_list = load_laterality_list()
neutral_tags_list = load_neutral_tags_list()
thesaurus_list = load_thesaurus_list()


target_tags_list, correspondance_dataset = simplified_key_words()

# Notify the reader that the data was successfully loaded.
data_load_state.success(dict_lang['message']['loaded_successfully'])

# SIDEBAR WINDOWS

# Patient ID navigation
st.sidebar.subheader(dict_lang['sidebar']['legend']['patient_id_nav'])

seizure_only_filter = 1
seizure_only_filter = st.sidebar.checkbox(dict_lang['sidebar']['checkbox']['seizure_patient'], value=0)
show_only_epilepsy = st.sidebar.checkbox(dict_lang['sidebar']['checkbox']['seizure_report'], value=0)
sorted_list = sorted_list_definition(dataset, seizure_only_filter)

last_patient_classified_df, last_patient_classified = last_patient_classified()

# Condition if the last saved patient is in the smaller list
if last_patient_classified in sorted_list:
    selected_patient = last_patient_classified
else:
    for element in sorted_list:
        if element > last_patient_classified:
            selected_patient = element
            break


if st.sidebar.button(dict_lang['sidebar']['button']['next']):
    selected_patient = update_last_patient_classified_next(last_patient_classified_df, selected_patient, sorted_list)
    state.key += 1

if st.sidebar.button(dict_lang['sidebar']['button']['previous']):
    selected_patient = update_last_patient_classified_previous(last_patient_classified_df, selected_patient, sorted_list)
    state.key += 1

selected_patient = st.sidebar.selectbox(dict_lang['sidebar']['selectbox']['manual_selection'], sorted_list, index=sorted_list.index(selected_patient), key=state.key)
last_patient_classified_df['last_patient_classified'].iloc[0] = selected_patient
last_patient_classified_df.to_csv('data/parameters/last_patient_classified.csv', index=False)

single_patient_df = extract_info(selected_patient, dataset)

if show_only_epilepsy == 1:
    single_patient_df = single_patient_df[single_patient_df["Nb_Seizures"] > 0]

# Manual classification part

default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes = extract_defaut_values(selected_patient, classified_dataset)

st.sidebar.subheader(dict_lang['sidebar']['legend']['information'])

epilepsy_type_input = st.sidebar.multiselect(dict_lang['sidebar']['selectbox']['epilepsy_type_input'], epilepsy_type_list, default=default_epilepsy_type, key=state.key)
keywords_input = st.sidebar.multiselect(dict_lang['sidebar']['selectbox']['keyword_input'], tags_list, default=default_tags, key=state.key)
laterality_input = st.sidebar.multiselect(dict_lang['sidebar']['selectbox']['laterality_input'], laterality_list, default=default_laterality, key=state.key)
free_notes_input = st.sidebar.text_area(dict_lang['sidebar']['selectbox']['free_notes'], value=default_free_notes, key=state.key)

st.sidebar.subheader(dict_lang['sidebar']['legend']['classification'])

def index_thesaurus_list(default_thesaurus):
    if default_thesaurus is None:
        return thesaurus_list[0]
    else:
        return re.sub(r"([\]\'\[])",'',str(default_thesaurus))

thesaurus_input = st.sidebar.selectbox(dict_lang['sidebar']['selectbox']['epilepsy_classification'], thesaurus_list, index=thesaurus_list.index(index_thesaurus_list(default_thesaurus)))

status = completion_status(classified_dataset, selected_patient)

if st.sidebar.button(dict_lang['sidebar']['button']['save']):
    classified_dataset = update_classified_dataset(selected_patient, classified_dataset, epilepsy_type_input, keywords_input, laterality_input, thesaurus_input, free_notes_input)
    classified_dataset.to_csv('data/classified_reports/classified_report_database.csv', index=False, encoding='UTF-8', sep=';')
    update_last_patient_classified(last_patient_classified_df, selected_patient)
    # Checking if report is now completed
    status = completion_status(classified_dataset, selected_patient)
    data_save_state = st.sidebar.info('Saving data...')
    data_save_state.success("Classification saved!")
    state.key += 1

if st.sidebar.button(dict_lang['sidebar']['button']['reviewed']):
    classified_dataset.loc[classified_dataset['Patient_name'] == selected_patient, 'classified'] = 1
    classified_dataset.to_csv('data/classified_reports/classified_report_database.csv', index=False, encoding='UTF-8', sep=';')
    update_last_patient_classified(last_patient_classified_df, selected_patient)
    status = completion_status(classified_dataset, selected_patient)
    data_save_state = st.sidebar.info('Saving data...')
    data_save_state.success("Classification reviewed!")
    state.key += 1

# MAIN WINDOW
st.title(dict_lang['main_panel']['title'])
st.subheader(dict_lang['main_panel']['current_patient']+str(selected_patient))

if status == 1:
    st.subheader(dict_lang['main_panel']['status_completed'])
    st.image('static/icons/correct.jpg', width = 150)
else:
    st.subheader(dict_lang['main_panel']['status_progress'])
    st.image('static/icons/incorrect.jpg', width = 150)

# Render report list + meta informations

# Filtering filters with reports

for index, row in single_patient_df.iterrows():

    st.header(dict_lang['main_panel']['seizure_during_exam']+ index)

    # Display of the informative elements
    st.subheader(dict_lang['main_panel']['seizure_during_exam'])
    st.write(html_decorate_text("YES", background_color="#66CD00") if row["Nb_Seizures"] > 0 else html_decorate_text("NO", background_color="#FF7F7F"), unsafe_allow_html=True)

    md_report, keyword_list = create_highlighted_markdown_text(row["Patient_report"], target_tags_list, neutral_tags_list)

    st.subheader(dict_lang['main_panel']['tags'])
    st.write(html_decorate_tag_list(keyword_list), unsafe_allow_html=True)
    
    st.subheader(dict_lang['main_panel']['suggestion'])
    crisis_type_list = crisis_type_correspondance(keyword_list, correspondance_dataset)

    st.write(html_decorate_tag_list(crisis_type_list) , unsafe_allow_html=True)


    #Display highlighted repport

    st.markdown(md_report, unsafe_allow_html=True)
