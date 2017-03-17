# Embedded file name: scripts/client/account_helpers/__init__.py
import BigWorld
import consts
import clientConsts
import datetime

def isPremiumAccount(attrs):
    return attrs is not None and attrs & consts.ACCOUNT_ATTR.PREMIUM != 0


def getPremiumExpiryDelta(expiryTime):
    check = datetime.datetime.utcfromtimestamp(expiryTime)
    now = datetime.datetime.utcnow()
    return check - now


def isDemonstrator(attrs):
    return attrs is not None and attrs & consts.ACCOUNT_ATTR.ARENA_CHANGE != 0


def convertGold(gold):
    return gold