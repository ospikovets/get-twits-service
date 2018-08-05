__all__ = ['not_found', 'method_not_allowed']

from flask import jsonify

from . import app


@app.errorhandler(404)
def not_found(error):
    return jsonify({
            'error': 'NotFound',
            'errorMessage': 'The requested URL was not found on the server.',
        }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'MethodNotAllowed',
        'errorMessage': 'The method is not allowed for the requested URL.',
    }), 405
