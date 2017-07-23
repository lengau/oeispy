"""Sequence generators taken from the OEIS website.

Each of these generators should include a docstring attributing the contributor
who provided the generator to OEIS.
If a Python implementation of an OEIS sequence was provided to OEIS in a form
other than as a generator, it should be noted that the implementation given
here is modified from the implementation on the site.

All sequences herein should conform to the OEIS licence agreements:
http://oeis.org/wiki/Legal_Documents

If you believe a generator in this file violates the licence, please file an
issue about it and (preferably) a pull request to fix or if necessary remove
the offending generator.

This file is licenced under the terms of the OEIS end-user licence agreement:
http://oeis.org/wiki/The_OEIS_End-User_License_Agreement
"""


def kolakoski():
    """Generator for Kolakoski numbers (A000002).
    Provided by David Eppstein to OEIS. Taken from the OEIS website.
    """
    x = y = -1
    while True:
        yield [2, 1][x & 1]
        f = y & ~(y + 1)
        x ^= f
        y = (y + 1) | (f & (x >> 1))
