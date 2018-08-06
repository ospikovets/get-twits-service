from flask import Flask

from .views import main
from .error_handlers import not_found, method_not_allowed

app = Flask(__name__)

app.register_error_handler(404, not_found)
app.register_error_handler(405, method_not_allowed)

app.register_blueprint(main, url_prefix='/')
