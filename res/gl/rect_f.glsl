#version 150 core

precision lowp float;

in vec2 texture_coord;

uniform sampler2D diffuse_texture;
uniform int layer;

out vec4 color_out;

void
main()
{
    vec3 texture_array_coord = vec3(texture_coord.xy, float(layer));
    color_out = texture(diffuse_texture, (texture_coord.xy - 1) * 0.5);
    if (color_out.a < 0.1) discard;
}
