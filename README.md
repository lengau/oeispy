# OEISPy

Python interface for the Online Encyclopedia of Integer Sequences (OEIS).

This provides a simple factory for generating OEIS sequence objects, which will
get the metadata for an OEIS sequence from the OEIS website and will, if 
available, provide a generator or a getter. (If a getter is provided but no
generator is provided, a generator will be wrapped around the getter 
automatically.)

## What is OEIS?

[OEIS](https://oeis.org/), the online encyclopedia of integer sequences, is a
project to collect integer sequences in a single, useful format. Find out more
at the [OEIS Welcome Page](https://oeis.org/wiki/Welcome).

## Usage

OEISPy is designed primarily to be used in an interactive Python shell or
Jupyter notebook to get OEIS sequences. However, a secondary purpose is to allow
programmers who don't have much experience contributing to open source projects
a friendly and easy way to begin. For this reason, this library is intended
to be easy to add getters or generators to. To this end, we intend to provide
easy documentation for beginners. However, this is 
[not yet done](https://github.com/lengau/oeispy/issues/7).