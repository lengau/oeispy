"""Tests for items in __init__"""
from unittest import mock

import pytest

import oeispy

SEARCH_TERMS = (
    ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), '0,1,2,3,4,5,6,7,8,9,10'),
    ('some string', 'some string'),
)


@pytest.fixture()
def oeis():
    return oeispy._OEIS()


def test_call_creates_sequence(oeis, monkeypatch):
    rq_get = mock.MagicMock()
    monkeypatch.setattr('requests.get', rq_get)
    assert len(oeis.sequences) == 0
    actual = oeis(0)
    assert actual is oeis.sequences[0]
    rq_get.assert_called_once()
    rq_get.return_value.json.assert_called_once_with()


def test_call_singleton(oeis, monkeypatch):
    rq_get = mock.Mock()
    monkeypatch.setattr('requests.get', rq_get)
    seq = mock.Mock()
    oeis.sequences[0] = seq
    assert oeis(0) is seq


@pytest.mark.parametrize('input_term,output_term', SEARCH_TERMS)
def test_search_term_normalized(input_term, output_term, oeis, monkeypatch):
    rq_get = mock.Mock()
    monkeypatch.setattr('requests.get', rq_get)
    rq_get.return_value.json.return_value = {'results': None}
    a = mock.Mock()
    monkeypatch.setattr('oeispy.oeis.A', a)
    assert oeis.search(input_term) == []
    rq_get.assert_called_once_with(oeispy.URI.format(term=output_term))


def test_search_returns_many(oeis, monkeypatch):
    rq_get = mock.Mock()
    monkeypatch.setattr('requests.get', rq_get)
    rq_get.return_value.json.return_value = {
        'results': [{'number': i} for i in range(10)]
    }
    a = mock.Mock()
    monkeypatch.setattr('oeispy.oeis.A', a)
    assert len(oeis.search('{term}')) == 10
    rq_get.assert_called_once_with(oeispy.URI)
