# vim: fdm=manual
import os, sys
sys.path.append(os.getcwd())
import math
import random
import bpy
import mathutils
import lturtle
import lsystems
import lturtlealphabet as la
import datamanager as dt


bl_info = {
    "name": "Controlled Procedural Plant Generation Using L-Systems in Blender",
    "author": "Daniel Csillag"
}


def factorial(n):
    out = 1
    for i in range(1, n+1):
        out *= i
    return out


def choose(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))


def bezier_data(nts, *ps):
    n = len(ps) - 1

    def b(t):
        p_out = mathutils.Vector((0, 0, 0))
        for i in range(n+1):
            p_out = p_out + (choose(n, i) * (1-t)**(n-i) * t**i * ps[i])
        return p_out

    data = dt.DataPoint(ps[-1])
    step_t = 1 / nts
    for i in reversed(list(range(nts))):
        newdata = dt.DataPoint(b(i*step_t))
        newdata.add_child(data)
        data = newdata

    return data


def data_from_list(lst):
    return [dt.DataPoint(point, data_from_list(children)) for point, children in lst]


nleaves = 12
trunk_length = 6
depth = 6

leaves_thetas = []
tol = 0.05
for i in range(nleaves):
    ok = False
    while not ok:
        newtheta = random.uniform(0, 2*math.pi)
        for theta in leaves_thetas:
            if abs(theta - newtheta) <= tol:
                break
        else:
            ok = True
    leaves_thetas.append(newtheta)


# Define the operator

class BushOperator(bpy.types.Operator):
    bl_idname = "mesh.bush_generator"
    bl_label = "Bush Generator"

    axiom = [la.TurtleT(trunk_length), la.TurtleC(nleaves)]
    rules = [
        # + yaw_left
        # - yaw_right
        # & pitch_down
        # ^ pitch_up
        # \ roll_left
        # / roll_right
        # | yaw_left(pi)

        ((1, la.TurtleT), lambda s: [
            # la.TurtleT(0.5*s.amount),
            la.TurtleT(),
            la.ConsiderData(),
            la.TurtleT(),
            # la.TurtleT(0.5*s.amount),
        ]),
        ((1, la.TurtleC), lambda s: [la.TurtlePitchDown(0.5*math.pi)] + sum([
            [
                la.TurtleYawRight(theta),
                la.TurtlePush(),
                la.TurtleInitialL(),
                la.TurtlePop(),
            ] for theta in leaves_thetas
        ], [])),
        ((0.33, la.TurtleInitialL), lambda s: [
            la.TurtlePitchDown(),
            la.TurtleForward(),
            la.TurtlePush(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtlePush(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtleL(),
        ]),
        ((0.33, la.TurtleInitialL), lambda s: [
            la.TurtlePitchUp(),
            la.TurtleForward(),
            la.TurtlePush(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtlePush(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtleL(),
        ]),
        ((0.34, la.TurtleInitialL), lambda s: [
            la.TurtlePitchUp(),
            la.TurtlePitchUp(),
            la.TurtlePitchUp(),
            # la.TurtlePush(),
            # la.TurtleYawLeft(),
            # la.TurtleYawLeft(),
            # la.TurtleYawLeft(),
            # la.TurtleForward(),
            # la.TurtlePop(),
            # la.TurtlePush(),
            # la.TurtleYawRight(),
            # la.TurtleYawRight(),
            # la.TurtleYawRight(),
            # la.TurtleForward(),
            # la.TurtlePop(),
            la.TurtleL(),
        ]),
        ((1, la.TurtleL), lambda s: [
            la.TurtlePitchDown(),
            la.TurtleForward(),
            la.TurtlePush(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleYawLeft(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtlePush(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleYawRight(),
            la.TurtleForward(),
            la.TurtlePop(),
            la.TurtleL(),
        ]),
    ]

    depth: bpy.props.IntProperty(name="Depth", min=1, max=10, default=5)
    stepsize: bpy.props.FloatProperty(name="Step Size", default=0.5)
    stepangle: bpy.props.FloatProperty(name="Step Angle", min=0, max=360, default=22.5)
    radius: bpy.props.FloatProperty(name="Radius", default=0.1)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def addface(self, *verts):
        i = len(self.vertices)
        for vert in verts:
            self.vertices.append(vert)
        self.faces.append([i+k for k in range(len(verts))])

    def execute(self, context):
        instructions = lsystems.lsystem_stochastic_evolve(self.axiom, self.rules, self.depth)

        self.vertices = []
        self.faces = []
        turtle = lturtle.Turtle(mathutils.Vector((0, 0, 0)),
                                mathutils.Vector((0, 0, 1)),
                                mathutils.Vector((0, 1, 0)),
                                mathutils.Vector((1, 0, 0)),
                                self.stepsize,
                                math.radians(self.stepangle),
                                self.radius,
                                self.addface)
        data = data_from_list([
            (mathutils.Vector((0, 0, 0)), [
                (mathutils.Vector((0, 0, 5)), [
                    (mathutils.Vector((-5, 0, 0)), []),
                    (mathutils.Vector(( 5, 0, 0)), []),
                ])
            ])
        ])
        turtles = lturtle.Turtles(0.1, 0.5, data, [turtle])

        lsystems.doturtle(instructions, turtles, [])

        # Generate the mesh from (vertices, faces)
        mesh = bpy.data.meshes.new("Generated")
        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.update()
        obj = bpy.data.objects.new("Generated", mesh)
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(state=True)
        context.view_layer.objects.active = obj

        return {"FINISHED"}


# Registering and stuff

def menu_func(self, context):
    self.layout.operator(BushOperator.bl_idname)


def register():
    bpy.utils.register_class(BushOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(BushOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
