'''
Created on Sep 9, 2013

@author: Harold
'''
import types
from functools import reduce
from unittest import TestCase, main as test_runner
from src.main.pic_parser import create_pic_mutator_fns

def _run(fn_list, value):
    return reduce(lambda x, fn: fn(x), fn_list, value)

class MutatorFns88ValuesTest(TestCase):
    def test_pic_parser_creates_regex_validator_for_88_type(self):
        fns = create_pic_mutator_fns(['A', 'B'])

        self.assertIsInstance(fns, list)
        self.assertIs(len(fns), 1)
        self.assertIsInstance(fns.pop(), types.FunctionType)

    def test_pic_parser_raises_value_error_when_multiple_values_not_same_length(self):
        values = ['A', 'AA']
        self.assertRaisesRegex(ValueError, 'A, AA', create_pic_mutator_fns, values)

    def test_pic_parser_regex_validator_returns_unchanged_value_for_valid_input(self):
        valid_value = 'A'
        sut = create_pic_mutator_fns([valid_value])

        output_val = _run(sut, valid_value)

        self.assertEqual(output_val, valid_value)

    def test_pic_parser_regex_validator_handles_multiple_possible_values(self):
        valid_values = ['A', 'B']
        sut = create_pic_mutator_fns(valid_values)

        for test_value in valid_values:
            output_val = _run(sut, test_value)
            self.assertEqual(output_val, test_value)

    def test_pic_parser_regex_validator_casts_input_to_string_when_coerce(self):
        valid_values = ['1']
        sut = create_pic_mutator_fns(valid_values, coerce=True)

        output_val = _run(sut, 1)
        self.assertEqual(output_val, valid_values[0])

    def test_pic_parser_regex_validator_raises_value_error_given_invalid_option(self):
        valid_values = ['A']
        sut = create_pic_mutator_fns(valid_values)
        self.assertRaisesRegex(ValueError, '^B ', _run, sut, 'B')


if __name__ == "__main__":
    test_runner()