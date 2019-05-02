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


bl_info = {
    "name": "Procedural Palm Tree Generation Using L-Systems in Blender",
    "author": "Daniel Csillag"
}


# Define the operator

class BushOperator(bpy.types.Operator):
    bl_idname = "mesh.bush_generator"
    bl_label = "Bush Generator"

    depth: bpy.props.IntProperty(name="Depth", min=1, max=10, default=6)
    stepsize: bpy.props.FloatProperty(name="Step Size", default=0.5)
    stepangle: bpy.props.FloatProperty(name="Step Angle", min=0, max=360, default=14.5)
    radius: bpy.props.FloatProperty(name="Radius", default=0.5)
    trunk_length: bpy.props.FloatProperty(name="Trunk Length", min=0, default=5)
    nleaves: bpy.props.IntProperty(name="Number of Leaves", min=1, default=20)
    total_trunk_theta: bpy.props.FloatProperty(name="Total Trunk Inclination", default=30)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def addface(self, *verts):
        i = len(self.vertices)
        for vert in verts:
            self.vertices.append(vert)
        self.faces.append([i+k for k in range(len(verts))])

    def execute(self, context):
        axiom = [la.TurtleT(self.trunk_length), la.TurtleC(self.nleaves)]

        leaves_thetas = []
        tol = 0.05
        for i in range(self.nleaves):
            ok = False
            while not ok:
                newtheta = random.uniform(0, 2*math.pi)
                for theta in leaves_thetas:
                    if abs(theta - newtheta) <= tol:
                        break
                else:
                    ok = True
            leaves_thetas.append(newtheta)

        rules = {
            # + yaw_left
            # - yaw_right
            # & pitch_down
            # ^ pitch_up
            # \ roll_left
            # / roll_right
            # | yaw_left(pi)

            ((1, la.TurtleT), lambda s: [
                la.TurtleT(0.5*s.amount),
                la.TurtleYawRight(math.radians(self.total_trunk_theta) / 2**self.depth),
                la.TurtleT(0.5*s.amount),
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
        }

        instructions = lsystems.lsystem_stochastic_evolve(axiom, rules, self.depth)

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
