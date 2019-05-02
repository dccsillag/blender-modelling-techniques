# vim: fdm=manual


class DataPoint(object):
    def __init__(self, point, children=None):
        self.point = point
        if children is None:
            self.children = []
        else:
            self.children = children

    def add_child(self, child):
        self.children.append(child)
