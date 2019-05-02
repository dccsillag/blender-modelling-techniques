# vim: fdm=manual
import copy
import lsystems


# Define Turtle Symbols

class TurtleForward(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.forward(self.amount)
        return [turtle, stack], {}


class TurtleSkip(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.skip(self.amount)
        return [turtle, stack], {}


class TurtleYawLeft(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.yaw_left(self.amount)
        return [turtle, stack], {}


class TurtleYawRight(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.yaw_right(self.amount)
        return [turtle, stack], {}


class TurtlePitchUp(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.pitch_up(self.amount)
        return [turtle, stack], {}


class TurtlePitchDown(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.pitch_down(self.amount)
        return [turtle, stack], {}


class TurtleRollLeft(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.roll_left(self.amount)
        return [turtle, stack], {}


class TurtleRollRight(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.roll_right(self.amount)
        return [turtle, stack], {}


class TurtlePush(lsystems.TurtleSymbol):
    def do(self, turtle, stack):
        stack.append(copy.copy(turtle))
        return [turtle, stack], {}


class TurtlePop(lsystems.TurtleSymbol):
    def do(self, turtle, stack):
        turtle = stack.pop()
        return [turtle, stack], {}


class TurtleSetRadius(lsystems.TurtleSymbol):
    def __init__(self, amount):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.set_radius(self.amount)
        return [turtle, stack], {}


class TurtleStartPoly(lsystems.TurtleSymbol):
    def do(self, turtle, stack):
        turtle.startpoly()
        return [turtle, stack], {}


class TurtleEndPoly(lsystems.TurtleSymbol):
    def do(self, turtle, stack):
        turtle.endpoly()
        return [turtle, stack], {}


class TurtleHoriz(lsystems.TurtleSymbol):
    def do(self, turtle, stack):
        turtle.horiz()
        return [turtle, stack], {}


class TurtleT(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtle, stack):
        turtle.forward(self.amount)
        return [turtle, stack], {}


class TurtleC(lsystems.TurtleSymbol):
    def __init__(self, nleaves):
        self.nleaves = nleaves


class TurtleInitialL(lsystems.TurtleSymbol):
    pass


class TurtleL(lsystems.TurtleSymbol):
    pass

#
