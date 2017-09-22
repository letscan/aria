# coding: utf-8
"""Form
"""
from itertools import tee


__all__ = ['Form']


class Form(object):
    """Form
    """
    def __init__(self, fields):
        self.fields = fields

    def iter_cases(self, priority=1):
        """Return an iterator

        priority=0: only primary value of each field
        priority=1: good values for one field, primary value for others
        priority=2: good and bad values for one field, primary value for others
        priority=3: good and bad values for all fields
        """
        fields = self.fields.items()
        return iter_cases(fields, priority)

    def list_cases(self, priority=1):
        return list(self.iter_cases(priority))


class NoMoreField(Exception):
    """No more field in ``other``
    """

def iter_cases(fields, priority):
    _, other = list(tee(fields))
    try:
        name, field = next(other)
    except StopIteration:
        raise NoMoreField()
    for value in field.iter_cases(priority):
        try:
            for case in iter_cases(other, priority):
                case.update({name: value})
                yield case
        except NoMoreField:
            yield {name: value}
