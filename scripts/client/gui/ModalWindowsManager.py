# Embedded file name: scripts/client/gui/ModalWindowsManager.py
from Singleton import singleton

@singleton

class ModalWindowsManager(object):

    def __init__(self):
        self.__modalWindows = []

    def add(self, modalWindow):
        if modalWindow not in self.__modalWindows:
            self.__modalWindows.append(modalWindow)

    def remove(self, modalWindow):
        if modalWindow in self.__modalWindows:
            self.__modalWindows.remove(modalWindow)

    def destroy(self):
        for modalWindow in self.__modalWindows:
            modalWindow.close()

    def handleAxisEvent(self, event):
        for modalWindow in reversed(self.__modalWindows):
            result = modalWindow.handleAxisEvent(event)
            if result:
                return result

        return False

    def handleKeyEvent(self, event):
        for modalWindow in reversed(self.__modalWindows):
            result = modalWindow.handleKeyEvent(event)
            if result:
                return result

        return False

    def handleMouseEvent(self, event):
        for modalWindow in reversed(self.__modalWindows):
            result = modalWindow.handleMouseEvent(modalWindow, event)
            if result:
                return result

        return False