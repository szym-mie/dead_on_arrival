from pyglet.gl import *


class Engine:
    def __init__(self, camera):
        self.camera = camera

        self._mesh_protos = []
        self._effect_protos = []

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
        glClearDepth(GLdouble(1.0))

        for mesh_proto in self._mesh_protos:
            mesh_proto.draw(self.camera)
        for effect_proto in self._effect_protos:
            effect_proto.draw(self.camera)

    def add_mesh_prototype(self, mesh_prototype):
        self._mesh_protos.append(mesh_prototype)

    def add_effect_prototype(self, effect_prototype):
        self._effect_protos.append(effect_prototype)
