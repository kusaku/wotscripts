# Embedded file name: scripts/client/gui/HangarScripts/NewYearHangarScript.py
from HangarScriptBase import HangarScriptBase
import BigWorld
from functools import partial
from random import randint, choice
import EffectManager
from db.DBEffects import Effects

class NewYearHangarScript(HangarScriptBase):
    TIMELINES = []

    def __init__(self):
        super(NewYearHangarScript, self).__init__()
        self._effectsActive = False
        l = len(self.TIMELINES)
        if not l:
            raise Exception('TIMELINES should not be empty')
        self.__timers = [0] * l
        self.__callbacks = [0] * l

    def onHangarLoaded(self):
        EffectManager.Init()

    def _startEffects(self):
        if self._effectsActive:
            return
        self._effectsActive = True
        for i, timeline in enumerate(self.TIMELINES):
            self.__timers[i] = 0
            t = timeline['TIMERS'][0]
            self.__callbacks[i] = BigWorld.callback(randint(t[0], t[1]), partial(self.__onTimer, i))

    def onHangarUnloaded(self):
        self._stopEffects()

    def _stopEffects(self):
        if not self._effectsActive:
            return
        else:
            self._effectsActive = False
            for k, callback in enumerate(self.__callbacks):
                BigWorld.cancelCallback(callback)
                self.__callbacks[k] = None

            return

    def __onTimer(self, lineIndex):
        timeline = self.TIMELINES[lineIndex]
        particle = choice(timeline['PARTICLES'])
        pos = choice(timeline['POSITIONS'])
        linetimers = timeline['TIMERS']
        if EffectManager.g_instance:
            EffectManager.g_instance.createWorldEffect(Effects.getEffectId(particle), pos, {})
        self.__timers[lineIndex] += 1
        if self.__timers[lineIndex] >= len(linetimers):
            self.__timers[lineIndex] = 0
        t = linetimers[self.__timers[lineIndex]]
        self.__callbacks[lineIndex] = BigWorld.callback(randint(t[0], t[1]), partial(self.__onTimer, lineIndex))