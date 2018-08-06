from flask import jsonify, request

from twits_service.models.twit import Twit as twit_model
from twits_service.services.twits import TwitsService
from twits_service.twitter_apis.search import TwitterSearchApi
from . import app

api = TwitterSearchApi(url='https://api.twitter.com/1.1/search/tweets.json')
ts = TwitsService(api, twit_model)


@app.route('/hashtags/<hashtag>', methods=['GET'], provide_automatic_options=True)
def hashtags(hashtag):
    pages_limit = request.args.get('pages_limit', 10, int)
    twits = ts.get_twits_by_hashtag(hashtag, pages_limit=pages_limit)
    twit_dicts = [twit.as_dict() for twit in twits]
    return jsonify(twit_dicts)


@app.route('/users/<user>', methods=['GET'], provide_automatic_options=True)
def users(user):
    pages_limit = request.args.get('pages_limit', 10, int)
    twits = ts.get_twits_by_username(user, pages_limit=pages_limit)
    twit_dicts = [twit.as_dict() for twit in twits]
    return jsonify(twit_dicts)
