#version 330

uniform sampler2D sector_map;

uniform float core_radius;
uniform float edge_width;

in float vs_dist;
in float vs_fraction;
in vec3 vs_pos;
flat in int vs_sector;

out vec4 fs_colour;

void main(){
    float logistics = texelFetch(sector_map, ivec2(0, vs_sector), 0).r;
    float growth = texelFetch(sector_map, ivec2(2, vs_sector), 0).r;
    float drain = texelFetch(sector_map, ivec2(3, vs_sector), 0).r;

    float inv_dist = (vs_dist / vs_fraction) - vs_dist;
    if (vs_fraction == 0.0) inv_dist = 1. / 0.;
    fs_colour = vec4(vec3(logistics, growth, drain) * (1.0 - step(core_radius, vs_dist)) + vec3(1.0 - step(edge_width, inv_dist)), 1.0);
}