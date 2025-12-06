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


def palindromes():
    """Generate palindromic numbers (A002113).

    A palindrome is a number that reads the same forwards and backwards.
    Examples: 0, 1, 2, ..., 9, 11, 22, 33, ..., 99, 101, 111, 121, ...
    """
    # Single digit palindromes: 0-9
    yield from range(10)

    # Multi-digit palindromes
    # Generate by length: 2-digit, 3-digit, 4-digit, etc.
    length = 2
    while True:
        # For a given length, we generate the first half and mirror it
        half_length = (length + 1) // 2

        # Range for the first half (excluding leading zeros)
        start = 10 ** (half_length - 1)
        end = 10**half_length

        for num in range(start, end):
            num_str = str(num)
            if length % 2 == 0:
                # Even length: mirror the entire first half
                palindrome = num_str + num_str[::-1]
            else:
                # Odd length: mirror all but the middle digit
                palindrome = num_str + num_str[-2::-1]
            yield int(palindrome)

        length += 1
