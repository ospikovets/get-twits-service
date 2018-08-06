from flask import jsonify, Blueprint


def not_found(error):
    return jsonify({
            'error': 'NotFound',
            'errorMessage': 'The requested URL was not found on the server.',
        }), 404


def method_not_allowed(error):
    return jsonify({
        'error': 'MethodNotAllowed',
        'errorMessage': 'The method is not allowed for the requested URL.',
    }), 405
