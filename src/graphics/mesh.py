from pyglet.gl import glUniform3f, glUniform1f, GLfloat, glDrawArrays


class Mesh:
    def __init__(self, position, rotation, scale, mesh_prototype):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.mesh_prototype = mesh_prototype

    def bind(self):
        glUniform3f(self.mesh_prototype.material.u_position,
                    GLfloat(self.position.x),
                    GLfloat(self.position.y),
                    GLfloat(self.position.z))
        glUniform1f(self.mesh_prototype.material.u_rotation,
                    GLfloat(self.rotation))
        glUniform3f(self.mesh_prototype.material.u_scale,
                    GLfloat(self.scale.x),
                    GLfloat(self.scale.y),
                    GLfloat(self.scale.z))

    def draw(self, camera):
        self.mesh_prototype.pre_bind(camera)
        self.bind()
        glDrawArrays(self.mesh_prototype.draw_mode, 0, self.mesh_prototype.vertex_position_buffer.vertex_count)

    def remove(self):
        self.mesh_prototype.remove_mesh(self)