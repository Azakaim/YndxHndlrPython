from CORE.BL import BL
from DAL.Enums.ChooseRepo import ChooseRepo
from DAL.Factorys.MarketHandlerFactory import MarketHandlerFactory


fabric = MarketHandlerFactory(ChooseRepo.WbHandler)
bl = BL(fabric)
handler = bl.get_handler_market(ChooseRepo.WbHandler)

handler.common_process()
