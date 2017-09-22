# coding: utf-8
"""Walk around the work flow
"""
import os
import subprocess


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

    def draw(self, graphviz, img_path):
        edges = []  # use list to keep order
        for start, end, label in self.graph:
            edge = '"{}" -> "{}" [ label = "{}" ];\n'.format(
                    Z(start), Z(end) or '流程结束', Z(label))
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
            gv.write('node [shape=box fontname="{}"];\n'.format(font))
            gv.write('edge [fontname="{}" fontsize="12" fontcolor="blue"];\n'.format(font))
            gv.writelines(edges)
            gv.write('}')
        with open(img_path, 'wb') as img:
            subprocess.call([graphviz, '-Tpng', gv_path], stdout=img)


def Z(text):
    if not text:
        return text
    text = str(text)
    return '\n'.join(text.split()).replace('\\', '\\\\')
