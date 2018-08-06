from urllib.parse import quote_plus


class TwitsService:

    def __init__(self, api, twit_model):
        self.api = api
        self.twit_model = twit_model
        self.twits = []

    def get_twits_by_hashtag(self, hashtag, pages_limit=10):
        """Search Twits by the specified hashtag"""

        query = f'#{hashtag}'
        query = quote_plus(query)

        search_results = self.api.search(query, count=pages_limit)
        twit_dicts = search_results['statuses'][:pages_limit]

        return list(map(self.twit_model.from_dict, twit_dicts))

    def get_twits_by_username(self, username, pages_limit=10):
        """Search Twits by the specified username"""

        query = f'from:{username}'
        query = quote_plus(query)

        search_results = self.api.search(query, count=pages_limit)
        twit_dicts = search_results['statuses'][:pages_limit]

        return list(map(self.twit_model.from_dict, twit_dicts))
