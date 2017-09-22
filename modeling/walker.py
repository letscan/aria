# coding: utf-8
"""Walk around the work flow
"""


class FlowFinished(Exception):
    pass


class StepError(Exception):
    pass


class LoginError(StepError):
    pass


class SubmitError(StepError):
    pass


class Step(object):
    """Step Base Class
    """
    def __init__(self, name):
        self.name = name

    def run(self, params):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}>'.format(self.name)


class Flow(object):
    """Flow of steps
    """
    graph = []

    def __init__(self, first_step):
        self.step = first_step

    def trace(self, route):
        step = self.step
        for label, case in route:
            self.log(step, label)
            step = step.run(case)
        return step

    def walk(self, step=None, route=None, priority=1):
        step = step or self.step
        route = route or []
        tt = False
        for label, case in step.form.iter_cases(priority):
            if tt:
                step = self.trace(route)
            self.log(step, label)
            try:
                new_step = step.run(case)
            except StepError as e:
                print(e)
            except FlowFinished:
                self.log('流程结束')
                self.graph.append((step, None, label))
                print('=' * 40)
                tt = True
            else:
                route.append((label, case))
                self.graph.append((step, new_step, label))
                self.walk(new_step, route, priority)
                tt = True
        try:
            route.pop()
        except IndexError:
            """All finished"""
        return self.graph

    log = print
