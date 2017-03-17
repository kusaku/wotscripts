# Embedded file name: scripts/common/db/DBChecker.py
import sys, os
sys.path.append(os.path.abspath('./../../server_common'))
sys.path.append(os.path.abspath('./../../common'))
sys.path.append(os.path.abspath('./../../surrogates'))
import config_consts
config_consts.DB_ENABLE_LOG = True
config_consts.DB_AIRCRAFT_CHECK = True
import time

class DBError(Exception):
    pass


def validate(bundle):
    ERROR_PREFIX = ('ERROR_DB', 'ERROR', 'CRITICAL_ERROR')
    WARNING_PREFIX = ('WARNING',)
    old_out = sys.stdout

    class CustomOut(object):

        def write(self, s, *args, **kw):
            if s.startswith(ERROR_PREFIX + (WARNING_PREFIX if not bundle else ())):
                bundleStop = s.find(':bundleStop:') != -1
                if bundleStop:
                    s.replace(':bundleStop:', ':')
                if not bundle:
                    old_out.write((s + '\n'), *args, **kw)
                elif bundleStop:
                    raise DBError, s

    sys.stdout = CustomOut()
    t = time.time()
    from db.DBLogic import initDB
    initDB()
    sys.stdout = old_out
    print '\n\nDB checked, seconds: %d' % int(time.time() - t)


if __name__ == '__main__':
    validate('--bundle' in sys.argv[1:])