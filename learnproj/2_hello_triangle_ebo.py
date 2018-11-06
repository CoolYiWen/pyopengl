#coding=utf-8


from ctypes import sizeof, c_float, c_void_p
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import glfw
import sys

floatsize = sizeof(c_float)
vertex_offset = c_void_p(0 * floatsize)

def OnWindowSizeChangeCB(window, width, height):
	glViewport(0, 0, width, height)


def ProcessInput(window):
	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		glfw.set_window_should_close(window, True)


def main():
	glfw.init()
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)     #定义使用gl的版本号为3.3，主版本
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)     #次版本
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)     #使用核心模式

	window = glfw.create_window(800, 600, "Hello Triangle", None, None)   #创建窗口
	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)   #绑定当前窗口
	glViewport(0, 0, 800, 600)          #设置视口
	glfw.set_framebuffer_size_callback(window, OnWindowSizeChangeCB)    #窗口大小改变回调

	#生成编译顶点着色器
	vShader = glCreateShader(GL_VERTEX_SHADER)
	with open("../shader/2_normal.vsh", "r") as f:
		data = f.read()
		glShaderSource(vShader, [data])	#可绑定多份代码
		glCompileShader(vShader)
		iSuccess = glGetShaderiv(vShader, GL_COMPILE_STATUS)
		if not iSuccess:
			print(glGetShaderInfoLog(vShader))
	#生成编译片段着色器
	fShader = glCreateShader(GL_FRAGMENT_SHADER)
	with open("../shader/2_normal.fsh", "r") as f:
		data = f.read()
		glShaderSource(fShader, [data])
		glCompileShader(fShader)
		iSuccess = glGetShaderiv(fShader, GL_COMPILE_STATUS)
		if not iSuccess:
			print(glGetShaderInfoLog(fShader))
	#生成绑定着色器程序
	oProgram = glCreateProgram()
	glAttachShader(oProgram, vShader)
	glAttachShader(oProgram, fShader)
	glLinkProgram(oProgram)
	iSuccess = glGetProgramiv(oProgram, GL_LINK_STATUS)
	if not iSuccess:
		print(glGetProgramInfoLog(oProgram))
	glDeleteShader(vShader)
	glDeleteShader(fShader)

	vertices = [
		0.5,	0.5,	0.0,
		0.5,	-0.5,	0.0,
		-0.5, -0.5, 0.0,
		-0.5, 0.5, 0.0,
	]
	indexs = [
		0, 1, 3,
		1, 2, 3
	]
	vertices = numpy.array(vertices, dtype="float32")	#必须指定为float32，默认为int32
	indexs = numpy.array(indexs)	#这里使用int32类型
	# 绑定顶点数组对象
	ebo, vbo = glGenBuffers(2)
	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)
	glBindBuffer(GL_ARRAY_BUFFER, vbo)  #绑定缓冲对象
	glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)  #写入顶点数据
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexs, GL_STATIC_DRAW)
	# 链接顶点属性
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * floatsize, vertex_offset)
	glEnableVertexAttribArray(0)
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	glBindVertexArray(0)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	while not glfw.window_should_close(window):
		ProcessInput(window)
		glClearColor(0.2, 0.3, 0.3, 1.0)
		glClear(GL_COLOR_BUFFER_BIT)

		glUseProgram(oProgram)
		glBindVertexArray(vao)
		# glDrawArrays(GL_TRIANGLES, 0, 6)
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, c_void_p(0))

		glfw.poll_events()  #检查并调用事件，交换缓冲
		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ == "__main__":
	main()


