# Embedded file name: scripts/client/Helpers/BoolCombiner.py
from cStringIO import StringIO
from tokenize import generate_tokens
STRING = 1

class ParseException(Exception):
    pass


def parse(stringCondition):
    """
    Parse condition string
    >> parse("TEST, TEST2, test3, ~TEST3 | wer, werewr | ~ss")
    [[(True, 'TEST')], [(True, 'TEST2')], [(True, 'test3')], [(False, 'TEST3'), (True, 'wer')], [(True, 'werewr'), (False, 'ss')]]
    """
    tokens = list((token[STRING] for token in generate_tokens(StringIO(stringCondition).readline) if token[STRING]))
    tokens.append(',')
    andPart = list()
    orPart = list()
    stateSymbol = ','
    for token in tokens:
        if token == ',':
            if stateSymbol != 'S':
                raise ParseException, 'unexpected "," after {0}'.format(stateSymbol)
            andPart.append(orPart)
            orPart = list()
            stateSymbol = token
        elif token == '|':
            if stateSymbol != 'S':
                raise ParseException, 'unexpected "," after {0}'.format(stateSymbol)
            stateSymbol = token
        elif token == '~':
            if stateSymbol not in (',', '|'):
                raise ParseException, 'unexpected "~" after {0}'.format(stateSymbol)
            stateSymbol = token
        else:
            if stateSymbol not in (',', '|', '~'):
                raise ParseException, 'unexpected symbol "{0}"  after {1}'.format(token, stateSymbol)
            sumbolData = (stateSymbol != '~', token)
            if orPart is not None:
                orPart.append(sumbolData)
            stateSymbol = 'S'

    return andPart


def toString(conditions):
    step1 = [ ' | '.join(map(lambda (operator, symbol): ('{0}' if operator else '~{0}').format(symbol), orCondition)) for orCondition in conditions ]
    return ', '.join(step1)


class _SymbolData:

    def __init__(self):
        self.__calbacks = list()
        self.__value = False

    def addCallback(self, sign, callback):
        self.__calbacks.append((sign, callback))
        if self.__value == sign:
            callback(True)
            return True
        return False

    @property
    def used(self):
        return bool(self.__calbacks)

    @property
    def value(self):
        return self.__value

    def setValue(self, value):
        if value != self.__value:
            self.__value = value
            for sign, callback in self.__calbacks:
                callback(value == sign)

            return True
        return False


class _Part:

    def __init__(self, goal, onChangeCallback):
        self.__goal = goal
        self.__value = 0
        self.__onChangeCallback = onChangeCallback

    @property
    def state(self):
        return self.__value >= self.__goal

    def onSubPartChange(self, value):
        oldState = self.state
        self.__value += 1 if value else -1
        state = self.state
        if state != oldState and self.__onChangeCallback:
            self.__onChangeCallback(state)


class BoolCombiner:

    def __init__(self):
        self.__symbols = dict()

    def __mapSymbol(self, condition, onChangeCallback):
        """
        condition: (sign, symbolName)
        """
        symbol = condition[1]
        if symbol not in self.__symbols:
            symbolData = _SymbolData()
            self.__symbols[symbol] = symbolData
        else:
            symbolData = self.__symbols[symbol]
        return symbolData.addCallback(condition[0], onChangeCallback)

    def __mapOrPart(self, conditions, onChangeCallback):
        if len(conditions) == 1:
            return self.__mapSymbol(conditions[0], onChangeCallback)
        else:
            part = _Part(1, onChangeCallback)
            for condition in conditions:
                self.__mapSymbol(condition, part.onSubPartChange)

            return part.state

    def addObject(self, conditions, onChangeCallback):
        """
        conditions: [[(true,condition), (false,condition)], [] ]
        """
        value = True
        if len(conditions) == 1:
            value = self.__mapOrPart(conditions[0], onChangeCallback)
        elif len(conditions) == 0:
            onChangeCallback(True)
        else:
            part = _Part(len(conditions), onChangeCallback)
            for conditionPart in conditions:
                self.__mapOrPart(conditionPart, part.onSubPartChange)

            value = part.state
        if not value:
            onChangeCallback(False)

    def setCondition(self, symbol, isEnable):
        if symbol not in self.__symbols:
            self.__symbols[symbol] = _SymbolData()
        return self.__symbols[symbol].setValue(isEnable)

    def getCondition(self, symbol):
        return self.__symbols[symbol].value

    def hasSymbol(self, symbol):
        symbolData = self.__symbols.get(symbol, None)
        return symbolData is not None and symbolData.used

    @property
    def symbols(self):
        return filter(lambda symbol: self.__symbols[symbol].used, self.__symbols.iterkeys())