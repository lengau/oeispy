"""Functions that get an item from an OEIS sequence.

All functions in GETTERS take a single integer argument and return a single
integer. The prototype from typing would be:
Callable[[int], int]

If a getter function is retrieved from the OEIS website, it should be in 
`from_site.py`.
"""
import typing

__all__ = ['GETTERS']

GETTERS: typing.Dict[int, typing.Callable[[int], int]] = {
    4: lambda _: 0,
    7: lambda n: 1 if n == 0 else 0,
    12: lambda _: 1,
    27: lambda n: n,
}
