import json
import pandas as pd
from datetime import datetime


def load_language(lang: str = 'en') -> dict:
    with open('data/language/{}.json'.format(lang), "r") as read_file:
        dict_lang = json.load(read_file)
    return dict_lang


def load_parameters() -> [list, pd.DataFrame]:
    df_tags_list = pd.read_csv('data/parameters/tags_list.csv',
                               encoding="utf-8")
    tags_list = df_tags_list['tags'].tolist()

    df_epilepsy_types = pd.read_csv('data/parameters/epilepsy_types.csv',
                                    encoding="utf-8")
    epilepsy_type_list = df_epilepsy_types['epilepsy_types'].tolist()

    df_laterality_list = pd.read_csv('data/parameters/laterality_list.csv',
                                     encoding="utf-8")
    laterality_list = df_laterality_list['laterality'].tolist()

    df_neutral_tags_list = pd.read_csv('data/parameters/neutral_tags_list.csv',
                                       encoding="utf-8")
    neutral_tags_list = df_neutral_tags_list['neutral_tags'].tolist()

    df_thesaurus_list = pd.read_csv('data/parameters/thesaurus_list.csv',
                                    encoding="utf-8")
    thesaurus_list = df_thesaurus_list['thesaurus'].tolist()

    correspondance_dataset = pd.read_csv('data/parameters/' +
                                         'simplified_key_words.csv',
                                         encoding="utf-8")
    target_tags_list = correspondance_dataset['symptome-en-simple'].tolist()

    return (tags_list,
            epilepsy_type_list,
            laterality_list,
            neutral_tags_list,
            thesaurus_list,
            target_tags_list,
            correspondance_dataset)


def load_report_and_classification():

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    save_path = ('data/classified_reports/classified_report_database - {}.csv'
        ).format(now)

    df_classified_db = pd.read_csv('data/classified_reports/' +
                                   'classified_report_database.csv',
                                   encoding='UTF-8', sep=';')
    df_classified_db.to_csv(save_path, index=False, encoding='UTF-8', sep=';')

    target_database = 'data/structured_reports/Annotated_reports_database.csv'
#   target_database = 'data/structured_reports/Sample_annotated_report_\
#                    database.csv'

    df_report_database = pd.read_csv(target_database,
                                     encoding='utf8', sep=";")

    return df_report_database, save_path
