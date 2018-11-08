## Hello Triangle

### 图形渲染管线
在OpenGL中，任何事物都在3D空间中，而屏幕和窗口却是2D像素数组，这导致OpenGL的大部分工作都是关于把3D坐标转变为适应你屏幕的2D像素。3D坐标转为2D坐标的处理过程是由OpenGL的图形渲染管线（Graphics Pipeline，大多译为管线，实际上指的是一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程）管理的。图形渲染管线可以被划分为两个主要部分：第一部分把你的3D坐标转换为2D坐标，第二部分是把2D坐标转变为实际的有颜色的像素。

- 图形渲染管线的第一个部分是顶点着色器(Vertex Shader)，它把一个单独的顶点作为输入。顶点着色器主要的目的是把3D坐标转为另一种3D坐标（后面会解释），同时顶点着色器允许我们对顶点属性进行一些基本处理。

- 图元装配(Primitive Assembly)阶段将顶点着色器输出的所有顶点作为输入（如果是GL_POINTS，那么就是一个顶点），并所有的点装配成指定图元的形状；本节例子中是一个三角形。

- 图元装配阶段的输出会传递给几何着色器(Geometry Shader)。几何着色器把图元形式的一系列顶点的集合作为输入，它可以通过产生新顶点构造出新的（或是其它的）图元来生成其他形状。例子中，它生成了另一个三角形。

- 几何着色器的输出会被传入光栅化阶段(Rasterization Stage)，这里它会把图元映射为最终屏幕上相应的像素，生成供片段着色器(Fragment Shader)使用的片段(Fragment)。在片段着色器运行之前会执行裁切(Clipping)。裁切会丢弃超出你的视图以外的所有像素，用来提升执行效率。

### 编译着色器

```
#生成编译顶点着色器
vShader = glCreateShader(GL_VERTEX_SHADER)
with open("../shader/2_normal.vsh", "r") as f:
	data = f.read()
	glShaderSource(vShader, [data])
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
```
==注意：glShaderSource(iShader, [data..])跟C++不一样的是不需要传入大小，所以必须传入源代码的列表==

### 顶点输入
```
vertices = [
		-0.5,   -0.5,   0.0,
		0.5,    -0.5,   0.0,
		0.0,    0.5,    0.0
	]
vertices = numpy.array(vertices, dtype="float32")
```
==注意：生成数组对象时，dtype若取默认值，则是int32，所以这里必须强制转为32位float==

### 顶点缓冲对象(Vertex Buffer Objects, VBO)
管理输入顶点的内存，它会在显存中储存大量顶点。使用这些缓冲对象的好处是我们可以一次性的发送一大批数据到显卡上，而不是每个顶点发送一次。

```
from ctypes import sizeof, c_float, c_void_p
floatsize = sizeof(c_float) #32位大小，为4
vertex_offset = c_void_p(0 * floatsize) #偏移量，强制为void*类型

#创建一个vbo
vbo = glGenBuffers(1)   #param：数量
#绑定当前缓冲对象
glBindBuffer(GL_ARRAY_BUFFER, vbo)
#写入顶点数据
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STREAM_DRAW) 
# 链接顶点属性
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * floatsize, vertex_offset)
glBindBuffer(GL_ARRAY_BUFFER, 0)
```
==注意点==
- glBufferData()里可以传入顶点数组的大小（传小了会截断），也可以不传自行判断
- glVertexAttribPointer( index , size , type , normalized , stride , pointer )，layout索引值，大小，类型，是否归一化，步长，偏移量(强制为void*)

### 顶点数组对象(Vertex Array Object, VAO)
可以像顶点缓冲对象那样被绑定，任何随后的顶点属性调用都会储存在这个VAO中。也就是VAO管理着一堆VBO。
==OpenGL的核心模式要求我们使用VAO，所以它知道该如何处理我们的顶点输入。如果我们绑定VAO失败，OpenGL会拒绝绘制任何东西。==

```
vao = glGenVertexArrays(1)  #创建一个vao
glBindVertexArray(vao) #绑定这个vao
vbo .....   #开始操作vbo
glEnableVertexAttribArray(0)    #启用这个索引(layout)的顶点属性，默认禁止
glBindVertexArray(0)    #取消绑定
```

### 索引缓冲对象(Element Buffer Object，EBO，也叫Index Buffer Object，IBO)
保存着vbo的索引

### 画个三角形

```
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawArrays(GL_TRIANGLES, 0, 3);
```
