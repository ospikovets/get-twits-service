import unittest
from unittest.mock import patch

from twits_service.flask_app.views import app, ts


class FlaskAppTestCase(unittest.TestCase):
    """Base class to enclose shared tests functionality."""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()


class ViewsTests(FlaskAppTestCase):
    """Test requests handling by the application."""

    MOCK_TWITS = [
        {
            'account': {
                'fullname': 'Twitter',
                'href': '/Twitter',
                'id': 783214,
            },
            'date': '2:54 PM - 8 Mar 2018',
            'hashtags': ['#InternationalWomensDay'],
            'likes': 287,
            'replies': 17,
            'retweets': 70,
            'text': 'Powerful voices. Inspiring women.\n\n#InternationalWomensDay '
                    'https://twitter.com/i/moments/971870564246634496'
        },
    ]

    class MockTwitModel:
        def __init__(self, twit_dict):
            self.twit_dict = twit_dict

        def as_dict(self):
            return self.twit_dict

    def mock_get_twits(self, pages_limit):
        all_twits = [self.MockTwitModel(twit_dict) for twit_dict in self.MOCK_TWITS]
        return all_twits[:pages_limit]

    def mock_get_twits_by_hashtag(self, hashtag, pages_limit):
        return self.mock_get_twits(pages_limit)

    def mock_get_twits_by_username(self, username, pages_limit):
        return self.mock_get_twits(pages_limit)

    @patch.object(ts, 'get_twits_by_hashtag')
    def test_hashtags_get(self, mock_get_twits_by_hashtag):
        """Test GET request to /hashtags/<hashtag> endpoint."""

        hashtag = 'InternationalWomensDay'
        mock_get_twits_by_hashtag.side_effect = self.mock_get_twits_by_hashtag

        rsp = self.client.get(f'/hashtags/{hashtag}')

        # Test base response parameters
        self.assertEqual(200, rsp.status_code)
        self.assertEqual('application/json', rsp.mimetype)

        for index, twit in enumerate(rsp.json):
            self.validate_twit_layout(twit)
            self.assertDictEqual(self.MOCK_TWITS[index], twit)

    @patch.object(ts, 'get_twits_by_hashtag')
    def test_hashtags_get_custom_pages_limit(self, mock_get_twits_by_hashtag):
        """Test pages_limit query parameter for GET request to /hashtags/<hashtag> endpoint."""

        hashtag = 'InternationalWomensDay'
        pages_limit = 3
        mock_get_twits_by_hashtag.side_effect = self.mock_get_twits_by_hashtag

        rsp = self.client.get(f'/hashtags/{hashtag}?pages_limit={pages_limit}')

        mock_get_twits_by_hashtag.assert_called_once_with(hashtag, pages_limit=pages_limit)
        self.assertLessEqual(len(rsp.json), pages_limit)

    @patch.object(ts, 'get_twits_by_hashtag')
    def test_hashtags_get_default_pages_limit(self, mock_get_twits_by_hashtag):
        """Test default pages_limit==10 for GET request to /hashtags/<hashtag> endpoint."""

        hashtag = 'InternationalWomensDay'
        mock_get_twits_by_hashtag.side_effect = self.mock_get_twits_by_hashtag

        rsp = self.client.get(f'/hashtags/{hashtag}')

        mock_get_twits_by_hashtag.assert_called_once_with(hashtag, pages_limit=10)
        self.assertLessEqual(len(rsp.json), 10)

    @patch.object(ts, 'get_twits_by_username')
    def test_users_get(self, mock_get_twits_by_username):
        """Test GET request to /users/<user> endpoint."""

        user = 'Twitter'
        mock_get_twits_by_username.side_effect = self.mock_get_twits_by_username

        rsp = self.client.get(f'/users/{user}')

        # Test base response parameters
        self.assertEqual(200, rsp.status_code)
        self.assertEqual('application/json', rsp.mimetype)

        for index, twit in enumerate(rsp.json):
            self.validate_twit_layout(twit)
            self.assertDictEqual(self.MOCK_TWITS[index], twit)

    @patch.object(ts, 'get_twits_by_username')
    def test_users_get_custom_pages_limit(self, mock_get_twits_by_username):
        """Test pages_limit query parameter for GET request to /users/<user> endpoint."""

        user = 'Twitter'
        pages_limit = 3

        rsp = self.client.get(f'/users/{user}?pages_limit={pages_limit}')

        mock_get_twits_by_username.assert_called_once_with(user, pages_limit=pages_limit)
        self.assertLessEqual(len(rsp.json), pages_limit)

    @patch.object(ts, 'get_twits_by_username')
    def test_users_get_default_pages_limit(self, mock_get_twits_by_username):
        """Test default pages_limit==10 for GET request to /users/<user> endpoint."""

        user = 'Twitter'

        rsp = self.client.get(f'/users/{user}')

        mock_get_twits_by_username.assert_called_once_with(user, pages_limit=10)
        self.assertLessEqual(len(rsp.json), 10)

    # =====================================================
    # ================== Test Helpers =====================
    # =====================================================

    def validate_twit_layout(self, twit):
        """Validate that twit object is properly formed."""

        self.assertIn('account', twit)
        self.assertIn('fullname', twit['account'])
        self.assertIn('href', twit['account'])
        self.assertIn('id', twit['account'])
        self.assertIn('date', twit)
        self.assertIn('hashtags', twit)
        self.assertIn('likes', twit)
        self.assertIn('replies', twit)
        self.assertIn('retweets', twit)
        self.assertIn('text', twit)


class ErrorHandlersTests(FlaskAppTestCase):
    """Test handling errors by the application."""

    def test_404(self):
        """Test 404 Not Found error."""

        rsp = self.client.get(f'/not_existing_endpoint')

        self.assertEqual(404, rsp.status_code)
        self.assertEqual('application/json', rsp.mimetype)
        self.assertDictEqual({
            'error': 'NotFound',
            'errorMessage': 'The requested URL was not found on the server.',
        }, rsp.json)

    def test_405(self):
        """Test 405 Method Not Allowed error."""

        app.add_url_rule('/test', view_func=lambda: None, methods=['GET'])

        rsp = self.client.post(f'/test')

        self.assertEqual(405, rsp.status_code)
        self.assertEqual('application/json', rsp.mimetype)
        self.assertDictEqual({
            'error': 'MethodNotAllowed',
            'errorMessage': 'The method is not allowed for the requested URL.',
        }, rsp.json)
