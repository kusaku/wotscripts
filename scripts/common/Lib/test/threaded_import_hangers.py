# Embedded file name: scripts/common/Lib/test/threaded_import_hangers.py
TIMEOUT = 10
import threading
import tempfile
import os.path
errors = []

class Worker(threading.Thread):

    def __init__(self, function, args):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args

    def run(self):
        self.function(*self.args)


for name, func, args in [('tempfile.TemporaryFile', tempfile.TemporaryFile, ()), ('os.path.abspath', os.path.abspath, ('.',))]:
    t = Worker(func, args)
    t.start()
    t.join(TIMEOUT)
    if t.is_alive():
        errors.append('%s appeared to hang' % name)