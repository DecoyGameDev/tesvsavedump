# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti

import sys
import data
from cStringIO import StringIO

def gdata_factory(gdata):
    io = StringIO(gdata.data)
    if gdata.datatype == 0:
        return MiscStats().from_fobj(io)
    elif gdata.datatype == 3:
        sys.stderr.write('global variables datalen: {0}\n'.format(gdata.datalen))
        return GlobalVariables().from_fobj(io)
    return None

class MiscStats(object):    
    def __init__(self):
        self.items = []
        
    def from_fobj(self, fobj):        
        count = data.f_uint32(fobj)
        for i in xrange(0, count):
            self.items.append( MiscStat().from_fobj(fobj) )
        return self
    def __str__(self):
        return "MISC STATS:\n" + '\n'.join( [ str(x) for x in self.items ] )
    
class MiscStat(object):
    CATEGS = [
        "General ",
        "Quest   ",
        "Combat  ",
        "Magic   ",
        "Crafting",
        "Crime   "
        ]
        
    def __init__(self, name = '', value = 0, categ = 0):
        self.name  = name
        self.value = value
        self.categ = categ
        
    def from_fobj(self, fobj):
        self.name  = data.f_wstring(fobj)
        self.categ = data.f_uint8(fobj)
        self.value = data.f_int32(fobj)
        return self
        
    def __str__(self):
        return '[{0}] {1}: {2}'.format(
            MiscStat.CATEGS[self.categ],
            self.name,
            self.value)
            
class GlobalVariables(object):    
    def __init__(self):
        self.items = []
        
    def from_fobj(self, fobj):        
        count = data.f_vsval(fobj)
        sys.stderr.write('global variables count: {0}\n'.format(count))
        for i in xrange(0, count):
            self.items.append( GlobalVariable().from_fobj(fobj) )
        return self
    def __str__(self):
        return "GLOBAL VARIABLES:\n" + '\n'.join( [ str(x) for x in self.items ] )
        
class GlobalVariable(object):       
    def __init__(self):
        self.form_id = 0
        self.value   = 0.0
        
    def from_fobj(self, fobj):
        self.form_id  = data.f_refid(fobj)
        self.value = data.f_float32 (fobj)
        return self
        
    def __str__(self):
        return '{0}: {1}'.format(
            data.buf2hex(self.form_id),
            self.value)        