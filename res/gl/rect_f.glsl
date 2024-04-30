#version 150 core

precision lowp float;

in vec2 texture_coord;

uniform sampler2D diffuse_texture;

out vec4 color_out;

void
main()
{
    color_out = texture(diffuse_texture, texture_coord);
}