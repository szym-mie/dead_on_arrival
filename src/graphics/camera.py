from pyglet.gl import GLfloat, glUniformMatrix4fv, GL_FALSE
from pyglet.math import Vec3, Mat4


class Camera:
    def __init__(self, projection_matrix):
        self._projection = projection_matrix
        self.projection_array = (GLfloat * 16)()
        self.update_projection()
        self._view = Mat4()
        self.view_array = (GLfloat * 16)()
        self.position = Vec3()
        self.scale = 1.0

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, projection_matrix):
        self._projection = projection_matrix
        self.update_projection()

    def update(self):
        self._view = Mat4.from_translation(self.position)
        scale_vector = Vec3(self.scale, self.scale, self.scale)
        self._view.scale(scale_vector)
        self.update_view()

    def bind_to(self, u_projection, u_view):
        glUniformMatrix4fv(u_projection, 1, GL_FALSE, self.projection_array)
        glUniformMatrix4fv(u_view, 1, GL_FALSE, self.view_array)

    def update_projection(self):
        self.projection_array = (GLfloat * 16)(*self._projection)

    def update_view(self):
        self.view_array = (GLfloat * 16)(*self._view)