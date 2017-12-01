# coding: utf-8
"""Walk through the work flow
"""
import logging
import os
import subprocess
from collections import defaultdict, namedtuple


__all__ = ['Flow', 'Step', 'FlowFinished', 'FlowError']


Node = namedtuple('Node', ('case', 'step'))


def setup_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
logger = setup_logger()


class FlowFinished(Exception):
    """Indicate the flow finished without any error
    """


class FlowError(Exception):
    """Indicate the flow is on unexpected situation
    """


class Step(object):
    """Step Base Class
    """
    name = 'Step'

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if name.startswith('_'):
                continue
            if callable(getattr(self, name, None)):
                continue
            setattr(self, name, value)

    def run(self, params):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self)


class Flow(object):
    """Flow of steps
    """
    def __init__(self, first_step):
        self.step = first_step
        self.routes = []

    def trace(self, route):
        self.log(' {} '.format(len(self.routes) + 1).center(40, '='))
        step = self.step
        for case, _ in route:
            self.log(step, case.label)
            step = step.run(case.values)
        return step

    def route_end(self, route):
        self.routes.append(route)

    def walk(self, step=None, route=None, priority=1):
        step = step or self.step
        route = route or []
        need_trace = False
        for case in step.form.iter_cases(priority):
            route_priority = sum(node.case.priority for node in route)
            if case.priority + route_priority > priority:
                continue
            if not self.routes and not route:
                self.log(' 1 '.center(40, '='))
            label = case.label
            if need_trace:
                step = self.trace(route)
            self.log(step, label)
            try:
                new_step = step.run(case.values)
            except FlowFinished as e:
                self.log(e)
                self.route_end(route + [Node(case, e)])
            except FlowError as e:
                self.log(e)
                self.route_end(route + [Node(case, e)])
            except Exception as e:
                logger.exception('Something goes wrong with %s(%s)',
                                                          step, label)
                self.route_end(route + [Node(case, e.__class__.__name__)])
            else:
                route.append(Node(case, new_step))
                self.walk(new_step, route, priority)
            need_trace = True
        try:
            route.pop()
        except IndexError:
            self.log(' THE END '.center(40, '='))

    def log(self, step, label=None, *args, **kwargs):
        msg = str(step)
        if label:
            msg += ' ({})'.format(label)
        logger.info(msg, *args, **kwargs)

    def _merge_routes(self):
        """
        route = [(case, step), ... , (case, FlowError)]
        routes = [route, ... , route]
        graph = [(start_step, end_step, label), ...]
        """
        groups = defaultdict(list)
        for route in self.routes:
            name = ' '.join(str(node.step) for node in route)
            groups[name].append(route)
        graph = []
        for name, group in groups.items():
            start = self.step
            for nodes in zip(*group):
                end = nodes[0].step
                label = ' ---- '.join(set(node.case.label for node in nodes))
                graph.append((start, end, label))
                start = end
        return graph

    def draw(self, graphviz, img_path):
        edges = []  # use list to keep order
        for start, end, label in self._merge_routes():
            edge = '"{}" -> "{}" [ label = "{}" ];\n'.format(
                    Z(start), Z(end), Z(label))
            if edge not in edges:
                edges.append(edge)
        img_dir = os.path.dirname(os.path.realpath(img_path))
        try:
            os.makedirs(img_dir)
        except (IOError, OSError):
            """dir already exists"""
        gv_path = os.path.splitext(img_path)[0] + '.gv'
        font = 'Microsoft Yahei'
        with open(gv_path, 'w', encoding='utf-8') as gv:
            gv.write('digraph {\n')
            gv.write('node [shape="box"];\n')
            gv.write('edge [fontsize="12" fontcolor="blue"];\n')
            gv.writelines(edges)
            gv.write('}')
        _, img_type = os.path.splitext(img_path)
        subprocess.call([graphviz, '-T{}'.format(img_type[1:]),
            '-Efontname={}'.format(font),
            '-Nfontname={}'.format(font),
            '-o' + img_path, gv_path
        ])


def Z(text):
    if not text:
        return text
    text = str(text)
    return '\n'.join(text.split()).replace('\\', '\\\\')
