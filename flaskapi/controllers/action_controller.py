from controllers.actions.google_answer import GoogleAnswerAction
from controllers.actions.joke import JokeAction
from controllers.actions.news import NewsAction
from controllers.actions.time import TimeAction
from controllers.actions.weather import WeatherAction


class ActionFactory:
    def __init__(self):
        """Factory class for registering action classes and matching
        them with their labels."""
        self._actions = {}

    def register_action(self, action_name, action_class):
        """Method for registering new action classes.

        :Parameters:
            - `action_name`: String. Label for new class.
            - `action_class`: Object. Instance of new class. 
        """
        self._actions[action_name] = action_class

    def get_action(self, action_name):
        """Method for finding appropriate class by its label.

        :Parameters:
            - `action_name`: String. Label associated with the class.
        """
        action = self._actions.get(action_name)
        if not action:
            raise ValueError(action_name)
        return action
        

def perform_action(action_name, question):
    """Factory method to choose appropriate action class and call its
    perform method.
    
    :Parameters:
        - `action_name`: String. Received label from model.
        - `question`: String. Question text.
    """
    if action_name:
        action = factory.get_action(action_name)    
        return action.perform(question)
    return None

factory = ActionFactory()
factory.register_action("joke", JokeAction())
factory.register_action("news", NewsAction())
factory.register_action("other", GoogleAnswerAction())
factory.register_action("time", TimeAction())
factory.register_action("weather", WeatherAction())
