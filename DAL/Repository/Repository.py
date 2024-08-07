from DAL.IRepository.IRepository import IRepository


class RepositoryYandex(IRepository):
    def get_data(self):
        return "data"


class RepositoryWildberries(IRepository):
    def get_data(self):
        return "data"


class RepositoryOzon(IRepository):
    def get_data(self):
        return "data"
