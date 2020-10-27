import re
from modules.levenstein_research.levenstein_research import \
    levenshtein_extraction
from modules.decorate.decorate import (
    tags_underlining,
    bolded_tagged_sentenced
)


def create_highlighted_markdown_text(report: str,
                                     target_tags_list: list,
                                     neutral_tags_list: list) -> str:

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

    except Exception:
        return('ERROR WITH KEYWORDS \n \n'+report, 'error')
