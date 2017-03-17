# Embedded file name: scripts/common/db/DiffTool.py
PATH_SEPARATOR = '/'
VALUE_TYPES = (int,
 float,
 basestring,
 bool,
 long)

class _EditValue:

    @staticmethod
    def apply(targetObject, diff, test):
        """
        Applies diff
        @param targetObject:
        @param diff:
        @param test:
        """
        currObj = targetObject
        path = diff[1].split(PATH_SEPARATOR)
        for k, v in enumerate(path):
            isLast = k == len(path) - 1
            if v.isdigit():
                if not isinstance(currObj, list) or int(v) >= len(currObj):
                    return False
                if isLast:
                    if not test:
                        currObj[int(v)] = diff[0]
                else:
                    currObj = currObj[int(v)]
            else:
                if not hasattr(currObj, v):
                    return False
                if isLast:
                    if not test:
                        setattr(currObj, v, diff[0])
                else:
                    currObj = currObj.__dict__[v]

        return True


def _generateDiff(newObject, oldObject, diff, path, diffObjectType, logger):
    if isinstance(newObject, list):
        for k, v in enumerate(newObject):
            p = path + '%s%s' % (PATH_SEPARATOR, str(k)) if path else str(k)
            if k < len(oldObject):
                _generateDiff(v, oldObject[k], diff, p, diffObjectType, logger)
            elif logger is not None:
                logger('[DiffTool] Objects structure differs. Skipping path = "{0}"'.format(p))

    elif isinstance(newObject, diffObjectType):
        for k, v in newObject.__dict__.iteritems():
            p = path + '%s%s' % (PATH_SEPARATOR, str(k)) if path else str(k)
            if hasattr(oldObject, k):
                _generateDiff(v, oldObject.__dict__[k], diff, p, diffObjectType, logger)
            elif logger is not None:
                logger('[DiffTool] Objects structure differs. Skipping path = "{0}"'.format(p))

    elif isinstance(newObject, VALUE_TYPES):
        if oldObject != newObject:
            diff.append((newObject, path))
    elif logger is not None:
        logger('[DiffTool] Skipping unhandled type at path = "{0}"'.format(path))
    return


def generateDiff(newObject, oldObject, diffObjectType, logger = None):
    """
    Generates diff. Work up only public fields and objects structure should be the same
    @param newObject:
    @param oldObject:
    @param diffObjectType: class-or-type-or-tuple
    @param logger: type logger(<string>)
    @return: diff
    @rtype: list
    """
    diff = []
    _generateDiff(newObject, oldObject, diff, '', diffObjectType, logger)
    return diff


def applyDiff(targetObject, diff, logger = None):
    """
    Applies diff to object
    @param targetObject:
    @param diff:
    @param logger: type logger(<string>)
    """
    for d in diff:
        _EditValue.apply(targetObject, d, False)


def cleanupDiff(targetObject, sourceDiff):
    """
    Creates diff from sourceDiff that contains only records that can be applied to the target object.
    @param targetObject:
    @param sourceDiff:
    """
    res = []
    for d in sourceDiff:
        if _EditValue.apply(targetObject, d, True):
            res.append(d)

    return res


def iterAffectedChildDBObjects(dbObject, diff):
    """
    @param dbObject:
    @param diff:
    """
    for val, path in diff:
        attr = dbObject
        attrName = None
        for i in path.split(PATH_SEPARATOR):
            if i.isdigit():
                yield (attrName, attr[int(i)])
                break
            else:
                attrName, attr = i, getattr(attr, i)

    return