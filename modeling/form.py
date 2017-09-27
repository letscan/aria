# coding: utf-8
"""Form
"""
from itertools import tee, product, chain


__all__ = ['Form']


class Form(object):
    """Form
    """
    def __init__(self, fields):
        self.fields = fields

    def iter_cases(self, priority=1):
        """Return an iterator

        priority=0: only p0 values of each field
        priority=1: p0 + p1 values for one field, p0 values for others
        priority=2: p0 + p1 + p2 values for one field, p0 values for others
        priority=3: p0 + p1 + p2 values for all fields
        """
        priority = max(0, priority)
        fields = self.fields.items()
        #return iter_cases(fields, priority)
        case_gens = []
        if priority >= 0:
            case_gens.extend(product(*(
                [(key, case) for case in field.iter_cases(['p0'])]
                for key, field in fields))
            )
        if priority >= 1:
            # def p1():
            #     for name in self.fields.keys():
            #         for case in product(*([(key, case)
            #                                for case in field.iter_cases(1 if key == name else 0)]
            #                               for key, field in fields)):
            #             yield case
            # cases = p1()
            for name in self.fields.keys():
                case_gens.extend(product(*(
                    [(key, case) for case in field.iter_cases(
                                            ['p1' if key == name else 'p0'])]
                    for key, field in fields))
                )
        if priority >= 2:
            for name in self.fields.keys():
                case_gens.extend(product(*(
                    [(key, case) for case in field.iter_cases(
                                            ['p2' if key == name else 'p0'])]
                    for key, field in fields
                )))
        if priority >= 3:
            case_gens.extend(product(*(
                [(key, case) for case in field.iter_cases(['p1', 'p2'])]
                for key, field in fields))
            )
        return (reform(case) for case in chain(case_gens))

    def list_cases(self, priority=1):
        return list(self.iter_cases(priority))


def reform(case):
    kvs = {k: v for k, (n, v) in case}
    name = ' '.join(n for k, (n, v) in case)
    return name, kvs

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
