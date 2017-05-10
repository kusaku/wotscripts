# Embedded file name: scripts/client/Vibroeffects/Controllers/OnceController.py
from Vibroeffects import VibroManager

class OnceController:

    def __init__(self, effectName, gain = 100):
        VibroManager.g_instance.launchQuickEffect(effectName, 1, gain)