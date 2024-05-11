from ctypes import c_char_p, cast, c_buffer, create_string_buffer

from _ctypes import POINTER
from pyglet.gl import *


class MeshMaterial:
    def __init__(self, vertex_source, fragment_source):
        self.vertex_shader_source = vertex_source
        self.vertex_shader = MeshMaterial._attach_shader(GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader_source = fragment_source
        self.fragment_shader = MeshMaterial._attach_shader(GL_FRAGMENT_SHADER, fragment_source)
        self.program_handler = MeshMaterial._create_program(self.vertex_shader, self.fragment_shader)

        self.diffuse_texture = None
        self.normal_texture = None
        self.emission_texture = None

        self.u_position = self.get_uniform_location('position')
        self.u_rotation = self.get_uniform_location('rotation')
        self.u_scale = self.get_uniform_location('scale')
        self.u_projection = self.get_uniform_location('projection')
        self.u_view = self.get_uniform_location('view')

        self.u_diffuse_texture = self.get_uniform_location('diffuse_texture')
        self.u_normal_texture = self.get_uniform_location('normal_texture')
        self.u_emission_texture = self.get_uniform_location('emission_texture')
        self.a_vertex = self.get_attrib_location('vertex')

    def use_program(self):
        glUseProgram(self.program_handler)

    def pre_bind(self, camera):
        self.use_program()
        camera.bind_to(self.u_projection, self.u_view)
        MeshMaterial.try_bind_texture(self.diffuse_texture, 0, self.u_diffuse_texture)
        MeshMaterial.try_bind_texture(self.normal_texture, 1, self.u_normal_texture)
        MeshMaterial.try_bind_texture(self.emission_texture, 2, self.u_emission_texture)

    @staticmethod
    def try_bind_texture(texture, unit, uniform):
        if texture is None:
            return
        texture.bind(unit, uniform)

    @staticmethod
    def _get_location_string_buffer(location_name):
        location_bytes = bytes(location_name, 'utf-8')
        return create_string_buffer(location_bytes, 64)

    def get_attrib_location(self, location_name):
        location_string_buffer = MeshMaterial._get_location_string_buffer(location_name)
        return glGetAttribLocation(self.program_handler, location_string_buffer)

    def get_uniform_location(self, location_name):
        location_string_buffer = MeshMaterial._get_location_string_buffer(location_name)
        return glGetUniformLocation(self.program_handler, location_string_buffer)

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
            glGetProgramInfoLog(program, 256, None, info_log_array)
            info_log = bytearray(info_log_array).decode('utf-8')
            raise RuntimeError(f'program link failed:\n{info_log}')
        return program
