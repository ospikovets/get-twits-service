from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_):
        """Build a model from dictionary"""

    @abstractmethod
    def as_dict(self):
        """Represents model as dictionary"""
