# Embedded file name: scripts/client/audio/InteractiveMix/InteractiveMixHandler.py
from GamePhases import GamePhases

class InteractiveMixTypes:
    GAME_PHASE = 0


class InteractiveMixHandler:
    GAME_PHASES = 'GamePhases'

    def __init__(self):
        self.__features = {}
        self.create()

    def push(self, id, feature):
        self.__features[id] = feature

    def get(self, name):
        return self.__features[id]

    def create(self):
        self.push(InteractiveMixTypes.GAME_PHASE, GamePhases())