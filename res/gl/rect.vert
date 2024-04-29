#version 150 core

in vec2 vertex;
out vec2 texture_coord;

uniform vec3 position;
uniform float azimuth;
uniform float scale;

uniform mat4 projection;

void
main()
{
    float s = sin(scale);
    float c = cos(scale);

    mat2 model_view = mat2(
        scale * c, scale * s,
        -scale * s, scale * c
    );

    texture_coord = vertex;

    vec2 model_vertex = model_view * vertex;
    vec4 full_vertex = vec4(
        model_vertex.x + position.x,
        model_vertex.y + position.y,
        position.z,
        1.0
    );
    gl_Position = projection * full_vertex;
}