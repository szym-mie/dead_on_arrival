#version 150 core

in vec3 vertex;
in vec3 atlas_coord;
out vec2 texture_coord;

uniform int chunk_width;
uniform int atlas_size;

uniform vec3 position;

uniform mat4 projection;
uniform mat4 view;

vec2
get_atlas_texture_coord(vec3 atlas_coord)
{
    int column = atlas_coord.z % float(atlas_size);
    int row = floor(atlas_coord.z / float(atlas_size));
    vec2 start_point = vec2(float(column), float(row));
    return (start_point + atlas_coord.xy) / float(atlas_size);
}

void
main()
{

    vec4 full_vertex = vec4(
        model_vertex.x + position.x,
        model_vertex.y + position.y,
        position.z,
        1.0
    );
    gl_Position = projection * view * full_vertex;
}
