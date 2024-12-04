#version 330

in float vs_dist;
in vec3 vs_pos;

out vec4 fs_colour;

void main(){
    fs_colour = vec4((vs_pos*0.5 + 0.5), 1.0);
}