# Embedded file name: scripts/client/gui/HangarScripts/HangarNY2016Script.py
import time
import BigWorld
import EffectManager
from db.DBEffects import Effects
from gui.HangarScripts import Hangar5Script
from audio import GameSound
from adapters.IHangarSpacesAdapter import getHangarSpaceByID

class HangarNY2016Script(Hangar5Script):
    _FIREWORKS_START = time.mktime((2015, 12, 30, 22, 0, 0, 0, 0, 0))
    _FIREWORKS_END = time.mktime((2016, 1, 11, 22, 0, 0, 0, 0, 0))
    _SWITCH_TIME_2016 = time.mktime((2015, 12, 31, 22, 0, 0, 0, 0, 0))
    _FIREWORKS_MUSIC = 'NY2015Theme4'
    _WITHOUT_FIREWORKS_MUSIC = 'NY2015Theme2'
    _FIREWORKS_AMBIENT = 2
    _WITHOUT_FIREWORKS_AMBIENT = 1
    _LABEL_POS = (0.29, 2.817, -9.864)
    _CHECK_TIME = 10
    _REINIT_TIME = 1
    _LABEL_ID_2015 = 'NY_TEXT_2015'
    _LABEL_ID_2016 = 'NY_TEXT_2016'

    def __init__(self):
        super(HangarNY2016Script, self).__init__()
        self._yearLabel = None
        self._activationCB = None
        self._switchedTo2016 = False
        return

    def onHangarLoaded(self):
        Hangar5Script.onHangarLoaded(self)
        import BWPersonality
        self._hangarSpace = getHangarSpaceByID(BWPersonality.g_settings.hangarSpaceSettings['spaceID'])
        self._checkActivation()

    def _checkActivation(self):
        from Account import PlayerAccount
        player = BigWorld.player()
        if not player or player.__class__ != PlayerAccount or self._hangarSpace is None:
            self._createLabel(self._LABEL_ID_2015)
            self._activationCB = BigWorld.callback(self._REINIT_TIME, self._checkActivation)
            return
        else:
            cmpTime = time.time() + time.timezone - player.deltaTimeClientServer
            if cmpTime >= self._FIREWORKS_START and cmpTime <= self._FIREWORKS_END:
                self._startEffects()
                self._changeSound(self._FIREWORKS_AMBIENT, self._FIREWORKS_MUSIC)
            elif cmpTime < self._FIREWORKS_START or cmpTime > self._FIREWORKS_END:
                self._stopEffects()
                self._changeSound(self._WITHOUT_FIREWORKS_AMBIENT, self._WITHOUT_FIREWORKS_MUSIC)
            if cmpTime < self._SWITCH_TIME_2016:
                self._createLabel(self._LABEL_ID_2015)
            elif cmpTime >= self._SWITCH_TIME_2016 and not self._switchedTo2016:
                self._switchedTo2016 = True
                self._removeLabel()
                self._createLabel(self._LABEL_ID_2016)
            self._activationCB = BigWorld.callback(self._CHECK_TIME, self._checkActivation)
            return

    def _removeLabel(self):
        if self._yearLabel is not None:
            for effect in self._yearLabel:
                effect.destroy()

            EffectManager.g_instance.clearParticlesCache()
            self._yearLabel = None
        return

    def _createLabel(self, labelID):
        if self._yearLabel is None:
            self._yearLabel = EffectManager.g_instance.createWorldEffect(Effects.getEffectId(labelID), self._LABEL_POS, {})
        return

    def _changeSound(self, ambient, music):
        _rtpc = self._hangarSpace.get('ambient', {}).get('rtpc', None)
        _music = self._hangarSpace.get('music', None)
        if _rtpc is not None and _music is not None and (_rtpc['value'] != ambient or _music['play'] != music):
            _rtpc['value'] = ambient
            _music['play'] = music
            GameSound().music.stopHangar()
            GameSound().music.start()
        return

    def onHangarUnloaded(self):
        self._removeLabel()
        if self._activationCB is not None:
            BigWorld.cancelCallback(self._activationCB)
            self._activationCB = None
        self._switchedTo2016 = False
        self._hangarSpace = None
        Hangar5Script.onHangarUnloaded(self)
        return