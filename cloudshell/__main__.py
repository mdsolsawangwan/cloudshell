#!/usr/bin/env python
"""
custom interactive python interpreter.
"""

# pylint: disable=fixme
# pylint: disable=unused-import
# pylint: disable=ungrouped-imports
# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=unused-wildcard-import

# TODO:
#
#   - include parameter and return type arguments in 'about()'
#

# required imports
#
import os
import sys
import code
import json
import atexit
import inspect
import pathlib
import readline
import rlcompleter

from cloudshell.terminal import formatting as fmt

# import aliases
aws = None
awscore = None

# aliased imports
#
try:
    import boto3 as aws
except ImportError:
    print('failed to load the "boto3" module, the alias "aws" will not be available')

try:
    import botocore as awscore
except ImportError:
    print('failed to load the "botocore" module, the alias "awscore" will not be available')

from cloudshell.functions.bash import *
from cloudshell.functions.clock import *
from cloudshell.functions.conversion import *
from cloudshell.functions.filesystem import *

# session constants
#
SESSION_HIST_FILE = pathlib.Path('~/.cloud-shell.hist').expanduser()

# session globals
#
ABOUT_CACHE = {
    'funcs': None
}

# session builtins
#
def about() -> None:
    """print detailed information about the custom shell environment."""

    indentation = '            '

    if ABOUT_CACHE['funcs'] is None:
        from cloudshell.functions import definitions

        ABOUT_CACHE['funcs'] = [
            f'{fmt.cyan(f"{n}")}\n' for n in definitions.__all__
        ]

        ABOUT_CACHE['funcs'].sort(key=lambda name: len(name))

    # pylint: disable=not-an-iterable

    msg = inspect.cleandoc(f'''\
        =========================================
        *** {fmt.white("cloud-shell")} ***

        interactive shell for the cloud.

        aliases:

            {fmt.cyan("aws")}     == {fmt.cyan("boto3")}
            {fmt.cyan("awscore")} == {fmt.cyan("botocore")}

        functions:

            {f"{indentation}".join([f for f in ABOUT_CACHE["funcs"]])}
        ======================================
    ''')

    # pylint: enable=not-an-iterable

    print(msg)

# session state
#
def session_load_history(hist_file: pathlib.Path) -> int:
    """utility function, loads sessions history into the current session."""

    line_count = 0

    try:
        readline.read_history_file(str(hist_file))
    except FileNotFoundError: # create a new history file if not found
        with open(hist_file, 'wb'):
            pass
    else:
        line_count = readline.get_current_history_length()

    return line_count

def session_store_history(hist_file: pathlib.Path, last_history_size: int, max_history_size: int = 1000) -> None:
    """utility function, appends the current sessions history to existing history."""

    num_lines = readline.get_current_history_length() - last_history_size

    readline.set_history_length(max_history_size)
    readline.append_history_file(num_lines, str(hist_file))

def session_on_enter(tab_completable_symbols: dict) -> None:
    """interactive shell entrypoint."""

    banner = inspect.cleandoc(f'''\
        ========================================
        *** {fmt.white("cloud-shell")} ***

        interactive shell for the cloud.

        run "{fmt.cyan("about()")}" for more information.

        ======================================
    ''')

    expr_handler = fmt.PromptStateExpressionHandler()
    indent_handler = fmt.AutoindentHandler()

    sys.displayhook = expr_handler

    completer = rlcompleter.Completer(tab_completable_symbols)

    readline.set_pre_input_hook(indent_handler)
    readline.set_completer(completer.complete)

    readline.parse_and_bind('tab: complete')

    history_size = session_load_history(SESSION_HIST_FILE)

    atexit.register(session_store_history, SESSION_HIST_FILE, history_size)

    shell = code.InteractiveConsole(tab_completable_symbols)

    shell.interact(
        banner=banner
    )

# start here
#
try:
    session_on_enter({
        **globals(),
        **locals(),
    })
except SystemExit:
    pass
