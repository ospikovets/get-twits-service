import unittest
from unittest.mock import MagicMock
import requests_mock
from twits_service.twitter_apis.search import TwitterSearchApi
from twits_service.twitter_apis.exceptions import QueryException, HTTPError
from ..resources.mock_api_responses import MOCK_TWITTER_SEARCH_API_RESPONSE as API_RESPONSE


class TwitterSearchApiTests(unittest.TestCase):

    def test_search_success(self):
        """Test TwitterSearchApi.search() return twits that satisfy search query."""

        api_url = 'https://api.twitter.com/1.1/search/tweets.json'
        search_query = 'nasa'
        mock_validate_query = MagicMock(name='validate_query')
        sa = TwitterSearchApi(api_url)
        sa.validate_query = mock_validate_query

        with requests_mock.mock() as rm:
            rm.get(api_url, status_code=200, json=API_RESPONSE)
            search_results = sa.search(search_query)

        mock_validate_query.assert_called_once_with(search_query)
        self.assertEqual(API_RESPONSE, search_results)

    def test_search_error(self):
        """Test TwitterSearchApi.search() raises HTTPError when response status_code != 200."""

        api_url = 'https://api.twitter.com/1.1/search/tweets.json'
        search_query = 'nasa'
        mock_validate_query = MagicMock(name='validate_query')
        sa = TwitterSearchApi(api_url)
        sa.validate_query = mock_validate_query

        for status_code in [400, 401, 403, 404, 500]:
            with requests_mock.mock() as rm:
                rm.get(api_url, status_code=status_code)

                self.assertRaises(HTTPError, sa.search, search_query)

    def test_validate_query(self):
        """Test TwitterSearchApi.validate_query() raises QueryException when query length > 500."""

        query = "a" * 501
        self.assertRaises(QueryException, TwitterSearchApi.validate_query, query)
