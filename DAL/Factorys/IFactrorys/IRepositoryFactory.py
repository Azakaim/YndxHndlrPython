class IRepositoryFactory(ABC):
    @abstractmethod
    def get_instance_repo(self, repo_name: ChooseRepo):
        pass