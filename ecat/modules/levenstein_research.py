from fuzzywuzzy import fuzz
import re


def levenshtein_extraction(report: str,
                           tags_targets: list,
                           threshold: int) -> (list, list):
    keyword_list = []
    targets_list = []
    for tag_target in tags_targets:
        for i in report.split('.'):
            if fuzz.partial_ratio(i.lower(), tag_target.lower()) >= threshold:
                for j in re.split(';|,|:| |:|-', i):
                    # CONFIRM PARTIAL RATIO
                    if (fuzz.partial_ratio(j.lower(), tag_target.lower()) >=
                            threshold and len(j) > 4):
                        keyword_list.append(tag_target)
                        targets_list.append(j)
    keyword_list = list(set(keyword_list))
    targets_list = targets_list = list(set(targets_list))

    return keyword_list, targets_list
