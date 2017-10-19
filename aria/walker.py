# coding: utf-8
"""Walk around the work flow
"""
import os
import subprocess


__all__ = ['Flow', 'Step', 'FlowFinished', 'FlowError']


class FlowFinished(Exception):
    """Indicate the flow finished without any error
    """


class FlowError(Exception):
    """Indicate the flow is on unexpected situation
    """


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
        self.routes = []

    def trace(self, route):
        step = self.step
        for label, case in route:
            self.log(step, label)
            step = step.run(case)
        return step

    def route_end(self, route):
        self.routes.append(route)
        print(str(len(self.routes)).center(40, '='))

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
            except FlowFinished as e:
                self.log(e)
                self.graph.append((step, e, label))
                self.route_end(route)
                tt = True
            except FlowError as e:
                self.log(e)
                self.graph.append((step, e, label))
                self.route_end(route)
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

    def draw(self, graphviz, img_path):
        edges = []  # use list to keep order
        for start, end, label in self.graph:
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
