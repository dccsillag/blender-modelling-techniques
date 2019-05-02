# vim: fdm=manual
import copy
import math


def rodriguescs(vec, axis, s, c):
    vec = copy.copy(vec)
    axis = copy.copy(axis)
    return vec*c + (axis.cross(vec))*s + axis*(axis.dot(vec))*(1 - c)


def rodrigues(vec, axis, theta):
    return rodriguescs(vec, axis, math.sin(theta), math.cos(theta))


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


class Turtles(object):
    """ Represents a 3D graphics turtle """
    def __init__(self, proximity_tolerance, leniency, data, turtles, initial_stepsizes=None):
        self.proximity_tolerance = proximity_tolerance
        self.leniency = leniency
        self.data = data
        self.turtles = turtles
        if initial_stepsizes is None:
            self.initial_stepsizes = [turtle.stepsize for turtle in turtles]
        else:
            self.initial_stepsizes = initial_stepsizes

    def clone(self):
        return Turtles(self.proximity_tolerance, self.leniency, copy.copy(self.data), [copy.copy(turtle) for turtle in self.turtles], self.initial_stepsizes)

    def forward(self, amount=None):
        for turtle in self.turtles:
            turtle.forward(amount)

    def skip(self, amount=None):
        for turtle in self.turtles:
            turtle.skip(amount)

    def yaw_right(self, amount=None):
        for turtle in self.turtles:
            turtle.yaw_right(amount)

    def yaw_left(self, amount=None):
        for turtle in self.turtles:
            turtle.yaw_left(amount)

    def pitch_up(self, amount=None):
        for turtle in self.turtles:
            turtle.pitch_up(amount)

    def pitch_down(self, amount=None):
        for turtle in self.turtles:
            turtle.pitch_down(amount)

    def roll_right(self, amount=None):
        for turtle in self.turtles:
            turtle.roll_right(amount)

    def roll_left(self, amount=None):
        for turtle in self.turtles:
            turtle.roll_left(amount)

    def startpoly(self):
        for turtle in self.turtles:
            turtle.startpoly()

    def endpoly(self):
        for turtle in self.turtles:
            turtle.endpoly()

    def horiz(self):
        for turtle in self.turtles:
            turtle.horiz()

    def set_radius(self, amount):
        for turtle in self.turtles:
            turtle.set_radius(amount)

    def consider_data(self):
        newdata = []
        newinitial_stepsizes = []
        newturtles = []

        for data, turtle, initial_stepsize in zip(self.data, self.turtles, self.initial_stepsizes):
            if len(data.children) == 0:
                newdata.append(data)
                turtle.stepsize = initial_stepsize
                newinitial_stepsizes.append(initial_stepsize)
                newturtles.append(turtle)
                continue

            if (data.point - turtle.position).length <= self.proximity_tolerance:
                for child in data.children:
                    newturtle = copy.copy(turtle)
                    newdirection = (child.point - turtle.position).normalized()
                    costheta = turtle.direction.dot(newdirection)
                    sintheta = turtle.direction.cross(newdirection).length
                    axis = newdirection.cross(turtle.direction)
                    newturtle.direction = newdirection
                    newturtle.left = rodriguescs(turtle.left, axis, sintheta, costheta).normalized()
                    newturtle.up = rodriguescs(turtle.up, axis, sintheta, costheta).normalized()
                    newturtle.stepsize = self.leniency*(data.point - turtle.position).length
                    newdata.append(child)
                    newinitial_stepsizes.append(initial_stepsize)
                    newturtles.append(newturtle)
            else:
                newturtle = copy.copy(turtle)
                newdirection = (data.point - turtle.position).normalized()
                costheta = turtle.direction.dot(newdirection)
                sintheta = turtle.direction.cross(newdirection).length
                axis = newdirection.cross(turtle.direction)
                newturtle.direction = newdirection
                newturtle.left = rodriguescs(turtle.left, axis, sintheta, costheta).normalized()
                newturtle.up = rodriguescs(turtle.up, axis, sintheta, costheta).normalized()
                newturtle.stepsize = self.leniency*(data.point - turtle.position).length
                newdata.append(data)
                newinitial_stepsizes.append(initial_stepsize)
                newturtles.append(newturtle)

        self.data = newdata
        self.initial_stepsizes = newinitial_stepsizes
        self.turtles = newturtles
