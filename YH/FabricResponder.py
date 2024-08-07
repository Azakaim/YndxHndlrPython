from abc import ABC

from ConcreteResponder import PatternResponder, GPTResponder
from Interfaces import TypeResponder, IConcreteResponder, IFabricResponder


class FabricResponder(IFabricResponder, ABC):
    def get_responder_instance(self, type_responder: TypeResponder) -> IConcreteResponder:
        if type_responder == TypeResponder.PATTERN:
            return PatternResponder()
        if type_responder == TypeResponder.GPT:
            return GPTResponder()
