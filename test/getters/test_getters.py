"""Tests for getters implemented as lambdas."""
import typing

import pytest

from oeispy.getters import GETTERS


class GetterTest(typing.NamedTuple):
    number: int
    function: typing.Callable[[int], int]
    inputs: typing.Sequence[int]
    outputs: typing.Sequence[int]


TESTS = (
    GetterTest(4, GETTERS[4], range(10), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    GetterTest(7, GETTERS[7], range(10), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    GetterTest(12, GETTERS[12], range(10), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    GetterTest(27, GETTERS[27], range(1000), range(1000))
)


@pytest.mark.parametrize('number,func,inputs,outputs', TESTS)
def test_getter(number, func, inputs, outputs):
    for in_, out in zip(inputs, outputs):
        assert func(in_) == out, (
            f'Getter for sequence {number} failed test on item {in_}')
