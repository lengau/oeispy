"""Generators for OEIS sequences.
"""

import itertools

from . import from_site
from . import generic

__all__ = ['GENERATORS']

GENERATORS = {
    # Note: It is only necessary to provide a generator when there is no getter
    # or the generator would be significantly more efficient than the getter.
    2: from_site.kolakoski,
    45: lambda: generic.lucas(0, 1),
}
