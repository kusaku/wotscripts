# Embedded file name: scripts/common/Lib/test/test_pty.py
from test.test_support import verbose, run_unittest, import_module
fcntl = import_module('fcntl')
import_module('termios')
import errno
import pty
import os
import sys
import select
import signal
import socket
import unittest
TEST_STRING_1 = 'I wish to buy a fish license.\n'
TEST_STRING_2 = 'For my pet fish, Eric.\n'
if verbose:

    def debug(msg):
        print msg


else:

    def debug(msg):
        pass


def normalize_output(data):
    if data.endswith('\r\r\n'):
        return data.replace('\r\r\n', '\n')
    if data.endswith('\r\n'):
        return data.replace('\r\n', '\n')
    return data


class PtyTest(unittest.TestCase):

    def setUp(self):
        self.old_alarm = signal.signal(signal.SIGALRM, self.handle_sig)
        signal.alarm(10)

    def tearDown(self):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.old_alarm)

    def handle_sig(self, sig, frame):
        self.fail('isatty hung')

    def test_basic(self):
        try:
            debug('Calling master_open()')
            master_fd, slave_name = pty.master_open()
            debug("Got master_fd '%d', slave_name '%s'" % (master_fd, slave_name))
            debug('Calling slave_open(%r)' % (slave_name,))
            slave_fd = pty.slave_open(slave_name)
            debug("Got slave_fd '%d'" % slave_fd)
        except OSError:
            raise unittest.SkipTest, 'Pseudo-terminals (seemingly) not functional.'

        self.assertTrue(os.isatty(slave_fd), 'slave_fd is not a tty')
        orig_flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, orig_flags | os.O_NONBLOCK)
        try:
            s1 = os.read(master_fd, 1024)
            self.assertEqual('', s1)
        except OSError as e:
            if e.errno != errno.EAGAIN:
                raise

        fcntl.fcntl(master_fd, fcntl.F_SETFL, orig_flags)
        debug('Writing to slave_fd')
        os.write(slave_fd, TEST_STRING_1)
        s1 = os.read(master_fd, 1024)
        self.assertEqual('I wish to buy a fish license.\n', normalize_output(s1))
        debug('Writing chunked output')
        os.write(slave_fd, TEST_STRING_2[:5])
        os.write(slave_fd, TEST_STRING_2[5:])
        s2 = os.read(master_fd, 1024)
        self.assertEqual('For my pet fish, Eric.\n', normalize_output(s2))
        os.close(slave_fd)
        os.close(master_fd)

    def test_fork(self):
        debug('calling pty.fork()')
        pid, master_fd = pty.fork()
        if pid == pty.CHILD:
            if not os.isatty(1):
                debug("Child's fd 1 is not a tty?!")
                os._exit(3)
            debug('In child, calling os.setsid()')
            try:
                os.setsid()
            except OSError:
                debug('Good: OSError was raised.')
            except AttributeError:
                debug('No setsid() available?')
            except:
                debug('An unexpected error was raised.')
                os._exit(1)
            else:
                debug('os.setsid() succeeded! (bad!)')
                os._exit(2)

            os._exit(4)
        else:
            debug('Waiting for child (%d) to finish.' % pid)
            while True:
                try:
                    data = os.read(master_fd, 80)
                except OSError:
                    break

                if not data:
                    break
                sys.stdout.write(data.replace('\r\n', '\n'))

            pid, status = os.waitpid(pid, 0)
            res = status >> 8
            debug('Child (%d) exited with status %d (%d).' % (pid, res, status))
            if res == 1:
                self.fail('Child raised an unexpected exception in os.setsid()')
            elif res == 2:
                self.fail('pty.fork() failed to make child a session leader.')
            elif res == 3:
                self.fail('Child spawned by pty.fork() did not have a tty as stdout')
            elif res != 4:
                self.fail('pty.fork() failed for unknown reasons.')
        os.close(master_fd)


class SmallPtyTests(unittest.TestCase):
    """These tests don't spawn children or hang."""

    def setUp(self):
        self.orig_stdin_fileno = pty.STDIN_FILENO
        self.orig_stdout_fileno = pty.STDOUT_FILENO
        self.orig_pty_select = pty.select
        self.fds = []
        self.select_rfds_lengths = []
        self.select_rfds_results = []

    def tearDown(self):
        pty.STDIN_FILENO = self.orig_stdin_fileno
        pty.STDOUT_FILENO = self.orig_stdout_fileno
        pty.select = self.orig_pty_select
        for fd in self.fds:
            try:
                os.close(fd)
            except:
                pass

    def _pipe(self):
        pipe_fds = os.pipe()
        self.fds.extend(pipe_fds)
        return pipe_fds

    def _mock_select(self, rfds, wfds, xfds):
        self.assertEqual(self.select_rfds_lengths.pop(0), len(rfds))
        return (self.select_rfds_results.pop(0), [], [])

    def test__copy_to_each(self):
        """Test the normal data case on both master_fd and stdin."""
        read_from_stdout_fd, mock_stdout_fd = self._pipe()
        pty.STDOUT_FILENO = mock_stdout_fd
        mock_stdin_fd, write_to_stdin_fd = self._pipe()
        pty.STDIN_FILENO = mock_stdin_fd
        socketpair = socket.socketpair()
        masters = [ s.fileno() for s in socketpair ]
        self.fds.extend(masters)
        os.write(masters[1], 'from master')
        os.write(write_to_stdin_fd, 'from stdin')
        pty.select = self._mock_select
        self.select_rfds_lengths.append(2)
        self.select_rfds_results.append([mock_stdin_fd, masters[0]])
        self.select_rfds_lengths.append(2)
        with self.assertRaises(IndexError):
            pty._copy(masters[0])
        rfds = select.select([read_from_stdout_fd, masters[1]], [], [], 0)[0]
        self.assertEqual([read_from_stdout_fd, masters[1]], rfds)
        self.assertEqual(os.read(read_from_stdout_fd, 20), 'from master')
        self.assertEqual(os.read(masters[1], 20), 'from stdin')

    def test__copy_eof_on_all(self):
        """Test the empty read EOF case on both master_fd and stdin."""
        read_from_stdout_fd, mock_stdout_fd = self._pipe()
        pty.STDOUT_FILENO = mock_stdout_fd
        mock_stdin_fd, write_to_stdin_fd = self._pipe()
        pty.STDIN_FILENO = mock_stdin_fd
        socketpair = socket.socketpair()
        masters = [ s.fileno() for s in socketpair ]
        self.fds.extend(masters)
        os.close(masters[1])
        socketpair[1].close()
        os.close(write_to_stdin_fd)
        pty.select = self._mock_select
        self.select_rfds_lengths.append(2)
        self.select_rfds_results.append([mock_stdin_fd, masters[0]])
        self.select_rfds_lengths.append(0)
        with self.assertRaises(IndexError):
            pty._copy(masters[0])


def test_main(verbose = None):
    run_unittest(SmallPtyTests, PtyTest)


if __name__ == '__main__':
    test_main()