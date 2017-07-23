"""Tests for generators taken from the OEIS website."""

import pytest

from oeispy.generators import from_site as gen

KOLAKOSKI = (
    1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1,
    2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2,
    1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2,
    1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2,
    1, 2, 1, 1, 2, 1, 2, 2
)

TESTS = (
    ('Kolakoski', gen.kolakoski, KOLAKOSKI),
)


@pytest.mark.parametrize('name,func,sequence_start', TESTS)
def test_generic(name, func, sequence_start):
    for i, (val, exp) in enumerate(zip(sequence_start, func())):
        assert val == exp, (
            f'{name} generator failed on item {i}')
