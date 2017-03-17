# Embedded file name: scripts/service/TWResources/KeepAliveMailboxes.py
import BigWorld
import logging
TIMEOUT_PERIOD = 600
CHECK_PERIOD = 20

class KeepAliveCache(object):

    def __init__(self, mailbox):
        self.mailbox = mailbox
        self.updateTimestamp()

    def updateTimestamp(self):
        self.lastTime = BigWorld.time()

    def isOlderThan(self, time):
        return self.lastTime < time

    def pingEntity(self):
        self.mailbox.webKeepAlivePing()


caches = {}

def add(entityType, dbID, mailbox):
    key = (entityType, str(dbID))
    if hasattr(mailbox, 'webKeepAlivePing'):
        caches[key] = KeepAliveCache(mailbox)
    else:
        logging.error('Not caching %s', mailbox)


def get(entityType, dbID):
    cache = caches.get((entityType, str(dbID)), None)
    if not cache:
        return
    else:
        cache.updateTimestamp()
        return cache.mailbox


def tick(timerID, userArg):
    thresholdTime = BigWorld.time() - TIMEOUT_PERIOD
    for key, cache in caches.items():
        if cache.isOlderThan(thresholdTime):
            logging.info('KeepAliveMailboxes.tick: %s is gone', key)
            del caches[key]
        else:
            cache.pingEntity()


BigWorld.addTimer(tick, 0, CHECK_PERIOD)