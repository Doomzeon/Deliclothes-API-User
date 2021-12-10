import sentry_sdk
from enum import Enum
import logging

class LogLevel(Enum):
    fatal = 1
    error = 2
    warning = 3
    info = 4
    debug = 5

class Logger(object):
    def __init__(self):
        #setup sentry
        sentry_sdk.init(
            "https://bf52e362a6e14645851721b5fe956fe1@o560382.ingest.sentry.io/5695899",

                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                # We recommend adjusting this value in production.
                traces_sample_rate=1.0
            )
        
        
    def logMessage(self, message):
        print(message)
        with sentry_sdk.configure_scope() as scope:
            scope.level = LogLevel.info.name
            sentry_sdk.capture_message(message)


    def log(self, e, severity: LogLevel, message=None):
        logging.error(f'Exception: {e}, Message:{message}')
        with sentry_sdk.configure_scope() as scope:
            scope.level = severity.name
            if message is not None:
                sentry_sdk.capture_message(message)
            else:
                sentry_sdk.capture_exception(e)
            