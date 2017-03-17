# Embedded file name: scripts/client/ProfileDiffer.py
import ResMgr
from bwdebug import *
from gui.Scaleform.GameOptions.vo import MarkerSettings

class SectionsDiffer(object):

    def __init__(self, default, actual):
        """
        @param default: DataSection
        @param actual: DataSection
        """
        self._default = default
        self._actual = actual
        self._isDiff = False

    def destroy(self):
        self._default = None
        self._actual = None
        return

    def applyDiff(self):
        if self._default is not None and self._actual is not None:
            self._fillDiff(self._default, self._actual)
            if self._isDiff:
                self._isDiff = False
                try:
                    self._actual.save()
                except IOError as e:
                    ERROR_MSG(e)
                finally:
                    self.destroy()

            else:
                self.destroy()
        return

    def _fillDiff(self, default, actual):
        self._deleteOldSections(default, actual)
        self._createNewSection(default, actual)

    def _createNewSection(self, default, actual):
        for key in default.keys():
            defaultDs = getDataSectionNodeByName(default, key)
            if not actual.has_key(key):
                actual.createSection(key).copy(defaultDs)
                self._isDiff = True
            elif len(defaultDs.keys()):
                actualDs = getDataSectionNodeByName(actual, key)
                self._createNewSection(defaultDs, actualDs)
            else:
                self._checkAttribute(actual, key, defaultDs)

    def _deleteOldSections(self, default, actual):
        for key in actual.keys():
            if not default.has_key(key):
                actual.deleteSection(key)
                self._isDiff = True
            else:
                defaultDs = getDataSectionNodeByName(default, key)
                if defaultDs is not None and len(defaultDs.keys()):
                    actualDs = getDataSectionNodeByName(actual, key)
                    self._deleteOldSections(defaultDs, actualDs)

        return

    def _checkAttribute(self, actual, key, defaultDs):
        pass


class MarkerSectionsDiffer(SectionsDiffer):

    def _checkAttribute(self, actual, key, defaultDs):
        SectionsDiffer._checkAttribute(self, actual, key, defaultDs)
        if key == 'version':
            self._isDiff = True
            actual.writeInt(key, defaultDs.asInt)
        elif key in MarkerSettings.AVAILABLE_MARKER_PROPERTIES:
            defaultValue = str(defaultDs.asString).split(',')
            actualValue = str(actual.readString(key)).split(',')
            if len(defaultValue) > len(actualValue):
                actualValue.extend(defaultValue[len(defaultValue) - len(actualValue) - 1:])
                actual.writeString(key, ','.join([ str(v) for v in actualValue ]))
                self._isDiff = True


def getDataSectionNodeByName(res, name):
    """
    @param res: DataSection
    @param name: str
    @return: DataSection or None
    """
    for x in res.values():
        if x.name == name:
            return x

    return None


class ProfileDiffer:

    def __init__(self, default, actual):
        self.__defaultProfile = default
        self.__actualProfile = actual

    def getDiff(self):
        return self.__getDiff(self.__actualProfile, self.__defaultProfile)

    def applyDiff(self, diff):
        for key in diff.keys():
            if self.__actualProfile.has_key(key):
                if self.__isArrayOfPoints(diff[key]) or self.__isSimpleNode(diff[key]):
                    self.__actualProfile[key].copy(diff[key])
                else:
                    self.__applyDiffToSubKey(diff[key], self.__actualProfile[key])

        try:
            self.__actualProfile.save()
        except IOError as e:
            ERROR_MSG(e)

    def __applyDiffToSubKey(self, diff, actual):
        for key in diff.keys():
            if actual.has_key(key):
                diff_val = diff[key]
                if self.__isArrayOfPoints(diff_val) or self.__isSimpleNode(diff_val) or self.__isFireKeys(diff_val):
                    actual[key].copy(diff_val)
                else:
                    self.__applyDiffToSubKey(diff[key], actual[key])

    def __getDiff(self, source, target):
        if source == None or target == None:
            return
        else:
            ResMgr.purge(source.name + '.diff')
            diff = ResMgr.openSection(source.name + '.diff', True)
            for key in source.keys():
                if not self.__fillDiff(source[key], target[key], diff, key):
                    diff.deleteSection(key)

            return diff

    def __fillDiff(self, source, target, diff, key):
        if source == None or target == None:
            return False
        elif self.__isArrayOfPoints(source):
            if not self.__isEqualArrayOfPoints(source, target):
                diff.createSection(key).copy(source)
                return True
            return False
        elif self.__isFireKeys(source):
            if not self.__isEqualFireKeys(source, target):
                diff.createSection(key).copy(source)
                return True
            return False
        else:
            if self.__isSimpleNode(source):
                if source.asString == target.asString:
                    return False
                else:
                    diff.createSection(key).copy(source)
                    return True
            else:
                ret = False
                diff = diff.createSection(key)
                for k, v in source.items():
                    if not self.__fillDiff(v, target[k], diff, k):
                        diff.deleteSection(k)
                    else:
                        ret = True

                return ret
            return

    def __isSimpleNode(self, ds):
        return len(ds) == 0

    def __isArrayOfPoints(self, ds):
        if ds is not None:
            return ds.has_key('pointCount')
        else:
            return False

    def __isEqualArrayOfPoints(self, source, target):
        if source['pointCount'].asInt != target['pointCount'].asInt:
            return False
        sourcePoints = source.readStrings('p')
        targetPoints = target.readStrings('p')
        if sourcePoints != targetPoints:
            return False
        return True

    def __isFireKeys(self, ds):
        return str(ds.name).upper() == 'FIRE_KEYS'

    def __isEqualFireKeys(self, source, target):
        s_items = source.values()
        t_items = target.values()
        if len(s_items) != len(t_items):
            return False
        for i in range(0, len(s_items)):
            if not self.__isEqualDS(s_items[i], t_items[i]):
                return False

        return True

    def __isEqualDS(self, source, target):
        if source.name != target.name:
            return False
        else:
            s_items = source.values()
            t_items = target.values()
            if s_items is None and t_items is None or len(s_items) == 0 and len(t_items) == 0:
                return source.asString == target.asString
            if len(s_items) != len(t_items):
                return False
            for i in range(0, len(s_items)):
                if not self.__isEqualDS(s_items[i], t_items[i]):
                    return False

            return True