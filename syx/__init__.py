from __future__ import absolute_import, division

import platform
import six


if False:
    from typing import Any, Union, Text  # noqa


def ensure_str(str_or_bytes, encoding='utf-8'):
    # type: (Union[Text, bytes], str) -> Text
    """Ensures an input is a string, decoding if it is bytes.
    """
    if not isinstance(str_or_bytes, six.text_type):
        return str_or_bytes.decode(encoding)
    return str_or_bytes


s = ensure_str


def ensure_bytes(str_or_bytes, encoding='utf-8', errors='strict'):
    # type: (Union[Text, bytes], str, str) -> bytes
    """Ensures an input is bytes, encoding if it is a string.
    """
    if isinstance(str_or_bytes, six.text_type):
        return str_or_bytes.encode(encoding, errors)
    return str_or_bytes


b = ensure_bytes


_original_round = round


def bankers_round(value, ndigits=None):
    # type: (Union[float, int], int) -> float
    """Backport of Python 3 implementation of round.
    """
    return_int = False
    if ndigits is None:
        ndigits = 0
        return_int = True
    multiplier = 10 ** ndigits
    large_value = value * multiplier
    remainder = large_value - int(large_value)
    if abs(remainder) == 0.5:
        large_value = ((int(large_value) % 2) * (
            (value > 0) - (value < 0))) + int(large_value)

    result = _original_round(large_value) / multiplier
    if return_int:
        return int(result)
    return result


if not six.PY2:
    hasattr = hasattr
    round = round
else:
    def hasattr(obj, attr_name):
        # type: (Any, str) -> bool
        """Backport of Python 3 implementation of hasattr
        """
        try:
            getattr(obj, attr_name)
        except AttributeError:
            return False
        return True

    if platform.python_implementation() == 'PyPy':
        round = bankers_round
    else:
        try:
            from syx._speedups import bankers_round as round
        except ImportError:
            round = bankers_round
