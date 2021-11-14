# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti

# refer to: http://www.uesp.net/wiki/Tes5Mod:File_Format_Conventions

from struct import unpack, unpack_from, calcsize
import string
import os

class _SYSTEMTIME(object):
  #WORD wYear;
  #WORD wMonth;
  #WORD wDayOfWeek;
  #WORD wDay;
  #WORD wHour;
  #WORD wMinute;
  #WORD wSecond;
  #WORD wMilliseconds;
  
  def __init__(self, tup = None):
    if tup is not None and len(tup) == 8:
        self.from_tuple(tup)
    else:
        self.wYear         = 0
        self.wMonth        = 0
        self.wDayOfWeek    = 0
        self.wDay          = 0
        self.wHour         = 0
        self.wMinute       = 0
        self.wSecond       = 0
        self.wMilliseconds = 0
    
  def from_tuple(self, tup):
    self.wYear         = tup[0]
    self.wMonth        = tup[1]
    self.wDayOfWeek    = tup[2]
    self.wDay          = tup[3]
    self.wHour         = tup[4]
    self.wMinute       = tup[5]
    self.wSecond       = tup[6]
    self.wMilliseconds = tup[7]
    
class _FILETIME(object):
  #DWORD dwLowDateTime;
  #DWORD dwHighDateTime;
  
  def __init__(self, tup = None):
    if tup is not None and len(tup) == 8:
        self.from_tuple(tup)
    else:
        self.dwLowDateTime  = 0
        self.dwHighDateTime = 0
    
  def from_tuple(self, tup):
    self.dwLowDateTime  = tup[0]
    self.dwHighDateTime = tup[1]
    
  def __str__(self):
    return "%d %d" % (self.dwLowDateTime, self.dwHighDateTime)

_GLOBALDATATYPES = {    0:'Misc Stats',
                        1:'Player Location',
                        2:'TES',
                        3:'Global Variables',
                        4:'Created Objects',
                        5:'Effects',
                        6:'Weather',
                        7:'Audio',
                        8:'SkyCells',
                        100:'Process Lists',
                        101:'Combat',
                        102:'Interface',
                        103:'Actor Causes',
                        104:'Detection Manager',
                        105:'Location MetaData',
                        106:'Quest Static Data',
                        107:'StoryTeller',
                        108:'Magic Favorites',
                        109:'PlayerControls',
                        110:'Story Event Manager',
                        111:'Ingredient Shared',
                        112:'MenuControls',
                        113:'MenuTopicManager',
                        114:'???',
                        1000:'Temp Effects',
                        1001:'Papyrus',
                        1002:'Anim Objects',
                        1003:'Timer',
                        1004:'Synchronized Animations',
                        1005:'Main'
                        1006:'OBVvoxCOL12'}                      
    
class _GLOBALDATA(object):
    def __init__(self):
        self.type_ = 0
        self.len_  = 0
        self.data_ = ''
    
    @property
    def datatype(self):
        return self.type_
    
    @property
    def datalen(self):
        return self.len_
    
    @property
    def data(self):
        return self.data_
        
    @data.setter
    def data(self, value):
        self.data_ = value
        
    def __str__(self):
        type_str = 'N/A'
        if self.type_ in _GLOBALDATATYPES:
            type_str = _GLOBALDATATYPES[self.type_]
        return str.format("Type {0} DataLen {1}", type_str, self.len_)
    
class _CHANGEDFORM(object):
    def __init__(self):
        self.unknown_1 = 0
        self.unknown_2 = 0
        self.unknown_3 = 0
        self.unknown_4 = 0
        self.flags     = 0
        self.version   = 0
        self.len_1     = 0
        self.len_2     = 0
        self.data      = ''
        
    def __str__(self):
        if self.len_2 == 0:
            return str.format("DataLen {0} Version {1}", 
            self.len_1, self.version)
        else:
            return str.format("Compressed DataLen {0} Uncompressed DataLen {1} Version {2}", 
            self.len_1, self.len_2, self.version)        
    
# FILE OBJECT UTILITY
def f_num(fmt, fobj):
    len_   = calcsize(fmt)
    buffer = fobj.read(len_)
    return unpack_from(fmt, buffer)[0]

def f_int8(fobj):
    return f_num('b', fobj)
    
def f_uint8(fobj):
    return f_num('B', fobj)
    
def f_int16(fobj):
    return f_num('<h', fobj)

def f_uint16(fobj):
    return f_num('<H', fobj)
    
def f_int32(fobj):
    return f_num('<i', fobj)    

def f_uint32(fobj):
    return f_num('<I', fobj)
    
def f_int64(fobj):
    return f_num('<q', fobj)    

def f_uint64(fobj):
    return f_num('<Q', fobj)

def f_char(fobj):
    return chr(f_int8(fobj))

def f_float32(fobj):
    return f_num('f', fobj)
    
def f_float64(fobj):
    return f_num('d', fobj)    
    
def f_vsval(fobj):
    import sys
    first_byte = f_byte(fobj)
    len_ = (first_byte & 0x03)
    sys.stderr.write('vsval len: {0}. first_byte: {1}\n'.format(len_, first_byte))
    if len_ == 0:
        return first_byte
    fobj.seek(-1, os.SEEK_CUR)
    if len_ == 1:
        return (f_uint16(fobj) >> 2) | 1
    elif len_ == 2:
        return (f_uint32(fobj) >> 2) | 2
    raise Exception('Invalid vsval field!')
    
# ALIAS    
f_byte    = f_int8
f_ubyte   = f_uint8
f_short   = f_int16
f_ushort  = f_uint16
f_long    = f_int32
f_ulong   = f_uint32
f_formid  = f_ulong
f_iref    = f_ulong
f_hash    = f_uint64
f_lstring = f_ulong
f_float   = f_float32
f_double  = f_float64
    
def f_bstring(fobj):
    len_ = f_byte(fobj)
    data_ = unpack_from('%ds' % len_, fobj.read(len_))[0]
    return data_
    
def f_bzstring(fobj):    
    len_ = f_byte(fobj) + 1
    data_ = unpack_from('%ds' % len_, fobj.read(len_))[0]
    return data_
    
def f_zstring(fobj):
    data_ = ''
    while True:
        c = g_char(fobj)
        if c == 0:
            return data_
        data_ += c

def f_string(size, fobj):
    return unpack_from('%ds' % size, fobj.read(size))[0]
    
def f_wstring(fobj):
    len_ = f_short(fobj)
    if len_ > 1000:
        raise Exception('string too long')
    data_ = unpack_from('%ds' % len_, fobj.read(len_))[0]
    return data_
    
def f_wzstring(fobj):    
    len_ = unpack_from('<H', fobj.read(2))[0] + 1
    data_ = unpack_from('%ds' % len_, fobj.read(len_))[0]
    return data_    
     
def f_buf(size, fobj):
    return fobj.read(size)
    
def f_systemtime(fobj):
    fmt  = '>HHHHHHHH'
    size = calcsize(fmt)
    tup  = unpack_from(fmt, fobj.read(size))
    return _SYSTEMTIME(tup)
    
def f_filetime(fobj):
    fmt  = '>II'
    size = calcsize(fmt)
    tup  = unpack_from(fmt, fobj.read(size))
    return _FILETIME(tup)
    
def f_refid(fobj):
    return f_buf(3, fobj)

def buf2hex(buffer):
    h_line = ''
    for c in buffer:
        h_line += '%02X ' % ord(c)
    return h_line
    
def h_dump(buffer, include_ascii = True):
    i = 0
    lines = []
    h_line  = ''
    s_line  = ''
    for c in buffer:
        i += 1
        
        h_line += '%02X ' % ord(c)
        if c in string.digits or c in string.letters or c in string.punctuation or c == ' ':
            s_line += c
        else:
            s_line += '.'
        if i and (i % 16) == 0:
            lines.append('%s %s' % (h_line, s_line))
            h_line = s_line = ''
        
    if len(s_line) < 16:
        for i in xrange(len(s_line), 16):
            h_line += '   '
    lines.append('%s %s' % (h_line, s_line))
    return '\n'.join(lines)

