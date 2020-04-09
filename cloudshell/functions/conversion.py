#!/usr/bin/env python

__all__ = [
    'bytes_to_human_readable',
]

KILOBYTE = 1000
KIBIBYTE = 1024

STORAGE_UNITS = (
    'K',
    'M',
    'G',
    'T',
    'P',
    'E',
    'Z',
    'Y',
)

SUFFIX_TABLE = {
    s: 1 << (i + 1)* 10 for i, s in enumerate(STORAGE_UNITS)
}

def bytes_to_human_readable(n: int) -> str:
    """
    parse the number `n` as a number of bytes into a human-readable string.

    >>> bytes_to_human_readable(100240000)
    '95.6M'
    """

    for s in reversed(STORAGE_UNITS):
        if n >= SUFFIX_TABLE[s]:
            value = float(n) / SUFFIX_TABLE[s]

            return f'{value:.1f}{s}'

    return f'{n}B'
