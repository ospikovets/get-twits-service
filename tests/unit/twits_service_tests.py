import unittest
from unittest.mock import MagicMock

from twits_service.services import TwitsService


class MockTwitterApi:
    def __init__(self, *args, **kwargs):
        self.search = MagicMock()


class MockTwitModel:
    from_dict = MagicMock()


class TwitsServiceTests(unittest.TestCase):

    def setUp(self):
        twit_model = MockTwitModel
        mock_twit_dicts = [f'Twit {number}' for number in range(30)]
        api = MockTwitterApi()
        api.search.return_value = {
            'statuses': mock_twit_dicts,
            'search_metadata': {},
        }

        self.mock_twits = [MockTwitModel.from_dict(twit_dict) for twit_dict in mock_twit_dicts]
        self.ts = TwitsService(api, twit_model)

    def test_get_twits_by_hashtag(self):
        """Test getting twits by HashTag."""

        twits = self.ts.get_twits_by_hashtag('TestTag')

        self.ts.api.search.assert_called_once()
        self.assertEqual(self.mock_twits[:10], twits)

    def test_get_twits_by_hashtag_default_pages_limit(self):
        """Test getting twits by HashTag with default pages_limit=10."""

        twits = self.ts.get_twits_by_hashtag('TestTag')

        self.assertLessEqual(len(twits), 10)

    def test_get_twits_by_hashtag_with_pages_limit(self):
        """Test getting twits by HashTag page_limit varies."""

        for pages_limit in range(5, 10, 15):
            twits = self.ts.get_twits_by_hashtag('TestTag', pages_limit=pages_limit)

            self.assertLessEqual(len(twits), pages_limit)

    def test_get_twits_by_username(self):
        """Test getting twits by username."""

        twits = self.ts.get_twits_by_username('TestUser')

        self.ts.api.search.assert_called_once()
        self.assertEqual(self.mock_twits[:10], twits)

    def test_get_twits_by_username_default_pages_limit(self):
        """Test getting twits by username with default pages_limit=10."""

        twits = self.ts.get_twits_by_username('TestUser')

        self.assertLessEqual(len(twits), 10)

    def test_get_twits_by_username_with_pages_limit(self):
        """Test getting twits by username page_limit varies."""

        for pages_limit in range(5, 10, 15):
            twits = self.ts.get_twits_by_username('TestUser', pages_limit=pages_limit)

            self.assertLessEqual(len(twits), pages_limit)
