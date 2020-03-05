#!/usr/bin/env python

import os
import json

__all__ = [
    'ls',
    'jq',
    'clear',
]

def clear() -> None:
    """
    simulate the shell command `clear`, clearing terminal output.
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def ls(*flags: str) -> None:
    """
    simulate the shell command `ls`, listing the contents of the current directory.
    """

    os.system(f'ls {" ".join(list(flags))}')

def jq(o: object, return_only: bool = False, indent: int = 1) -> str:
    """
    simulate the shell command `jq`, either dumping objects (i.e., `json`) to `stdout`
    or optionally if `return_only` is `True`, return the formatted string without writing
    to `stdout`.
    """

    formatted = json.dumps(o, indent=indent, default=str)

    if return_only:
        return formatted

    print(formatted)

    return None
