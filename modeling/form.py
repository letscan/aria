# coding: utf-8
"""Form
"""

__all__ = ['Form']


class Form(object):
    """Form
    """
    def __init__(self, fields):
        pass

    def iter_cases(self, priority=1):
        """Return an iterator

        priority=0: only primary value of each field
        priority=1: good values for one field, primary value for others
        priority=2: good and bad values for one field, primary value for others
        priority=3: good and bad values for all fields
        """
        pass

    def list_cases(self, priority=1):
        return list(self.iter_cases(priority))
