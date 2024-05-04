from ctypes import create_string_buffer

from pyglet.gl import *


class MeshRef:
    def __init__(self, vertices, per_vertex, draw_mode, vertex_source, fragment_source, diffuse_texture):
        self.vertex_shader_source = vertex_source
        self.vertex_shader = MeshRef._attach_shader(GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader_source = fragment_source
        self.fragment_shader = MeshRef._attach_shader(GL_FRAGMENT_SHADER, fragment_source)

        self.diffuse_texture = diffuse_texture
        self.program_handler = MeshRef._create_program(self.vertex_shader, self.fragment_shader)

        self.u_position = self.get_uniform_location('position')
        self.u_rotation = self.get_uniform_location('rotation')
        self.u_scale = self.get_uniform_location('scale')
        self.u_projection = self.get_uniform_location('projection')
        self.u_view = self.get_uniform_location('view')
        self.u_diffuse_texture = self.get_uniform_location('diffuse_texture')
        self.a_vertex = self.get_attrib_location('vertex')

    @staticmethod
    def _get_location_string_buffer(location_name):
        location_bytes = bytes(location_name, 'utf-8')
        return create_string_buffer(location_bytes, 64)

    def get_attrib_location(self, location_name):
        location_string_buffer = MeshRef._get_location_string_buffer(location_name)
        return glGetAttribLocation(self.program_handler, location_string_buffer)

    def get_uniform_location(self, location_name):
        location_string_buffer = MeshRef._get_location_string_buffer(location_name)
        return glGetUniformLocation(self.program_handler, location_string_buffer)

    def set_vertex_buffer(self, vertex_array):
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_handler)
        glBufferData(GL_ARRAY_BUFFER, self.data_size, vertex_array, GL_STATIC_DRAW)

    def pre_bind(self, camera):
        glUseProgram(self.program_handler)
        camera.bind(self.u_projection, self.u_view)
        self.diffuse_texture.bind(self.u_diffuse_texture)

        glEnableVertexAttribArray(self.a_vertex)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_handler)
        glVertexAttribPointer(self.a_vertex,
                              self.per_vertex,
                              GL_FLOAT, GL_FALSE,
                              0, 0)

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
        glShaderSource(shader, 1, shader_source, len(shader_source))
        glCompileShader(shader)
        compile_status = GLint()
        glGetShaderiv(shader, GL_COMPILE_STATUS, compile_status)
        if compile_status == GL_FALSE:
            info_log = (GLchar * 256)()
            info_log_length = GLsizei()
            glGetShaderInfoLog(shader, 256, info_log_length, info_log)
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
        if link_status == GL_FALSE:
            info_log = (GLchar * 256)()
            info_log_length = GLsizei()
            glGetProgramInfoLog(program, 256, info_log_length, info_log)
            raise RuntimeError(f'program link failed:\n{info_log}')
        return program
