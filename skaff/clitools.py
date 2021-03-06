#!/usr/bin/env python3

"""
A suite of command line based tools.
"""

# ------------------------------- MODULE INFO ---------------------------------
__all__ = [
    "key_get",
    "timed_key_get",
    "timeout",
    "ANSIColor",
    "SmartFormatter",
]
# ------------------------------- MODULE INFO ---------------------------------

# --------------------------------- MODULES -----------------------------------
import argparse
import os
import signal
import sys

if "posix" == os.name:
    import fcntl
    import termios
elif "nt" == os.name:
    import msvcrt
    import time

from functools import wraps
from typing import Callable
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class ANSIColor:
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    KHAKI = "\x1b[1;33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    PURPLE = "\x1b[1;35m"
    CYAN = "\x1b[36m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"


class SmartFormatter(argparse.HelpFormatter):
    """
    You can only specify one formatter in standard argparse, so you cannot
    both have pre-formatted description (RawDescriptionHelpFormatter)
    and ArgumentDefaultsHelpFormatter.
    The SmartFormatter has sensible defaults (RawDescriptionFormatter) and
    the individual help text can be marked ( help="R|" ) for
    variations in formatting.
    Version string is formatted using _split_lines and preserves any
    line breaks in the version string.
    """
    # Use a custom formatter to ensure the custom formatted version string
    # got printed properly while still preserves line-wrapping and other
    # functionality for all the rest of the help text (argparse)
    # Borrowed from
    # https://bitbucket.org/ruamel/std.argparse/overview
    def __init__(self, *args, **kwargs):
        self._add_defaults = None
        super(SmartFormatter, self).__init__(*args, **kwargs)

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        if text.startswith('D|'):
            self._add_defaults = True
            text = text[2:]
        elif text.startswith('*|'):
            text = text[2:]
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _get_help_string(self, action):
        if self._add_defaults is None:
            return argparse.HelpFormatter._get_help_string(self, action)
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: %(default)s)'
        return help

    def _expand_help(self, action):
        """
        Mark a password help with '*|' at the start, so that
        when global default adding is activated (e.g. through a helpstring
        starting with 'D|') no password is show by default.
        Orginal marking used in repo cannot be used because of decorators.
        """
        hs = self._get_help_string(action)
        if hs.startswith('*|'):
            params = dict(vars(action), prog=self._prog)
            if params.get('default') is not None:
                # you can update params, this will change the default, but we
                # are printing help only
                params['default'] = '*' * len(params['default'])
            return self._get_help_string(action) % params
        return super(SmartFormatter, self)._expand_help(action)
# --------------------------------- CLASSES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def timed_key_get(seconds: int) -> str:
    """
    Gets a single key press from the terminal within the given number of
    'seconds' and returns a 'str' representing the key pressed; returns empty
    "" string upon time out.

    Based on the version from StackOverflow by Paul:
    http://stackoverflow.com/questions/3471461/raw-input-and-timeout/3911560
    """
    if "posix" == os.name:
        return timeout(seconds)(key_get)()
    elif "nt" == os.name:
        start_time = time.time()
        key = str()

        while True:
            if msvcrt.kbhit():
                key = key_get()
                break
            if len(key) == 0 and (time.time() - start_time) > seconds:
                raise TimeoutError()
        return key


def timeout(seconds: int) -> Callable:
    """
    Sets a timer on a function; should be used as a decorator.
    Raises 'TimeOutError' upon expiration.

    Reference (StackOverflow):
    /questions/2281850/timeout-function-if-it-takes-too-long-to-finish
    """
    if "posix" == os.name:
        def decorator(func):
            def _timeout_handle(signum, frame):
                raise TimeoutError()

            def wrapper(*args, **kwargs):
                signal.signal(signal.SIGALRM, _timeout_handle)
                signal.alarm(seconds)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result

            return wraps(func)(wrapper)

        return decorator
    elif "nt" == os.name:
        raise NotImplementedError(("'timeout' is not implemented on "
                                   "'Windows'"))


def key_get() -> str:
    """
    Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    Reference (StackOverflow):
    /questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
    """
    if "posix" == os.name:
        fd = sys.stdin.fileno()
        # save old state
        flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
        attrs_save = termios.tcgetattr(fd)
        # make raw - the way to do this comes from the termios(3) man page.
        attrs = list(attrs_save)  # copy the stored version to update
        # iflag
        attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                      | termios.ISTRIP | termios.INLCR | termios. IGNCR
                      | termios.ICRNL | termios.IXON)
        # oflag
        attrs[1] &= ~termios.OPOST
        # cflag
        attrs[2] &= ~(termios.CSIZE | termios. PARENB)
        attrs[2] |= termios.CS8
        # lflag
        attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                      | termios.ISIG | termios.IEXTEN)
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        # turn off non-blocking
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
        # read a single keystroke
        try:
            ret = sys.stdin.read(1)  # returns a single character
        except KeyboardInterrupt:
            ret = str()
        finally:
            # restore old state
            termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
        return ret
    elif "nt" == os.name:
        try:
            # 'getch' by default returns a 'bytes' object;
            # so an extra conversion is required
            ret = msvcrt.getch().decode()
        except KeyboardInterrupt:
            ret = str()
        return ret
# -------------------------------- FUNCTIONS ----------------------------------
