"""Generic generators that can be used to generate more than one OEIS sequence.

NOTE: If a generic generator was provided on the OEIS website, it should be
placed in `from_site.py` instead.
"""
import itertools


def lucas(a, b):
    """A general generator for Lucas sequences.
    
    Examples:
    >>> lucas(0, 1)  # Fibonacci sequence
    >>> lucas(2, 1)  # Lucas numbers
    """
    yield a
    while True:
        yield b
        a, b = b, a + b


def with_getter(getter, offset):
    """A generic generator for any sequence with a getter.

    :param getter: The getter function to use.
    :param the offset for this sequence. (Normally 0, but specified by OEIS)
    """
    for i in itertools.count(offset):
        yield getter(i)
