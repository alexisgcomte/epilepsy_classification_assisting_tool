from ecat.modules.decorate import (
    html_decorate_text,
    tags_underlining,
    bolded_tagged_sentenced,
    html_decorate_tag_list
)


def test_str_output___html_decorate_text():
    text = 'text'
    html_decorate_text_output = html_decorate_text(text)
    assert type(html_decorate_text_output) == str


def test_str_output__tags_underlining():
    report = 'This is an example.'
    neutral_tags_list = ['an']
    html_decorate_text_output = tags_underlining(report, neutral_tags_list)
    assert type(html_decorate_text_output) == str


def test_str_output__bolded_tagged_sentenced():
    report = 'This is an example.'
    bolded_report = bolded_tagged_sentenced(report)
    assert type(bolded_report) == str


def test_regex_on_span_working__bolded_tagged_sentenced():
    report = 'This is an' + html_decorate_text('example')
    expected_report = str('**') + report + str('**.')
    assert bolded_tagged_sentenced(report) == expected_report


def test_empty_tag_list_output_tag_list__html_decorate_tag_list():
    tag_list = []
    assert html_decorate_tag_list(tag_list) == tag_list


def test_str_output_if_len_positive__html_decorate_tag_list():
    tag_list = ['tag1', 'tag2', 'tag3']
    assert type(html_decorate_tag_list(tag_list)) == str
