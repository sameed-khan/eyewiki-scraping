## page_scrape.py
## Sameed Khan, 01/16/2023
## Entry point script to scrape EyeWiki pages and extract data
## May also handle text preprocessing in the future, undetermined.


from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

import _html_controls as htmlc
import _text_controls as txtc

import os
import pickle
import logging

logging.basicConfig(filename = f"../logs/{datetime.strftime(datetime.now(), '%m-%d-%y__%H-%M')}.log", level = logging.DEBUG)

STANDARD_JSON_TEMPLATE = {
    "title": "",
    "eyewiki_page_link":"",
    "error_tags":[],
    "abbreviation_processed": False,
    "text":""
}

test_links = [
    "https://eyewiki.org/Orbital_Adipose_Tissue",
    "https://eyewiki.org/Mooren%27s_Ulcer",
    "https://eyewiki.org/Functional_Visual_Loss",
    "https://eyewiki.org/Geographic_Atrophy",
    "https://eyewiki.org/Eye_Tattooing",
    "https://eyewiki.org/Eyelid_Burns",
    "https://eyewiki.org/Eyelid_Laceration",
    "https://eyewiki.org/Corneal_Allograft_Rejection_and_Failure",
    "https://eyewiki.org/Uveitic_Glaucoma",
    "https://eyewiki.org/Visual_Neglect",
    "https://eyewiki.org/Slit_Lamp_Examination",
    "https://eyewiki.org/Aniseikonia",
    "https://eyewiki.org/Cataract_Surgery_in_the_Setting_of_Posterior_Keratoconus",
    "https://eyewiki.org/Blepharospasm"
]
# Load in all links for scraping from pickle folder
with open("../pickle/all_links.pkl", "rb") as fp:
    all_links = pickle.load(fp)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
# options.add_argument("--headless")
options.add_argument("--log-level=3")
# options.add_argument("--log-level=0")
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# driver = webdriver.Chrome("bin/chromedriver.exe", options = options, service_log_path=os.devnull)
driver = webdriver.Chrome("../bin/chromedriver.exe", options = options)

# Sample scraping from one page
driver.get(test_links[-1])
soup = BeautifulSoup(driver.page_source, "html.parser")

# Set up variables to hold our output
return_text = ""
title = soup.find("h1", id="firstHeading").text
page_link = test_links[-1]
etags = []

logging.info(f"STARTING PROCESSING PAGE {title} AT URL {page_link}")

# Get the first header and collect <p>, <ol>, and <ul> elements for processing
info_elements = soup.find("span", class_ = "mw-headline").parent.find_next_siblings(["h2", "h3", "h4", "p", "ol", "ul"])

# Filter through HTML controls
html_processed = htmlc.remove_excluded_headers(info_elements)
html_processed = htmlc.remove_superscript_references(html_processed)
difftext, html_processed = htmlc.convert_differential_to_text(html_processed, title)

# Extract relevant text elements
for tag in html_processed:
    if tag.name not in ["p", "ol", "ul"]:
        continue
    else:
        text_processed = txtc.remove_figure_or_table_reference(tag.text)
        text_processed = txtc.remove_etal(text_processed)
        text_processed = txtc.replace_newline_period_delimiter(text_processed) 
        text_processed = txtc.remove_icd9(text_processed)

        return_text = return_text + text_processed

return_text + " " + difftext

# Filter through text controls

print(return_text)