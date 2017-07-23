"""Test OEIS sequence implementation."""
from unittest import mock

import pytest

from oeispy import oeis
from test import data

SEQUENCE_DEFINITIONS = (
    (2, data.a2_json),
)


@pytest.fixture(params=SEQUENCE_DEFINITIONS)
def seq(request):
    return oeis.A(*request.param)


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_init_with_json_given(number, json):
    seq = oeis.A(number, json)
    assert seq.entry == json
    assert seq.number == number


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_init_without_json(number, json, monkeypatch):
    rq_get = mock.Mock()
    rq_get.return_value.json.return_value = {'results': [json]}
    monkeypatch.setattr('requests.get', rq_get)
    seq = oeis.A(number)
    assert seq.entry == json
    assert seq.number == number
    rq_get.assert_called_once_with(
        oeis.URI_FORMAT.format(number=number))
    rq_get.return_value.json.assert_called_once()


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_has_getter(number, json, monkeypatch):
    getters = {}
    monkeypatch.setattr('oeispy.getters.GETTERS', getters)
    seq = oeis.A(number, json)
    assert seq.has_getter is False
    getters[number] = lambda x: None
    seq = oeis.A(number, json)
    assert seq.has_getter is True


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_has_generator(number, json, monkeypatch):
    generators = {}
    monkeypatch.setattr('oeispy.generators.GENERATORS', generators)
    seq = oeis.A(number, json)
    assert seq.has_generator is False
    generators[number] = lambda: None
    seq = oeis.A(number, json)
    assert seq.has_generator is True


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_retrievable(number, json, monkeypatch):
    generators = {}
    getters = {}
    monkeypatch.setattr('oeispy.generators.GENERATORS', generators)
    monkeypatch.setattr('oeispy.getters.GETTERS', getters)
    seq = oeis.A(number, json)
    assert seq.retrievable is False
    generators[number] = lambda x: None
    seq = oeis.A(number, json)
    assert seq.retrievable is True
    del generators[number]
    seq = oeis.A(number, json)
    assert seq.retrievable is False
    getters[number] = lambda: None
    seq = oeis.A(number, json)
    assert seq.retrievable is True


def test_repr(seq):
    assert repr(seq) == f'A({seq.entry["number"]})'


def test_str(seq):
    str(seq)


@pytest.mark.parametrize('number, json', SEQUENCE_DEFINITIONS)
def test_iter_no_generator(number, json, monkeypatch):
    generators = {}
    monkeypatch.setattr('oeispy.generators.GENERATORS', generators)
    seq = oeis.A(number, json)
    with pytest.raises(NotImplementedError):
        iter(seq)


@pytest.mark.parametrize('number, json', SEQUENCE_DEFINITIONS)
def test_iter_with_generator(number, json, monkeypatch):
    expected = (a for a in range(0))
    generators = {number: lambda: expected}
    monkeypatch.setattr('oeispy.generators.GENERATORS', generators)
    seq = oeis.A(number, json)
    output = iter(seq)
    assert output == expected


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_get_no_getter(number, json, monkeypatch):
    monkeypatch.setattr('oeispy.getters.GETTERS', {})
    seq = oeis.A(number, json)
    assert seq._get is None
    with pytest.raises(NotImplementedError):
        seq.get(0)


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_get_less_than_offset(number, json, monkeypatch):
    getter = mock.Mock()
    monkeypatch.setattr('oeispy.getters.GETTERS', {number: getter})
    seq = oeis.A(number, json)
    assert seq._get is getter
    with pytest.raises(IndexError):
        seq.get(seq.offset - 1)


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_get_succeeds(number, json, monkeypatch):
    getter = mock.Mock()
    monkeypatch.setattr('oeispy.getters.GETTERS', {number: getter})
    seq = oeis.A(number, json)
    assert seq._get is getter
    assert seq.get(seq.offset) == getter.return_value


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_getitem_less_than_offset(number, json, monkeypatch):
    getter = mock.Mock()
    monkeypatch.setattr('oeispy.getters.GETTERS', {number: getter})
    seq = oeis.A(number, json)
    assert seq._get is getter
    with pytest.raises(IndexError):
        _ = seq[seq.offset - 1]


@pytest.mark.parametrize('number,json', SEQUENCE_DEFINITIONS)
def test_getitem_gets_from_data(number, json, monkeypatch):
    monkeypatch.setattr('oeispy.getters.GETTERS', {})
    seq = oeis.A(number, json)
    seq.data = mock.MagicMock()
    seq.data.__len__.return_value = 1
    assert seq[seq.offset] == seq.data[0]


def test_getitem_uses_get(seq):
    input_value = 'This is totally an integer.'
    seq.get = mock.Mock()
    expected = seq.get.return_value
    actual = seq[input_value]
    assert actual == expected


def test_getitem_not_implemented(seq):
    seq._get = None
    seq.generator = None
    with pytest.raises(NotImplementedError):
        _ = seq[seq.offset + len(seq.data)]


def test_getitem_generator(seq):
    seq.generator = lambda: iter([1, 2, 3])
    seq._get = None
    seq.data = []
    gen = seq.generator()
    next(gen)
    expected = next(gen)
    assert seq[seq.offset + 1] == expected
