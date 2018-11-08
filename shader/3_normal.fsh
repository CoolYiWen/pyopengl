#version 330 core
out vec4 FragColor;
in vec2 color;

uniform vec4 u_v4_color;

void main()
{
    FragColor = vec4(color.rg, u_v4_color.r, 1);
}