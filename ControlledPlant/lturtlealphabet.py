# vim: fdm=manual
import lsystems
import objload


magnolia = objload.ObjModel("magnolia.obj", 0.01)


# Define Turtle Symbols

class TurtleForward(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.forward(self.amount)
        return [turtles, stack], {}


class TurtleSkip(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.skip(self.amount)
        return [turtles, stack], {}


class TurtleYawLeft(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.yaw_left(self.amount)
        return [turtles, stack], {}


class TurtleYawRight(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.yaw_right(self.amount)
        return [turtles, stack], {}


class TurtlePitchUp(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.pitch_up(self.amount)
        return [turtles, stack], {}


class TurtlePitchDown(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.pitch_down(self.amount)
        return [turtles, stack], {}


class TurtleRollLeft(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.roll_left(self.amount)
        return [turtles, stack], {}


class TurtleRollRight(lsystems.TurtleSymbol):
    def __init__(self, amount=None):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.roll_right(self.amount)
        return [turtles, stack], {}


class TurtlePush(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        stack.append(turtles.clone())
        return [turtles, stack], {}


class TurtlePop(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        turtles = stack.pop()
        return [turtles, stack], {}


class TurtleSetRadius(lsystems.TurtleSymbol):
    def __init__(self, amount):
        self.amount = amount

    def do(self, turtles, stack):
        turtles.set_radius(self.amount)
        return [turtles, stack], {}


class TurtleStartPoly(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        turtles.startpoly()
        return [turtles, stack], {}


class TurtleEndPoly(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        turtles.endpoly()
        return [turtles, stack], {}


class TurtleHoriz(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        turtles.horiz()
        return [turtles, stack], {}


class ConsiderData(lsystems.TurtleSymbol):
    def do(self, turtles, stack):
        turtles.consider_data()
        return [turtles, stack], {}


class TurtleT(TurtleForward):
    pass


class TurtleC(lsystems.TurtleSymbol):
    def __init__(self, nleaves):
        self.nleaves = nleaves


class TurtleInitialL(lsystems.TurtleSymbol):
    pass


class TurtleL(lsystems.TurtleSymbol):
    pass

#
