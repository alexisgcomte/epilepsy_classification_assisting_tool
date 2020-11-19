import streamlit as st
import pandas as pd
import re
from datetime import datetime
from modules import SessionState
from modules.decorate import (
    html_decorate_text,
    tags_underlining,
    bolded_tagged_sentenced,
    html_decorate_tag_list)
from modules.levenstein_search  import levenshtein_extraction
from modules.mutimodule_functions import create_highlighted_markdown_text
from modules.in_out import (
    load_language,
    load_parameters,
    load_report_and_classification)
from modules.transformations import (
    update_classified_dataset,
    extract_info,
    crisis_type_correspondance,
    defaut_value_listing
    )


state = SessionState.get(key=0)

# FUNCTION DEFINITIONS


def extract_defaut_values(selected_patient, classified_dataset):
    # Extract previously input fields
    defaut_values_df = classified_dataset[classified_dataset["Patient_name"] == selected_patient]
    default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes = defaut_value_listing(defaut_values_df)
    return default_epilepsy_type, default_tags, default_laterality, default_thesaurus, default_free_notes


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
    if classified_dataset[classified_dataset['Patient_name']
                          == selected_patient]['classified'].iloc[0] == 1:
        return 1
    else:
        return 0

@st.cache
def load_cached_data():
    (tags_list,
     epilepsy_type_list,
     laterality_list,
     neutral_tags_list,
     thesaurus_list,
     target_tags_list,
     correspondance_dataset) = load_parameters()

    df_report_database, save_path = load_report_and_classification()

    return (tags_list,
            epilepsy_type_list,
            laterality_list,
            neutral_tags_list,
            thesaurus_list,
            target_tags_list,
            correspondance_dataset,
            df_report_database,
            save_path)

def last_patient_classified():
    last_patient_classified_df = pd.read_csv('data/parameters/last_patient_classified.csv', encoding="utf-8")
    last_patient_classified = last_patient_classified_df['last_patient_classified'].iloc[0]
    return last_patient_classified_df, last_patient_classified

def load_classified_reports():
    data = pd.read_csv('data/classified_reports/classified_report_database.csv', encoding='UTF-8', sep=';')
    return data
# test nombre de colonnes

def sorted_list_definition(df_report_database, seizure_only_filter):
    agg_dataset = df_report_database[['Patient_name','Nb_Seizures']].groupby(by='Patient_name').sum()
    agg_dataset = agg_dataset[agg_dataset['Nb_Seizures'] >= seizure_only_filter]
    sorted_list = sorted(list(set(agg_dataset.index)))
    return sorted_list

# SIDEBAR

# Language Selection


selectbox_language = st.sidebar.selectbox('', ['EN', 'FR'])

dict_lang = load_language(selectbox_language.lower())

data_load_state = st.sidebar.info(dict_lang['message']['loading'])

(tags_list,
 epilepsy_type_list,
 laterality_list,
 neutral_tags_list,
 thesaurus_list,
 target_tags_list,
 correspondance_dataset,
 df_report_database,
 save_path) = load_cached_data()


classified_dataset = load_classified_reports()


# Notify the reader that the data was successfully loaded.
data_load_state.success(dict_lang['message']['loaded_successfully'])

# Patient ID navigation
st.sidebar.subheader(dict_lang['sidebar']['legend']['patient_id_nav'])

seizure_only_filter = 1
seizure_only_filter = st.sidebar.checkbox(dict_lang['sidebar']['checkbox']
                                            ['seizure_patient'], value=0)
show_only_epilepsy = st.sidebar.checkbox(dict_lang['sidebar']['checkbox']
                                            ['seizure_report'], value=0)
sorted_list = sorted_list_definition(df_report_database, seizure_only_filter)

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

single_patient_df = extract_info(selected_patient, df_report_database)

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

    st.header(dict_lang['main_panel']['seizure_during_exam'] + index)

    # Display of the informative elements
    st.subheader(dict_lang['main_panel']['seizure_during_exam'])
    st.write(html_decorate_text("YES", background_color="#66CD00")
             if row["Nb_Seizures"] > 0
             else html_decorate_text("NO", background_color="#FF7F7F"),
             unsafe_allow_html=True)

    md_report, keyword_list = create_highlighted_markdown_text(row["Patient_report"], target_tags_list, neutral_tags_list)

    st.subheader(dict_lang['main_panel']['tags'])
    st.write(html_decorate_tag_list(keyword_list), unsafe_allow_html=True)

    st.subheader(dict_lang['main_panel']['suggestion'])
    crisis_type_list = crisis_type_correspondance(keyword_list, correspondance_dataset)

    st.write(html_decorate_tag_list(crisis_type_list) , unsafe_allow_html=True)

    #Display highlighted repport

    st.markdown(md_report, unsafe_allow_html=True)
