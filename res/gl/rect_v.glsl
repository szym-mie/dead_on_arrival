#version 150 core

in vec2 vertex;
out vec2 texture_coord;

uniform vec3 position;
uniform float rotation;
uniform vec3 scale;

uniform mat4 projection;
uniform mat4 view;

void
main()
{
    float s = sin(rotation);
    float c = cos(rotation);

    mat2 model_view = mat2(
        scale.x * c, scale.x * s,
        -scale.y * s, scale.y * c
    );

    texture_coord = vertex;

    vec2 model_vertex = model_view * vertex;
    vec4 full_vertex = vec4(
        model_vertex.x + position.x,
        model_vertex.y + position.y,
        position.z,
        1.0
    );
    gl_Position = projection * view * full_vertex;
}
