# Embedded file name: scripts/common/SubscribedConditions.py


class SubscribedConditions(object):

    def __init__(self):
        self.__subscriptions = {}
        self.__lastID = 0

    def addSubscription(self, conditionF, callback):
        self.__lastID += 1
        self.__subscriptions[self.__lastID] = (conditionF, callback)

    def delSubscription(self, subscriptionID):
        self.__subscriptions.pop(subscriptionID, None)
        return

    def update1sec(self):
        for s_id, p in self.__subscriptions.items():
            condition_f, callback = p
            if condition_f():
                del self.__subscriptions[s_id]
                callback()

    def destroy(self):
        self.__subscriptions = None
        return