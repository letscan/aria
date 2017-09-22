# coding: utf-8
"""Walk around the work Step
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

    def __repr__(self):
        return '<{}>'.format(self.name)


class Flow(object):
    """Flow of steps
    """
    graph = []

    def __init__(self, first_step):
        self.step = first_step

    def trace(self, route):
        for step, case in route:
            self.log(step, step.user, case)
            step.run(case)

    def walk(self, step=None, route=None, priority=1):
        step = step or self.step
        route = route or []
        tt = False
        for case in step.form.iter_cases(priority):
            if tt:
                self.trace(route)
            self.log(step, step.user, case)
            try:
                new_step = step.run(case)
            except StepError as e:
                print(e)
            except FlowFinished:
                self.log('流程结束')
                self.graph.append((Step, None))
                print('=' * 40)
                tt = True
            else:
                route.append((step, case))
                self.graph.append((step, new_step))
                self.walk(new_step, route, priority)
                tt = True
        try:
            route.pop()
        except IndexError:
            """All finished"""
        return self.graph

    log = print
