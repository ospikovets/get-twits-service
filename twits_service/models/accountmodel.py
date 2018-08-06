from .base_model import BaseModel


class AccountModel(BaseModel):

    def __init__(self, id_, fullname, href):
        self.id = id_
        self.fullname = fullname
        self.href = href

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            id_=dict_['id'],
            fullname=dict_['screen_name'],
            href=dict_['url'],
        )

    def as_dict(self):
        return self.__dict__
