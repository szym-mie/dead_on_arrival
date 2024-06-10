#version 150 core

in vec2 vertex_position;
in vec2 vertex_texcoord;

out vec2 texcoord;

uniform vec3 position;
uniform float rotation;
uniform vec3 scale;

uniform mat4 projection;
uniform mat4 view;

void
main()
{
    texcoord = vertex_texcoord;

    float s = sin(rotation);
    float c = cos(rotation);

    mat2 model = mat2(
        scale.x * c, scale.x * s,
        -scale.y * s, scale.y * c
    );

    vec2 model_vertex = model * vertex_position;
    vec4 full_vertex = vec4(
        model_vertex.x + position.x,
        model_vertex.y + position.y,
        position.z,
        1.0
    );
    gl_Position = projection * view * full_vertex;
}
