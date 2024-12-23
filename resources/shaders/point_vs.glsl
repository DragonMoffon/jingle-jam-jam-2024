#version 330

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

uniform float radius;

in vec3 in_pos;

out float vs_depth;
out vec3 vs_pos;

void main(){
    gl_Position = window.projection * window.view * vec4(radius * in_pos, 1.0);
    vs_depth = gl_Position.w;
    vs_pos = in_pos;
}