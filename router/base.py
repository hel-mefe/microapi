from abc import ABC, abstractmethod
from typing import Callable, Optional

Handler = Callable[..., object]

class BaseRouter(ABC):
    @abstractmethod
    def add(self, method: str, path: str, handler: Handler) -> None:
        """
        Register a new route
        """

        raise NotImplementedError
    

    @abstractmethod
    def match(self, method: str, path: str) -> Optional[Handler]:
        """
        Register a new route.
        """
            
        raise NotImplementedError
