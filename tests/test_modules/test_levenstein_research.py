from ecat.modules.levenstein_research import levenshtein_extraction


def test_two_lists_output__levenshtein_extraction():
    report = 'This is an example'
    tags_targets = ['example']
    threshold = 90
    keyword_list, targets_list = levenshtein_extraction(report,
                                                        tags_targets,
                                                        threshold)
    assert type(keyword_list) == list
    assert type(targets_list) == list


def test_function_extracts_keyword_properly__levenshtein_extraction():
    report = 'This is an exemple'
    tags_targets = ['example']
    threshold = 80
    keyword_list, targets_list = levenshtein_extraction(report,
                                                        tags_targets,
                                                        threshold)
    assert keyword_list == ['example']
    assert targets_list == ['exemple']
