# coding=utf-8

from OpenGL.GL import *


class CShader(object):
	def __init__(self, vPath, fPath):
		self.m_Program = None
		self.m_VPath = vPath  # 顶点着色器文件路径
		self.m_FPath = fPath  # 片段着色器
		self.Init()

	def Init(self):
		vShader = glCreateShader(GL_VERTEX_SHADER)
		with open(self.m_VPath, "r") as f:
			data = f.read()
			glShaderSource(vShader, [data])  # 可绑定多份代码
			glCompileShader(vShader)
			if not glGetShaderiv(vShader, GL_COMPILE_STATUS):
				print("Compile Vertex Shader Error: ", glGetShaderInfoLog(vShader))
				return
		# 生成编译片段着色器
		fShader = glCreateShader(GL_FRAGMENT_SHADER)
		with open(self.m_FPath, "r") as f:
			data = f.read()
			glShaderSource(fShader, [data])
			glCompileShader(fShader)
			if not glGetShaderiv(fShader, GL_COMPILE_STATUS):
				print("Compile Fragment Shader Error: ", glGetShaderInfoLog(fShader))
				return
		# 生成绑定着色器程序
		oProgram = glCreateProgram()
		glAttachShader(oProgram, vShader)
		glAttachShader(oProgram, fShader)
		glLinkProgram(oProgram)
		if not glGetProgramiv(oProgram, GL_LINK_STATUS):
			print("Link Shader Program Error: ", glGetProgramInfoLog(oProgram))
			return
		self.m_Program = oProgram
		glDeleteShader(vShader)
		glDeleteShader(fShader)

	def Use(self):
		glUseProgram(self.m_Program)

	def SetUniform(self, key, *value):
		size = len(value)
		if size == 0:
			return
		if isinstance(value[0], int):
			type = "i"
		else:
			type = "f"
		sfunc = "glUniform{size}{type}".format(size=size, type=type)
		func = globals().get(sfunc)
		if not func:
			return
		func(glGetUniformLocation(self.m_Program, key), *value)

	@property
	def Program(self):
		return self.m_Program

