syx
===

Python 2 and 3 compatibility library from Lyft.  Pronounced "Six with a Y".

``syx`` builds off of the ubiquitous
`six <https://github.com/benjaminp/six>`__ library, backporting some behavior
from Python 3 to Python 2 and includes some helper methods for handling
``bytes`` and ``str`` differences between Python 2 and Python 3.

Bytes vs. strings
-----------------

Python 3 splits up strings and bytes into separate data types. To go
from bytes to a string, you must decode. To go from a string to bytes,
you must encode. These changes propagated through the standard library.
For example, in `Python 2
b64encode <https://docs.python.org/2/library/base64.html>`__ accepted a
string and returned a string, whereas `Python 3's
b64encode <https://docs.python.org/3.6/library/base64.html>`__ requires
a bytes-like object and returns bytes. Dealing with these small changes
can be arduous as mentioned during a `PyCon 2017
Keynote <https://youtu.be/66XoCk79kjM?t=1828>`__, so ``syx`` includes
two helper methods, ``ensure_bytes`` (aliased as ``b``) and
``ensure_str`` (aliased as ``s``). ``ensure_bytes`` converts it's input
to ``bytes`` if needed, ``ensure_str`` converts it's input to a string
if needed.

For example, say we have a function ``encode_value_as_b64_str`` that
accepts a value that could be a string or bytes and returns a base64
encoded string. Using ``syx``, this function can be written as:

.. code:: python

    from base64 import b64encode
    from syx import b, s

    def encode_value_as_b64_str(value):
      return s(b64encode(b(value)))

Rounding
--------

Python 3 changed the default rounding implementation from "Round away
from 0" to "Banker's Rounding". As the name implies, banker's rounding
is the internationally accepted way of rounding numbers for financial
transactions. The main difference is instead of always rounding up
during a tie (which introduces a slight skew upwards in your data)
banker's rounding rounds towards the nearest even. So, for example,
rounding both ``1.5`` and ``2.5`` will result in ``2``. While this is
not what's taught in grade school, it is more accurate.

As a concrete example:

.. code:: python

    import numpy as np
    from syx import round

    def bad_round(num):
        return int(num + .5)

    count = int(1e6)
    values = np.random.randint(101, size=count) / 10
    real_mean = sum(values) / count
    py3_rounded_mean = sum(round(x) for x in values) / count
    py2_rounded_mean = sum(bad_round(x) for x in values) / count

    print('actual %f' % real_mean)
    print('py3 round: %f, error: %f' % (py3_rounded_mean, abs(real_mean - py3_rounded_mean)))
    print('py2 round: %f, error: %f' % (py2_rounded_mean, abs(real_mean - py2_rounded_mean)))

::

    actual 4.998499
    py3 round: 4.998387, error: 0.000112
    py2 round: 5.048665, error: 0.050166

The old rounding method predictably introduces a 1% error upwards.
``syx`` ships an implementation of banker's rounding in Cython so it's
as fast or faster than the built in rounding method.

hasattr
-------

As has been observed by others, ``hasattr`` in Python 2 can dangerously
hide bugs. Some would even say that `hasattr is Considered
Harmful <https://hynek.me/articles/hasattr/>`__. ``syx`` ships a
backport of Python 3's ``hasattr`` behavior.

.. code:: python

    from syx import hasattr

    class GoesBoom(object):
          @property
          def boom(self):
              raise Exception('Oh Noes!')

    hasattr(GoesBoom(), 'boom')  # Now properly raises an Exception


Fixers
======

``syx`` ships with some ``lib2to3`` fixers to automatically start using
the Python 3 backports of ``round`` and ``hasattr``. You can run these
fixers with
`python-modernize <https://github.com/python-modernize/python-modernize>`__,
for example:

::

    python-modernize -w -f syx.fixers.fix_hasattr -f syx.fixers.fix_round ...
