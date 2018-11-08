## Hello Window

### 常用库介绍
OpenGL函数库相关的API有核心库(gl)、实用库(glu)、辅助库(aux)、实用工具库(glut)、窗口库(glx、agl、wgl)和扩展函数库等。
- gl是核心，包含了最基本的3D函数。
- glu是对gl的部分封装，glu是对gl的辅助，如果数学足够好，不用glu也是可以实现同样的效果。
    - 43个函数，以glu开头，包括纹理映射、坐标变换、多边形分化、绘制一些如椭球、圆柱、茶壶等简单多边形实体。  
- glut是OpenGL的跨平台工具库。
    - glut是基本的窗口界面，独立于gl和glu，如果不喜欢用glut可以用MFC和Win32窗口等代替，但是glut是跨平台的，这就保证了我们编出的程序是跨平台的，如果用MFC或者Win32只能在windows操作系统上使用。选择OpenGL的一个很大原因就是因为它的跨平台性，所以我们可以尽量的使用glut库。
- glew
    - GLUT或者FREEGLUT主要是1.0的基本函数功能；GLEW是使用OPENGL2.0之后的一个工具函数。
    -不同的显卡公司，也会发布一些只有自家显卡才支 持的扩展函数，你要想用这数涵数，不得不去寻找最新的glext.h,有了GLEW扩展库，你就再也不用为找不到函数的接口而烦恼，因为GLEW能自动识别你的平台所支持的全部OpenGL高级扩展函数。也就是说，只要包含一个glew.h头文件，你就能使用gl,glu,glext,wgl,glx的全部函数。
- glfw
    - GLFW无愧于其号称的lightweight的OpenGL框架，的确是除了跨平台必要做的事情都没有做，所以一个头文件，很少量的API，就完成了任务。GLFW的开发目的是用于替代glut的，从代码和功能上来看，我想它已经完全的完成了任务。
    - 一个轻量级的，开源的，跨平台的library。支持OpenGL及OpenGL ES，用来管理窗口，读取输入，处理事件等。因为OpenGL没有窗口管理的功能，所以很多热心的人写了工具来支持这些功能，比如早期的glut，现在的freeglut等。glut太老了，最后一个版本还是90年代的。

### glfw安装
- http://www.glfw.org/ 下载最新版的glfw，这里我直接下的编译好的。根据自己的本地vs版本添加进系统环境变量
- http://www.glfw.org/community.html 里有各个语言的调用工具。
- https://github.com/FlorianRhiem/pyGLFW 下载python对应的glfw库，python setup.py install


### 使用glfw创建窗口
代码见 https://github.com/CoolYiWen/pyopengl/blob/master/learnproj/hello_window.py

- 值得一提的是，这里并不需要教程里的glad来进行opengl指针管理，显而易见python也不需要。
- glViewport(0, 0, width, height)，这里坐标只能传int