from ctypes import create_string_buffer, cast, c_char, c_buffer, c_char_p

from _ctypes import POINTER
from pyglet.gl import *

from src.graphics.mesh import Mesh


class MeshPrototype:
    def __init__(self,
                 draw_mode,
                 vertex_source, fragment_source,
                 vertex_buffer,
                 diffuse_texture):
        self.draw_mode = draw_mode

        self.vertex_shader_source = vertex_source
        self.vertex_shader = MeshPrototype._attach_shader(GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader_source = fragment_source
        self.fragment_shader = MeshPrototype._attach_shader(GL_FRAGMENT_SHADER, fragment_source)
        self.program_handler = MeshPrototype._create_program(self.vertex_shader, self.fragment_shader)

        self.use_program()

        self.u_position = self.get_uniform_location('position')
        self.u_rotation = self.get_uniform_location('rotation')
        self.u_scale = self.get_uniform_location('scale')
        self.u_projection = self.get_uniform_location('projection')
        self.u_view = self.get_uniform_location('view')
        self.u_diffuse_texture = self.get_uniform_location('diffuse_texture')
        self.a_vertex = self.get_attrib_location('vertex')

        self.vertex_buffer = vertex_buffer
        self.diffuse_texture = diffuse_texture

        self.meshes = []

    def create_mesh(self, position, rotation, scale):
        mesh = Mesh(position, rotation, scale, self)
        self.meshes.append(mesh)
        return mesh

    @staticmethod
    def _get_location_string_buffer(location_name):
        location_bytes = bytes(location_name, 'utf-8')
        return create_string_buffer(location_bytes, 64)

    def get_attrib_location(self, location_name):
        location_string_buffer = MeshPrototype._get_location_string_buffer(location_name)
        return glGetAttribLocation(self.program_handler, location_string_buffer)

    def get_uniform_location(self, location_name):
        location_string_buffer = MeshPrototype._get_location_string_buffer(location_name)
        return glGetUniformLocation(self.program_handler, location_string_buffer)

    def use_program(self):
        glUseProgram(self.program_handler)

    def pre_bind(self, camera):
        glUseProgram(self.program_handler)
        camera.bind_to(self.u_projection, self.u_view)
        self.vertex_buffer.bind(self.a_vertex)
        self.diffuse_texture.bind(0, self.u_diffuse_texture)

    def draw_all(self, camera):
        self.pre_bind(camera)
        for mesh in self.meshes:
            mesh.bind()
            glDrawArrays(self.draw_mode, 0, self.vertex_buffer.vertex_count)

    @staticmethod
    def _create_buffer():
        buffer = GLuint()
        glGenBuffers(1, buffer)
        return buffer

    @staticmethod
    def _create_texture():
        texture = GLuint()
        glGenTextures(1, texture)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return texture

    @staticmethod
    def _attach_shader(shader_type, shader_source):
        shader = glCreateShader(shader_type)
        shader_source_bytes = shader_source.encode('utf-8')
        shader_source_array = c_char_p(shader_source_bytes)
        shader_source_ptr = cast(shader_source_array, POINTER(GLchar))
        shader_source_count = GLint(len(shader_source_bytes))
        glShaderSource(shader, 1, shader_source_ptr, shader_source_count)
        glCompileShader(shader)
        compile_status = GLint()
        glGetShaderiv(shader, GL_COMPILE_STATUS, compile_status)
        if compile_status.value == GL_FALSE:
            info_log_array = c_buffer(256)
            info_log_length = GLsizei()
            glGetShaderInfoLog(shader, 256, None, info_log_array)
            info_log = bytearray(info_log_array).decode('utf-8')
            raise RuntimeError(f'shader compilation failed:\n{info_log}\nsource:\n{shader_source}')
        return shader

    @staticmethod
    def _create_program(vertex_shader, fragment_shader):
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        link_status = GLint()
        glGetProgramiv(program, GL_LINK_STATUS, link_status)
        if link_status.value == GL_FALSE:
            info_log_array = c_buffer(256)
            info_log_length = GLsizei()
            glGetProgramInfoLog(program, 256, None, info_log_array)
            info_log = bytearray(info_log_array).decode('utf-8')
            raise RuntimeError(f'program link failed:\n{info_log}')
        return program
