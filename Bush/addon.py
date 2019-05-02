# vim: fdm=manual
import os, sys
sys.path.append(os.getcwd())
import math
import bpy
import mathutils
import lturtle
import lsystems
import lturtlealphabet as la


bl_info = {
    "name": "Procedural Bush Generation Using L-Systems in Blender",
    "author": "Daniel Csillag"
}


# Define the operator

class BushOperator(bpy.types.Operator):
    bl_idname = "mesh.bush_generator"
    bl_label = "Bush Generator"

    axiom = [la.TurtleA()]
    rules = [
        # + yaw_left
        # - yaw_right
        # & pitch_down
        # ^ pitch_up
        # \ roll_left
        # / roll_right
        # | yaw_left(pi)

        ((0.34, la.TurtleA), lambda _: [
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleForward(),         # F
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleForward(),         # F
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtlePush(),            # [
            la.TurtleForward(),         # F
            la.TurtleB(),               # B
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
        ]),
        ((0.33, la.TurtleA), lambda _: [
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleForward(),         # F
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtlePush(),            # [
            la.TurtleForward(),         # F
            la.TurtleB(),               # B
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
        ]),
        ((0.33, la.TurtleA), lambda _: [
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleForward(),         # F
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtlePush(),            # [
            la.TurtlePitchDown(),       # &
            la.TurtleL(),               # L
            la.TurtleA(),               # A
            la.TurtlePop(),             # ]
        ]),
        ((1, la.TurtleForward), lambda _: [
            la.TurtleS(),               # S
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleRollRight(),       # /
            la.TurtleForward(),         # F
        ]),
        ((1, la.TurtleS), lambda _: [
            la.TurtleForward(),         # F
            la.TurtleL(),               # L
        ]),
        ((1, la.TurtleL), lambda _: [
            la.TurtlePush(),            # [
            la.TurtlePitchUp(),         # ^
            la.TurtlePitchUp(),         # ^
            la.TurtleStartPoly(),       # {
            la.TurtleYawRight(),        # -
            la.TurtleSkip(),            # f
            la.TurtleYawLeft(),         # +
            la.TurtleSkip(),            # f
            la.TurtleYawLeft(),         # +
            la.TurtleSkip(),            # f
            la.TurtleYawRight(),        # -
            la.TurtleYawLeft(math.pi),  # |
            la.TurtleYawRight(),        # -
            la.TurtleSkip(),            # f
            la.TurtleYawLeft(),         # +
            la.TurtleSkip(),            # f
            la.TurtleYawLeft(),         # +
            la.TurtleSkip(),            # f
            la.TurtleEndPoly(),         # }
            la.TurtlePop(),             # ]
        ]),
        ((1, la.TurtleB), lambda _: [
            la.TurtlePush(),            # [
            la.TurtleYawRight(),        # -
            la.TurtleForward(),         # F
            la.TurtleFlower(),          # Flower
            la.TurtlePop(),             # ]
        ]),
    ]

    depth: bpy.props.IntProperty(name="Depth", min=1, max=10, default=7)
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

        lsystems.doturtle(instructions, turtle, [])

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
