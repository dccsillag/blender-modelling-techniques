# vim: fdm=manual
import os, sys
sys.path.append(os.getcwd())
import math
import random
import bpy
import mathutils


bl_info = {
    "name": "Vase Generation Using Revolution Surfaces in Blender",
    "author": "Daniel Csillag"
}


# Bezier Function

def factorial(n):
    out = 1
    for i in range(1, n+1):
        out *= i
    return out


def choose(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))


def bezier_n(n, t, *ps):
    p_out = mathutils.Vector((0, 0, 0))
    for i in range(n+1):
        p_out = p_out + (choose(n, i) * (1-t)**(n-i) * t**i * ps[i])
    return p_out


# Define the operator

class VaseOperation(bpy.types.Operator):
    bl_idname = "mesh.vase_generator"
    bl_label = "Vase Generator"

    degree: bpy.props.IntProperty(name="Bezier Curve Degree", min=2, default=3)
    radiusinit: bpy.props.FloatProperty(name="Initial Radius Step", default=3)
    radiusmin: bpy.props.FloatProperty(name="Minimum Radius Step", default=-3)
    radiusmax: bpy.props.FloatProperty(name="Minimum Radius Step", default=3)
    heightmin: bpy.props.FloatProperty(name="Minimum Height", default=2)
    heightmax: bpy.props.FloatProperty(name="Minimum Height", default=4)
    nrotations: bpy.props.IntProperty(name="Number of rotations", min=3, default=60)
    nts: bpy.props.IntProperty(name="Number of samples", min=2, default=40)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        vertices = []
        faces = []

        # f = lambda t: bezier_n(2, t, mathutils.Vector((0, 0, 0)), mathutils.Vector((3, 0, 0)), mathutils.Vector((3, 0, 3)))
        # f = lambda t: bezier_n(3, t, mathutils.Vector((0, 0, 0)), mathutils.Vector((3, 0, 0)), mathutils.Vector((1, 0, 3)), mathutils.Vector((3, 0, 5)))

        height_incrs = [random.uniform(self.heightmin, self.heightmax) for _ in range(self.degree - 1)]
        radius_diffs = [random.uniform(self.radiusmin, self.radiusmax) for _ in range(self.degree - 1)]
        ps = [mathutils.Vector((0, 0, 0)), mathutils.Vector((self.radiusinit, 0, 0))]
        for i in range(self.degree-1):
            p = ps[-1]
            ps.append(p + mathutils.Vector((radius_diffs[i], 0, height_incrs[i])))
        f = lambda t: bezier_n(self.degree, t, *ps)

        vi = 0
        rotation_step = 2*math.pi / self.nrotations
        t_step = 1 / self.nts
        for i in range(self.nrotations):
            # for t in range(self.nts):
            for j in range(self.nts):
                v0 = f(j*t_step)
                v1 = f(j*t_step)
                v2 = f((j+1)*t_step)
                v3 = f((j+1)*t_step)
                v0.rotate(mathutils.Euler((0, 0, i*rotation_step), 'XYZ'))
                v1.rotate(mathutils.Euler((0, 0, (i+1)*rotation_step), 'XYZ'))
                v2.rotate(mathutils.Euler((0, 0, (i+1)*rotation_step), 'XYZ'))
                v3.rotate(mathutils.Euler((0, 0, i*rotation_step), 'XYZ'))
                vertices.append(v0)
                vertices.append(v1)
                vertices.append(v2)
                vertices.append(v3)
                faces.append([vi, vi+1, vi+2, vi+3])
                vi += 4

        # Generate the mesh from (vertices, faces)
        mesh = bpy.data.meshes.new("Generated")
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        obj = bpy.data.objects.new("Generated", mesh)
        context.collection.objects.link(obj)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(state=True)
        context.view_layer.objects.active = obj

        return {"FINISHED"}


# Registering and stuff

def menu_func(self, context):
    self.layout.operator(VaseOperation.bl_idname)


def register():
    bpy.utils.register_class(VaseOperation)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(VaseOperation)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
