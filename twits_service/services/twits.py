class TwitsService:

    def __init__(self, api, twit_model):
        self.api = api
        self.twit_model = twit_model
        self.twits = []

    def get_twits_by_hashtag(self, hashtag, pages_limit=10):
        """Search Twits by the specified hashtag"""

    def get_twits_by_username(self, username, pages_limit=10):
        """Search Twits by the specified username"""
