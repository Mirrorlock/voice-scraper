import os

from flask import Flask, request
from utils.utils import compose_message

import constants

from controllers.action_controller import perform_action
from controllers.speech_processor import SpeechProcessor


app = Flask(__name__)
processor = SpeechProcessor(os.getenv("MODEL_PATH"))


@app.route("/question", methods = ['POST'])
def process_question():
    if('application/json' in request.headers.get('Content-Type')):
        question = request.get_json().get(constants.REQUEST_TEXT_KEY) 
        if(question):
            print("Question: ", question)
            action = processor.process(question) or "other"
            response = perform_action(action, question)
            if not response:
                return compose_message(None, False)
            print("Responding with: ", response)
            print("-" * 10)
            return compose_message(str(response), True), 200
        return compose_message(constants.REQUEST_FORMAT_ERROR, False), 400
    return compose_message("Wrong content type!", False), 400