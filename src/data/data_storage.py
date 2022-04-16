from abc import ABC, abstractmethod


class DataStorage(ABC):

    @abstractmethod
    def save_data(self, uuid, msg):
        pass

    @abstractmethod
    def get_data_by_id(self, uuid):
        pass

    @abstractmethod
    def get_all_data(self):
        pass
