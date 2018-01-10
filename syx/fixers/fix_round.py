# Adopted from 2to3's `fix_intern`:
# https://github.com/python/cpython/blob/master/Lib/lib2to3/fixes/fix_intern.py

from __future__ import absolute_import

from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import, is_probably_builtin


class FixRound(fixer_base.BaseFix):
    """Fixer to use syx.round instead of the builtin round method.
    """
    BM_compatible = True
    order = "pre"

    skip_on = "syx.round"

    PATTERN = """
    power<
        'round'
        trailer< '(' any ')' >
    >
    """

    def transform(self, node, results):
        if is_probably_builtin(node):
            touch_import('syx', 'round', node)
            return node
