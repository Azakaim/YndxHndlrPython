from abc import ABC, abstractmethod


class IHandlerMarket(ABC):
    @abstractmethod
    def common_process(self):
        pass
