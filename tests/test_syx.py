# -*- coding: UTF-8 -*-

import pytest

from syx import b, ensure_bytes, ensure_str, hasattr, bankers_round, round, s


def test_b_alias():
    assert b == ensure_bytes


def test_ensure_bytes():
    assert b'hello' == ensure_bytes(b'hello')
    assert b'hello' == ensure_bytes('hello')
    assert b'\xff\xfeS0\x930k0a0o0' == ensure_bytes(
        b'\xff\xfeS0\x930k0a0o0'.decode('utf-16'), 'utf-16')
    assert b'' == ensure_bytes(b'\xff\xfeS0\x930k0a0o0'.decode('utf-16'),
                               'ascii', 'ignore')


def test_ensure_str():
    assert 'hello' == ensure_str(b'hello')
    assert 'hello' == ensure_str(u'hello')
    assert 'hello' == ensure_str(b'hello', 'utf-8')
    assert 'hello' == ensure_str('hello')
    assert b'\xff\xfeS0\x930k0a0o0'.decode('utf-16') == ensure_str(
        b'\xff\xfeS0\x930k0a0o0', 'utf-16')


def test_s_alias():
    assert s == ensure_str


@pytest.mark.parametrize('round_method', [round, bankers_round])
def test_round(round_method):
    assert round_method(0.5) == 0
    assert round_method(-0.5) == 0
    assert round_method(1.5) == 2
    assert round_method(-1.5) == -2
    assert round_method(2.5) == 2
    assert round_method(-2.5) == -2
    assert round_method(2.51) == 3
    assert round_method(-2.51) == -3
    assert isinstance(round_method(2.5), int)
    assert isinstance(round_method(2.5, 0), float)
    assert isinstance(round_method(2.52525, 1), float)


def test_hasattr():
    class GoesBoom(object):
        @property
        def ok(self):
            return True

        @property
        def foo(self):
            raise Exception('Oh Noes!')

        def __getattr__(self, item):
            if item == 'boom':
                raise Exception('boom')
            if item != 'dynamic':
                raise AttributeError
            return True

    assert hasattr(GoesBoom(), 'ok')
    assert hasattr(GoesBoom(), 'dynamic')
    assert not hasattr(GoesBoom(), 'bar')
    with pytest.raises(Exception, message='Oh Noes!'):
        hasattr(GoesBoom(), 'foo')
    with pytest.raises(Exception, message='boom'):
        hasattr(GoesBoom(), 'boom')
