#version 150 core

precision lowp float;

uniform sampler2DArray diffuse_texture;
in vec3 texcoord;
in vec3 normal;

out vec4 color_out;

void
main()
{
    float sun_intensity = 0.5;
    float amb_intensity = 0.5;
    vec3 sun_vector = normalize(vec3(-1, 0.5, 1));

    float sun_irradiance = dot(sun_vector, normal);
    float intensity = amb_intensity + sun_intensity * clamp(sun_irradiance, 0.0, 1.0);

    vec3 color = texture(diffuse_texture, texcoord).rgb * intensity;
    color_out = vec4(color.rgb, 1.0);
    //color_out = vec4(normal.xyz * 0.5 + 0.5, 1.0);
}
