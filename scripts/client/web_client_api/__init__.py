# Embedded file name: scripts/client/web_client_api/__init__.py


class WebCommandException(Exception):

    def __init__(self, description):
        super(WebCommandException, self).__init__(description)