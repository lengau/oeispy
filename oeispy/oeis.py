"""Implementation of OEIS objects."""
import typing

import requests

from . import generators
from . import getters

URI_FORMAT = 'http://oeis.org/search?q=id:A{number}&fmt=json'
INDEX_TOO_SMALL_MSG = (
    'Index {idx} is less than the sequence offset ({offset}) for {repr_}. '
    'Please check the OEIS Wiki for further information: '
    'http://oeis.org/wiki/Offsets')


class A:
    """A sequence from OEIS."""

    def __init__(self,
                 number: int,
                 json: typing.Optional[typing.Dict[str, typing.Any]] = None):
        """Instantiate an OEIS sequence.
        
        :param number: The ID of a sequence (for example, 796 for
            A000796, the decimal expansion of pi)
        :param json: An optional dictionary of the JSON for this sequence. If
            not provided, requests the sequence via the OEIS JSON API.
        """
        self.number = number
        if json is None:
            uri = URI_FORMAT.format(number=number)
            self.entry = requests.get(uri).json()['results'][0]
        else:
            self.entry = json
        self.name = self.entry.get('name', 'No Description')
        self.comment = self.entry.get('comment')
        self.keywords = self.entry.get('keyword', '').split(',')
        self.offset = int(self.entry['offset'].split(',')[0])
        self.data = [int(i) for i in self.entry['data'].split(',')]
        self.generator = generators.GENERATORS.get(number)
        self._get = getters.GETTERS.get(number)
        if self._get is not None and self.generator is None:
            self.generator = lambda: generators.generic.with_getter(
                self._get, self.offset)

    @property
    def has_getter(self) -> bool:
        """Whether or not this particular sequence has a getter function."""
        return self._get is not None

    @property
    def has_generator(self) -> bool:
        """Whether or not this particular sequence has a generator."""
        return self.generator is not None

    @property
    def retrievable(self) -> bool:
        return self.has_getter or self.has_generator

    def get(self, index: int) -> int:
        """Get an item from the OEIS sequence by its index.
        
        This method only uses a getter function for this sequence.
        :param index: The index of the sequence item to retrieve.
        :returns: The integer corresponding to the input index.
        :raises: NotImplementedError if there is no getter for this sequence.
        :raises: IndexError if the given index is not in the sequence.
        """
        repr_ = repr(self)
        if self._get is None:
            raise NotImplementedError(f'There is no getter for {repr_}.')
        if index < self.offset:
            raise IndexError(INDEX_TOO_SMALL_MSG.format(
                idx=index, offset=self.offset, repr_=repr_
            ))
        return self._get(index)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.number})'

    def __str__(self) -> str:
        return f'A{self.number:06d}: {self.name}'

    def __iter__(self) -> typing.Generator[int, None, None]:
        repr_ = repr(self)
        if self.generator is None:
            raise NotImplementedError(f'There is no generator for {repr_}.')
        return self.generator()

    def __getitem__(self, index: int) -> int:
        try:
            return self.get(index)
        except NotImplementedError:
            pass
        if index - self.offset < len(self.data):
            return self.data[index - self.offset]
        if self.generator is None:
            raise NotImplementedError(
                f'A{self.number:06d} has not yet been implemented.')
        generator = self.generator()
        for i in range(self.offset, index):
            next(generator)
        return next(generator)
