from abc import ABC, abstractmethod

from utils import config

class BaseAction(ABC):
    def __init__(self):
        self._conf = config.get_json_config()
    
    @abstractmethod
    def perform(self, question):
        """Method for performing action. Should be implemented by every specific action type."""
        raise NotImplementedError()        