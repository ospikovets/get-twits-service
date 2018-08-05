from flask import jsonify

from . import app


@app.route('/hashtags/<hashtag>', methods=['GET'], provide_automatic_options=True)
def hashtags(hashtag):
    return jsonify({'hashtag': hashtag})


@app.route('/users/<user>', methods=['GET'], provide_automatic_options=True)
def users(user):
    return jsonify({'user': user})
