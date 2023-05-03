import re
import requests

from bs4 import BeautifulSoup

from controllers.actions.base import BaseAction


GOOGLE_COOKIES = {'CONSENT': 'YES+'}

GOOGLE_DIV_CLASSES = ["hgKElc", "di3YZe", "Z0LcW t2b5Cf", "BNeawe iBp4i AP7Wnd", "BNeawe s3v9rd AP7Wnd"]
GOOGLE_SEARCH_URL = "https://www.google.com/search?hl=en&q="

STARTS_WITH_DATA_REGEX = r'^\d\d (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d\d\d\d'
STARTS_WITH_DATA_RE = re.compile(STARTS_WITH_DATA_REGEX)
class GoogleAnswerAction(BaseAction):
    def perform(self, question):
        """Perform action - Scraping answers from Google."""
        question = question.lower().split()
        full_url = GOOGLE_SEARCH_URL + "+".join(question)
        page = requests.get(full_url, cookies=GOOGLE_COOKIES)
        print("Searching on Google url: " + full_url)
        soup = BeautifulSoup(page.text, "html.parser")
        for c in GOOGLE_DIV_CLASSES:
            res = soup.find("div", {"class" : c})
            if(res):
                res = res.get_text(separator=" ")
                break
            
        if STARTS_WITH_DATA_RE.search(res):
            return None
        return res