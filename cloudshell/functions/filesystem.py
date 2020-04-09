#!/usr/bin/env python

import typing
import pathlib

__all__ = [
    'file_sizes_bytes',
    'directory_contents',
    'directory_size_total_bytes',
]

pathlike = typing.Union[str, pathlib.Path]

def directory_contents(p: pathlike, recursive: bool = True, max_depth: int = None) -> typing.Iterable[pathlib.Path]:
    """iterate the contents of a directory, yielding absolute paths to each item found."""

    abs_path: pathlib.Path = None

    try:
        abs_path = p.resolve()
    except AttributeError:
        abs_path = pathlib.Path(p).resolve()

    if not abs_path.exists():
        raise FileNotFoundError(f'no such directory {p}')

    if max_depth is None or max_depth < 0: # no maximum depth TODO: DOESN"T WORK
        max_depth = 1

    for f in abs_path.iterdir():
        yield f

        if f.is_dir() and recursive and max_depth > 0:
            yield from directory_contents(
                f, recursive=recursive, max_depth=max_depth - 1)

def file_sizes_bytes(p: pathlike, recursive: bool = True, max_depth: int = None) -> typing.Iterable[int]:
    """iterate the contents of a directory, yielding the size (bytes) of each file."""

    if max_depth is None or max_depth < 0:
        max_depth = 1

    for f in directory_contents(p, recursive=recursive, max_depth=max_depth):
        if f.is_dir():
            # if recursive and max_depth > 0:
            #     yield from file_sizes_bytes(f, recursive=recursive, max_depth=max_depth - 1)

            continue
        yield f.stat().st_size

def directory_size_total_bytes(p: pathlike, max_depth: int = None) -> int:
    """similar to the unix `df` command, get the size (bytes) of a directories contents."""

    max_depth = max_depth if max_depth else -1

    return sum([
        b for b in file_sizes_bytes(p, recursive=True, max_depth=max_depth)
    ])
