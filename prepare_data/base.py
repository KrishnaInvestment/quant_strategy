from abc import ABC, abstractmethod

class Prepare(ABC):
    """
    Abstract base class for preparing data.
    """

    @abstractmethod
    def get_data(self):
        pass