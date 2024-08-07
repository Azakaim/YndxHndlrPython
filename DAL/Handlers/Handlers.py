from abc import ABC

from DAL.IHandlers.IHandlerMarket import IHandlerMarket
from DAL.IHandlers.IHandlerMarketCommonLogic import IHandlerMarketCommonLogic
from DAL.IRepository.IRepository import IRepository


class YandexHandler(IHandlerMarketCommonLogic, IHandlerMarket, ABC):
    repo: IRepository

    def __init__(self, repo: IRepository):
        super().__init__(repo)
        self.repo = repo

    def _auth(self):
        return NotImplementedError()

    def _get_market_data(self):
        return NotImplementedError()

    def _process_market_data(self):
        return NotImplementedError()

    def _give_away_market_data(self):
        return NotImplementedError()

    def common_process(self):
        self._auth()
        self._get_market_data()
        self._process_market_data()
        self._give_away_market_data()


class WbHandler(IHandlerMarketCommonLogic, IHandlerMarket, ABC):
    repo: IRepository

    def __init__(self, repo: IRepository):
        super().__init__(repo)
        self.repo = repo

    def _auth(self):
        return NotImplementedError()

    def _get_market_data(self):
        return NotImplementedError()

    def _process_market_data(self):
        return NotImplementedError()

    def _give_away_market_data(self):
        return NotImplementedError()

    def common_process(self):
        self._auth()
        self._get_market_data()
        self._process_market_data()
        self._give_away_market_data()


class OzonHandler(IHandlerMarketCommonLogic, IHandlerMarket, ABC):
    repo: IRepository

    def __init__(self, repo: IRepository):
        super().__init__(repo)
        self.repo = repo

    def _auth(self):
        return NotImplementedError()

    def _get_market_data(self):
        return NotImplementedError()

    def _process_market_data(self):
        return NotImplementedError()

    def _give_away_market_data(self):
        return NotImplementedError()

    def common_process(self):
        self._auth()
        self._get_market_data()
        self._process_market_data()
        self._give_away_market_data()