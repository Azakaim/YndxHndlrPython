from CORE.IMarketHandlerFactory import IMarketHandlerFactory
from DAL.Enums.ChooseRepo import ChooseRepo
from DAL.Factorys.IFactrorys.IRepositoryFactory import IRepositoryFactory
from DAL.Handlers.Handlers import YandexHandler, WbHandler, OzonHandler
from DAL.IHandlers.IHandlerMarket import IHandlerMarket


class MarketHandlerFactory(IMarketHandlerFactory):
    def __init__(self, check_type: ChooseRepo):
        self.check_type = check_type

    def get_instance(self, name_repo: ChooseRepo) -> IHandlerMarket:
        if self.check_type == ChooseRepo.YandexHandler:
            return YandexHandler(IRepositoryFactory().get_instance_repo(ChooseRepo.YandexHandler))
        if self.check_type == ChooseRepo.WbHandler:
            return WbHandler(IRepositoryFactory().get_instance_repo(ChooseRepo.WbHandler))
        if self.check_type == ChooseRepo.OzonHandler:
            return OzonHandler(IRepositoryFactory().get_instance_repo(ChooseRepo.OzonHandler))