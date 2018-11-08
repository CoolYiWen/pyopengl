## Shader

#### 经典的着色器
- 着色器是使用一种叫GLSL的类C语言写成的。GLSL是为图形计算量身定制的，它包含一些针对向量和矩阵操作的有用特性。
- 着色器的开头总是要声明版本，接着是输入和输出变量、uniform和main函数。每个着色器的入口点都是main函数，在这个函数中我们处理所有的输入变量，并将结果输出到输出变量中。
```
#version version_number
in type in_variable_name;
in type in_variable_name;

out type out_variable_name;

uniform type uniform_name;

int main()
{
  // 处理输入并进行一些图形操作
  ...
  // 输出处理过的结果到输出变量
  out_variable_name = weird_stuff_we_processed;
}
```

#### 数据类型
- 向量最为重要，语法也十分灵活，可以重组
```
vecn	包含n个float分量的默认向量
bvecn	包含n个bool分量的向量
ivecn	包含n个int分量的向量
uvecn	包含n个unsigned int分量的向量
dvecn	包含n个double分量的向量

vec2 vect = vec2(0.5, 0.7);
vec4 result = vec4(vect, 0.0, 0.0);
vec4 otherResult = vec4(result.xyz, 1.0);
```

#### 输入输出
- layout (location=i) in type name  location为顶点索引，

```
#以下步骤定义了这个索引值
glVertexAttribPointer(i,...)
glEnableVertexAttribArray(i)
```

- in type name  输入
- out type name 输出
- uniform type name 外部传入的uniform
- 注意：同一个着色器程序里只有命名相同，才会被认为是同一个变量。同全局变量。


#### 着色器类

```
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
		"""
		激活使用
		"""
		glUseProgram(self.m_Program)

	def SetUniform(self, key, *value):
		"""
		设置uniform
		这里会根据value的数量和类型自动调用glUniform{size}{type}方法
		注意：只有在本着色器程序被激活之后才能调用
		"""
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


```
