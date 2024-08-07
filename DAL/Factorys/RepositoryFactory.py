from DAL.Enums.ChooseRepo import ChooseRepo
from DAL.Repository.Repository import RepositoryYandex, RepositoryOzon, RepositoryWildberries


class RepositoryFactory:
    def get_instance_repo(self, repo_name: ChooseRepo):
        if repo_name == ChooseRepo.YandexHandler:
            return RepositoryYandex()
        if repo_name == ChooseRepo.WbHandler:
            return RepositoryWildberries()
        if repo_name == ChooseRepo.OzonHandler:
            return RepositoryOzon()
