import requests

from .exceptions import *


class TwitterSearchApi:

    MAX_QUERY_LENGTH = 500

    def __init__(self, url):
        self.url = url

    def search(self, query, count=15, max_id=None):
        """Get twits from Twitter REST api"""

        self.validate_query(query)

        params = {
            'q': query,
            'count': count
        }
        if max_id is not None:
            params['max_id'] = max_id

        try:
            rsp = requests.get(
                self.url,
                params=params,
                auth=()
            )
        except requests.exceptions.RequestException as e:
            raise RequestException from e

        return self._validate_response(rsp)

    @classmethod
    def validate_query(cls, query):
        """Validates the search query"""

        if len(query) > cls.MAX_QUERY_LENGTH:
            raise QueryException(f"Too long. The query should't be longer than {cls.MAX_QUERY_LENGTH} symbols")

    @classmethod
    def _validate_response(cls, response):
        """Validate API response"""

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HTTPError from e

        return response.json()
