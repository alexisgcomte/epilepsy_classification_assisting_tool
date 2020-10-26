import pandas as pd

def simplified_key_words()->(list, pd.DataFrame):
    correspondance_dataset = pd.read_csv('data/parameters/simplified_key_words.csv', encoding="utf-8")
    target_tags_list = correspondance_dataset['symptome-en-simple'].tolist()
    return target_tags_list, correspondance_dataset