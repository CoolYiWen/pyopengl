'''OpenGL extension FJ.shader_binary_GCCSO

This module customises the behaviour of the 
OpenGL.raw.GLES2.FJ.shader_binary_GCCSO to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension enables loading precompiled binary shaders compatible with
	chips designed by Fujitsu Semiconductor.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/FJ/shader_binary_GCCSO.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.FJ.shader_binary_GCCSO import *
from OpenGL.raw.GLES2.FJ.shader_binary_GCCSO import _EXTENSION_NAME

def glInitShaderBinaryGccsoFJ():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION