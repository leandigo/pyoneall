# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase, main

from pyoneall import OneAll
from pyoneall.classes import BadOneAllCredentials, Connections


class TestOneAll(TestCase):
    VALID_CREDENTIALS = {
        'site_name': 'python',
        'public_key': '2d27cffd-1ced-4991-83d1-acce715461e5',
        # I really hope this doesn't Jynx my accounts.
        'private_key': '84d94998-4029-4ac3-be9b-f2825100da6a',
    }

    INVALID_CREDENTIALS = {
        'site_name': 'python',
        'public_key': '01234567-89ab-cdef-0123-456789abcdef',
        'private_key': '01234567-89ab-cdef-0123-456789abcdef',
    }

    def test_00_whether_test_runs(self):
        self.assertTrue(True)

    def test_01_users_list(self):
        auth = OneAll(**self.VALID_CREDENTIALS)
        c = auth.connections()
        self.assertIsInstance(c, Connections)

    def test_02_bad_credentials(self):
        auth = OneAll(**self.INVALID_CREDENTIALS)
        with self.assertRaises(BadOneAllCredentials):
            auth.connections()

    def dont_test_03_swapped_credentials(self):
        kwargs = dict(self.VALID_CREDENTIALS)
        kwargs['private_key'], kwargs['public_key'] = kwargs['public_key'], kwargs['private_key']
        auth = OneAll(**kwargs)
        # How should this result be different from test 02?
        with self.assertRaises(BadOneAllCredentials):
            auth.connections()


if __name__ == '__main__':
    main()
