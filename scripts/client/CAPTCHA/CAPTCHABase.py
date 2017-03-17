# Embedded file name: scripts/client/CAPTCHA/CAPTCHABase.py
from Helpers import i18n

class CAPTCHABase(object):
    """
    Base class for CAPTCHA API
    """
    _SERVER_API_URL = None
    _SERVER_ERROR_CODES = {}
    _RESPONSE_IS_INCORRECT_CODE = None
    _IMAGE_SIZE = (0, 0)

    def getI18nServerErrorText(self, errorCode, defaultErrorCode = 'unknown'):
        """
        Return i18n error text by server error code.
        @param errorCode: server error code.
        @param defaultErrorCode: If error code isn't in dictionary of server codes, than return i18n error text by this key.
        @return:
        @raise:
        """
        key = self._SERVER_ERROR_CODES.get(errorCode)
        if key is None:
            key = self._SERVER_ERROR_CODES.get(defaultErrorCode)
        if key is None:
            raise Exception, "It is impossible to determine error text for code = '%s', default code = '%s'" % (errorCode, defaultErrorCode)
        return i18n.makeString(key)

    def getImageSource(self, publicKey, *args):
        """
        Gets image binary source.
        @param publicKey: CAPTCHA public key.
        @param args:
        @raise:
        """
        raise NotImplemented, 'method getImageSource must be implement'