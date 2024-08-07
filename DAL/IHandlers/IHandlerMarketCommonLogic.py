from abc import ABC, abstractmethod
from DAL.IRepository.IRepository import IRepository


class IHandlerMarketCommonLogic(ABC):
    repo: IRepository

    def __init__(self, repo: IRepository):
        self.repo = repo
        pass

    @abstractmethod
    def _auth(self):
        pass

    @abstractmethod
    def _get_market_data(self):
        pass

    @abstractmethod
    def _process_market_data(self):
        pass

    @abstractmethod
    def _give_away_market_data(self):
        pass