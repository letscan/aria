# coding: utf-8
"""Form
"""

__all__ = ['Form']


class Form(object):
    """
    """
    def __init__(self, fields):
        pass

    def iter(self, priority=1):
        pass

    def list(self, priority=1):
        return list(self.iter(priority))
