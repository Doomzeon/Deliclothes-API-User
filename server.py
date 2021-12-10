from flask import Flask
from flask_cors import CORS
from bin.handler.router import Router
import logging
app = Flask(__name__)
CORS(app)
import sentry_sdk

sentry_sdk.init(
   "https://bf52e362a6e14645851721b5fe956fe1@o560382.ingest.sentry.io/5695899",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

logging.basicConfig(level=logging.INFO)

# Set essential variables
default_encoding = 'UTF-8' # => in settings

# Configure Routing
Router(app)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
