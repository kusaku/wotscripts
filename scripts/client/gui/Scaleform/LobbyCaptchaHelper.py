# Embedded file name: scripts/client/gui/Scaleform/LobbyCaptchaHelper.py
import time
import threading
from Helpers.i18n import localizeCAPTCHA
from OperationCodes import OPERATION_RETURN_CODE
import BigWorld
from CAPTCHA import CAPTCHA_API_CLASS
from clientConsts import CAPTCHA_WAITING_SCREEN_MESSAGE
from debug_utils import LOG_DEBUG, LOG_CURRENT_EXCEPTION, LOG_ERROR
from gui.Scaleform.Waiting import Waiting
from functools import partial
CAPTCHA_IMAGE_NAME = 'captcha-cache-%s'
CAPTCHA_IMAGE_URL = 'img://' + CAPTCHA_IMAGE_NAME
CAPTCHA_CAPTION = 'gui/labels/recaptcha_instructions_image'
CAPTCHA_SUBMIT_BTN = 'gui/buttons/submit'
CAPTCHA_RELOAD_BTN = 'gui/buttons/reload'
CAPTCHA_ATTEMPTS_LEFT = 'notification/remains-to-attempt'

class _CaptchaImageWorker(threading.Thread):

    def __init__(self, captchaMgr, callback):
        """
        @type captchaMgr: LobbyCaptchaHelper
        
        """
        super(_CaptchaImageWorker, self).__init__()
        self.captchaMgr = captchaMgr
        self.callback = callback

    def __del__(self):
        LOG_DEBUG('CaptchaImageWorker deleted')

    def run(self):
        if self.captchaMgr is None:
            return
        else:
            try:
                image, challenge = self.captchaMgr.api.getImageSource(self.captchaMgr.getPublicKey(), self.captchaMgr.getCaptchaRegex())
                if not image or not challenge:
                    BigWorld.callback(0.1, lambda : self.callback(None))
                    self.captchaMgr = None
                    return
                imageID = CAPTCHA_IMAGE_NAME % self.captchaMgr.generateImageID()
                BigWorld.wg_addTempScaleformTexture(imageID, image)
            except AttributeError:
                LOG_CURRENT_EXCEPTION()
                challenge = None

            BigWorld.callback(0.1, lambda : self.callback(challenge))
            self.captchaMgr = None
            return


class LobbyCaptchaHelper(object):

    def __init__(self, lobby):
        self.__lobby = lobby
        self.api = CAPTCHA_API_CLASS()
        self.__challenge = None
        self.__imageID = 0
        self.__captchaTriesLeft = None
        self.__battlesTillCaptcha = None
        self.__publicKey = None
        self.__captchaRegex = ''
        self.__captchaWaitingID = None
        return

    def registerCallbacks(self):
        """
        Register callbacks
        """
        self.__lobby.addExternalCallbacks({'captcha.initialized': self.__onInitialized,
         'captcha.submitText': self.__onEnterCaptchaResponse,
         'captcha.reloadCaptcha': self.__reloadCaptcha})

    def updateDataRequest(self, onDataReceivedCallback = None):
        """
        Update captcha data from server
        @param onDataReceivedCallback: callback when data is received. type delegate(isSuccess)
        """
        waitingID = Waiting.show(CAPTCHA_WAITING_SCREEN_MESSAGE)

        def onResponse(waitingID, operation, returnCode, publicKey = None, captchaTriesLeft = None, battlesTillCaptcha = None):
            if returnCode == OPERATION_RETURN_CODE.SUCCESS:
                self.__publicKey = publicKey
                self.__captchaTriesLeft = captchaTriesLeft
                self.__battlesTillCaptcha = battlesTillCaptcha
                if onDataReceivedCallback is not None:
                    onDataReceivedCallback(True)
            else:
                LOG_ERROR('Unable to retrieve CAPTCHA data from server')
                if onDataReceivedCallback is not None:
                    onDataReceivedCallback(False)
            Waiting.hide(waitingID)
            return

        self.__lobby.getPlayer().accountCmd.getCaptchaData(partial(onResponse, waitingID))
        return

    def generateImageID(self):
        self.__imageID = int(time.time())
        return self.__imageID

    def showCaptcha(self):
        if self.__captchaWaitingID is not None:
            Waiting.hide(self.__captchaWaitingID)
            self.__captchaWaitingID = None
        self.__captchaWaitingID = Waiting.show(CAPTCHA_WAITING_SCREEN_MESSAGE)
        self.__lobby.call_1('hangar.showCaptcha')
        return

    def getPublicKey(self):
        return self.__publicKey

    def getCaptchaRegex(self):
        return self.__captchaRegex

    def __onImageReceived(self, challenge):
        self.__challenge = challenge
        if challenge:
            width, height = self.api._IMAGE_SIZE
            self.__lobby.call_1('captcha.SetImageUrl', CAPTCHA_IMAGE_URL % self.__imageID, width, height)
        Waiting.hide(self.__captchaWaitingID)
        self.__captchaWaitingID = None
        return

    def __onInitialized(self):
        self.__lobby.call_1('captcha.SetMsg', localizeCAPTCHA(CAPTCHA_CAPTION))
        self.__lobby.call_1('captcha.SetNameSubmit', localizeCAPTCHA(CAPTCHA_SUBMIT_BTN))
        self.__lobby.call_1('captcha.SetNameReload', localizeCAPTCHA(CAPTCHA_RELOAD_BTN))
        _CaptchaImageWorker(self, self.__onImageReceived).start()

    def __onEnterCaptchaResponse(self, response):
        """
        @type response: string
        """
        if not self.__challenge:
            return
        else:
            response = response.strip()
            if not response:
                return

            def onResponse(operation, returnCode, captchaTriesLeft, errorCode = None):
                self.__captchaTriesLeft = int(captchaTriesLeft)
                if returnCode == OPERATION_RETURN_CODE.SUCCESS:
                    self.__setCaptchaVerified()
                else:
                    self.__lobby.call_1('captcha.SetAttempts', localizeCAPTCHA(CAPTCHA_ATTEMPTS_LEFT) % self.__captchaTriesLeft)
                    if self.__captchaTriesLeft > 0:
                        self.__reloadCaptcha()
                    self.__setCaptchaServerError(errorCode)

            self.__lobby.getPlayer().accountCmd.verifyCaptcha(self.__challenge, response, onResponse)
            return

    def __setCaptchaVerified(self):
        self.__lobby.call_1('hangar.hideCaptcha')

    def __reloadCaptcha(self):
        if self.__captchaWaitingID is not None:
            Waiting.hide(self.__captchaWaitingID)
            self.__captchaWaitingID = None
        self.__captchaWaitingID = Waiting.show(CAPTCHA_WAITING_SCREEN_MESSAGE)
        _CaptchaImageWorker(self, self.__onImageReceived).start()
        return

    def __setCaptchaServerError(self, errorCode):
        pass

    def isCaptchaRequired(self):
        return self.__battlesTillCaptcha <= 0

    def destroy(self):
        self.__lobby = None
        self.api = None
        return