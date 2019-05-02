# vim: fdm=manual
import os, sys
sys.path.append(os.getcwd())
import bpy
import random


bl_info = {
    "name": "Bridge Generation Using Bezier Curves in Blender",
    "author": "Daniel Csillag"
}


# Define the parametric model for the bridge

def quadratic_bezier(p0x, p0y, p1x, p1y, p2x, p2y, t):
    def b(p0, p1, p2):
        return (1-t)*(1-t)*p0 + 2*(1-t)*t*p1 + t*t*p2
    return b(p0x, p1x, p2x), b(p0y, p1y, p2y)


def mapto(a, b, c, d, x):
    return (x - a)*(d - c)/(b - a) + c


C = -0.2


class BridgeParametric(object):
    def __init__(self, width, length, height, thickness, railing_height, railing_width, railing_length):
        self.width = width
        control = random.uniform(0.1*length, 0.5*length)
        self.p0 = (-0.5*length, 0)
        self.p1 = (-control, height)
        self.p2 = (0, height)
        self.p3 = (control, height)
        self.p4 = (0.5*length, 0)
        self.thickness = thickness
        self.railing_height = railing_height
        self.railing_width = railing_width
        self.railing_length = railing_length

    def walkway0(self, u, v):
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z

    def walkway1(self, u, v):
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z

    def bottom0(self, u, v):
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z - self.thickness

    def bottom1(self, u, v):
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z - self.thickness

    def railingpostfront0(self, u, v, offset):
        root_x, root_z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        root_v = v

        start = min(abs(root_v - self.railing_width), root_v)
        end = max(abs(root_v - self.railing_width), root_v)

        def f(u, v):
            v = mapto(0, 1, start, end, abs(root_v - v))
            y = -self.width + v*(2*self.width)
            z = u*self.railing_height
            return root_x + offset, y, root_z + z

        return f

    def railingpostfront1(self, u, v, offset):
        root_x, root_z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        root_v = v

        start = min(abs(root_v - self.railing_width), root_v)
        end = max(abs(root_v - self.railing_width), root_v)

        def f(u, v):
            v = mapto(0, 1, start, end, abs(root_v - v))
            y = -self.width + v*(2*self.width)
            z = u*self.railing_height
            return root_x + offset, y, root_z + z

        return f

    def railingpostside0(self, u, v, offset):
        root_x, root_z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        root_y = -self.width + v*(2*self.width)

        def f(u, v):
            x = u*self.railing_length
            z = v*self.railing_height
            return root_x + x, root_y + offset, root_z + z

        return f

    def railingpostside1(self, u, v, offset):
        root_x, root_z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        root_y = -self.width + v*(2*self.width)

        def f(u, v):
            x = u*self.railing_length
            z = v*self.railing_height
            return root_x - x, root_y + offset, root_z + z

        return f

    def railingtop0(self, u, v):
        v = mapto(0, 1, 0, self.railing_width, v)
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + self.thickness + C

    def railingbottom0(self, u, v):
        v = mapto(0, 1, 0, self.railing_width, v)
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + C

    def railingtop1(self, u, v):
        v = mapto(0, 1, 1-self.railing_width, 1, v)
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + self.thickness + C

    def railingbottom1(self, u, v):
        v = mapto(0, 1, 1-self.railing_width, 1, v)
        x, z = quadratic_bezier(*self.p0, *self.p1, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + C

    def railingtop2(self, u, v):
        v = mapto(0, 1, 0, self.railing_width, v)
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + self.thickness + C

    def railingbottom2(self, u, v):
        v = mapto(0, 1, 0, self.railing_width, v)
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + C

    def railingtop3(self, u, v):
        v = mapto(0, 1, 1-self.railing_width, 1, v)
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + self.thickness + C

    def railingbottom3(self, u, v):
        v = mapto(0, 1, 1-self.railing_width, 1, v)
        x, z = quadratic_bezier(*self.p4, *self.p3, *self.p2, u)
        y = -self.width + v*(2*self.width)
        return x, y, z + self.railing_height + C


# Define the operator

class BridgeOperator(bpy.types.Operator):
    bl_idname = "mesh.bridge_generator"
    bl_label = "Bridge Generator"

    width: bpy.props.FloatProperty(name="Bridge Width", default=3)
    length: bpy.props.FloatProperty(name="Bridge Length", default=10)
    height: bpy.props.FloatProperty(name="Bridge Height", default=1.5)
    thickness: bpy.props.FloatProperty(name="Bridge Thickness", default=0.2)
    u_step: bpy.props.FloatProperty(name="U Step", default=0.1)
    v_step: bpy.props.FloatProperty(name="V Step", default=0.1)
    addrailings: bpy.props.BoolProperty(name="Add Railings", default=True)
    railing_width: bpy.props.FloatProperty(name="Railing Width", default=0.1)
    railing_height: bpy.props.FloatProperty(name="Railing Width", default=3)
    railing_length: bpy.props.FloatProperty(name="Railing Width", default=0.3)
    nposts: bpy.props.IntProperty(name="Number of Railing Posts on Each Half", min=3, default=6)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def polygonize_parametric(self, f, vertices, faces):
        i = len(vertices)
        for u in (self.u_step*i for i in range(0, round(1/self.u_step))):
            for v in (self.v_step*j for j in range(0, round(1/self.v_step))):
                vertices.append(f(            u,             v))
                vertices.append(f(            u, v+self.v_step))
                vertices.append(f(u+self.u_step, v+self.v_step))
                vertices.append(f(u+self.u_step,             v))
                faces.append([i, i+1, i+2, i+3])
                i += 4
        return vertices, faces

    def polygonize_alternate_v(self, f, g, v, vertices, faces):
        i = len(vertices)
        for u in (self.u_step*i for i in range(0, round(1/self.u_step))):
            vertices.append(f(            u, v))
            vertices.append(g(            u, v))
            vertices.append(g(u+self.u_step, v))
            vertices.append(f(u+self.u_step, v))
            faces.append([i, i+1, i+2, i+3])
            i += 4
        return vertices, faces

    def execute(self, context):
        bridge_parametric = BridgeParametric(self.width, self.length, self.height, self.thickness, self.railing_height, self.railing_width, self.railing_length)
        vertices, faces = [], []
        vertices, faces = self.polygonize_parametric(bridge_parametric.walkway0, vertices, faces)
        vertices, faces = self.polygonize_parametric(bridge_parametric.walkway1, vertices, faces)
        vertices, faces = self.polygonize_parametric(bridge_parametric.bottom0, vertices, faces)
        vertices, faces = self.polygonize_parametric(bridge_parametric.bottom1, vertices, faces)
        vertices, faces = self.polygonize_alternate_v(bridge_parametric.walkway0, bridge_parametric.bottom0, 0, vertices, faces)
        vertices, faces = self.polygonize_alternate_v(bridge_parametric.walkway0, bridge_parametric.bottom0, 1, vertices, faces)
        vertices, faces = self.polygonize_alternate_v(bridge_parametric.walkway1, bridge_parametric.bottom1, 0, vertices, faces)
        vertices, faces = self.polygonize_alternate_v(bridge_parametric.walkway1, bridge_parametric.bottom1, 1, vertices, faces)
        if self.addrailings:
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingbottom0, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingtop0, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingbottom1, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingtop1, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom0, bridge_parametric.railingtop0, 0, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom0, bridge_parametric.railingtop0, 1, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom1, bridge_parametric.railingtop1, 0, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom1, bridge_parametric.railingtop1, 1, vertices, faces)

            vertices, faces = self.polygonize_parametric(bridge_parametric.railingbottom2, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingtop2, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingbottom3, vertices, faces)
            vertices, faces = self.polygonize_parametric(bridge_parametric.railingtop3, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom2, bridge_parametric.railingtop2, 0, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom2, bridge_parametric.railingtop2, 1, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom3, bridge_parametric.railingtop3, 0, vertices, faces)
            vertices, faces = self.polygonize_alternate_v(bridge_parametric.railingbottom3, bridge_parametric.railingtop3, 1, vertices, faces)

            post_step = 1 / (self.nposts+1)
            for i in range(1, self.nposts+1):
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront0(i*post_step, 0, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront0(i*post_step, 0, self.railing_length), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside0(i*post_step, 0, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside0(i*post_step, 0, self.railing_width*(2*self.width)), vertices, faces)

                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront1(i*post_step, 0, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront1(i*post_step, 0, -self.railing_width), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside1(i*post_step, 0, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside1(i*post_step, 0, self.railing_width*(2*self.width)), vertices, faces)

                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront0(i*post_step, 1, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront0(i*post_step, 1, self.railing_width), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside0(i*post_step, 1, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside0(i*post_step, 1, self.railing_width*(-2*self.width)), vertices, faces)

                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront1(i*post_step, 1, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostfront1(i*post_step, 1, -self.railing_length), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside1(i*post_step, 1, 0), vertices, faces)
                vertices, faces = self.polygonize_parametric(bridge_parametric.railingpostside1(i*post_step, 1, self.railing_width*(-2*self.width)), vertices, faces)

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
    self.layout.operator(BridgeOperator.bl_idname)


def register():
    bpy.utils.register_class(BridgeOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(BridgeOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
