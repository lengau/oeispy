"""Tests for generic generators."""

import pytest

from oeispy.generators import generic

TESTS = (
    ("Lucas", generic.lucas, (0, 1), (0, 1, 1, 2, 3, 5, 8, 13)),
    ("Lucas", generic.lucas, (2, 1), (2, 1, 3, 4, 7, 11, 18, 29, 47)),
    (
        "Palindromes",
        generic.palindromes,
        (),
        (
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            11,
            22,
            33,
            44,
            55,
            66,
            77,
            88,
            99,
            101,
            111,
            121,
            131,
            141,
            151,
            161,
            171,
            181,
            191,
            202,
        ),
    ),
)


@pytest.mark.parametrize("name,func,params,sequence_start", TESTS)
def test_generic(name, func, params, sequence_start):
    for i, (val, exp) in enumerate(zip(sequence_start, func(*params))):
        assert val == exp, f"{name} generator failed for params {params} on item {i}"
