# vim: fdm=manual
import os, sys
sys.path.append(os.getcwd())
import bpy
import random
from lookuptable import lookup_table
from interval import Interval, exp


bl_info = {
    "name": "Procedural Rock Generation Using Implicit Skeletons in Blender",
    "author": "Daniel Csillag"
}


# Define the rock implicit function generator

class ImplicitRock(object):
    def __init__(self, cx, cy, cz, minradiusx, maxradiusx, minradiusy, maxradiusy, minradiusz, maxradiusz, nballs):
        self.cx = cx
        self.cy = cy
        self.cz = cz

        self.metaballs = []
        for i in range(nballs):
            radiusx = random.uniform(minradiusx, maxradiusx)
            radiusy = random.uniform(minradiusy, maxradiusy)
            radiusz = random.uniform(minradiusz, maxradiusz)
            x = random.uniform(self.cx - maxradiusx + radiusx, self.cx + maxradiusx - radiusx)
            y = random.uniform(self.cy - maxradiusy + radiusy, self.cy + maxradiusy - radiusy)
            z = random.uniform(self.cz - maxradiusz + radiusz, self.cz + maxradiusz - radiusz)
            self.metaballs.append({
                "x": x,
                "y": y,
                "z": z,
                "radius": max(radiusx, radiusy, radiusz),
                "invradiusx": 1/radiusx,
                "invradiusy": 1/radiusy,
                "invradiusz": 1/radiusz,
            })

    def metaball_dist2(self, metaball, x, y, z):
        return (x*metaball["invradiusx"]-metaball["x"])*(x*metaball["invradiusx"]-metaball["x"]) + \
               (y*metaball["invradiusy"]-metaball["y"])*(y*metaball["invradiusy"]-metaball["y"]) + \
               (z*metaball["invradiusz"]-metaball["z"])*(z*metaball["invradiusz"]-metaball["z"])

    def fieldfunc(self, r, d):
        # Blinn's field function (gaussian)
        return exp(-r * d)

    def __call__(self, x, y, z):
        return sum([self.fieldfunc(metaball["radius"], self.metaball_dist2(metaball, x, y, z)) for metaball in self.metaballs]) - 1


# Linear interpolation function

def linear_interpolate(px, py, pz, fp, qx, qy, qz, fq):
    alpha = -fp / (fq - fp)
    return (1 - alpha)*px + alpha*qx, (1 - alpha)*py + alpha*qy, (1 - alpha)*pz + alpha*qz


# Define the operator

class RockOperator(bpy.types.Operator):
    bl_idname = "mesh.rock_generator"
    bl_label = "Rock Generator"

    maxdepth: bpy.props.IntProperty(name="Maximum Depth (Marching Cubes)", default=3)
    minradiusx: bpy.props.FloatProperty(name="Minimum Radius (X)", default=0.5)
    maxradiusx: bpy.props.FloatProperty(name="Maximum Radius (X)", default=2)
    minradiusy: bpy.props.FloatProperty(name="Minimum Radius (Y)", default=0.5)
    maxradiusy: bpy.props.FloatProperty(name="Maximum Radius (Y)", default=2)
    minradiusz: bpy.props.FloatProperty(name="Minimum Radius (Z)", default=0.5)
    maxradiusz: bpy.props.FloatProperty(name="Maximum Radius (Z)", default=2)
    nballs: bpy.props.IntProperty(name="Number of Metaballs", min=1, default=6)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def marching_cubes(self, f, vertices, faces, startx, starty, startz, endx, endy, endz, depth=0):
        def vert2coord(i):
            if i == 0: return startx, starty, startz
            if i == 1: return   endx, starty, startz
            if i == 2: return   endx,   endy, startz
            if i == 3: return startx,   endy, startz
            if i == 4: return startx, starty,   endz
            if i == 5: return   endx, starty,   endz
            if i == 6: return   endx,   endy,   endz
            if i == 7: return startx,   endy,   endz

        def edge2verts(i):
            if i ==  0: return 0, 1
            if i ==  1: return 1, 2
            if i ==  2: return 2, 3
            if i ==  3: return 3, 0
            if i ==  4: return 4, 5
            if i ==  5: return 5, 6
            if i ==  6: return 6, 7
            if i ==  7: return 7, 4
            if i ==  8: return 0, 4
            if i ==  9: return 1, 5
            if i == 10: return 2, 6
            if i == 11: return 3, 7

        def edge2coords(i):
            v0, v1 = edge2verts(i)
            return vert2coord(v0), vert2coord(v1)

        fX = f(Interval(startx, endx), Interval(starty, endy), Interval(startz, endz))
        f0 = f(startx, starty, startz) >= 0
        f1 = f(  endx, starty, startz) >= 0
        f2 = f(  endx,   endy, startz) >= 0
        f3 = f(startx,   endy, startz) >= 0
        f4 = f(startx, starty,   endz) >= 0
        f5 = f(  endx, starty,   endz) >= 0
        f6 = f(  endx,   endy,   endz) >= 0
        f7 = f(startx,   endy,   endz) >= 0

        if 0 not in fX:
            return vertices, faces
        if depth >= self.maxdepth:
            # Draw
            index = 0
            if f0: index +=   1  # 2**0
            if f1: index +=   2  # 2**1
            if f2: index +=   4  # 2**2
            if f3: index +=   8  # 2**3
            if f4: index +=  16  # 2**4
            if f5: index +=  32  # 2**5
            if f6: index +=  64  # 2**6
            if f7: index += 128  # 2**7
            from_table = lookup_table[index]

            for (edge0, edge1, edge2) in from_table:
                if edge0 == -1 or edge1 == -1 or edge2 == -1: break
                v00, v01 = (x00, y00, z00), (x01, y01, z01) = edge2coords(edge0)
                v10, v11 = (x10, y10, z10), (x11, y11, z11) = edge2coords(edge1)
                v20, v21 = (x20, y20, z20), (x21, y21, z21) = edge2coords(edge2)
                # NOTE: No linear interpolation
                nverts = len(vertices)
                vertices.append(linear_interpolate(*v00, f(*v00), *v01, f(*v01)))
                vertices.append(linear_interpolate(*v10, f(*v10), *v11, f(*v11)))
                vertices.append(linear_interpolate(*v20, f(*v20), *v21, f(*v21)))
                # vertices.append([(x00 + x01)*0.5, (y00 + y01)*0.5, (z00 + z01)*0.5])
                # vertices.append([(x10 + x11)*0.5, (y10 + y11)*0.5, (z10 + z11)*0.5])
                # vertices.append([(x20 + x21)*0.5, (y20 + y21)*0.5, (z20 + z21)*0.5])
                faces.append([nverts, nverts+1, nverts+2])

            return vertices, faces

        splitx = (startx + endx)*0.5
        splity = (starty + endy)*0.5
        splitz = (startz + endz)*0.5

        # Subdivide
        vertices, faces = self.marching_cubes(f, vertices, faces, startx, splity, startz, splitx,   endy, splitz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, splitx, splity, startz,   endx,   endy, splitz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, startx, starty, startz, splitx, splity, splitz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, splitx, starty, startz,   endx, splity, splitz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, startx, splity, splitz, splitx,   endy,   endz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, splitx, splity, splitz,   endx,   endy,   endz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, startx, starty, splitz, splitx, splity,   endz, depth+1)
        vertices, faces = self.marching_cubes(f, vertices, faces, splitx, starty, splitz,   endx, splity,   endz, depth+1)

        return vertices, faces

    def execute(self, context):
        rock_implicit = ImplicitRock(0, 0, 0, self.minradiusx, self.maxradiusx, self.minradiusy, self.maxradiusy, self.minradiusz, self.maxradiusz, self.nballs)
        vertices, faces = self.marching_cubes(rock_implicit, [], [], -2, -2, -2, 2, 2, 2)

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
    self.layout.operator(RockOperator.bl_idname)


def register():
    bpy.utils.register_class(RockOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(RockOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
