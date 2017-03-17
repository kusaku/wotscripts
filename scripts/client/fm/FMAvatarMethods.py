# Embedded file name: scripts/client/fm/FMAvatarMethods.py


def fmEmpty(func):
    return func


def fmAvatarMethods(decorator):
    if decorator is None:
        decorator = fmEmpty

    def addFMAvatarMethods(objClass):

        class decorated(objClass):

            @decorator
            def fmData(self, data):
                pass

            @decorator
            def fmInit(self, ticksPerUpdate, position, rotation):
                pass

            @decorator
            def fmSync(self, frames):
                pass

            @decorator
            def fmDiff(self, data):
                pass

            @decorator
            def fmBinDataBegin(self):
                pass

            @decorator
            def fmBinData(self, data):
                pass

            @decorator
            def fmBinDataComplete(self):
                pass

        decorated.__name__ = objClass.__name__
        return decorated

    return addFMAvatarMethods