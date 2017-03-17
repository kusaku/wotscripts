# Embedded file name: scripts/common/Lib/test/subprocessdata/sigchild_ignore.py
import signal, subprocess, sys
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
subprocess.Popen([sys.executable, '-c', 'print("albatross")']).wait()