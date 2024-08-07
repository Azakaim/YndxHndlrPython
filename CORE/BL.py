from CORE.IMarketHandlerFactory import IMarketHandlerFactory
from DAL.Enums.ChooseRepo import ChooseRepo
from DAL.IHandlers.IHandlerMarket import IHandlerMarket


class BL:
    def __init__(self, fabric: IMarketHandlerFactory):
        self._fabric = fabric

    def get_handler_market(self, type_repo: ChooseRepo) -> IHandlerMarket:
        return self._fabric.get_instance(type_repo)
