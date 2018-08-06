from .base_model import BaseModel
from .accountmodel import AccountModel


class TwitModel(BaseModel):
    """Model to represent Twit"""

    def __init__(self, account, text, date, hashtags, likes, replies, retwits):
        self.account = account
        self.text = text
        self.date = date
        self.hashtags = hashtags
        self.likes = likes
        self.replies = replies
        self.retwits = retwits

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            account=AccountModel.from_dict(dict_['user']),
            text=dict_['text'],
            date=dict_['created_at'],
            hashtags=dict_['entities']['hashtags'],
            likes=dict_['favorite_count'],
            replies=0,
            retwits=dict_['retweet_count']
        )

    def as_dict(self):
        """Represents model as dictionary"""
        result = {}
        for key, attr in self.__dict__.items():
            if issubclass(type(attr), BaseModel):
                result[key] = attr.as_dict()
            else:
                result[key] = attr

        return result
