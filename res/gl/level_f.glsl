#version 150 core

precision lowp float;

uniform sampler2DArray diffuse_texture;
in vec3 frag_position;
in vec3 frag_texcoord;
in vec3 frag_normal;

out vec4 color_out;

void
main()
{
    float sun_intensity = 0.5;
    float amb_intensity = 0.5;
    vec3 sun_vector = normalize(vec3(-1, 0.5, 1));

    float floor_bias = abs(frag_normal.z);
    float shade = clamp(frag_position.z * 2.0 + floor_bias, 0.5, 1.0);

    float sun_irradiance = dot(sun_vector, frag_normal);
    float intensity = amb_intensity + sun_intensity * clamp(sun_irradiance, 0.0, 1.0);

    vec3 color = texture(diffuse_texture, frag_texcoord).rgb * intensity * shade;
    color_out = vec4(color.rgb, 1.0);
    //color_out = vec4(normal.xyz * 0.5 + 0.5, 1.0);
}
