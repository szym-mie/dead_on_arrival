from pyglet.gl import glUniform3f, glUniform1f, GLfloat, glDrawArrays


class Mesh:
    def __init__(self, position, rotation, scale, mesh_prototype):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.mesh_prototype = mesh_prototype

    def bind(self):
        glUniform3f(self.mesh_prototype.u_position,
                    GLfloat(self.position.x),
                    GLfloat(self.position.y),
                    GLfloat(self.position.z))
        glUniform1f(self.mesh_prototype.u_rotation,
                    GLfloat(self.rotation))
        glUniform1f(self.mesh_prototype.u_scale,
                    GLfloat(self.scale))

    def draw(self, camera):
        self.mesh_prototype.pre_bind(camera)
        self.bind()
        glDrawArrays(self.mesh_prototype.draw_mode, 0, self.mesh_prototype.vertex_count)