# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti

import data
from cStringIO import StringIO

def gdata_factory(gdata):
    io = StringIO(gdata.data)
    if gdata.datatype == 0:
        return MiscStats().from_fobj(io)
    return None

class MiscStats(object):    
    def __init__(self):
        self.items = []
        
    def from_fobj(self, fobj):        
        count = data.f_uint32(fobj)
        for i in xrange(0, count):
            self.item.append( MiscStat().from_fobj(fobj) )
    
class MiscStat(object):
    CATEGS = [
        "General"  ,
        "Quest"    ,
        "Combat"   ,
        "Magic"    ,
        "Crafting" ,
        "Crime"
        ]
        
    def __init__(self, name = '', value = 0, categ = 0):
        self.name  = name
        self.value = value
        self.categ = categ
        
    def from_fobj(self, fobj):
        self.name  = data.f_wstring(fobj)
        self.categ = data.f_uint8(fobj)
        self.value = data.f_int32(fobj)
        
    def __str__(self):
        return '[{0}] {1}: {2}'.format(
            MiscStat.CATEGS[self.categ],
            self.name,
            self.value)