#version 150 core

in vec4 vertex_position;
in vec2 vertex_texcoord;
in vec3 vertex_normal;

out vec3 texcoord;
out vec3 normal;

uniform vec3 position;

uniform mat4 projection;
uniform mat4 view;

void
main()
{
    float atlas_layer = vertex_position.w;
    texcoord = vec3(vertex_texcoord.xy, atlas_layer);
    normal = vertex_normal;

    vec4 full_vertex = vec4(
        vertex_position.x + position.x,
        vertex_position.y + position.y,
        vertex_position.z + position.z,
        1.0
    );
    gl_Position = projection * view * full_vertex;
}
