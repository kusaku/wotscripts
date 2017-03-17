# Embedded file name: scripts/client/audio/debug.py
from config_consts import IS_DEVELOPMENT
from debug_utils import LOG_INFO
from audio.AKConsts import DEBUG_AUDIO_TAG
from DebugManager import SHOW_DEBUG_OBJ
IS_AUDIO_DEBUG = False

def enable():
    global IS_AUDIO_DEBUG
    IS_AUDIO_DEBUG = True and IS_DEVELOPMENT


def disable():
    global IS_AUDIO_DEBUG
    IS_AUDIO_DEBUG = False


def LOG_AUDIO(msg):
    LOG_INFO('%s %s' % (DEBUG_AUDIO_TAG, msg))