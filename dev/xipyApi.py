# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 19:52:48 2014

@author: David Moorhouse
"""

import ctypes
xi=ctypes.cdll.LoadLibrary('libm3api.so')     

def NewDeviceHandle():
    xiH=ctypes.pointer(ctypes.c_void_p(0))
    return xiH
    
def NewImagePointer():
    image = ctypes.pointer(XI_IMG(ctypes.sizeof(XI_IMG),None,512))
    return image

def OpenDevice(xiH):
    print
    print('Opening device...')
    stat=xi.xiOpenDevice(0, xiH)    
    print('xiApi error code: %i')%(stat)
    assert stat == 0
    return None
    
def StartAcquisition(xiH):
    print
    print('Starting aquisition...')
    stat = xi.xiStartAcquisition(xiH.contents)
    print('xiApi error code: %i')%(stat)
    assert stat == 0
    return None
    
def GetImage(xiH, timeout, image):
#    print
#    print('Getting Image...')
    if isinstance(timeout,int):
        timeout=ctypes.c_uint32(timeout)
    assert isinstance(timeout,ctypes.c_uint)         
    stat = xi.xiGetImage(xiH.contents,timeout, image)
#    print('xiApi error code: %i')%(stat)
    raw = (ctypes.c_uint8*image.contents.width*image.contents.height).from_address(image.contents.bp) 
    assert stat == 0
    return raw    
    
def CloseDevice(xiH):
    print
    print('Closing device...')
    stat=xi.xiCloseDevice(xiH)
    print('xiApi error code: %i')%(stat)
    assert stat == 0
    return None
      
def SetParamInt(xiH, value, param):
    print
    print('Setting %s...')%(param)
    if isinstance(value,float):
        print
        print 'Warning: data type float, converting to int'
        print
        value=int(value)
    if isinstance(value,int):
        value=ctypes.c_uint32(value)
    assert type(value) is ctypes.c_uint,'Invalid data type: %s, int required'%((str(type(value))[7:])[:-2])
    stat = xi.xiSetParamInt(xiH.contents, param , value)
    print('xiApi error code: %i')%(stat)
    assert stat == 0
    return None
    
def SetParamFloat(xiH, value, param):
    print
    print('Setting %s...')%(param)
    if isinstance(value,int):
        print
        print 'Warning: data type int, converting to float'
        print
        value=float(value)
    if isinstance(value,float):
        value=ctypes.c_float(value)
    assert type(value) is ctypes.c_float,'Invalid data type: %s, float required'%((str(type(value))[7:])[:-2])
    stat = xi.xiSetParamFloat(xiH.contents, param , value)
    print('xiApi error code: %i')%(stat)
    assert stat == 0
    return None
    
class XI_IMG(ctypes.Structure):
     _fields_ = [("size", ctypes.c_uint32),
                 ("bp", ctypes.c_void_p),  
                 ("bp_size", ctypes.c_uint32), 
                 ("frm", ctypes.c_uint32), 
                 ("width", ctypes.c_uint32), 
                 ("height", ctypes.c_uint32), 
                 ("nframe", ctypes.c_uint32), 
                 ("tsSec", ctypes.c_uint32), 
                 ("tsUSec", ctypes.c_uint32), 
                 ("GPI_level", ctypes.c_uint32), 
                 ("black_level", ctypes.c_uint32), 
                 ("padding_x", ctypes.c_uint32)] 