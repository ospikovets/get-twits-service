import abc
import inspect
import unittest
from unittest.mock import patch, MagicMock

from twits_service.models.base_model import BaseModel
from twits_service.models.accountmodel import AccountModel
from twits_service.models.twitmodel import TwitModel


class BaseModelTests(unittest.TestCase):

    def test_base_model_interface(self):
        """Test BaseModel class interface."""

        # BaseModel is abstract
        self.assertIsInstance(BaseModel, abc.ABCMeta)
        # from_dict is an abstract classmethod
        self.assertIn('from_dict', BaseModel.__abstractmethods__)
        self.assertTrue(inspect.ismethod(BaseModel.from_dict))
        # as_dict is an abstract method
        self.assertIn('as_dict', BaseModel.__abstractmethods__)
        self.assertFalse(inspect.ismethod(BaseModel.as_dict))


class AccountModelTests(unittest.TestCase):

    def test_account_model_is_subclassed_from_the_base_model(self):
        """Test AccountModel is subclassed from the BaseModel."""

        self.assertTrue(issubclass(AccountModel, BaseModel))

    def test_account_model_from_dict(self):
        """Test AccountModel.from_dict instantiates AccountModel from the given dictionary."""

        id_ = 12345
        fullname = 'TestName'
        href = '/TestName'
        dict_ = {
            "id": id_,
            "id_str": str(id_),
            "name": "NASA JPL",
            "screen_name": fullname,
            "location": "Pasadena, Calif.",
            "url": href,
            "entities": {
                "url": {
                    "urls": [
                        {
                            "url": "http://t.co/gcM9d1YLUB",
                            "expanded_url": "http://www.jpl.nasa.gov",
                            "display_url": "jpl.nasa.gov",
                            "indices": [
                                    0,
                                    22
                            ]
                        }
                    ]
                },
                "description": {
                    "urls": []
                }
            },
        }

        ac = AccountModel.from_dict(dict_)

        self.assertIsInstance(ac, AccountModel)
        self.assertEqual(id_, ac.id)
        self.assertEqual(fullname, ac.fullname)
        self.assertEqual(href, ac.href)

    def test_account_model_as_dict(self):
        """Test AccountModel.as_dict() returns a dict like representation of the AccountModel."""

        id_ = 12345
        fullname = 'TestName'
        href = '/TestName'
        ac = AccountModel(id_, fullname, href)

        account_dict = ac.as_dict()

        self.assertIsInstance(account_dict, dict)
        self.assertEqual(id_, account_dict['id'])
        self.assertEqual(fullname, account_dict['fullname'])
        self.assertEqual(href, account_dict['href'])


class TwitModelTests(unittest.TestCase):

    def test_twit_model_is_subclassed_from_the_base_model(self):
        """Test TwitModel is subclassed from the BaseModel."""

        self.assertTrue(issubclass(TwitModel, BaseModel))

    @patch.object(AccountModel, 'from_dict')
    def test_twit_model_from_dict(self, mock_account_model_from_dict):
        """Test TwitModel.from_dict instantiates TwitModel from the given dictionary."""

        account = 'Mock Account'
        mock_account_model_from_dict.return_value = account

        account_dict = {"id": 12345}
        text = 'Twit #text'
        date = 'Sun Feb 25 18:11:01 +0000 2018'
        hashtags = ['#text']
        likes = 10
        replies = 0
        retwits = 5
        dict_ = {
            "created_at": date,
            "id": 12345,
            "id_str": "12345",
            "text": text,
            "entities": {
                "hashtags": hashtags,
            },
            "user": account_dict,
            "retweet_count": retwits,
            "favorite_count": likes,
            "favorited": False,
            "retweeted": False,
            "possibly_sensitive": False,
            "lang": "en"
        }

        t = TwitModel.from_dict(dict_)

        self.assertIsInstance(t, TwitModel)
        self.assertEqual(account, t.account)
        mock_account_model_from_dict.assert_called_once_with(account_dict)
        self.assertEqual(text, t.text)
        self.assertEqual(date, t.date)
        self.assertEqual(hashtags, t.hashtags)
        self.assertEqual(likes, t.likes)
        self.assertEqual(replies, t.replies)
        self.assertEqual(retwits, t.retwits)

    def test_twit_model_as_dict(self):
        """Test TwitModel.as_dict() returns a dict like representation of the TwitModel."""

        class MockAccountModel(BaseModel):
            def as_dict(self):
                return 'Test Account'

            @classmethod
            def from_dict(cls, dict_):
                pass

        account = MockAccountModel()
        text = 'Twit #text'
        date = 'Sun Feb 25 18:11:01 +0000 2018'
        hashtags = ['#text']
        likes = 10
        replies = 0
        retwits = 5
        t = TwitModel(
            account,
            text,
            date,
            hashtags,
            likes,
            replies,
            retwits,
        )

        twit_dict = t.as_dict()

        self.assertIsInstance(twit_dict, dict)
        self.assertEqual(account.as_dict(), twit_dict['account'])
        self.assertEqual(text, twit_dict['text'])
        self.assertEqual(date, twit_dict['date'])
        self.assertEqual(hashtags, twit_dict['hashtags'])
        self.assertEqual(likes, twit_dict['likes'])
        self.assertEqual(replies, twit_dict['replies'])
        self.assertEqual(retwits, twit_dict['retwits'])
