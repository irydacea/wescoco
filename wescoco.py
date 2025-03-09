#!/usr/bin/env python3
'''
WesCoco - Wesnoth Console Colorizer

Copyright (C) 2024 - 2025 by Iris Morelle <iris@irydacea.me>
See COPYING for use and distribution terms.
'''

from enum import StrEnum
import fileinput
import re
import sys
from typing import Union


class AnsiFormat(StrEnum):
    '''
    Collection of standard ANSI escape sequences to configure text attributes
    on a Unix terminal emulator.
    '''
    DEFAULT         = ''
    RESET           = '\033[0m'
    BOLD            = '\033[1m'
    DIM             = '\033[2m'
    MEDIUM          = '\033[22m'
    ITALIC          = '\033[3m'
    NO_ITALIC       = '\033[23m'
    UNDERLINE       = '\033[4m'
    INVERT          = '\033[7m'
    BLACK           = '\033[30m'
    RED             = '\033[31m'
    GREEN           = '\033[32m'
    YELLOW          = '\033[33m'
    BLUE            = '\033[34m'
    MAGENTA         = '\033[35m'
    CYAN            = '\033[36m'
    WHITE           = '\033[37m'
    BRIGHT_BLACK    = '\033[1;30m'
    BRIGHT_RED      = '\033[1;31m'
    BRIGHT_GREEN    = '\033[1;32m'
    BRIGHT_YELLOW   = '\033[1;33m'
    BRIGHT_BLUE     = '\033[1;34m'
    BRIGHT_MAGENTA  = '\033[1;35m'
    BRIGHT_CYAN     = '\033[1;36m'
    BRIGHT_WHITE    = '\033[1;37m'

    def apply(self, text: str, reset: Union[str, bool] = True) -> str:
        '''
        Applies the ANSI escape sequence to the argument.
        '''
        if isinstance(reset, str):
            return f'{self}{text}{reset}'
        elif reset:
            return f'{self}{text}{AnsiFormat.RESET}'
        else:
            return f'{self}{text}'


ALL_LOGLEVELS = (
    'debug',
    'info',
    'warning',
    'error'
)

LOGLEVEL_FORMATS = {
    'debug':        AnsiFormat.BRIGHT_BLACK,
    'warning':      AnsiFormat.BRIGHT_YELLOW,
    'error':        AnsiFormat.BRIGHT_RED,
}

LEVEL_PADDING = max(map(len, ALL_LOGLEVELS))


class CocoProcessor:
    '''
    Colorizes a text input and handles any relevant state.
    '''

    # Standard log message regex
    _re_standard = re.compile(r'''^
                              (\d{8})           # Date DDDDDDDD
                              \x20
                              (\d\d:\d\d:\d\d)  # Time HH:MM:SS
                              \x20
                              ([^\s]+)          # Log level
                              \x20
                              ([^\s]+)          # Log domain
                              :\x20
                              (.*)              # Log contents
                              $''',
                              flags = re.VERBOSE | re.ASCII)

    @staticmethod
    def process_line(raw: str):
        '''
        Processes a single line of input.
        '''
        match = CocoProcessor._re_standard.match(raw)
        if not match:
            sys.stderr.write(raw)
        else:
            date, tm, loglevel, logdomain, body = match.groups()
            fmt = LOGLEVEL_FORMATS.get(loglevel, AnsiFormat.DEFAULT)
            parts = (
                AnsiFormat.DIM.apply(f'{date} {tm}', AnsiFormat.MEDIUM),
                AnsiFormat.ITALIC.apply(loglevel.rjust(LEVEL_PADDING), AnsiFormat.NO_ITALIC),
                AnsiFormat.BOLD.apply(logdomain, ':'),
                AnsiFormat.MEDIUM.apply(body, False),
                '\n')
            sys.stderr.write(fmt.apply(' '.join(parts)))
        sys.stderr.flush()


def main():
    '''
    Application entry point.
    '''
    try:
        coco = CocoProcessor()
        for line in fileinput.input(encoding='utf-8'):
            coco.process_line(line)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
