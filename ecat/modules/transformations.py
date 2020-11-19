import re
import pandas as pd


def update_classified_dataset(selected_patient: str,
                              classified_dataset: pd.DataFrame,
                              epilepsy_type_input: list,
                              keywords_input: list,
                              laterality_input: list,
                              thesaurus_input: list,
                              # change name of thesaurus input
                              free_notes_input: str) -> pd.DataFrame:

    # Update the classification CSV with input values
    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'Seizure_type'] = (
                           re.sub(r"([\]\'\[])", '', str(epilepsy_type_input)))

    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'Tags'] = (
                           re.sub(r"([\]\'\[])", '', str(keywords_input)))

    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'Laterality'] = (
                           re.sub(r"([\]\'\[])", '', str(laterality_input)))

    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'Free_Notes'] = (
                           free_notes_input)

    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'thesaurus'] = (
                           re.sub(r"([\]\\[])", '', str(thesaurus_input)))

    classified_dataset.loc[classified_dataset['Patient_name']
                           == selected_patient, 'classified'] = 1

    return classified_dataset


def extract_info(selected_patient, df_report_database):
    single_patient_df = df_report_database[df_report_database
                                           ["Patient_name"]
                                           == selected_patient]

    single_patient_df = single_patient_df[["Patient_name",
                                           "Exam_name",
                                           "Nb_Seizures",
                                           "Patient_report",
                                           "Exam_duration",
                                           "Tags",
                                           "Seizure_type",
                                           "Highlighted_data"]]

    single_patient_df = single_patient_df.groupby("Exam_name").agg(
        {"Patient_name": "first",
         "Nb_Seizures": "sum",
         "Patient_report": "first",
         "Exam_duration": "sum",
         "Tags": "first",
         "Seizure_type": "first",
         "Highlighted_data": "first"})

    single_patient_df = single_patient_df.sort_values(["Nb_Seizures",
                                                       "Exam_name"],
                                                      ascending=(False, True))
    return single_patient_df

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
    crisis_type_list = [crisis_type for crisis_type in crisis_type_list if
                        str(crisis_type) != 'nan']
    return crisis_type_list

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
