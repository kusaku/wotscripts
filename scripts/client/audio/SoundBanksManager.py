# Embedded file name: scripts/client/audio/SoundBanksManager.py
import WWISE_
g_soundBanksManager = None

class SoundBanksManager:
    PREPARATION_LOAD = True
    PREPARATION_UNLOAD = False
    TYPE_BANK = None
    TYPE_EVENT = None

    def __init__(self):
        SoundBanksManager.TYPE_BANK = WWISE_.TYPE_BANK()
        SoundBanksManager.TYPE_EVENT = WWISE_.TYPE_EVENT()

    @staticmethod
    def instance():
        global g_soundBanksManager
        if not g_soundBanksManager:
            g_soundBanksManager = SoundBanksManager()
        return g_soundBanksManager

    def loadInitBank(self, bankName):
        """
        Load wwise sound bank directly by name
        @type bankName: str
        @param bankName: name of loading bank
        """
        WWISE_.loadInitBank(bankName)

    def loadBank(self, bankName):
        """
        Load wwise init bank, which contains metadata (events and structures info without media content)
        Similar to loadBank function, but additionaly sets "init" flag for prepareEvent usage
        
        @type bankName: str
        @param bankName: name of loading bank
        """
        WWISE_.loadBank(bankName)

    def unloadBank(self, bankName):
        """
        Unload wwise sound bank directly by name
        @type bankName: str
        @param bankName: name of unloading bank
        """
        WWISE_.unloadBank(bankName)

    def prepareEvent(self, eventName, preparationType):
        """
        Prepare event content by event name
        
        @type eventName: str
        @param eventName: preparing event name
        @type preparationType: bool
        @param eventName: PREPARATION_LOAD or PREPARATION_UNLOAD
        """
        WWISE_.prepareEvent(eventName, preparationType)

    def attachWwiseObjectToCase(self, wwiseObjectName, soundCaseID):
        """
        Attaches wwise object (bank, event, game sync) for specific case (hangar, arena)
        
        @type wwiseObjectName: str
        @param wwiseObjectName: name of wwise bank or event
        @type soundCaseID: int
        @param soundCaseID: user defined category of specified object
        """
        WWISE_.attachWwiseObjectToCase(wwiseObjectName, soundCaseID)

    def unloadSoundCase(self, soundCaseID):
        """
        Anload all wwise resources for selected sound case
        
        @type soundCaseID: int
        @param soundCaseID: user defined category which must be unloaded
        """
        WWISE_.unloadSoundCase(soundCaseID)

    def loadFilePackage(self, packageName):
        """
        Load initialization table of specific package
        
        @type packageName: string
        @param packageName: wwise package name
        """
        WWISE_.loadFilePackage(packageName)

    def unloadFilePackage(self, packageName):
        """
        Unload initialization table of specific package
        
        @type packageName: string
        @param packageName: wwise package name
        """
        WWISE_.unloadFilePackage(packageName)

    def unloadAllFilePackages(self):
        """
        Unload initialization tables of all previously loaded packages
        """
        WWISE_.unloadAllFilePackages()