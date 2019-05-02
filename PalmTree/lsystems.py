# vim: fdm=manual
import random


class TurtleSymbol(object):
    """ Represents a turtle symbol. """
    def __init__(self):
        pass

    def fromString(self, str):
        pass

    def do(self, *args, **kwargs):
        return args, kwargs


def lsystem_evolve(axiom, rules, depth):
    if depth == 0:
        return axiom

    newaxiom = []

    for symbol in axiom:
        for primary, secondary in rules.items():
            if isinstance(symbol, primary):
                newaxiom.extend(secondary(symbol))
                break
        else:
            newaxiom.append(symbol)

    return lsystem_evolve(newaxiom, rules, depth-1)


def lsystem_stochastic_evolve(axiom, rules, depth):
    if depth == 0:
        return axiom

    newaxiom = []

    for symbol in axiom:
        matched = {(prob, secondary) for (prob, primary), secondary in rules if isinstance(symbol, primary)}
        rand = random.random()
        rsum = 0
        for prob, secondary in matched:
            rsum += prob
            if rand < rsum:
                newaxiom.extend(secondary(symbol))
                break
        else:
            newaxiom.append(symbol)

    return lsystem_stochastic_evolve(newaxiom, rules, depth-1)


def doturtle(instructions, *args, **kwargs):
    for instruction in instructions:
        args, kwargs = instruction.do(*args, **kwargs)
