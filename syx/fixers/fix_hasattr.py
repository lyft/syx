from __future__ import absolute_import

from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import, is_probably_builtin


class FixHasattr(fixer_base.BaseFix):
    """Fixer to use syx.hasattr instead of the built in hasattr method
    """
    BM_compatible = True
    order = "pre"

    skip_on = "syx.hasattr"

    PATTERN = """
    power<
        'hasattr'
        trailer< '('
            (
                arglist<arg1=any ',' arg2=any> |
                arg1=any
            )
        ')' >
    >
    """

    def transform(self, node, results):
        if is_probably_builtin(node):
            arg1 = results['arg1']
            if 'arg2' not in results:
                is_kwarg_expansion = (arg1.type == self.syms.argument and
                                      arg1.children[0].value == '**')
                if arg1.type != self.syms.star_expr and not is_kwarg_expansion:
                    return
            touch_import('syx', 'hasattr', node)
            return node
