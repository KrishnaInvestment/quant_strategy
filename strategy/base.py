from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Abstract base class for geometric shapes.
    """

    @abstractmethod
    def generate_signal(self):
        pass