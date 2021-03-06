#coding=utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import glfw


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

	window = glfw.create_window(800, 600, "Hello Window", None, None)   #创建窗口
	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)   #绑定当前窗口
	glViewport(0, 0, 800, 600)          #设置视口
	glfw.set_framebuffer_size_callback(window, OnWindowSizeChangeCB)    #窗口大小改变回调

	while not glfw.window_should_close(window):
		ProcessInput(window)
		glClearColor(0.2, 0.3, 0.3, 1.0)
		glClear(GL_COLOR_BUFFER_BIT)

		glfw.poll_events()  #检查并调用事件，交换缓冲
		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ == "__main__":
	main()


