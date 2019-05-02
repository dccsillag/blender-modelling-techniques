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
    "name": "Procedural Tree Generation Using L-Systems in Blender",
    "author": "Daniel Csillag"
}


r_1 = 0.9
r_2 = 0.8
a_0 = math.radians(45)
a_2 = math.radians(45)
d = math.radians(137.5)


# Define the operator

class BushOperator(bpy.types.Operator):
    bl_idname = "mesh.bush_generator"
    bl_label = "Bush Generator"

    axiom = [la.TurtleA(1)]
    rules = {
        # + yaw_left
        # - yaw_right
        # & pitch_down
        # ^ pitch_up
        # \ roll_left
        # / roll_right
        # | yaw_left(pi)

        (1, la.TurtleA): lambda s: [
            la.TurtleForward(s.l),          # F(l)
            la.TurtlePush(),                # [
            la.TurtlePitchDown(a_0),        # &(a_0)
            la.TurtleB(s.l*r_2),            # B(l*r_2)
            la.TurtlePop(),                 # ]
            la.TurtleRollRight(d),          # /(d)
            la.TurtleA(s.l*r_1),            # A(l*r_1)
        ],
        (1, la.TurtleB): lambda s: [
            la.TurtleForward(s.l),          # F(l)
            la.TurtlePush(),                # [
            la.TurtleYawRight(a_2),         # -(a_2)
            la.TurtleHoriz(),               # $
            la.TurtleC(s.l*r_2),            # C(l*r_2)
            la.TurtlePop(),                 # ]
            la.TurtleC(s.l*r_1),            # C(l*r_1)
        ],
        (1, la.TurtleC): lambda s: [
            la.TurtleForward(s.l),          # F(l)
            la.TurtlePush(),                # [
            la.TurtleYawLeft(a_2),          # +(a_2)
            la.TurtleHoriz(),               # $
            la.TurtleB(s.l*r_2),            # B(l*r_2)
            la.TurtlePop(),                 # ]
            la.TurtleB(s.l*r_1),            # B(l*r_1)
        ]
    }

    depth: bpy.props.IntProperty(name="Depth", min=1, max=10, default=10)
    stepsize: bpy.props.FloatProperty(name="Step Size", default=1)
    stepangle: bpy.props.FloatProperty(name="Step Angle", min=0, max=360, default=22.5)
    radius: bpy.props.FloatProperty(name="Radius", default=0.5)

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
                                0.1,
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
