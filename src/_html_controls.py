## html_controls.py

## This is a utilty file that contains the definitions of functions designed to account for edge cases when processing the HTML of EyeWiki pages
## All HTML control functions take the entire list of extracted tags as input and output processed text with the relevant HTML tags removed from the list

from bs4 import BeautifulSoup
import logging
import re

def remove_superscript_references(html_input: list):
    """ Removes all superscript references to content within the text """
    for tag in html_input:
        [subtag.decompose() for subtag in tag.find_all("sup")]

    return html_input

def remove_excluded_headers(html_input: list):
    """ Removes content under excluded headers """

    modified_html_input = html_input
    excluded_headers = ["prognosis", "additional resources", "references"]
    for idx, tag in enumerate(html_input):
        if tag.text.lower() in excluded_headers:
            for iidx, next_tag in enumerate(html_input[idx:]):
                if next_tag.name.lower in ["h1", "h2", "h3", "h4"]:
                    del modified_html_input[idx:idx+iidx]
                    break
            
            del modified_html_input[idx:]
            

    return modified_html_input

def convert_differential_to_text(html_input: list, page_name: str):
    """ Converts differential diagnosis into a comma separated list of items when it is usually a bullet list"""
    
    modified_html_input = html_input.copy()
    for idx, tag in enumerate(html_input):
        if tag.get("id") is not None and tag["id"] == "Differential_diagnosis" and html_input[idx+1].name == "ul":
            ul = html_input[idx+1]
            ul_mod = re.sub(r'\n', ', ', ul.text)
            modified = f"A differential diagnosis for {page_name} includes {ul_mod}"
            del modified_html_input[idx:idx+2]
            logging.debug(f"html control: convert_differential_to_text: converted tag {ul} to {modified}")
            return modified, modified_html_input

        elif tag.get("id") is not None and tag["id"] == "Differential_diagnosis":
            logging.debug("html control: convert_differential_to_text: Differential diagnosis header found but no bullet list followed after")

    return "", modified_html_input



    

