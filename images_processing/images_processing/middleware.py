import logging

from django.http import HttpResponse

db_logger = logging.getLogger('db')

class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, get_response, exception):
        db_logger.exception(exception)