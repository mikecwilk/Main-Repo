#******************************************************************************************************************************
# File: Heater.py
# Desc: Heater file Input/Output for automatic script generation
#******************************************************************************************************************************

import xlrd
import os
import re

#******************************************************************************************************************************
# Input
#******************************************************************************************************************************

class HeaterReader:
    """ Read heater file data
    
    Description:
    Usage:
    Public Variables:
    Public Methods:
    """
    
    def __init__(self, gui, dbase, spacecraft):
        """ Constructor
        
        Arguments: gui -- GUI object
                   dbase -- Database object
                   spacecraft -- Spacecraft object
        """
        self.gui = gui
        self.dbase = dbase
        self.spacecraft = spacecraft
    
    def _read_values(self):
        # Determine if limits are in database (O3 only) or if we need to use separate file
        use_database = False
        if self.spacecraft.omega == '3':
            if len(self.dbase.limits) > 0:
                use_database = True
            else:
                self.gui.output_text('  Limits database is empty! Searching for limits.xlsx...')
        
        # Sort through limit data
        thrm_limits = []
        if use_database:
            sorted_lines = []
            for line in self.dbase.limits:
                line = self.dbase.parse_line(line, self.spacecraft.omega)
                tlm_no = line[0]
                tlm_name = line[1]
                limit_set_name = line[3]
                if 'TH' in tlm_no and 'Temp' in tlm_name and limit_set_name == 'Ambient':
                    sorted_lines.append(line)
            for index in range(0,len(sorted_lines),2):
                throw_warning = False
                thrm_pid1 = sorted_lines[index+0][0]
                thrm_pid2 = sorted_lines[index+1][0]
                operator1 = sorted_lines[index+0][12]
                operator2 = sorted_lines[index+1][12]
                limit1 = sorted_lines[index+0][13]
                limit2 = sorted_lines[index+1][13]
                if (operator1 == '<' or operator1 == '&lt;') and (operator2 == '>' or operator2 == '&gt;'):
                    thrm_min = int(float(limit1))
                    thrm_max = int(float(limit2))
                elif (operator1 == '>' or operator1 == '&gt;') and (operator2 == '<' or operator2 == '&lt;'):
                    thrm_min = int(float(limit2))
                    thrm_max = int(float(limit1))
                else:
                    throw_warning = True
                if thrm_pid1 != thrm_pid2:
                    throw_warning = True
                if throw_warning:
                    self.gui.output_text('  Warning - Unresolved limits: %s - %s' % (thrm_pid1, thrm_pid2))
                else:
                    thrm_limits.append([thrm_pid1, thrm_min, thrm_max])
        else:
            file = self.spacecraft.data_dir+'limits.xlsx'
            if os.path.isfile(file):
                self.gui.output_text('  Found %s.' % file)
                workbook = xlrd.open_workbook(file)
                worksheets = workbook.sheet_names()
                worksheet = workbook.sheet_by_name(worksheets[0])
                nrows = worksheet.nrows
                for r in range(0,nrows):
                    thrm_pid = str(worksheet.cell_value(r,0))
                    thrm_min = str(worksheet.cell_value(r,3)).replace(' (1)','')
                    thrm_max = str(worksheet.cell_value(r,4)).replace(' (1)','')
                    if thrm_pid != '' and 'N/A' not in thrm_min and 'N/A' not in thrm_max:
                        thrm_min = int(float(thrm_min))
                        thrm_max = int(float(thrm_max))
                        thrm_limits.append([thrm_pid, thrm_min, thrm_max])
                    else:
                        break
            else:
                self.gui.output_text('  Warning - Could not find %s! Heater file will not have limits.' % file)
        
        # Search for thermisters and apply limits       
        for thrm_limit in thrm_limits:
            found = False
            for u_name in sorted(self.spacecraft.heaters.keys()):
                therms = self.spacecraft.heaters[u_name].thermisters
                for therm in therms:
                    thrm_pid = thrm_limit[0]
                    thrm_min = thrm_limit[1]
                    thrm_max = thrm_limit[2]
                    if thrm_pid == therm.tlm.num:
                        therm.lower_limit = thrm_min
                        therm.upper_limit = thrm_max
                        found = True
            if not found:
                self.gui.output_text('  Unit not found for limit for Thermistor %s' % thrm_pid)
    
    def add_units(self):
        self._read_values()
    
#******************************************************************************************************************************
# Output
#******************************************************************************************************************************

class HeaterScript:
    
    def __init__(self, gui, dbase, spacecraft):
        """ Constructor
         
        Arguments: gui -- GUI object
                   dbase -- Database object
                   spacecraft -- Spacecraft object
        """
        self.gui = gui
        self.dbase = dbase
        self.spacecraft = spacecraft
        self.script_name = spacecraft.script_dir + 'textsrc\\heaterfile.xml'
    
    def write(self):
        # Sort list of heaters by on tlm
        sorter_dict = {}
        for u_name in self.spacecraft.heaters.keys():
            if 'sfty' not in u_name.lower():
                cmds_pids = self.spacecraft.heaters[u_name].cmds_pids
                sorter_pid = int(cmds_pids[next(iter(cmds_pids))].num[-5:])
                sorter_dict[sorter_pid] = u_name
        sorted_heaters = []
        for sorter in sorted(sorter_dict.keys()):
            sorted_heaters.append(sorter_dict[sorter])
        
        # Write file
        f = open(self.script_name,'w')
        text = '<DEVICES>\n'
        for u_name in sorted_heaters:
            unit = self.spacecraft.heaters[u_name]
            if 'sfty' not in unit.name.lower():
                cmd_pid = unit.cmds_pids['on_cmd'].num
                if re.search('\d',cmd_pid[2]):
                    cmd_pid = cmd_pid[:2] + '_' + cmd_pid[2:]
                text += '<Device pid="%s">\n' % cmd_pid
                for thrm in unit.thermisters:
                    cmd_pid = thrm.tlm.num
                    thrm_min = thrm.lower_limit
                    thrm_max = thrm.upper_limit
                    if thrm_min == None or thrm_max == None:
                        self.gui.output_text('  Warning - Could not find limit for %s - %s!' % (thrm.name, cmd_pid))
                        thrm_min = 0
                        thrm_max = 0
                    if re.search('\d',cmd_pid[2]):
                        cmd_pid = cmd_pid[:2] + '_' + cmd_pid[2:]
                    text += '\t<Thermistor pid="%s"><RED op="&gt;" lim="%s"/><RED op="&lt;" lim="%s"/></Thermistor>\n' % \
                    (cmd_pid, thrm_max, thrm_min)
                text = text[:-1] + '</Device>\n'
        text += '</DEVICES>'
        f.write(text)        
        f.close()
