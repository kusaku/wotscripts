# Embedded file name: scripts/client/gui/Scaleform/daapi/view/component_override.py


class ComponentOverride(object):

    def __init__(self, default, override, check):
        super(ComponentOverride, self).__init__()
        self.__default = default if isinstance(default, ComponentOverride) else (lambda : default)
        self.__override = override if isinstance(override, ComponentOverride) else (lambda : override)
        self.__check = check

    def __call__(self):
        if self.__check():
            return self.__override()
        return self.__default()