#!/usr/bin/env python
"""
custom interactive python interpreter.
"""

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import

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

# preloaded imports
#
import boto3 as aws
import botocore as awscore

from cloudshell.functions.bash import *
from cloudshell.functions.clock import *
from cloudshell.terminal.formatting import *

from cloudshell.terminal import formatting as fmt

# session constants
#
SESSION_HIST_FILE = pathlib.Path('~/.cloud-shell.hist').expanduser()

# session builtins
#
def about() -> None:
    """
    print detailed information about the custom shell environment.
    """

    indentation = '            '

    funcs = [
        f'{cyan(f"{n}")}\n' for n in fmt.__all__
    ]

    msg = inspect.cleandoc(f'''\
        =========================================
        *** {white("cloud-shell")} ***

        interactive shell for the cloud.

        aliases:

            {cyan("aws")}     == {cyan("boto3")}
            {cyan("awscore")} == {cyan("botocore")}

        functions:

            {f"{indentation}".join([f for f in funcs])}
        ======================================
    ''')

    print(msg)

# session state
#
def session_load_history(hist_file: pathlib.Path) -> int:
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
    num_lines = readline.get_current_history_length() - last_history_size

    readline.set_history_length(max_history_size)
    readline.append_history_file(num_lines, str(hist_file))

def session_on_enter(tab_completable_symbols: dict) -> None:
    """
    interactive shell entrypoint.
    """

    banner = inspect.cleandoc(f'''\
        ========================================
        *** {white("cloud-shell")} ***

        interactive shell for the cloud.

        run "{cyan("about()")}" for more information.

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
