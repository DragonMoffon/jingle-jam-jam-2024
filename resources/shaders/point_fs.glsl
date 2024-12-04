#version 330

in float vs_depth;
in vec3 vs_pos;

out vec4 fs_colour;

void main(){
    fs_colour = vec4((vs_pos*0.5 + 0.5) * vec3(1.0 - vs_depth / 1000.0), 1.0);
}