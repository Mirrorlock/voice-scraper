import requests

from controllers.actions.base import BaseAction


JOKES_API = "https://dad-jokes.p.rapidapi.com/random/joke"


class JokeAction(BaseAction):
    def __init__(self):
        super().__init__()
        self._headers = {
            "X-RapidAPI-Key": self._conf.get("X-RapidAPI-Key"),
            "X-RapidAPI-Host": self._conf.get("X-RapidAPI-Host")
        }

    def _get_random_joke(self):
        """Request a random joke from source."""
        joke = requests.get(JOKES_API, headers=self._headers).json()
        if joke.get("success"):
            body = joke.get("body")[0]
            joke_text = body.get("setup") + "\n"*2 + body.get("punchline") 
            print(joke_text)
            return joke_text
        return None

    def perform(self, question):
        """Perform action - Scraping answers from Google."""
        return self._get_random_joke()