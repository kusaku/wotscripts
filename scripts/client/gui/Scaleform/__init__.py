# Embedded file name: scripts/client/gui/Scaleform/__init__.py
SCALEFORM_SUPPORT = False
try:
    import _Scaleform
    SCALEFORM_SUPPORT = True
except ImportError:
    raise NotImplementedError, 'Client not support Scaleform'

SCALEFORM_SWF_PATH = 'gui/flash'
SCALEFORM_STARTUP_VIDEO_PATH = 'video/Logo_All.usm'
SCALEFORM_FONT_LIB_PATH = 'gui/flash'
SCALEFORM_FONT_CONFIG_FILE = 'fontconfig.xml'
SCALEFORM_FONT_CONFIG_PATH = 'gui/flash/%s' % SCALEFORM_FONT_CONFIG_FILE
SCALEFORM_DEFAULT_CONFIG_NAME = 'All'