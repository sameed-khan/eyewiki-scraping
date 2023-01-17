## link_scrape.py
## Sameed Khan, 01/16/2023
## Simple script to grab all the links from the EyeWiki front page first before processing each page
## Not relevant if "pickle/all_links.pkl" exists

from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pickle

### Begin script

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
driver.get("https://eyewiki.org/Special:AllPages")

all_links_list = []
for i in range(5):  # I'm hardcoding this since I know it takes 6 clicks to get to the end of all the pages in EyeWiki
    soup = BeautifulSoup(driver.page_source, "html.parser")
    top_ul = soup.find("ul", class_ = "mw-allpages-chunk")
    link_elements = top_ul.find_all("li")
    print(f"THERE WERE {len(link_elements)} FOUND IN PAGE")
    all_links_list.extend([f"https://eyewiki.org{tag.find('a')['href']}" for tag in link_elements])
    next_page_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Next page')]")))
    next_page_link.click()


with open("../pickle/all_links.pkl", "wb") as fp:
    pickle.dump(all_links_list, fp)

print(all_links_list)
print(len(all_links_list))