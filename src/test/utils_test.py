'''
Created on Sep 9, 2013

@author: Harold
'''
from unittest import TestCase, main as test_runner
from src.main.utils import stringify_args


class UtilsTest(TestCase):
    def test_stringify_args_handles_positional_arguments(self):
        @stringify_args
        def test_fn(*args):
            for arg in args:
                self.assertIsInstance(arg, str)

        test_fn(3, [], set(), object())

    def test_stringify_args_handles_keyword_arguments(self):
        @stringify_args
        def test_fn(**kwargs):
            for _, v in kwargs.items():
                self.assertIsInstance(v, str)

        test_fn(a=3, b=[], c=set(), d=object())

if __name__ == "__main__":
    test_runner()