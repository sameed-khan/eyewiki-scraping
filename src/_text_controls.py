## _text_controls.py
## Header file containing function definitions to preprocess EyeWiki text and remove elements SPECIFIC to EyeWiki
## NOTE: This is not a substitute for text preprocessing, which will still need to be done

from bs4 import BeautifulSoup
import logging
import re

def remove_figure_or_table_reference(input: str) -> str:
    """ Removes element such as (Figure X) or (Table X) from the string """
    ret = re.sub(r"\(Figure .*\)", "", input)
    ret = re.sub(r"\(Table .*\)", "", ret)

    if input != ret:
        logging.debug(f"text control: remove_figure_or_table_reference: converted {input} to {ret}")

    return ret

def remove_etal(input: str) -> str:
    """ Removes et al. with period from items since period is used as a delimiter """
    ret = re.sub(r"et al.", "", input)

    if input != ret:
        logging.debug(f"text control: remove_etal: converted {input} to {ret}")

    return ret

def replace_newline_period_delimiter(input: str) -> str:
    """ For text that has newlines in the middle, replace this with a period. If the newline has a period before it, do not add a period, remove the newline only """
    ret = re.sub(r"\.\n", " ", input, re.M)
    ret = re.sub(r"\n([a-zA-Z0-9]?)", r". \1", ret, re.M)
    ret = re.sub(r":\n", ": ", ret, re.M)
    ret = re.sub(r"\n", ". ", ret, re.M)

    if ret != input:
        logging.debug(f"text control: replace_newline_period_delimiter: converted {input} to {ret}")
    return ret

def remove_icd9(input: str) -> str:
    """ Remove any mention of ICD-9 codes from the text """
    ret = re.sub(r"ICD9 [\.\d]*", "", input)
    ret = re.sub(r"ICD-9 [\.\d]*", "", ret)
    
    if input != ret:
        logging.debug(f"text control: remove_icd9: converted {input} to {ret}")

    return ret