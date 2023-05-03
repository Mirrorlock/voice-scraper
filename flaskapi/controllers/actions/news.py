import random
import requests
from bs4 import BeautifulSoup

from controllers.actions.base import BaseAction


# GOOGLE_COOKIES = {'CONSENT': 'YES+'}

# GOOGLE_DIV_CLASSES = ["hgKElc", "di3YZe", "Z0LcW t2b5Cf", "BNeawe iBp4i AP7Wnd", "BNeawe s3v9rd AP7Wnd"]
# GOOGLE_SEARCH_URL = "https://www.google.com/search?hl=en&q="
BBC_NEWS_URL = "https://www.bbc.com/news/world"
SEARCH_CLASSES = ["gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text", 
                  "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"]
MAX_NUM_ARTICLES = 6


class NewsAction(BaseAction):
    def perform(self, question):
        """Perform action - Scraping news articles' titles."""
        # TODO: Write a doc string
        news = []
        page = requests.get(BBC_NEWS_URL)
        soup = BeautifulSoup(page.text, "html.parser")
        for c in SEARCH_CLASSES:
            res = soup.find_all("h3", {"class" : c})
            if(res):
                if(len(res) < MAX_NUM_ARTICLES):
                    news += res
                else:
                    news += res[:MAX_NUM_ARTICLES]
        return random.choice(list(set(news))).get_text()
