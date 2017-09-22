# coding: utf-8
"""Fields
"""
import random
from itertools import chain


ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

__all__ = ['EnumField', 'IntegerField', 'TextField']


class BaseField(object):
    """Base
    """
    def iter(self, priority=1):
        pass


class EnumField(BaseField):
    """Enum
    """
    def __init__(self, values, bad_values):
        self.values = values
        self.bad_values = bad_values

    def iter_cases(self, priority=1):
        if priority == 0:
            return self.values[:1]
        elif priority == 1:
            return iter(self.values)
        else:
            return chain(iter(self.values), iter(self.bad_values))


class IntegerField(BaseField):
    """Integer
    """
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value


class TextField(BaseField):
    """Text
    """
    def __init__(self, min_length, max_length=None, chars=None):
        self.min_length = min_length
        self.max_length = max_length or min_length
        self.chars = chars or ALPHANUM

    def random_text(self):
        length = random.randint(self.min_length, self.max_length)
        text = ''.join(random.choice(self.chars) for _ in range(length))
        return text
