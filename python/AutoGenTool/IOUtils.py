#******************************************************************************************************************************
# File: IOUtils.py
# Desc: Main backend file for input/output
#******************************************************************************************************************************

import Components
import Device
import Heater
import AutoHeaters
import CfHeaters
import Twtas
import glob
import re
import os
import time
import xlrd
import shutil
import zipfile

#******************************************************************************************************************************
# Miscellaneous supporting functions
#******************************************************************************************************************************

def underscore_it(cmd_pid):
    if re.search('\d',cmd_pid[2]):
        cmd_pid = cmd_pid[:2] + '_' + cmd_pid[2:]
    return cmd_pid

def get_file_list(gui, srch_strs, ext='txt'):
    """ Get list of file paths containing search string
    
    Description: Checks ddir for files containing srch_strs with extension ext and returns a dict of full path names for
    matching files.
    Arguments: ddir -- Directory string in which to search
               srch_strs -- Strings in pathnames to search
               ext -- Optional expected extension of files. Defaults to 'txt'
    Output: fNames -- dictionary of search string:found full path
    """
    fNames = {}
    # List files containing search string
    single = False
    for srch_str in srch_strs:
        if len(srch_str) == 1:
            srch_str = srch_strs
            single = True
        fName = glob.glob(srch_str)
        
        # Set appendix name
        if len(fName) == 0:
            gui.output_text('    Warning - Couldn\'t find ' + srch_str)
        elif len(fName) > 1:
            gui.output_text('    Warning - Found multiple matches for ' + srch_str)
        else:
            if single:
                fNames = fName[0]
            else:
                fNames[srch_str] = fName[0]
            gui.output_text('    Found ' + srch_str + ' - ' + fName[0])
        if single:
            break
    return fNames

def adjust_htr_name(name):
    """ Force consistent heater naming convention
    
    Description: Modifies heater name to format: heater_name xx where xx is the number, padded with a leading zero
    Arguments: name -- unit name string
    Output: name -- modified unit name string
    """
    # Standardize heater number
    h_ind = name.find('Htr')
    num = re.search('\d+',name[h_ind:])
    if num:
        name = name[:h_ind+3] + ' %02d ' % int(num.group(0)) + name[h_ind+4+len(num.group(0)):]
    else:
        name = name
    
    # Standardize RW numbering
    search_str = re.search('RW\w?(\d+)', name)
    if search_str:
        name = 'RW %d' % int(search_str.group(1)) + name[name.find(search_str.group(1))+1:]
    
    # Standardize Press Tnk numbering
    search_str = re.search('Press Tnk(\d+)', name)
    if search_str:
        name = 'Press Tnk %d' % int(search_str.group(1)) + name[name.find(search_str.group(1))+1:]
    
    # Finish up
    name = name.strip()
    return name

def get_rd(text):
    """ Determine RD
    
    Description: Determine RD, without all the extra fluff. This is needed because the RD convention
    in the database varies drastically. RD is first word in text that either starts with a letter and 
    has a number, or is a number. Based on RDs like 33630, 123B1, CVD201
    Arguments: text -- text string containing RD
    Output: rd -- RD stripped of fluff
    """
    for word in text.split(' '):
        if re.search('[a-zA-Z]?.*\d+', word):
            end_t = re.search('[^a-zA-Z\d]', word)
            if end_t:
                word = word[:end_t.start(0)]
            return word

#******************************************************************************************************************************
# Database
#******************************************************************************************************************************

class Dbase(object):
    """ Gather database information
    
    Description: Read databases and place into dictionaries
    Usage: Invoked by Reader object in IOUtils.py
    Public Variables: cmd -- Command database. Dictionary of command num:command object
                      mac -- Macro database. Dictionary of macro num:macro object
                      tlm -- Telemetry database. Dictionary of pid num:pid object
                      ver -- Verification database. Dictionary of pid num:max atten
                      wire_aux -- Auxiliary/Wiring database. Direct copy (not a dictionary)
                      subbuses -- Subbuses. Dictionary of subbus identifier:pid object
                      subbus_data -- Extended subbus data. Dictionary of unit name:(list of [subbus object, tray string])
    Public Methods: get_cmd_pid -- Get cmds/pids with description matching search string
                    check_dbase -- Check compiled spacecraft info against database
                    read_dbase -- Read the database
                    carve_subbuses -- Determine which subbus units are on
    """
    
    def __init__(self, gui, spacecraft):
        """ Constructor """
        self.gui = gui
        self.spacecraft = spacecraft
        self.cmd = {}
        self.mac = {}
        self.tlm = {}
        self.tlm_format = {}
        self.ver = {}
        self.sbus = {}
        self.limits = []
        self.wire_aux = []
        self.subbuses = {}
        self.carved_subbuses = {}
        self.carved_prefixes = {}
        self.mmdc_assoc = {}
    
    def get_cmd_pid(self, cmds_pids, des, con='=='):
        """ Get cmds/pids with description matching search string
        
        Description: Search through specified dictionary of cmds_pids for cmds/pids containing (or not containing) des in their
        description.
        Arguments: cmds_pids -- dictionary of cmds_pids
                   des -- search string
                   con -- Option operator. Defaults to '=='. Can also be specified as '!='
        Output: Dictionary of cmds/pids that satisfied search criterion
        """
        items_found = {}
        for value in cmds_pids.values():
            if con == '==':
                if re.search(des.lower(),value.des.lower()):
                    items_found[value.num] = value
            elif con == '!=':
                if not re.search(des.lower(),value.des.lower()):
                    items_found[value.num] = value
        return items_found
    
    def check_dbase(self):
        """ Check compiled spacecraft info against database
        
        TODO
        
        Description: Iterates through spacecraft info (gather from stirs, etc) and verifies it against the database in an
        effort to preemptively detect errors. Throws warnings if mismatches are detected.
        """
        # Loop through heaters
        self.gui.output_text('  Verifying STIRS heater data against database...')
        for htr in self.spacecraft.heaters.values():
            for cmd_pid_name,cmd_pid in htr.cmds_pids.items():
                # Set database
                if 'cmd' in cmd_pid_name:
                    dbase_t = self.cmd
                elif 'mac' in cmd_pid_name:
                    dbase_t = self.mac
                elif 'tlm' in cmd_pid_name or 'pid' in cmd_pid_name:
                    dbase_t = self.tlm
                if isinstance(cmd_pid, list):
                    for cmd_pid_s in cmd_pid:
                        if cmd_pid_s.num not in dbase_t.keys():
                            self.gui.output_text('    Warning - ' + cmd_pid_s.num + ': ' + cmd_pid_s.des + ' in STIRS but not dbase')
                            htr.cmds_pids.pop(cmd_pid_name)
                        else:
                            if cmd_pid_s.des != dbase_t[cmd_pid_s.num].des:
                                stirs = 'STIRS[' + cmd_pid_s.num + ': ' + cmd_pid_s.des + ']'
                                dbase = 'DBASE[' + dbase_t[cmd_pid_s.num].num + ': ' + dbase_t[cmd_pid_s.num].des + ']'
                                self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                                cmd_pid_s.des = dbase_t[cmd_pid_s.num].des
                else:
                    if cmd_pid.num not in dbase_t.keys():
                        self.gui.output_text('    Warning - ' + cmd_pid.num + ': ' + cmd_pid.des + ' in STIRS but not dbase')
                        htr.cmds_pids.pop(cmd_pid_name)
                    else:
                        if cmd_pid.des != dbase_t[cmd_pid.num].des:
                            stirs = 'STIRS[' + cmd_pid.num + ': ' + cmd_pid.des + ']'
                            dbase = 'DBASE[' + dbase_t[cmd_pid.num].num + ': ' + dbase_t[cmd_pid.num].des + ']'
                            self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                            cmd_pid.des = dbase_t[cmd_pid.num].des
            
            # Loop through thermisters
            for thrm in htr.thermisters:
                # Check for tlm pid. If exists, force consistent description
                if thrm.tlm.num not in self.tlm.keys():
                    self.gui.output_text('    Warning - ' + thrm.tlm.num + ': ' + thrm.tlm.des + ' in STIRS but not dbase')
                else:
                    if thrm.tlm.des != self.tlm[thrm.tlm.num].des:
                        stirs = 'STIRS[' + thrm.tlm.num + ': ' + thrm.tlm.des + ']'
                        dbase = 'DBASE[' + self.tlm[thrm.tlm.num].num + ':' + self.tlm[thrm.tlm.num].des + ']'
                        self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                        thrm.tlm.des = self.tlm[thrm.tlm.num].des
                    
        self.gui.output_text('  Verifying STIRS TWTA data against database...')
    
    def check_dbase_cfheaters(self):
        self.gui.output_text('  Verifying STIRS safety relay data against database...')
        for htr_name in self.spacecraft.sorted_htr_names:
            if 'Htr' not in htr_name or 'Side' in htr_name:
                continue
            htr = self.spacecraft.cf_heaters[htr_name]
            # Check heater
            items_to_pop = []
            for cmd_pid_name,cmd_pid in htr.cmds_pids.items():
                # Set database
                if 'cmd' in cmd_pid_name:
                    dbase_t = self.cmd
                elif 'mac' in cmd_pid_name:
                    dbase_t = self.mac
                elif 'tlm' in cmd_pid_name or 'pid' in cmd_pid_name:
                    dbase_t = self.tlm
                if cmd_pid.num not in dbase_t.keys():
                    self.gui.output_text('    Warning - ' + cmd_pid.num + ': ' + cmd_pid.des + ' in STIRS but not dbase')
                    items_to_pop.append(cmd_pid_name)
                else:
                    if cmd_pid.des != dbase_t[cmd_pid.num].des:
                        stirs = 'STIRS[' + cmd_pid.num + ': ' + cmd_pid.des + ']'
                        dbase = 'DBASE[' + dbase_t[cmd_pid.num].num + ': ' + dbase_t[cmd_pid.num].des + ']'
                        self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                        cmd_pid.des = dbase_t[cmd_pid.num].des
            for item in items_to_pop:
                htr.cmds_pids.pop(item)
                
            # Check heater safety relay
            items_to_pop = []
            for cmd_pid_name,cmd_pid in htr.sfty_rly.cmds_pids.items():
                # Set database
                if 'cmd' in cmd_pid_name:
                    dbase_t = self.cmd
                elif 'mac' in cmd_pid_name:
                    dbase_t = self.mac
                elif 'tlm' in cmd_pid_name or 'pid' in cmd_pid_name:
                    dbase_t = self.tlm
                if isinstance(cmd_pid, list):
                    for cmd_pid_s in cmd_pid:
                        if cmd_pid_s.num not in dbase_t.keys():
                            self.gui.output_text('    Warning - ' + cmd_pid_s.num + ': ' + cmd_pid_s.des + ' in STIRS but not dbase')
                            items_to_pop.append(cmd_pid_name)
                        else:
                            if cmd_pid_s.des != dbase_t[cmd_pid_s.num].des:
                                stirs = 'STIRS[' + cmd_pid_s.num + ': ' + cmd_pid_s.des + ']'
                                dbase = 'DBASE[' + dbase_t[cmd_pid_s.num].num + ': ' + dbase_t[cmd_pid_s.num].des + ']'
                                self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                                cmd_pid_s.des = dbase_t[cmd_pid_s.num].des
                else:
                    if cmd_pid.num not in dbase_t.keys():
                        self.gui.output_text('    Warning - ' + cmd_pid.num + ': ' + cmd_pid.des + ' in STIRS but not dbase')
                        items_to_pop.append(cmd_pid_name)
                    else:
                        if cmd_pid.des != dbase_t[cmd_pid.num].des:
                            stirs = 'STIRS[' + cmd_pid.num + ': ' + cmd_pid.des + ']'
                            dbase = 'DBASE[' + dbase_t[cmd_pid.num].num + ': ' + dbase_t[cmd_pid.num].des + ']'
                            self.gui.output_text('    Warning - %s != %s' % (stirs, dbase))
                            cmd_pid.des = dbase_t[cmd_pid.num].des
            for item in items_to_pop:
                htr.sfty_rly.cmds_pids.pop(item)
    
    def parse_line(self, line, omega):
        """ Parse a database row """
        if omega == '2':
            line = line.replace('"','')
            line = line.strip('\n')
            line = line.split('\t')
        else:
            line = line[5:-11]
            line = line.replace('<c t="inlineStr"><is><t>','')
            line = line.replace('</t></is>','')
            line = line.replace('<c><v>','')
            line = line.replace('</v>','')
            line = line.split('</c>')
        return line
    
    def read_dbase(self):
        """ Read the database
        
        Description: Reads the database and populates variables with processed data
        """
        # Setup database
        dbdir = self.spacecraft.db_dir
        local_dbdir = self.spacecraft.data_dir + 'database\\'
        cur_dir = os.getcwd()
        if self.spacecraft.omega == '2':
            # File names to search for
            files = {'command': '*_tc*.txt',
                     'macro': '*_mc*.txt',
                     'telemetry': '*_tm*.txt',
                     'telem_format': '*_fo*.txt',
                     'command_ver': '*_cv*.txt',
                     'sbus': '*_sb*.txt',
                     'wiring': '*_au*.txt'}
            f_dirs = {'command': 'cmd\\',
                     'macro': 'mcr\\',
                     'telemetry': 'tlm\\',
                     'telem_format': 'fmt\\',
                     'command_ver': 'ver\\',
                     'sbus': 'sbu\\',
                     'wiring': 'axl\\'}
            for key,db in files.items():
                copy_new_file = False
                fName = glob.glob(local_dbdir+db)
                os.chdir(dbdir+f_dirs[key])
                fName_newest = glob.glob(db)[0]
                os.chdir(cur_dir)
                if len(fName) == 0:
                    self.gui.output_text('    No local database %s file found. Copying from %s.' % (db, dbdir))
                    copy_new_file = True
                else:
                    # One file found, check version, archive old if found and copy new
                    fName = fName[0]
                    local_version = re.search('\d+', fName[fName.find('_')+1:]).group(0)
                    newest_version = re.search('\d+', fName_newest[fName_newest.find('_')+1:]).group(0)
                    if local_version != newest_version:
                        self.gui.output_text('    New database %s available. Removing old and copying new from %s.' 
                                             % (db, dbdir))
                        copy_new_file = True
                    else:
                        self.gui.output_text('    Using database %s' % local_dbdir+fName_newest)
                # Copy over database and extract
                if copy_new_file:
                    if not os.path.isdir(local_dbdir):
                        os.makedirs(local_dbdir)
                    if len(fName) != 0:
                        os.remove(fName)
                    shutil.copyfile(dbdir+f_dirs[key]+'\\'+fName_newest,local_dbdir+fName_newest)
                    self.gui.output_text('    Using database %s' % local_dbdir+fName_newest)
        else:
            # File names to search for
            ziped = '*Rev_*.xlsx'
            files = {'command': 'command.xml',
                     'limits': 'limits.xml',
                     'macro': 'macro_component.xml',
                     'telemetry': 'telemetry.xml',
                     'telem_format': 'tlm_format.xml',
                     'command_ver': 'cmd_verif_parameter.xml',
                     'sbus': 's-bus.xml',
                     'wiring': 'wiring.xml'}
            # Locate and copy files if necessary
            copy_new_file = False
            fName = glob.glob(local_dbdir+ziped)
            os.chdir(dbdir)
            fName_newest = glob.glob(ziped)[0]
            os.chdir(cur_dir)
            if len(fName) == 0:
                self.gui.output_text('    No local database file found. Copying from %s.' % dbdir)
                copy_new_file = True
            else:
                # One file found, check version, archive old if found and copy new
                fName = fName[0]
                local_version = fName[fName.find('Rev_')+4:fName.find('.xlsx')]
                newest_version = fName_newest[fName_newest.find('Rev_')+4:fName_newest.find('.xlsx')]
                if local_version != newest_version:
                    self.gui.output_text('    New database available. Removing old and copying new from %s.' % dbdir)
                    copy_new_file = True
                else:
                    self.gui.output_text('    Using database %s' % local_dbdir+fName_newest)
            # Copy over database and extract
            if copy_new_file:
                if os.path.isdir(local_dbdir):
                    shutil.rmtree(local_dbdir)
                os.makedirs(local_dbdir)
                shutil.copyfile(dbdir+fName_newest,local_dbdir+fName_newest)
                with zipfile.ZipFile(local_dbdir+fName_newest) as archive:
                    archive.extractall(local_dbdir)
                self.gui.output_text('    Using database %s' % local_dbdir+fName_newest)
        
        # Specify starting row for data (0 based indexing)
        if self.spacecraft.omega == '2':
            start_row = 2
            end_row_offset = 1
        else:
            start_row = 5
            end_row_offset = 2
        
        # Read commands
        file = get_file_list(self.gui, local_dbdir+files['command'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            cmd_num = line[0]
            cmd_name = line[1]
            if self.spacecraft.omega == '2':
                cmd_bin = line[10]
            else:
                cmd_bin = line[5]
            cmd = Components.CmdTlm()
            cmd.num = cmd_num
            cmd.des = cmd_name
            cmd.bin = cmd_bin
            self.cmd[cmd_num] = cmd
        f.close()
        
        # Read sbus
        file = get_file_list(self.gui, local_dbdir+files['sbus'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            sia_add = line[0]
            if self.spacecraft.omega == '2':
                router_ref = get_rd(line[7])
            else:
                router_ref = get_rd(line[5])
            self.sbus[sia_add] = router_ref
        f.close()
        
        # Read macros
        file = get_file_list(self.gui, local_dbdir+files['macro'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            mac_num = line[0]
            mac_name = line[1]
            if mac_num in self.mac.keys():
                mac = self.mac[mac_num]
            else:
                if self.spacecraft.omega == '2':
                    mac_name = line[3]
                else:
                    mac_name = line[1]
                mac = Components.CmdTlm()
                mac.num = mac_num
                mac.des = mac_name
                self.mac[mac_num] = mac
            if self.spacecraft.omega == '2':
                mac_bin = line[4]
            else:
                mac_bin = line[5]
            mac.bin += mac_bin
        f.close()
        
        # Read pids
        file = get_file_list(self.gui, local_dbdir+files['telemetry'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            tlm_num = line[0]
            tlm_name = line[1]
            tlm = Components.CmdTlm()
            tlm.num = tlm_num
            tlm.des = tlm_name
            if self.spacecraft.omega == '2':
                sia_address = line[9]
                tlm_format_key = tlm_num
            else:
                sia_address = line[10]
                tlm_format_key = line[6]
            tlm.sia_add = sia_address
            tlm.format_key = tlm_format_key
            self.tlm[tlm_num] = tlm
            if 'PCU' in tlm_name and ('Bus' in tlm_name or 'Bat' in tlm_name) and 'Cur' in tlm_name:
                if self.spacecraft.omega == '2':
                    tlm_des = line[3]
                else:
                    tlm_des = line[2]
                tray = re.search('Tray A(\d+)', tlm_des).group(1) # Get the tray number
                key = tlm_name[:4] + 'A%02d' % int(tray)
                key = key.replace(' ','')
                self.subbuses[key] = tlm
        f.close()
        self.subbuses['LVC'] = Components.CmdTlm()
        self.subbuses['LVC'].des = 'Total LoV Bus Curnt'
        self.subbuses['LVC'].num = 'PWD90065'
        
        # Read telemetry format
        file = get_file_list(self.gui, local_dbdir+files['telem_format'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            key = line[0]
            if self.spacecraft.omega == '2':
                value = line[1]
            else:
                value = line[3]
            if key not in self.tlm_format.keys():
                self.tlm_format[key] = []
            self.tlm_format[key].append(value)
        f.close()
        
        # Read verification
        file = get_file_list(self.gui, local_dbdir+files['command_ver'])
        f = open(file)
        lines = f.readlines()
        for r in range(start_row,len(lines)-end_row_offset):
            line = self.parse_line(lines[r], self.spacecraft.omega)
            tlm_num = line[0]
            if self.spacecraft.omega == '2':
                if line[7] != '':
                    max_atten = line[7]
                    self.ver[tlm_num] = max_atten
            else:
                if line[4] == 'MAX':
                    max_atten = line[5]
                    self.ver[tlm_num] = max_atten
        f.close()
        
        # Read limits
        if self.spacecraft.omega == '3':
            file = get_file_list(self.gui, local_dbdir+files['limits'])
            f = open(file)
            lines = f.readlines()
            self.limits = lines[start_row:-end_row_offset]
            f.close()
        
        # Read wiring/auxiliary
        file = get_file_list(self.gui, local_dbdir+files['wiring'])
        f = open(file)
        lines = f.readlines()
        self.wire_aux = lines[start_row:-end_row_offset]
        f.close()
    
    def carve_subbuses(self):
        """ Determine which subbus units are on
        
        Description: Populates subbus_data object with subbus data for all units
        Note: Currently only programmed for twta's and heaters - could be made generic in future.
        """
        data_by_dest = {}
        unit_filt = {}
        
        # First find LVC units and compile dictionaries/lists
        signal_name_prev = '' 
        orig = ''
        dest = ''
        for line in self.wire_aux:
            # Vectorize and gather data
            line = self.parse_line(line, self.spacecraft.omega)
            signal_name = line[1]
            signal_type = line[2]
            org_unit = line[3]
            org_ref = line[4]
            org_tray = line[5]
            os = 0 if self.spacecraft.omega == '2' else 1
            des_unit = line[9+os]
            des_ref = line[10+os]
            des_tray = line[11+os]
            
            # Sometimes data is on separate lines - full data is gathered from multiple lines
            # In such a case, the signal_name will be the same => reset when signal name is different
            if signal_name != signal_name_prev or (orig != '' and dest != ''):
                orig = ''
                dest = ''
                org_unit_full = ''
                org_ref_full = ''
                org_tray_full = ''
                des_unit_full = ''
            if org_unit != '' and org_ref != '' and (org_tray != '' or org_unit == 'MMDC' or org_unit == 'CPSU'):
                orig = (org_unit + org_ref + org_tray).replace(' ','')
                org_unit_full = org_unit
                org_ref_full = org_ref
                org_tray_full = org_tray
            if des_unit != '' and des_ref != '' and (des_tray != '' or des_unit == 'MMDC' or des_unit == 'CPSU'):
                dest = (des_unit + des_ref + des_tray).replace(' ','')
                des_unit_full = des_unit
            
            # Process units
            if orig != dest:
                if signal_type == '+31V' or signal_type == '31RTN': # Get 31V heaters
                    if 'Htr' in signal_name and 'Cur' not in signal_name:
                        u_name = adjust_htr_name(signal_name)
                        if 'rtn' in u_name.lower():
                            u_name = u_name[u_name.find('-')+1:]
                        u_name = u_name.replace(' ON/OFF','')
                        u_name = u_name.strip()
                        self.carved_subbuses[u_name] = self.subbuses['LVC']
                        self.carved_prefixes[u_name] = ''
                elif signal_type == 'PR':
                    # Group traceback data (wires)
                    if orig != '' and dest != '':
                        sb_key = org_tray_full.replace(' ','')
                        if re.search('104A|UPPC1', org_ref_full):
                            sb_key = 'PCU1' + sb_key
                        else:#if org_ref_full == '104B':
                            sb_key = 'PCU2' + sb_key
                        if des_unit_full == 'MMDC' or des_unit_full == 'CPSU':
                            if 'pri' in signal_name.lower():
                                dest += '_1'
                            elif 'red' in signal_name.lower():
                                dest += '_2'
                            else:
                                self.gui.output_text('    Warning - bad ass: %s - %s' % (dest, signal_name))
                        data_by_dest[dest] = [signal_name, orig, sb_key]
                    
                    # Find units to trace back and name appropriately
                    if 'TWT' in signal_name or 'EPC' in signal_name:
                        # Populate twta
                        rd = des_ref
                        if re.search('[A-Z]\d', rd[-2:]) and len(rd) > 4: # Strip out ending number for linked twtas
                            rd = rd[:-1]
                        u_name = 'TWTA ' + rd
                        if u_name not in unit_filt.keys():
                            unit_filt[u_name] = orig
                    elif 'Htr' in signal_name and 'Cur' not in signal_name and ('EHCT' in org_unit_full or 'BCE' in org_unit_full):
                        # Populate htr
                        u_name = adjust_htr_name(signal_name)
                        u_name = u_name.replace(' ON/OFF','')
                        if 'Comm' not in u_name and 'Pwr Htr' in u_name:
                            if 'Hi' in u_name:
                                t_ind = u_name.find('Hi')
                            else:
                                t_ind = u_name.find('Lo')
                            u_name = u_name[:t_ind] + 'Comm ' + u_name[t_ind:]
                        u_name.strip()
                        if u_name not in unit_filt.keys():
                            unit_filt[u_name] = orig
                    elif 'ace' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'ACE_' + re.search('\d', u_name).group(0)
                        unit_filt[u_name] = orig
                    elif 'icu' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'ICU_' + get_rd(u_name)
                        unit_filt[u_name] = orig
                    elif 'xmtr' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        unit_filt[u_name] = orig
                    elif 'rcvr' in signal_name.lower() and 'cmd' not in signal_name.lower():
                        u_name = re.search('Rcvr.*', signal_name).group(0)
                        unit_filt[u_name] = orig
                    elif re.search('dn?cnvtr|down converter', signal_name.lower()):
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'DCnvtr ' + get_rd(u_name)
                        unit_filt[u_name] = orig
                    elif re.search('up?cnvtr|up converter', signal_name.lower()):
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'UCnvtr ' + get_rd(u_name)
                        unit_filt[u_name] = orig
                    elif 'lna' in signal_name.lower() and 'htr' not in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'LNA ' + get_rd(u_name)
                        unit_filt[u_name] = orig
                    elif 'mro' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        if re.search('pri|red|side', signal_name.lower()):
                            num = get_rd(u_name)
                            u_name = 'MRO ' + num
                            if 'pri' in signal_name.lower():
                                u_name += ' Side 1'
                            elif 'red' in signal_name.lower():
                                u_name += ' Side 2'
                            elif 'side' in signal_name.lower():
                                u_name += signal_name[signal_name.find(num)+len(num):]
                        unit_filt[u_name] = orig
                    elif 'mlo' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        if re.search('pri|red|side', signal_name.lower()):
                            u_name = 'MLO ' + get_rd(u_name)
                            if 'pri' in signal_name.lower():
                                u_name += ' Side 1'
                            elif 'red' in signal_name.lower():
                                u_name += ' Side 2'
                            elif 'side' in signal_name.lower():
                                u_name += signal_name[signal_name.find(num)+len(num):]
                        unit_filt[u_name] = orig
                    elif 'mmdc' in signal_name.lower():
                        u_name = re.search('to .*', signal_name).group(0)[3:]
                        u_name = 'MMDC ' + get_rd(u_name)
                        if 'pri' in signal_name.lower():
                            u_name += ' Side 1'
                        elif 'red' in signal_name.lower():
                            u_name += ' Side 2'
                        else:
                            self.gui.output_text('    Warning - unknown MMDC side: %s' % signal_name)
                        unit_filt[u_name] = orig
                elif (signal_type == '+8V' and org_unit_full == 'MMDC') or (signal_type == '+6V' and org_unit_full == 'CPSU'):
                    if re.search('lna', signal_name.lower()):
                        u_name = 'LNA ' + get_rd(signal_name)
                    elif re.search('dn?cnvtr|down converter', signal_name.lower()):
                        u_name = 'DCnvtr ' + get_rd(signal_name)
                    elif re.search('up?cnvtr|up converter', signal_name.lower()):
                        u_name = 'UCnvtr ' + get_rd(signal_name)
                    elif re.search('mini', signal_name.lower()):
                        u_name = 'Mini-RX ' + get_rd(signal_name)
                    else:
                        self.gui.output_text('    Warning - unknown MMDC/CPSU unit: %s' % signal_name)
                    unit_filt[u_name+'_1'] = orig + '_1'
                    unit_filt[u_name+'_2'] = orig + '_2'
                    self.mmdc_assoc[u_name] = orig
                elif signal_type == '+8V' and 'cnvtr' in org_unit_full.lower() and 'dc/dc' not in signal_name.lower():
                    if re.search('lna', signal_name.lower()):
                        u_name = 'LNA ' + get_rd(signal_name)
                    elif re.search('dn?cnvtr|down converter', signal_name.lower()):
                        u_name = 'DCnvtr ' + get_rd(signal_name)
                    elif re.search('up?cnvtr|up converter', signal_name.lower()):
                        u_name = 'UCnvtr ' + get_rd(signal_name)
                    else:
                        self.gui.output_text('    Warning - unknown DC Cnvtr unit: %s' % signal_name)
                    unit_filt[u_name] = orig
                elif signal_type == 'Dig B' and org_unit_full == 'DC Cnvtr' and 'LNA' in signal_name:
                    u_name = 'LNA ' + get_rd(signal_name)
                    unit_filt[u_name] = orig
                signal_name_prev = signal_name
        
        # Trace back till find PCU
        for signal_name, orig in unit_filt.items():
            sb_key = ''
            u_name = signal_name
            u_orig = orig
            continue_search = True
            while 'PCU' not in signal_name and continue_search:
                if orig in data_by_dest.keys():
                    [signal_name, orig, sb_key] = data_by_dest[orig]
                else:
                    continue_search = False
            if continue_search:
                if sb_key in self.subbuses.keys():
                    self.carved_subbuses[u_name] = self.subbuses[sb_key]
                    self.carved_prefixes[u_name] = u_orig[-4] + u_orig[-1]
                else:
                    self.gui.output_text('    Warning - Couldn\'t trace subbus for ' + u_name)
            else:
                self.gui.output_text('    Warning - Couldn\'t trace subbus for ' + u_name)

#******************************************************************************************************************************
# Reader
#******************************************************************************************************************************

class Reader:
    """ Gather all inputs
    
    Description: Read databases and place into dictionaries
    Usage: Invoked by AutogenTool object in AutogenToolGui.py
    Public Methods: execute -- Get cmds/pids with description matching search string
    """
    def __init__(self, gui, spacecraft):
        """ Constructor
        
        Arguments: gui -- GUI object
                   spacecraft -- Spacecraft object
        """
        self.gui = gui
        self.spacecraft = spacecraft
        files = os.listdir(path=self.spacecraft.db_dir)
        if len(files) > 20:
            self.spacecraft.omega = '2'
        else:
            self.spacecraft.omega = '3'
    
    def _read_apps(self, file, a_type):
        """ Read thermal STIRS appendices
        
        Description: Reads thermal STIRS appendices for processing by scripts.
        Arguments: file -- Full path of file. See get_file_list().
                   a_type -- Type of appendix ('A', 'C', 'F', or 'G')
        Output: t_data -- dictionary of search string:found full path
        """
        # Open appendix
        workbook = xlrd.open_workbook(file)
        worksheets = workbook.sheet_names()
        worksheet = workbook.sheet_by_name(worksheets[0])
        nrows = worksheet.nrows
        ncols = worksheet.ncols
        
        # App G inits
        skip = False
        
        # Read data
        t_data = {}
        for r in range(nrows):
            data = []
            for c in range(ncols):
                val = str(worksheet.cell_value(r,c))
                # Get rid of float representation of exact numbers
                if len(val) > 2:
                    if val[-2:] == '.0':
                        val = val[:-2]
                data.append(val)
            if a_type == 'A': # Thermisters
                if r >= 1:
                    rt_num = data[1]
                    tlm = Components.CmdTlm()
                    tlm.num = data[0]
                    tlm.des = data[2].replace('"','')
                    t_data[rt_num] = tlm
            elif a_type == 'C': # Htr Cmd/Tlm
                if r >= 2:
                    htr_name = data[0]
                    i_d = {}
                    i_d['on_tlm'] = Components.CmdTlm()
                    i_d['on_tlm'].num = data[2]
                    i_d['on_tlm'].des = htr_name + ' ON/OFF St'
                    i_d['ena_tlm'] = Components.CmdTlm()
                    i_d['ena_tlm'].num = data[3]
                    i_d['ena_tlm'].des = htr_name + ' ENA/DIS St'
                    i_d['cur_mon_tlm'] = Components.CmdTlm()
                    i_d['cur_mon_tlm'].num = data[4]
                    i_d['cur_mon_tlm'].des = htr_name + ' Cur Mon'
                    i_d['on_cmd'] = Components.CmdTlm()
                    i_d['on_cmd'].num = data[5]
                    i_d['on_cmd'].des = htr_name + ' ON'
                    i_d['off_cmd'] = Components.CmdTlm()
                    i_d['off_cmd'].num = data[6]
                    i_d['off_cmd'].des = htr_name + ' OFF'
                    i_d['ena_cmd'] = Components.CmdTlm()
                    i_d['ena_cmd'].num = data[7]
                    i_d['ena_cmd'].des = htr_name + ' ENA'
                    i_d['dis_cmd'] = Components.CmdTlm()
                    i_d['dis_cmd'].num = data[8]
                    i_d['dis_cmd'].des = htr_name + ' DIS'
                    i_d_out = {}
                    for key in i_d.keys():
                        if re.search('\d+',i_d[key].num):
                            i_d_out[key] = i_d[key]
                    power_val = data[13]
                    t_data[htr_name] = [i_d_out, power_val]
                    self.spacecraft.sorted_htr_names.append(htr_name)
            elif a_type == 'F': # Heater Safety Relays
                if r >= 2:
                    htr_sfty_rly_name = data[0]
                    i_d = {}
                    i_d['on_tlm'] = Components.CmdTlm()
                    i_d['on_tlm'].num = data[2]
                    if data[3] == '':
                        i_d['on_tlm'].des = htr_sfty_rly_name + ' ON/OFF St'
                    else:
                        i_d['on_tlm'].des = htr_sfty_rly_name + '1 ON/OFF St'
                    i_d['on2_tlm'] = Components.CmdTlm()
                    i_d['on2_tlm'].num = data[3]
                    i_d['on2_tlm'].des = htr_sfty_rly_name + '2 ON/OFF St'
                    i_d['ena_tlm'] = Components.CmdTlm()
                    i_d['ena_tlm'].num = data[4]
                    i_d['ena_tlm'].des = htr_sfty_rly_name + ' ENA/DIS St'
                    i_d['on_mac'] = Components.CmdTlm()
                    i_d['on_mac'].num = data[5]
                    i_d['on_mac'].des = htr_sfty_rly_name + ' ON'
                    i_d['off_mac'] = Components.CmdTlm()
                    i_d['off_mac'].num = data[6]
                    i_d['off_mac'].des = htr_sfty_rly_name + ' OFF'
                    i_d['on_cmd'] = Components.CmdTlm()
                    i_d['on_cmd'].num = data[7]
                    i_d['on_cmd'].des = htr_sfty_rly_name + ' ON'
                    i_d['off_cmd'] = Components.CmdTlm()
                    i_d['off_cmd'].num = data[8]
                    i_d['off_cmd'].des = htr_sfty_rly_name + ' OFF'
                    i_d['ena_cmd'] = Components.CmdTlm()
                    i_d['ena_cmd'].num = data[9]
                    i_d['ena_cmd'].des = htr_sfty_rly_name + ' ENA'
                    i_d['dis_cmd'] = Components.CmdTlm()
                    i_d['dis_cmd'].num = data[10]
                    i_d['dis_cmd'].des = htr_sfty_rly_name + ' DIS'
                    # Remove entries that have no cmd/pid - do it in a single loop instead of individually
                    i_d_out = {}
                    for key in i_d.keys():
                        if re.search('\d+',i_d[key].num):
                            i_d_out[key] = i_d[key]
                    t_data[htr_sfty_rly_name] = i_d_out
            elif a_type == 'G': # Auto Heaters
                if r >= 2 and 'Spare' not in data[2]:
                    if data[1] == '1':
                        skip = False
                    if not skip:
                        # Add heater/safety relay
                        if data[1] == '1':
                            if 'Sfty Rly' in data[2]:
                                htr = Components.HtrSftyRly()
                            else:
                                htr = Components.Heater()
                            htr.name = data[2]
                            htr.vote_marg = [data[10], data[11]]
                            if self.spacecraft.omega == '3':
                                htr.rate = 'FAST'
                            else:
                                htr.rate = data[13]
                            t_data[htr.name] = htr
                        
                        # Add thermister
                        thrm = Components.Thermistor()
                        thrm.rt = data[3]
                        thrm.low_sp_dec = data[7]
                        thrm.high_sp_dec = data[8]
                        thrm.low_sp_hex = '0x%X' % int(data[5])
                        thrm.high_sp_hex = '0x%X' % int(data[6])
                        # Determine if higher counts are higher or lower temperature
                        if int(data[5]) < int(data[6]):
                            thrm.sp_dir = 1
                        else: 
                            thrm.sp_dir = -1
                        htr.thermisters.append(thrm)
                else:
                    skip = True
            else:
                self.gui.output_text('  Warning - Script sux ')
        
        # Close appendix and return
        return t_data
    
    def _sort_by_on(self, carve, source):
        """ Sort units by increasing on command number
        
        Description: Sorts units by increasing on command number to improve test flow.
        Arguments: carve -- Dictionary of script names:list of unit names
                   source -- Type of unit ('Htr', 'CfHtr', 'CfComTWT')
        Output: carve_t -- Sorted dictionary of script names:list of unit names
        """
        carve_t = carve
        if source == 'Htr':
            units = self.spacecraft.heaters
        elif source == 'CfHtr':
            units = self.spacecraft.cf_heaters
        elif source == 'CfComTWT':
            units = self.spacecraft.twtas
        for s_name in carve.keys():
            # Get on commands
            sorter_dict = {} 
            for u_name in carve[s_name]:
                cmds_pids = units[u_name].cmds_pids
                if 'on_cmd' in cmds_pids:
                    sorter = cmds_pids['on_cmd'].num
                else:
                    for cmd_pid in cmds_pids.values():
                        if len(cmd_pid) == 1:
                            sorter = cmd_pid[0].num
                            break
                sorter_dict[sorter] = u_name
            
            # Sort by on command
            carve_t[s_name] = []
            for sorter in sorted(sorter_dict.keys()):
                carve_t[s_name].append(sorter_dict[sorter])
        return carve_t
    
    def execute(self):
        """ Read spacecraft info
        
        Description: Reads spacecraft info in preparation for Writer object.
        """
        # Read database
        self.gui.output_text('  Reading database...')
        self.dbase = Dbase(self.gui, self.spacecraft)
        self.dbase.read_dbase()
        t0 = time.time()
        self.dbase.carve_subbuses()
        print('Subbusing: %s' % (time.time()-t0))
        self.spacecraft.data_dir
        # Read stirs
        self.gui.output_text('  Reading STIRS data...')
        files = get_file_list(self.gui, srch_strs=[self.spacecraft.data_dir+'*App A*.xls*',
                                                   self.spacecraft.data_dir+'*App C*.xls*',
                                                   self.spacecraft.data_dir+'*App F*.xls*',
                                                   self.spacecraft.data_dir+'*App G*.xls*'])
        self.app_a_data = self._read_apps(file=files[self.spacecraft.data_dir+'*App A*.xls*'], a_type='A')
        self.app_c_data = self._read_apps(file=files[self.spacecraft.data_dir+'*App C*.xls*'], a_type='C')
        self.app_f_data = self._read_apps(file=files[self.spacecraft.data_dir+'*App F*.xls*'], a_type='F')
        self.app_g_data = self._read_apps(file=files[self.spacecraft.data_dir+'*App G*.xls*'], a_type='G')
    
    def read_auto_heaters(self):
        """ Add auto heater data to spacecraft object """
        self.gui.output_text('  Adding auto heaters...')
        self.auto_heater_reader = AutoHeaters.AutoHeaterReader(self.gui, self.dbase, self.spacecraft)
        self.auto_heater_reader.add_units(self.app_a_data, self.app_c_data, self.app_f_data, self.app_g_data)
        self.auto_heater_reader.carve = self._sort_by_on(carve=self.auto_heater_reader.carve, source='Htr')
        self.dbase.check_dbase()
    
    def read_cf_heaters(self):
        """ Add cf heater data to spacecraft object """
        self.gui.output_text('  Adding cf heaters...')
        self.cf_heater_reader = CfHeaters.CfHeaterReader(self.gui, self.dbase, self.spacecraft)
        self.cf_heater_reader.add_units(self.app_c_data, self.app_f_data)
        self.cf_heater_reader.carve = self._sort_by_on(carve=self.cf_heater_reader.carve, source='CfHtr')
        self.dbase.check_dbase_cfheaters()
        self.cf_heater_reader.check_for_links()
    
    def read_twtas(self):
        """ Add twta data to spacecraft object """
        self.gui.output_text('  Adding twtas...')
        self.twta_reader = Twtas.TwtaReader(self.gui, self.dbase, self.spacecraft)
        t0 = time.time()
        self.twta_reader.add_units()
        print('TWTA Read: %s' % (time.time()-t0))
    
    def read_device(self):
        """ Add device file data to spacecraft object """
        self.read_cf_heaters()
        self.read_twtas()
        self.device_reader = Device.DeviceReader(self.gui, self.dbase, self.spacecraft)
        self.device_reader.add_units()
    
    def read_heater(self):
        """ Add device file data to spacecraft object """
        self.read_auto_heaters()
        self.heater_reader = Heater.HeaterReader(self.gui, self.dbase, self.spacecraft)
        self.heater_reader.add_units()

#******************************************************************************************************************************
# Writer
#******************************************************************************************************************************

class Writer:
    """ Write outputs
    
    Description: Writes output from input obtained by Reader
    Usage: Invoked by AutogenTool object in AutogenToolGui.py
    Public Methods: write_script -- Write specified script
    """
    def __init__(self, gui, dbase, spacecraft, author):
        """ Constructor
        
        Arguments: gui -- GUI object
                   dbase -- Database object
                   spacecraft -- Spacecraft object
                   author -- Author name string
        """
        self.gui = gui
        self.dbase = dbase
        self.spacecraft = spacecraft
        self.ah_carve = []
        self.cfh_carve = []
        self.twta_carve = []
        self.ah_scripter = AutoHeaters.AutoHeaterScript(gui, dbase, spacecraft, author)
        self.cfh_scripter = CfHeaters.CfHeaterScript(gui, dbase, spacecraft, author)
        self.twta_scripter = Twtas.TwtaScript(gui, dbase, spacecraft, author)
    
    # Main script writer func
    def write_script(self, s_name, s_type):
        """ Write specied script
        
        Description: Writes specied script
        Arguments: s_name -- script name string
                   s_type -- script type string ('AutoHtr', 'CfHtr', or 'CfComTWT')
        """
        # Determine type of script/units
        if s_type == 'AutoHtr':
            script = self.ah_scripter
            carve = self.ah_carve
        elif s_type == 'CfHtr':
            script = self.cfh_scripter
            carve = self.cfh_carve
        elif s_type == 'CfComTWT':
            script = self.twta_scripter
            carve = self.twta_carve
        
        # Setup script
        self.gui.output_text('  Generating ' + s_type + ' script ' + s_name + '...')
        script.name = s_name
        script.u_names = carve[s_name]
        
        # Write script
        script.write()
        
    def write_device(self):
        device_scripter = Device.DeviceScript(self.gui, self.dbase, self.spacecraft)
        device_scripter.write()
        
    def write_heater(self):
        heater_scripter = Heater.HeaterScript(self.gui, self.dbase, self.spacecraft)
        heater_scripter.write()

