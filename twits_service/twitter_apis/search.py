class TwitterSearchApi:

    def __init__(self, url):
        self.url = url

    def search(self, query, count=15, max_id=None):
        """Get twits from Twitter REST api"""
