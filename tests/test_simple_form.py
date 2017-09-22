# coding: utf-8
"""Tests for simple forms
"""
import unittest

from modeling import Form, EnumField, IntegerField, TextField


class SimpleFormTest(unittest.TestCase):
    """Tests for simple forms
    """
    def test_enum_form(self):
        form = Form({
            'ef': EnumField([('v1', 1), ('v2', 2)], [('v5', 5), ('v6', 6)]),
            'nf': IntegerField(4, 9),
            'tf': TextField(3, 8, 'abcdef'),
        })
        for case in form.iter_cases(priority=1):
            print(case)


if __name__ == '__main__':
    unittest.main()
