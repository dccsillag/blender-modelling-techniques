# vim: fdm=manual
import copy
import math


def rodrigues(vec, axis, theta):
    vec = copy.copy(vec)
    axis = copy.copy(axis)
    return vec*math.cos(theta) + (axis.cross(vec))*math.sin(theta) + axis*(axis.dot(vec))*(1 - math.cos(theta))


class Turtle(object):
    """ Represents a 3D graphics turtle """
    def __init__(self, position, direction, up, left, stepsize, stepangle, radius, addface):
        self.position = position
        self.direction = direction
        self.up = up
        self.left = left
        self.stepsize = stepsize
        self.stepangle = stepangle
        self.radius = radius
        self.addface = addface

        self.inpoly = False
        self.polyverts = []

    def forward(self, amount=None):
        if amount is None:
            direction = self.stepsize*self.direction
        else:
            direction = amount*self.direction

        north = self.position - self.radius*self.up
        east = self.position - self.radius*self.left
        south = self.position + self.radius*self.up
        west = self.position + self.radius*self.left

        self.addface(north, north + direction, east + direction, east)
        self.addface(east, east + direction, south + direction, south)
        self.addface(south, south + direction, west + direction, west)
        self.addface(west, west + direction, north + direction, north)

        self.position = self.position + direction

        if self.inpoly:
            self.polyverts.append(self.position)

    def skip(self, amount=None):
        if amount is None:
            direction = self.stepsize*self.direction
        else:
            direction = amount*self.direction

        self.position = self.position + direction

        if self.inpoly:
            self.polyverts.append(self.position)

    def yaw_right(self, amount=None):
        if amount is None:
            theta = self.stepangle
        else:
            theta = amount

        self.direction = rodrigues(self.direction, self.up, theta)
        self.left = rodrigues(self.left, self.up, theta)

    def yaw_left(self, amount=None):
        if amount is None:
            theta = -self.stepangle
        else:
            theta = -amount

        self.direction = rodrigues(self.direction, self.up, theta)
        self.left = rodrigues(self.left, self.up, theta)

    def pitch_up(self, amount=None):
        if amount is None:
            theta = self.stepangle
        else:
            theta = amount

        self.direction = rodrigues(self.direction, self.left, theta)
        self.up = rodrigues(self.up, self.left, theta)

    def pitch_down(self, amount=None):
        if amount is None:
            theta = -self.stepangle
        else:
            theta = -amount

        self.direction = rodrigues(self.direction, self.left, theta)
        self.up = rodrigues(self.up, self.left, theta)

    def roll_right(self, amount=None):
        if amount is None:
            theta = self.stepangle
        else:
            theta = amount

        self.up = rodrigues(self.up, self.direction, theta)
        self.left = rodrigues(self.left, self.direction, theta)

    def roll_left(self, amount=None):
        if amount is None:
            theta = -self.stepangle
        else:
            theta = -amount

        self.up = rodrigues(self.up, self.direction, theta)
        self.left = rodrigues(self.left, self.direction, theta)

    def startpoly(self):
        self.inpoly = True
        self.polyverts = [self.position]

    def endpoly(self):
        self.addface(*self.polyverts)
        self.inpoly = False

    def horiz(self):
        self.up = self.direction.cross(self.left)
        self.left = (self.left.cross(self.direction)).normalized()

    def set_radius(self, amount):
        self.radius = amount
