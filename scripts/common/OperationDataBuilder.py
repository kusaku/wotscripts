# Embedded file name: scripts/common/OperationDataBuilder.py
from functools import partial

class OperationBuilderException(Exception):
    """
    Just custom exception class to separate builder's errors from other exceptions
    """
    pass


class OperationDataBuilderMeta(type):
    """
    Metaclass for OperationDataBuilder. Used to implement flexible static initializer
    """

    def __getattr__(self, operationType):

        def initOperation(operationType, **kwargs):
            return OperationDataBuilder(operationType, **kwargs)

        return partial(initOperation, operationType)


class OperationDataBuilder(object):
    """
    Helper class to build operations data for transactions.
    Details: https://confluence.wargaming.net/pages/viewpage.action?pageId=169013657
    
    @DynamicAttrs
    """
    __metaclass__ = OperationDataBuilderMeta

    @staticmethod
    def __preProcessIdType(itemType, itemID):
        if not itemType.endswith('ID'):
            raise OperationBuilderException('Wrong argument format: {0}. Please, check the ID ending?'.format(itemType))
        itemType = itemType[:-2]
        if not len(itemType):
            raise OperationBuilderException('Wrong argument format. Item type cannot be empty.')
        if not (isinstance(itemID, int) or itemID is None):
            raise OperationBuilderException('Wrong value passed. Item ID must be either int or None.')
        return (itemID, itemType)

    def __init__(self, operationType, **kwargs):
        super(OperationDataBuilder, self).__init__()
        count = kwargs.pop('count', 1)
        if not isinstance(count, int):
            raise OperationBuilderException('Wrong value passed. Count must be int.')
        if len(kwargs) > 1:
            raise OperationBuilderException('Too many arguments passed, 2 expected, got {0}'.format(len(kwargs)))
        itemID, itemType = self.__preProcessIdType(*kwargs.items()[0])
        self.__operationDict = {'type': operationType,
         'idTypeList': [[itemID, itemType]],
         'count': count}

    def __appendIdType(self, **kwargs):
        if len(kwargs) > 1:
            raise OperationBuilderException('Too many arguments passed, 1 expected, got {0}'.format(len(kwargs)))
        itemID, itemType = self.__preProcessIdType(*kwargs.items()[0])
        self.__operationDict['idTypeList'].append([itemID, itemType])
        return self

    def for_(self, **kwargs):
        return self.__appendIdType(**kwargs)

    def from_(self, **kwargs):
        return self.__appendIdType(**kwargs)

    def to(self, **kwargs):
        return self.__appendIdType(**kwargs)

    def specify(self, **kwargs):
        self.__operationDict.setdefault('kwargs', {}).update(kwargs)
        return self

    def build(self):
        return self.__operationDict