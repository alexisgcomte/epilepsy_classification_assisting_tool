from ecat.modules.loading import (
    simplified_key_words)
import pandas as pd


def test_loading_simplified_key_words_output():
    target_tags_list, correspondance_dataset = simplified_key_words()
    assert type(target_tags_list) == list
    assert type(correspondance_dataset) == pd.DataFrame
