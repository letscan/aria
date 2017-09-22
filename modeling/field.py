# coding: utf-8
"""Fields
"""
import random


ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

__all__ = ['EnumField', 'IntegerField', 'TextField']


class BaseField(object):
    """Base
    """
    def iter_cases(self, include):
        include = include or ['p0', 'p1']
        for key in include:
            provider = getattr(self, key + '_cases', lambda: iter(''))
            for case in provider():
                yield case

    def p0_cases(self):
        raise NotImplementedError()

    def p1_cases(self):
        raise NotImplementedError()

    def p2_cases(self):
        raise NotImplementedError()


class EnumField(BaseField):
    """Enum
    """
    def __init__(self, values, bad_values):
        self.values = values
        self.bad_values = bad_values

    def p0_cases(self):
        return self.values[:1]

    def p1_cases(self):
        return self.values[1:]

    def p2_cases(self):
        return self.bad_values


class IntegerField(BaseField):
    """Integer
    """
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def p0_cases(self):
        return [random.randint(self.min_value + 1, self.max_value - 1)]

    def p1_cases(self):
        return [self.min_value, self.max_value, 0]

    def p2_cases(self):
        return [self.min_value - 1, self.max_value + 1, -1]


class TextField(BaseField):
    """Text
    """
    def __init__(self, min_length, max_length=None, chars=None):
        self.min_length = min_length
        self.max_length = max_length or min_length
        self.chars = chars or ALPHANUM

    def p0_cases(self):
        return [random_text(self.min_length, self.max_length, self.chars)]

    def p1_cases(self):
        return [
            random_text(self.min_length, chars=self.chars),
            random_text(self.max_length, chars=self.chars),
            '',
        ]

    def p2_cases(self):
        return [
            random_text(self.min_length - 1, chars=self.chars),
            random_text(self.max_length + 1, chars=self.chars),
            random_text(self.min_length, self.max_length, chars='"&?%#@*'),
        ]


def random_text(min_length, max_length=None, chars=None):
    min_length = max(min_length, 1)
    max_length = max_length or min_length
    chars = chars or ALPHANUM
    length = random.randint(min_length, max_length)
    text = ''.join(random.choice(chars) for _ in range(length))
    return text
