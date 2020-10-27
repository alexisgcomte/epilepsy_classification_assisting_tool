from ecat.mutimodule_functions import create_highlighted_markdown_text


def test_output__create_highlighted_markdown_text():
    report = 'this is an example of text'
    target_tags_list = 'example'
    neutral_tags_list = 'text'
    report, keyword_list = create_highlighted_markdown_text(
        report,
        target_tags_list,
        neutral_tags_list
    )
    assert type(report) == str
    assert type(keyword_list) == list
