#version 330

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

uniform float radius;

in float in_dist;
in vec3 in_pos;

out float vs_dist;
out float vs_fraction;
out vec3 vs_pos;
flat out int vs_sector;

void main(){
    gl_Position = window.projection * window.view * vec4(radius * in_pos, 1.0);
    vs_dist = in_dist * radius;
    vs_pos = in_pos;
    vs_fraction = in_dist == 0.0 ? 0.0 : 1.0;
    vs_sector = gl_VertexID;
}