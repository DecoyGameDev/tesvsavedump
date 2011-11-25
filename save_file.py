# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti

# refer to: http://www.uesp.net/wiki/Tes5Mod:Save_File_Format

import os
import data

class SaveGame(object):
    def __init__(self):
        pass
    
    def parse_lite(self, file):
        if not os.path.exists(file):
            return False
        with open(file, 'rb') as fp:
            self.parse_header(fp)
        return True
        
    def parse_lite_2(self, file):
        if not os.path.exists(file):
            return False
        with open(file, 'rb') as fp:
            self.parse_header(fp)
            self.parse_plugins(fp)
            self.parse_file_location_table(fp)            
        return True        
        
    def parse_full(self, file):
        if not os.path.exists(file):
            return False
                
        with open(file, 'rb') as fp:
            self.parse_header(fp)
            self.parse_plugins(fp)
            self.parse_file_location_table(fp)            
            self.global_data_table1 = []
            for i in xrange(0, self.glob_data_table1_count):
                self.global_data_table1.append(self.parse_global_data(fp))
            self.global_data_table2 = []
            for i in xrange(0, self.glob_data_table2_count):
                self.global_data_table2.append(self.parse_global_data(fp))                
            self.changed_forms      = []
            for i in xrange(0, self.changed_form_count):
                self.changed_forms.append(self.parse_changed_form(fp))            
            self.global_data_table3 = []
            for i in xrange(0, self.glob_data_table3_count+1):
                self.global_data_table3.append(self.parse_global_data(fp))            
            
            self.unknown_table1       = ''
            self.unknown_table2       = ''
            self.unknown_table3       = []
            
            self.unknown_table1_count = data.f_uint32(fp)
            #print 'unknown table1 count: %d' % self.unknown_table1_count
            if self.unknown_table1_count > 0:
                self.unknown_table1       = data.f_buf(self.unknown_table1_count*4, fp)
            self.unknown_table2_count = data.f_uint32(fp)
            #print 'unknown table2 count: %d' % self.unknown_table2_count
            if self.unknown_table2_count > 0:
                self.unknown_table2       = data.f_buf(self.unknown_table2_count*4, fp)
            self.unknown_table3_size  = data.f_uint32(fp)
            #print 'unknown table3 size: %d' % self.unknown_table3_size
            self.unknown_table3_count = data.f_uint32(fp)
            #print 'unknown table3 count: %d' % self.unknown_table3_count
            if self.unknown_table3_count > 0:                
                for i in xrange(0, self.unknown_table3_count):
                    self.unknown_table3.append( data.f_bstring(fp) )
                
        return True
        
    def parse_header(self, fp):
        self.file_magic = data.f_string(13, fp)
        self.hd_size    = data.f_uint32(fp)
        self.version    = data.f_uint32(fp)
        self.save_num   = data.f_uint32(fp)
        self.player_nm  = data.f_bstring(fp)
        self.player_lvl = data.f_uint32(fp)
        self.player_loc = data.f_bstring(fp)
        self.ingame_dt  = data.f_bstring(fp)
        self.player_race = data.f_bstring(fp)
        self.unknown_1 = data.f_uint16(fp)
        self.unknown_2 = data.f_float(fp)
        self.unknown_3 = data.f_float(fp)
        self.filetime  = data.f_filetime(fp)
        self.shot_w    = data.f_uint32(fp)
        self.shot_h    = data.f_uint32(fp)
        self.shot_data = data.f_buf(3*self.shot_h*self.shot_w, fp)
        self.form_ver  = data.f_uint8(fp)
            
    def parse_plugins(self, fp):        
        self.plugin_info_size = data.f_int32(fp)
        self.plugin_count     = data.f_uint8(fp)
        self.plugins          = []
        for i in xrange(0, self.plugin_count):
            self.plugins.append( data.f_bstring(fp) )
        
    def parse_file_location_table(self, fp):
        self.unknown_table1_offset   = data.f_uint32(fp)
        self.unknown_table3_offset   = data.f_uint32(fp)
        self.glob_data_table1_offset = data.f_uint32(fp)
        self.glob_data_table2_offset = data.f_uint32(fp)
        self.changed_forms_offset    = data.f_uint32(fp)
        self.glob_data_table3_offset = data.f_uint32(fp)
        self.glob_data_table1_count  = data.f_uint32(fp)
        self.glob_data_table2_count  = data.f_uint32(fp)
        self.glob_data_table3_count  = data.f_uint32(fp)
        self.changed_form_count      = data.f_uint32(fp)
        self.unknown_4               = data.f_buf(4*15, fp)
        
    def parse_global_data(self, fp):
        gb = data._GLOBALDATA()
        gb.type_ = data.f_uint32(fp)
        gb.len_  = data.f_uint32(fp)
        gb.data  = data.f_buf(gb.len_, fp)
        return gb
        
    def parse_changed_form(self, fp):
        cf = data._CHANGEDFORM()
        cf.unknown_1 = data.f_uint8(fp)
        cf.unknown_2 = data.f_uint8(fp)
        cf.unknown_3 = data.f_uint8(fp)
        cf.unknown_4 = data.f_uint32(fp)
        cf.flags     = data.f_uint8(fp)
        cf.version   = data.f_uint8(fp)
        len_flag = (cf.flags & 0xC0) >> 6
        #print "flags: %02X, version: %d, len_flag: %d" % (cf.flags, cf.version, len_flag)
        if len_flag == 0:
            cf.len_1     = data.f_uint8(fp)
            cf.len_2     = data.f_uint8(fp)
        elif len_flag == 1:
            cf.len_1     = data.f_uint16(fp)
            cf.len_2     = data.f_uint16(fp)
        elif len_flag == 2:
            cf.len_1     = data.f_uint32(fp)
            cf.len_2     = data.f_uint32(fp)
        #print "len1: %d, len2: %d" % (cf.len_1, cf.len_2)
        if cf.len_1 > 0:
            cf.data      = data.f_buf(cf.len_1, fp)
        return cf
    
    def dump_text(self):
        print "\nHEADER:"
        print str(self)
        
        print "\nSCREENSHOT DATA:"
        print data.h_dump(self.shot_data)
        
        print "\nPLUGINS:"
        for p in self.plugins:
            print "\t"+p
            
        dump_1 = str.format("""\
        Unknown Table1 Offset     : {0}
        Unknown Table3 Offset     : {1}
        Global Data Table 1 Offset: {2}
        Global Data Table 2 Offset: {3}
        Changed Forms Offset      : {4}
        Global Data Table 3 Offset: {5}
        Global Data Table 1 Count : {6}
        Global Data Table 2 Count : {7}
        Global Data Table 3 Count : {8}
        Changed Forms Count       : {9}
        """,
        self.unknown_table1_offset,
        self.unknown_table3_offset,
        self.glob_data_table1_offset,
        self.glob_data_table2_offset,
        self.changed_forms_offset,
        self.glob_data_table3_offset,
        self.glob_data_table1_count,
        self.glob_data_table2_count,
        self.glob_data_table3_count,
        self.changed_form_count)
        
        print "\nFILE LOCATION TABLE:"
        print dump_1
        
        print "\nGLOBAL DATA TABLE 1:"
        rec_n = 1
        for rec in self.global_data_table1:
            print str.format("""\nRec n. {0} {1}""", 
            rec_n, rec)
            print data.h_dump(rec.data)
            rec_n += 1
            
        print "\nGLOBAL DATA TABLE 2:"
        rec_n = 1
        for rec in self.global_data_table2:
            print str.format("""\nRec n. {0} {1}""", 
            rec_n, rec)
            print data.h_dump(rec.data)
            rec_n += 1  

        print "\nGLOBAL DATA TABLE 3:"
        rec_n = 1
        for rec in self.global_data_table3:
            print str.format("""\nRec n. {0} {1}""", 
            rec_n, rec)
            print data.h_dump(rec.data)
            rec_n += 1
            
        print "\nUNKNOWN TABLE 3:"
        for rec in self.unknown_table3:
            print rec
            
    def __str__(self):
        return str.format("""\
        File Magic   :   {0}
        Header Size  :   {1}
        Version      :   {2}
        Save Number  :   {3}
        Player Name  :   {4}
        Player Level :   {5}
        Player Loc   :   {6}
        Ingame Date  :   {7}
        Player Race  :   {8}
        Unknown 1    :   {9}
        Unknown 2    :   {10}
        Unknown 3    :   {11}
        Filetime     :   {12}
        Shot Width   :   {13}
        Shot Height  :   {14}
        """, 
        self.file_magic,
        self.hd_size,
        self.version,
        self.save_num,
        self.player_nm,
        self.player_lvl,
        self.player_loc,
        self.ingame_dt,
        self.player_race,
        repr(self.unknown_1),
        repr(self.unknown_2),
        repr(self.unknown_3),
        self.filetime,
        self.shot_w,
        self.shot_h)
               
def main():
    import sys   
    save_game = SaveGame()
    save_game.parse_full(sys.argv[1])
    #save_game.parse_lite_2(sys.argv[1])
    save_game.dump_text()
    
if __name__ == '__main__':
    main()