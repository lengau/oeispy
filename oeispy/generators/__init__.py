"""Generators for OEIS sequences.
"""

import itertools

from . import from_site
from . import generic

__all__ = ['GENERATORS']

GENERATORS = {
    2: from_site.kolakoski,
    4: lambda: itertools.repeat(0),
    7: lambda: itertools.chain([1], itertools.repeat(0)),
    12: lambda: itertools.repeat(1),
    27: lambda: itertools.count(1),
    45: lambda: generic.lucas(0, 1),
}
