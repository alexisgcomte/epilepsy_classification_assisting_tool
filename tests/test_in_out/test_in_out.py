from epilepsy_classification_assisting_tool.in_out.in_out import load_language


def test_dic_output___load_language():
    dict_lang = load_language()
    assert type(dict_lang) == dict
