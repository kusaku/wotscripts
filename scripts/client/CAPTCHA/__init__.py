# Embedded file name: scripts/client/CAPTCHA/__init__.py
from CAPTCHA.CAPTCHABase import CAPTCHABase
from consts import CAPTCHA_API, CURRENT_CAPTCHA_API
SUPPORTED_CAPTCHA_APIS = {CAPTCHA_API.RE_CAPTCHA: ('CAPTCHA.reCAPTCHA', 'reCAPTCHA'),
 CAPTCHA_API.KONG: ('CAPTCHA.Kong', 'Kong')}

def _CAPTCHA_API_FACTORY():
    module, clazz = SUPPORTED_CAPTCHA_APIS.get(CURRENT_CAPTCHA_API, (None, None))
    if module is not None:
        imported = __import__(module, globals(), locals(), [clazz])
        return getattr(imported, clazz)
    else:
        return CAPTCHABase


CAPTCHA_API_CLASS = _CAPTCHA_API_FACTORY()