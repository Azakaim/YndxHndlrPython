from abc import ABC, abstractmethod

from DAL.Enums.ChooseRepo import ChooseRepo
from DAL.IHandlers.IHandlerMarket import IHandlerMarket


class IMarketHandlerFactory(ABC):
    @abstractmethod
    def get_instance(self, check_type: ChooseRepo) -> IHandlerMarket:
        ...
