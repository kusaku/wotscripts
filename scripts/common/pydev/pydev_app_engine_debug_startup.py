# Embedded file name: scripts/common/pydev/pydev_app_engine_debug_startup.py
if False:
    config = None
if ':' not in config.version_id:
    import json
    import os
    import sys
    startup = config.python_config.startup_args
    if not startup:
        raise AssertionError('Expected --python_startup_args to be passed from the pydev debugger.')
    setup = json.loads(startup)
    pydevd_path = setup['pydevd']
    sys.path.append(os.path.dirname(pydevd_path))
    import pydevd
    pydevd.settrace(setup['client'], port=setup['port'], suspend=False, trace_only_current_thread=False)