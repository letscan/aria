# coding: utf-8
"""Tests for simple forms
"""
import unittest

from modeling import Form, EnumField


class SimpleFormTest(unittest.TestCase):
    """Tests for simple forms
    """
    def test_enum_form(self):
        form = Form({
            'ef1': EnumField([1, 2], [5, 6]),
            'ef2': EnumField([3, 4], [7, 8]),
            'ef3': EnumField([9, 16], [9, 10]),
        })
        for case in form.iter_cases(priority=2):
            print(case)


if __name__ == '__main__':
    unittest.main()
