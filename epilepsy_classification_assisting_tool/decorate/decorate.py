import re
from epilepsy_classification_assisting_tool.levenstein_research.\
    levenstein_research \
    import levenshtein_extraction


def html_decorate_text(text: str,
                       background_color: str = "#DDDDDD", 
                       font_weight: str = "500") -> str:

    html_decorate_text = ''.join([
        '<span style="background-color: ',
        background_color,
        '; font-weight: ',
        font_weight,
        ';">',
        text,
        '</span>'])

    return html_decorate_text


def tags_underlining(report: str,
                     neutral_tags_list: list,
                     background_color: str = "#DDDDDD") -> str:

    updated_report = report

    for neutral_tags in neutral_tags_list:
        search = neutral_tags
        updated_report = re.sub(search, html_decorate_text(neutral_tags,
                                background_color=background_color),
                                updated_report)

    return updated_report


def bolded_tagged_sentenced(report: str) -> str:
    bolded_report = ''
    for sentence in str(report).split('.'):
        if re.search('<span style=', sentence):
            sentence = str('**') + sentence + str('**.')
        else:
            sentence = sentence + '.'
        bolded_report += sentence
    return bolded_report


def html_decorate_tag_list(tag_list: list) -> str:
    if len(tag_list) == 0:
        return tag_list
    else:
        tag_list_content = [html_decorate_text(content) for content in
                            tag_list]
        tag_list_content = ", ".join(tag_list_content)
        return tag_list_content


def create_highlighted_markdown_text(report: str,
                                     target_tags_list: list,
                                     neutral_tags_list: list) -> [str, list]:

    try:

        # Keep newline in the markdown report

        keyword_list, targets_list = levenshtein_extraction(report,
                                                            target_tags_list,
                                                            90)
        targets_list.sort(key=len)
        report = tags_underlining(report, targets_list,
                                  background_color="#FFFF00")
        report = tags_underlining(report, neutral_tags_list,
                                  background_color="#00ecff")
        report = bolded_tagged_sentenced(report)
        report = re.sub("\n", "<br>", report)
        return report, keyword_list

    except:
        return('ERROR WITH KEYWORDS \n \n'+report, 'error')