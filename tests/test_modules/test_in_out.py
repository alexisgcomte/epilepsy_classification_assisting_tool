from ecat.modules.in_out import (load_language,
                                 load_parameters,
                                 load_report_and_classification)
import pandas as pd


def test_dic_output___load_language():
    dict_lang = load_language()
    assert type(dict_lang) == dict


def test_output__load_parameters():
    (tags_list,
     epilepsy_type_list,
     laterality_list,
     neutral_tags_list,
     thesaurus_list,
     target_tags_list,
     correspondance_dataset) = load_parameters()

    assert type(tags_list) == list
    assert type(epilepsy_type_list) == list
    assert type(laterality_list) == list
    assert type(neutral_tags_list) == list
    assert type(thesaurus_list) == list
    assert type(target_tags_list) == list
    assert type(correspondance_dataset) == pd.DataFrame


def test_output__load_report_and_classification():
    df_report_database, save_path = load_report_and_classification()
    assert type(save_path) == str
    assert type(df_report_database) == pd.DataFrame
