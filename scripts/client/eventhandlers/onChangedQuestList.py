# Embedded file name: scripts/client/eventhandlers/onChangedQuestList.py
from consts import EMPTY_IDTYPELIST

def onChangedQuestList(event):
    if event.ob != event.prevob and event.idTypeList == EMPTY_IDTYPELIST:
        try:
            from BWPersonality import g_lobbyCarouselHelper as lch
            lch.invalidateQuestList()
        except ImportError:
            pass