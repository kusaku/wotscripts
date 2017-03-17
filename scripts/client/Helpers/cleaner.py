# Embedded file name: scripts/client/Helpers/cleaner.py
from debug_utils import LOG_TRACE, LOG_WARNING, LOG_ERROR
import time
import os
from wofdecorators import noexcept

@noexcept
def deleteOldFiles(dirPath, days, ext):
    if os.path.exists(dirPath):
        allFiles = [ os.path.join(dirPath, f) for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f)) and f.endswith(ext) ]
        for t, f in [ (time.time() - os.path.getmtime(f), f) for f in allFiles ]:
            if int(t / 86400) >= days:
                LOG_TRACE('File to remove: %s' % f)
                try:
                    os.remove(f)
                except OSError as e:
                    LOG_WARNING('deleteOldFiles (%s) - %s' % (ext, e.strerror))

    else:
        LOG_WARNING('deleteOldFiles (%s) - directory is not exists: %s' % (ext, dirPath))