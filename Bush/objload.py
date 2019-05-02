# vim: fdm=manual
import copy
import math
import mathutils


def rodrigues(vec, axis, sintheta, costheta):
    vec = copy.copy(vec)
    axis = copy.copy(axis)
    return vec*costheta + (axis.cross(vec))*sintheta + axis*(axis.dot(vec))*(1 - costheta)


class ObjModel(object):
    def __init__(self, path=None, scale_factor=1):
        self.vertices = []
        self.faces = []
        self.scale_factor = scale_factor

        self.heading = mathutils.Vector((0, 0, 1))

        if path is not None:
            with open(path) as f:
                self.parse(f.read())

    def parse(self, contents):
        for line in contents.split('\n'):
            parts = line.split(' ')
            if parts[0] == "v":
                self.vertices.append(mathutils.Vector((self.scale_factor*float(parts[1]), self.scale_factor*float(parts[3]), self.scale_factor*float(parts[2]))))
            elif parts[0] == "f":
                self.faces.append([int(parts[1]), int(parts[2]), int(parts[3])])

    def tofaces(self, position, heading):
        faces = []
        costheta = (heading@self.heading) / (heading.length * self.heading.length)
        theta = math.acos(costheta)
        for ogface in self.faces:
            face = []
            for i in ogface:
                vert = self.vertices[i-1]
                vert = rodrigues(vert, heading.cross(self.heading), math.sin(theta), math.cos(theta))
                face.append(position + vert)
            faces.append(face)
        return faces
        # return [map(lambda i: position + self.vertices[i-1], face) for face in self.faces]
