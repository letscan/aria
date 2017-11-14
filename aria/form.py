# coding: utf-8
"""Form
"""
from itertools import tee, product, chain


__all__ = ['Form']


class Case(object):
    """Form Case
    """
    def __init__(self, case):
        self.priority = self._calc_priority([c.priority for _, c in case])
        self.label = ' '.join(c.label for _, c in case)
        self.values = {k: c.value for k, c in case}

    def _calc_priority(self, priorities):
        n_p0 = priorities.count('p0')
        n_p1 = priorities.count('p1')
        n_p2 = priorities.count('p2')
        if n_p0 == len(priorities):
            return 0
        elif n_p1 == 1 and n_p2 == 0:
            return 1
        elif n_p1 == 0 and n_p2 == 1:
            return 2
        else:
            return 3

    def __getitem__(self, key):
        return self.values[key]

    def __str__(self):
        return '(p{})"{}" {}'.format(self.priority, self.label, self.values)


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
        if priority >= 3:
            case_gens.extend(product(*(
                [(key, case) for case in field.iter_cases(['p0', 'p1', 'p2'])]
                for key, field in fields))
            )
        else:
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
        return (Case(case) for case in chain(case_gens))

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
