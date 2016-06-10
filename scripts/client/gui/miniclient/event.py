# Embedded file name: scripts/client/gui/miniclient/event.py
from helpers import aop

class _ParametrizeInitAspect(aop.Aspect):

    def atCall(self, cd):
        cd.avoid()
        return False


class InitEventPointcut(aop.Pointcut):

    def __init__(self):
        aop.Pointcut.__init__(self, 'gui.server_events.EventsCache', 'g_eventsCache', 'isEventEnabled', aspects=(_ParametrizeInitAspect,))