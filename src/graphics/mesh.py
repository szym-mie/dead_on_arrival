from pyglet.gl import glUniform3f, glUniform1f, GLfloat, glDrawArrays


class Mesh:
    def __init__(self, position, rotation, scale, mesh_ref):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.mesh_ref = mesh_ref

    def bind(self):
        glUniform3f(self.mesh_ref.u_position,
                    GLfloat(self.position.x),
                    GLfloat(self.position.y),
                    GLfloat(self.position.z))
        glUniform1f(self.mesh_ref.u_rotation,
                    GLfloat(self.rotation))
        glUniform1f(self.mesh_ref.u_scale,
                    GLfloat(self.scale))

    def draw(self):
        self.bind()
        glDrawArrays(self.mesh_ref.draw_mode, 0, self.mesh_ref.vertex_count)
