import random
import re
import requests
from bs4 import BeautifulSoup

from controllers.actions.base import BaseAction
from utils.utils import extract_location_from_question

TIME_IS_URL = "https://time.is/"

TIME_ID = "clock0_bg"
DIFF_TIME_ZONES_ID = "locw" 

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

BRACKETS_CONTENT_RE = re.compile("\([\w+ +\.+]*\)")
DEFAULT_LOCATION = "Krems"

class TimeAction(BaseAction):
    def perform(self, question):
        """Perform action - Scrape time data for a specific area."""

        result = ""
        location = extract_location_from_question(question)
        
        if not location:
            location = DEFAULT_LOCATION

        full_url = TIME_IS_URL + location
        page = requests.get(full_url, headers=HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        additional_info = soup.find("span", {"id" : DIFF_TIME_ZONES_ID})
        main_clock = soup.find("div", {"id" : TIME_ID})
        
        if main_clock:
            result += f"Current time in {location} is: {main_clock.get_text()}. " 

            if additional_info:
                add_info_text = BRACKETS_CONTENT_RE.sub("", additional_info.getText())
                print(add_info_text)
                additional_info_sentences = add_info_text.split(".")
                for sentence in additional_info_sentences: 
                    if "time zone" in sentence or "saving time" in sentence or "used" in sentence:
                        result += sentence + ". "
            return result
                    
        else:
            return None