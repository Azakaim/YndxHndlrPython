from abc import ABC, abstractmethod
from enum import Enum, auto


class TypeResponder(Enum):
    PATTERN = auto()
    GPT = auto()


class IFabricResponder(ABC):
    @abstractmethod
    def get_responder_instance(self, type_responder: TypeResponder):
        pass


class IConcreteResponder(ABC):
    @abstractmethod
    def response(self, **kwargs) -> str:
        pass
