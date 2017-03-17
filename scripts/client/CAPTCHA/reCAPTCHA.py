# Embedded file name: scripts/client/CAPTCHA/reCAPTCHA.py
from CAPTCHA.CAPTCHABase import CAPTCHABase
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION, LOG_DEBUG
import re
import time
import urllib
DEFAULT_RE_CAPTCHA_PATTERN = '<input[>]?[^>]*id[^=]?=[^"]?"recaptcha_challenge_field"[^>]*value[^=]?=[^"]?"(?P<challenge>[^"]+)"[^>]*>'

class reCAPTCHA(CAPTCHABase):
    """
    Google reCAPTCHA API.
    See documentation http://code.google.com/apis/recaptcha/.
    """
    _SERVER_API_URL = 'http://www.google.com/recaptcha/api'
    _SERVER_ERROR_CODES = {'unknown': '#recaptcha:error-codes/unknown',
     'invalid-site-public-key': '#recaptcha:error-codes/invalid-site-public-key',
     'invalid-site-private-key': '#recaptcha:error-codes/invalid-site-private-key',
     'invalid-request-cookie': '#recaptcha:error-codes/invalid-request-cookie',
     'incorrect-captcha-sol': '#recaptcha:error-codes/incorrect-captcha-sol',
     'verify-params-incorrect': '#recaptcha:error-codes/verify-params-incorrect',
     'invalid-referrer': '#recaptcha:error-codes/invalid-referrer',
     'recaptcha-not-reachable': '#recaptcha:error-codes/recaptcha-not-reachable',
     'enqueue-failure': '#recaptcha:error-codes/enqueue-failure',
     'captcha-sol-empty': '#recaptcha:error-codes/captcha-sol-empty'}
    _RESPONSE_IS_INCORRECT_CODE = 'incorrect-captcha-sol'
    _IMAGE_SIZE = (300, 57)

    def getImageSource(self, key, *args):
        """
        Routine loads html (noscript) from reCAPTCHA API server, parse this html and
        gets value of challenge. Next, routine load image by challenge from reCAPTCHA API server.
        @param key: public key for reCAPTCHA
        @param args: pattern to find value of challenge in html source.
        @return: tuple(<image url>, <value of challenge>). If an error occurs while loading or parsing, than routine return (None, None)
        """
        challenge_regexp = args[0] if args[0] is not None and len(args[0]) else DEFAULT_RE_CAPTCHA_PATTERN
        params = urllib.urlencode({'k': key})
        url = '%s/noscript?%s' % (self._SERVER_API_URL, params)
        resp = None
        challenge = None
        imageUrl = None
        start = time.time()
        try:
            resp = urllib.urlopen(url)
            html = resp.read()
            challenge = re.search(challenge_regexp, html, flags=re.DOTALL).group('challenge')
        except:
            LOG_ERROR('client can not load or parse reCAPTCHA html')
        finally:
            if resp is not None:
                resp.close()

        resp, data = (None, None)
        if challenge:
            url = '%s/image?c=%s' % (self._SERVER_API_URL, challenge)
            try:
                resp = urllib.urlopen(url)
                contentType = resp.headers.get('content-type')
                if contentType == 'image/jpeg':
                    data = resp.read()
                else:
                    LOG_ERROR('Client can not load reCAPTCHA image. contentType = {0}, response code = {1}'.format(contentType, resp.code))
            except:
                LOG_ERROR('client can not load reCAPTCHA image')
            finally:
                if resp is not None:
                    resp.close()

        LOG_DEBUG('get image from web for %.02f seconds' % (time.time() - start))
        return (data, challenge)