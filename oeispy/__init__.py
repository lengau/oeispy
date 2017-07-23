import typing

import requests

from . import oeis

__all__ = ['OEIS']

URI = 'https://oeis.org/search?fmt=json&q={term}'


class _OEIS:
    """OEIS sequence factory.

    A factory that generates OEIS sequences, keeping existing sequence
    objects for reuse.

    Call directly with a sequence number to get a sequence by its number. E.g.:
    >>> pi_digits = OEIS(796)

    Perform a search, returning a list of 0 or more sequences, using
    `OEIS.search`. See its documentation for further detail.
    """

    def __init__(self):
        self.sequences = {}

    def __call__(self, number: int) -> oeis.A:
        """Get an OEIS sequence by its sequence id.
        :param number: The sequence number of the requested sequence.
        """
        if number not in self.sequences:
            self.sequences[number] = oeis.A(number)
        return self.sequences[number]

    def search(self,
               term: typing.Union[str, typing.Sequence[int]]
               ) -> typing.List[oeis.A]:
        """Search for OEIS sequences using either a string or some ints.

        :param term: Either a string search term or a sequence of integers
            to find.

        Examples:
        >>> OEIS.search('natural numbers')
        Returns all sequences with the term 'natural numbers', based on the
        OEIS search algorithm. As of 2017-07-22, returns 10 sequences, the
        first being A000027, the positive integers.
        >>> OEIS.search([3,1,4,1,5,9,2,6,5,3,5,8,9,7,9])
        Returns sequences the list of numbers within from OEIS. As of
        2017-07-22, returns 4 sequences, the first being A000796, Decimal
        expansion of pi.
        """
        if isinstance(term[0], int):
            term = ','.join(str(i) for i in term)
        results = requests.get(URI.format(term=term)).json()['results']
        if results is None:
            return []
        return [oeis.A(r['number'], json=r) for r in results]


OEIS = _OEIS()
