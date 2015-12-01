#******************************************************************************************************************************
# File: Twtas.py
# Desc: Twta Input/Output for automatic script generation
#******************************************************************************************************************************

import IOUtils
import Components
import ScriptUtils
import re
import textwrap

#******************************************************************************************************************************
# Input
#******************************************************************************************************************************

class TwtaReader:
    """ Read twta data
    
    Description: Read information from database to populate twtas
    Usage: Invoked by Reader object in IOUtils.py
    Public Variables: carve -- Dictionary of script names:list of unit names
    Public Methods: add_units -- Populate spacecraft object with twtas
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
        self.carve = {}
    
    def _get_carve_prefix(self, name):
        """ Get script name prefix
        
        Description: Get script name prefix using subbus identifier. Ex: SA_, NX3_, etc.
        Arguments: name -- unit name string
        Output: prefix -- subbus prefix string
        """
        twta = self.spacecraft.twtas[name]
        subbus = twta.subbus
        prefix = twta.cmds_pids['on_cmd'].num[:2] + '_'
        if int(subbus.num[2:]) < 60000:
            prefix += 'N'
        else:
            prefix += 'S'
        prefix += subbus.des[subbus.des.find('Bus')+4:subbus.des.find('Out')-1]
        return prefix
    
    def _twta_carve(self, twta_num):
        """ Determine script in which to test unit
        
        Description: Populates relevant carve object with unit name.
        Arguments: twta_num -- twta number string
        """
        # Search for regex in heater name
        twta_name = 'TWTA ' + twta_num
        
        # Strategy is: Two twtas per script, cannot have linked off commands
        post_fix = 0
        next_script = True
        while next_script:
            post_fix += 1
            script_name = 'TWT_' + self._get_carve_prefix(twta_name) + '_%s' % post_fix
            next_script = False
            if script_name not in self.carve:
                self.carve[script_name] = []
            elif len(self.carve[script_name]) == 1:
                if self.spacecraft.twtas[twta_name].linked_twta == self.carve[script_name][0]:
                    next_script = True # Disallow grouping of twtas with linked off commands
            elif len(self.carve[script_name]) == 2:
                next_script = True # Limit to max 2 per script
        self.carve[script_name].append(twta_name)
    
    def add_units(self):
        """ Populate spacecraft object with twtas
        
        Description: Iterates through database to obtain twta properties (cmds, tlm, etc.), then
        populates spacecraft object twta list.
        """
        # Define search rules. List of commands/pids/macros and regular expressions. This will be used like an ordered dict.
        # The first column (underscored entries) act like dict keys, and the second column is the regular expression search.
        twta_cmd_srch = ['on_cmd','on',
                         'off_cmd','off',
                         'aru_ena_cmd','aru e',
                         'aru_dis_cmd','aru d']
        twta_tlm_srch = ['on_tlm','on/off',
                         'anode_volt_tlm','anode',
                         'helix_curnt_tlm','helix',
                         'aru_tlm','aru s',
                         'aru_ena_tlm','aru e',
                         'bus_curnt_tlm','bus']
        camp_cmd_srch = ['mute_on_cmd','mute on',
                         'mute_off_cmd','mute off',
                         'on_cmd',' on',
                         'off_cmd',' off',
                         'fg_mode_cmd','fg ?mode',
                         'alc_mode_cmd',' alc ?mode',
                         'opa_lin_incr_cmd','opa incr|lin incr',
                         'opa_lin_decr_cmd','opa decr|lin decr',
                         'camp_incr_cmd','incr',
                         'camp_decr_cmd','decr']
        camp_tlm_srch = ['mute_on_tlm','mute on/off',
                         'on_tlm','on/off',
                         'fg_alc_mode_tlm','fgm/alc',
                         'input_pwr_mon_tlm','input p',
                         'output_pwr_mon_tlm','output p',
                         'opa_lin_atten_tlm','opa |lin atten',
                         'camp_atten_tlm','atten']
        
        # Get TWTA/LCamp data
        twta_cmds = self.dbase.get_cmd_pid(self.dbase.cmd,'twt')
        twta_pids = self.dbase.get_cmd_pid(self.dbase.tlm,'twt')
        camp_cmds = self.dbase.get_cmd_pid(self.dbase.cmd,'camp')
        if self.spacecraft.omega == '2': # O2 databases have LCamp macros
            camp_mcrs = self.dbase.get_cmd_pid(self.dbase.mac,'camp')
            camp_cmds = dict(camp_mcrs,**camp_cmds)
        camp_pids = self.dbase.get_cmd_pid(self.dbase.tlm,'camp')
        twta_camp_cmds = dict(twta_cmds,**camp_cmds)
        
        # Loop through twtas
        lcamp = Components.LCamp()
        for cmd_num in sorted(twta_camp_cmds.keys()):
            cmd_placed = False
            cmd = twta_camp_cmds[cmd_num]
            
            # Filter out ganged commands (O2 only), TT&C twtas, sequences, and subcalls.
            if (self.spacecraft.omega == '2' and re.search(',|/', cmd.des)) or 'TC' in cmd.num or \
            re.search('seq|subcall', cmd.des.lower()):
                self.gui.output_text('    Skipping cmd %s %s ' % (cmd.num, cmd.des))
                continue
            
            # Make TWTA
            if 'TWT' in cmd.des:
                for ci, cmd_type in enumerate(twta_cmd_srch[::2]):
                    if re.search(twta_cmd_srch[2*ci+1], cmd.des.lower()):
                        cmd_placed = True
                        if cmd_type == 'on_cmd': # 1 per TWTA, so we can create a TWTA object when it's found
                            # Make TWTA
                            rd = IOUtils.get_rd(cmd.des)
                            twta = Components.Twta('TWTA '+rd)
                            if twta.name in self.spacecraft.twtas.keys():
                                self.gui.output_text('    Warning - Duplicates of %s found!' % twta.name)
                            else:
                                self.spacecraft.twtas[twta.name] = twta
                                
                            # Treat TWTAs with RDs ending in [A-Z]1 (A1 or T1, for example) as unlinked.
                            # Treat TWTAs with RDs ending in [A-Z](2|4) (A4 or T2, for example) as linked.
                            if len(rd) > 4 and re.search('[A-Z]1', rd[-2:]):
                                twta.linked_off = False
                            elif len(rd) > 4 and re.search('[A-Z](2|4)', rd[-2:]):
                                twta.linked_off = True
                            
                            # Get tlm. Use different regular expressions based on format of RD.
                            # Case 1: New schema for linked twtas. RD ends with T1 or T2. Must get the following:
                            #    TWTA TWM105T1 ON/OFF St
                            #    TWTA TWM105 Anode T1 Volt
                            #    TWTA TWM105 Helix Curnt
                            #    TWTA TWM105 Bus Curnt
                            #    TWTA TWM105 ARU St
                            #    But not TWTA TWM105 Anode T2 Volt nor TWTA TWM105T2 ON/OFF St
                            # Case 2: Old schema for linked twtas. RD ends with letter than number (A1 or A4). Must get the following:
                            #    TWTA 33600A1 ON/OFF St
                            #    TWTA 33600A1 Anode Volt
                            #    TWTA 33600A Helix Curnt
                            #    TWTA 33600A1,4 ARU St
                            #    But not TWTA 33600A4 ON/OFF St nor TWTA 33600A4 Anode Volt
                            # Case 3: Single TWTAs. Sufficient to look for plain old RD (followed by space).
                            if re.search('T\d', rd[-2:]): # Case 1
                                pids = self.dbase.get_cmd_pid(twta_pids, rd[:-2]+'('+rd[-2:]+'| )')
                                pids = self.dbase.get_cmd_pid(pids, ' Anode T%s' % (3-int(rd[-1])), '!=') # Discard other
                            elif re.search('[A-Z]\d', rd[-2:]) and len(rd) > 4: # Case 2
                                pids = self.dbase.get_cmd_pid(twta_pids, rd[:-1]+'('+rd[-1]+'| |\d,)')
                            else: # Case 3
                                pids = self.dbase.get_cmd_pid(twta_pids, rd+' ')
                            for pid in pids.values():
                                for pi, pid_type in enumerate(twta_tlm_srch[::2]):
                                    if re.search(twta_tlm_srch[2*pi+1], pid.des.lower()):
                                        if pid_type in twta.cmds_pids.keys():
                                            op = twta.cmds_pids[pid_type]
                                            self.gui.output_text('    Warning - Duplicate %s tlm for %s: [%s: %s] vs [%s: %s]' % \
                                                                 (pid_type, twta.name, pid.num, pid.des, op.num, op.des))
                                        else:
                                            twta.cmds_pids[pid_type] = pid
                                        break
                                else:
                                    if 'Temp' in pid.des:
                                        self.gui.output_text('    Skipping TWT tlm %s %s ' % (pid.num, pid.des))
                                    else:
                                        self.gui.output_text('    Warning - TWT tlm %s %s not associated' % (pid.num, pid.des))
                        if cmd_type in twta.cmds_pids.keys():
                            oc = twta.cmds_pids[cmd_type]
                            self.gui.output_text('    Warning - Duplicate %s cmd for %s: [%s: %s] vs [%s: %s]' % \
                                                 (cmd_type, twta.name, cmd.num, cmd.des, oc.num, oc.des))
                        else:
                            twta.cmds_pids[cmd_type] = cmd
                        break
                    
            # Make LCamp
            if 'Camp' in cmd.des and 'TWT' not in cmd.des:
                for ci, cmd_type in enumerate(camp_cmd_srch[::2]):
                    if re.search(camp_cmd_srch[2*ci+1], cmd.des.lower()):
                        cmd_placed = True
                        rd = IOUtils.get_rd(cmd.des)
                        lcamp_name = 'LCamp '+rd
                        if cmd.num[2] == 'M':
                            lcamp = self.spacecraft.lcamps[lcamp_name]
                        if lcamp_name != lcamp.name and cmd.num[2] != 'M':
                            # Make LCamp
                            lcamp = Components.LCamp(lcamp_name)
                            if lcamp.name in self.spacecraft.lcamps.keys():
                                self.gui.output_text('    Warning - Duplicates of %s found!' % lcamp.name)
                            else:
                                self.spacecraft.lcamps[lcamp.name] = lcamp
                                # For descriptive RD schema, need to select proper twta for lcamp
                                # by swapping out the L in the name with a T. For the old schema,
                                # you can just go in order of the commands.
                                if re.search('T\d', twta.name[-2:]):
                                    twta_name_temp = 'TWTA ' + rd[:-2] + 'T' + lcamp.name[-1]
                                    twta = self.spacecraft.twtas[twta_name_temp]
                                twta.lcamp = lcamp
                            
                            # Get tlm
                            pids = self.dbase.get_cmd_pid(camp_pids, lcamp.name)
                            [camp_pids.pop(key) for key in pids.keys()] # Remove found items from storage for ultra-mega speed opto
                            for pid in pids.values():
                                for pi, pid_type in enumerate(camp_tlm_srch[::2]):
                                    if re.search(camp_tlm_srch[2*pi+1], pid.des.lower()):
                                        if pid_type in lcamp.cmds_pids.keys():
                                            op = lcamp.cmds_pids[pid_type]
                                            self.gui.output_text('    Warning - Duplicate %s tlm for %s: [%s: %s] vs [%s: %s]' % \
                                                                 (pid_type, lcamp.name, pid.num, pid.des, op.num, op.des))
                                        else:
                                            lcamp.cmds_pids[pid_type] = pid
                                        break
                                else:
                                    if 'Temp' in pid.des:
                                        self.gui.output_text('    Skipping LCamp tlm %s %s ' % (pid.num, pid.des))
                                    else:
                                        self.gui.output_text('    Warning - Warning - LCamp tlm %s %s not associated' % (pid.num, pid.des))
                        if 'camp_' in cmd_type or 'opa_' in cmd_type: # Determine if incr/decr is pulse train or single pulse command
                            if 'ddddd' in cmd.bin:
                                cmd_type += '_arg'
                                cnt = cmd.num[:2]+cmd.num[3:] if cmd.num[2] == 'M' else cmd.num
                                setattr(lcamp, cmd_type.replace('_cmd_arg',''), int(self.dbase.ver[cnt]))
                            else:
                                cmd_type += '_one'
                        if cmd_type in lcamp.cmds_pids.keys():
                            oc = lcamp.cmds_pids[cmd_type]
                            self.gui.output_text('    Warning - Duplicate %s cmd for %s: [%s: %s] vs [%s: %s]' % \
                                                 (cmd_type, lcamp.name, cmd.num, cmd.des, oc.num, oc.des))
                        else:
                            lcamp.cmds_pids[cmd_type] = cmd
                        break
                        
            # Make sure command was properly placed
            if not cmd_placed:
                self.gui.output_text('    Warning - cmd %s %s not associated' % (cmd.num, cmd.des))
        
        # Reorder list - This is needed to facilitate test flow:
        # Having a linked off command means that if you turn off 1, you turn off another.
        # This is problematic when doing power checks - when turning one off, you see the power
        # change corresponding to 2 TWTAs. This methodology avoids that by forcing linked twtas
        # to be in different scripts (by placing linked twtas at end of list).
        twta_names = sorted(self.spacecraft.twtas.keys())
        twta_carve_list_sorted = list(twta_names)
        for ind in range(len(twta_names)):
            twta = self.spacecraft.twtas[twta_names[ind]]
            if twta.linked_off:
                # If linked off command, add off command from linked twta. Also tell twtas what their linked twta is
                linked_twta = self.spacecraft.twtas[twta_names[ind-1]]
                twta.linked_twta = linked_twta.name
                linked_twta.linked_twta = twta.name
                if 'off_cmd' in linked_twta.cmds_pids.keys():
                    twta.cmds_pids['off_cmd'] = linked_twta.cmds_pids['off_cmd']
                if 'off_cmd' in twta.cmds_pids.keys():
                    linked_twta.cmds_pids['off_cmd'] = twta.cmds_pids['off_cmd']
                # Move linked twta to end of list
                for ind_t,twta_name_t in enumerate(twta_carve_list_sorted):
                    if twta_name_t == twta.name:
                        twta_carve_list_sorted.append(twta_carve_list_sorted.pop(ind_t))
                        break
        
        # Carve
        for twta_name in twta_carve_list_sorted:
            # Set subbus
            twta = self.spacecraft.twtas[twta_name]
            if twta.name in self.dbase.carved_subbuses.keys():
                twta.subbus = self.dbase.carved_subbuses[twta.name]
                twta.tray = self.dbase.carved_prefixes[twta.name]
                found_sb = True
            elif twta.name[:-1] in self.dbase.carved_subbuses.keys():
                twta.subbus = self.dbase.carved_subbuses[twta.name[:-1]]
                twta.tray = self.dbase.carved_prefixes[twta.name[:-1]]
                found_sb = True
            elif twta.name[:-2]+'E' in self.dbase.carved_subbuses.keys(): # New RD schema for linked twtas
                twta.subbus = self.dbase.carved_subbuses[twta.name[:-2]+'E']
                twta.tray = self.dbase.carved_prefixes[twta.name[:-2]+'E']
                found_sb = True
            elif twta.name[:-2] in self.dbase.carved_subbuses.keys(): # New RD schema (IS36) for linked twtas
                twta.subbus = self.dbase.carved_subbuses[twta.name[:-2]]
                twta.tray = self.dbase.carved_prefixes[twta.name[:-2]]
                found_sb = True
            else:
                self.gui.output_text('    Warning - Subbus not associated for ' + twta.name + \
                                     '. Unit will not be added to script!')
                found_sb = False
            if found_sb:
                twta_num = IOUtils.get_rd(twta.cmds_pids['on_cmd'].des)
                self._twta_carve(twta_num)
    
#******************************************************************************************************************************
# Output
#******************************************************************************************************************************

class TwtaScript(ScriptUtils.BaseScript):
    """ Write twta data
    
    Description: Write information compiled from TwtaReader to script
    Usage: Invoked by Writer object in IOUtils.py
    Public Variables: None
    Public Methods: None (write inherited from BaseScript)
    """
    extension = '.icl2'
    description = 'TWTA Command Functional'
    outline = textwrap.dedent('''\
    ############################### OUTLINE ###############################################
    #
    #\tI. ISTC Setup
    #\t\t- Request required packages
    #\t\t- STAMP
    #\t\t- Set Config
    #\t\t- Warning Prompts
    #
    #\tII. S/C Setup
    #\t\t- Dwell on PCU Sub-Bus
    #\t\t- Use snap procedure to record TWTA ON/OFF states to restore later
    #\t\t- Verify that the units about to be tested are OFF
    #\t\t- Load Sub-Bus in Prep for Power Measurements later on
    #
    #\tIII. Body of Test
    #\t\tCommand Verification
    #\t\t- Turn ON TWTA and Associated LCamp
    #\t\t- LCamp Command Verification
    #\t\t\t- LCamp Mute On/Off
    #\t\t\t- Verify that Fixed Gain Mode is selected by default
    #\t\t\t- LCamp FG/ALC Mode Select
    #\t\t- Gain Step Commanding for LCamp
    #\t\t\t- Verify Max Attenuation by default
    #\t\t\t- Decrement Attenuation by 11 steps, then by 1 step
    #\t\t\t- Increment Attenuation by 1 step, then by 11 steps
    #\t\t- OPA Step Commanding for LCamp
    #\t\t\t- Verify Max Attenuation by default
    #\t\t\t- Step down 10 steps, then 1 step
    #\t\t\t- Step up 1 step, then 10 steps
    #
    #\t\tPower Measurement
    #\t\t\t- Delay to allow TWTAs to time in
    #\t\t\t- Report TWTA/LCamp tlm while LCamp is ON
    #\t\t\t- Take LCamp Power Measurement
    #\t\t\t- Report TWTA/LCamp tlm while LCamp is OFF
    #\t\t\t- Report TWTA/LCamp tlm while TWTA is ON
    #\t\t\t- Take TWTA Power Measurement
    #\t\t\t- Report TWTA/LCamp tlm while TWTA is OFF
    #
    #\tIV. Clean Up
    #\t\t- Turn Off any Comm units that may have turned ON
    #
    #\tV. Tlm_Ch
    #
    #######################################################################################
    ''')
    istc_setup = textwrap.dedent('''\
    \tpackage require STO
    \tCONFIGURATION SET TARGETMODE false
    \tSTAMP
    REPORT
    REPORT
    REPORT --------------------------------------------------------------------------------
    REPORT --------------------------------------------------------------------------------
    REPORT I. iTACS Setup
    REPORT --------------------------------------------------------------------------------
    REPORT --------------------------------------------------------------------------------
    REPORT
    REPORT
    ''')
    
    def __init__(self, gui, dbase, spacecraft, author):
        """ Constructor
         
        Arguments: gui -- GUI object
                   dbase -- Database object
                   spacecraft -- Spacecraft object
                   author -- Author name string 
        """
        ScriptUtils.BaseScript.__init__(self, gui, dbase, spacecraft, author)
        self.script_dir = spacecraft.script_dir + 'cf\\CfComTWT\\'
    
    def _unit_on(self, unit):
        """ Write unit on functionality
        
        Description: Writes on functionality for twta/lcamp
        Arguments: unit -- twta object
        Output: text -- unit on string
        """
        lcamp = unit.lcamp
        text = ''
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Turn ON %s and %s and verify\n' % (unit.name, lcamp.name)
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += '\tCMD %s\t\t\t;# %s\n' % (unit.cmds_pids['on_cmd'].num, unit.cmds_pids['on_cmd'].des)
        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        text += '\tset StartTime [clock seconds]\n'
        text += 'REPORT\n'
        if 'on_cmd' in lcamp.cmds_pids.keys():
            on_cmd = lcamp.cmds_pids['on_cmd']
            text += '\tCMD %s\t\t\t;# %s\n' % (on_cmd.num, on_cmd.des)
        else:
            text += 'REPORT -------- %s does not have a unique On/Off Cmd\n' % (lcamp.name)
        if 'on_tlm' in lcamp.cmds_pids.keys():
            on_tlm = lcamp.cmds_pids['on_tlm']
            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (on_tlm.num, on_tlm.des)
        else:
            text += 'REPORT -------- %s does not have unique On/Off TLM\n' % (lcamp.name)
        return text
    
    def _unit_measure(self, unit):
        """ Write unit power measurement functionality
        
        Description: Writes power measurement functionality for twta/lcamp
        Arguments: unit -- twta object
        Output: text -- unit on string
        """
        # Power measurement: lcamp
        lcamp = unit.lcamp
        text = ''
        shared_tl_off = True
        if 'off_cmd' in lcamp.cmds_pids.keys():
            off_cmd =  lcamp.cmds_pids['off_cmd']
            if 'off_cmd' in unit.cmds_pids.keys():
                if off_cmd.num != unit.cmds_pids['off_cmd'].num:
                    shared_tl_off = False
            else:
                shared_tl_off = False
        if not shared_tl_off:
            if unit.test_lcamp and self.spacecraft.measure_camps:
                text += 'REPORT ================================================================================\n'
                text += 'REPORT ======== %s ON State ========\n' % lcamp.name
                text += 'REPORT\n'
                text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (lcamp.cmds_pids['on_tlm'].num, lcamp.cmds_pids['on_tlm'].des)
                if 'anode_volt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['anode_volt_tlm'].num, unit.cmds_pids['anode_volt_tlm'].des)
                if 'helix_curnt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['helix_curnt_tlm'].num,
                                                       unit.cmds_pids['helix_curnt_tlm'].des)
                if 'aru_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num, unit.cmds_pids['aru_tlm'].des)
                elif 'aru_ena_tlm':
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num, unit.cmds_pids['aru_ena_tlm'].des)
                if 'bus_curnt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['bus_curnt_tlm'].num, unit.cmds_pids['bus_curnt_tlm'].des)
                if 'fg_alc_mode_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                       lcamp.cmds_pids['fg_alc_mode_tlm'].des)
                text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['camp_atten_tlm'].num, lcamp.cmds_pids['camp_atten_tlm'].des)
                if 'opa_lin_atten_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['opa_lin_atten_tlm'].num,
                                                       lcamp.cmds_pids['opa_lin_atten_tlm'].des)
                if 'mute_on_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
                if 'input_pwr_mon_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['input_pwr_mon_tlm'].num,
                                                       lcamp.cmds_pids['input_pwr_mon_tlm'].des)
                if 'output_pwr_mon_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['output_pwr_mon_tlm'].num,
                                                       lcamp.cmds_pids['output_pwr_mon_tlm'].des)
                text += 'REPORT ================================================================\n'
                text += 'REPORT\n'
                text += '\tif {$::ReqPwrCheck} {\n'
                text += '\t\tDevicePower %s\n' % (lcamp.name.replace(' ', '_'))
                text += 'REPORT\n'
                text += '\t}\n'
                text += '\tCMD -m %s\t\t\t;# %s\n' % (lcamp.cmds_pids['off_cmd'].num, lcamp.cmds_pids['off_cmd'].des)
                text += 'REPORT\n'
                text += 'REPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                text += 'REPORT ~~~~~~~~ %s OFF State ~~~~~~~~\n' % lcamp.name
                text += 'REPORT\n'
                if 'on_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (lcamp.cmds_pids['on_tlm'].num, lcamp.cmds_pids['on_tlm'].des)
                if 'anode_volt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['anode_volt_tlm'].num, unit.cmds_pids['anode_volt_tlm'].des)
                if 'helix_curnt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['helix_curnt_tlm'].num,
                                                       unit.cmds_pids['helix_curnt_tlm'].des)
                if 'aru_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num, unit.cmds_pids['aru_tlm'].des)
                elif 'aru_ena_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num, unit.cmds_pids['aru_ena_tlm'].des)
                if 'bus_curnt_tlm' in unit.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['bus_curnt_tlm'].num, unit.cmds_pids['bus_curnt_tlm'].des)
                if 'fg_alc_mode_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                       lcamp.cmds_pids['fg_alc_mode_tlm'].des)
                text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['camp_atten_tlm'].num, lcamp.cmds_pids['camp_atten_tlm'].des)
                if 'opa_lin_atten_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['opa_lin_atten_tlm'].num,
                                                       lcamp.cmds_pids['opa_lin_atten_tlm'].des)
                if 'mute_on_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
                if 'input_pwr_mon_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['input_pwr_mon_tlm'].num,
                                                       lcamp.cmds_pids['input_pwr_mon_tlm'].des)
                if 'output_pwr_mon_tlm' in lcamp.cmds_pids.keys():
                    text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['output_pwr_mon_tlm'].num,
                                                       lcamp.cmds_pids['output_pwr_mon_tlm'].des)
                text += 'REPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                text += 'REPORT\n'
                text += 'REPORT\n'
            else:
                text += 'REPORT\n'
                if self.spacecraft.measure_camps:
                    text += 'REPORT -------- %s is not tested on %s. It is tested on %s\n' % (lcamp.name, unit.name, lcamp.testing_twta)
                else:
                    text += 'REPORT -------- Power measurements on LCamps are not required\n'
                text += 'REPORT\n'
        
        # Power measurement: twta
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ======== %s ON State ========\n' % unit.name
        text += 'REPORT\n'
        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        if 'anode_volt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['anode_volt_tlm'].num, unit.cmds_pids['anode_volt_tlm'].des)
        if 'helix_curnt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % ( unit.cmds_pids['helix_curnt_tlm'].num,  unit.cmds_pids['helix_curnt_tlm'].des)
        if 'aru_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num, unit.cmds_pids['aru_tlm'].des)
        elif 'aru_ena_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num, unit.cmds_pids['aru_ena_tlm'].des)
        if 'bus_curnt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['bus_curnt_tlm'].num, unit.cmds_pids['bus_curnt_tlm'].des)
        if 'fg_alc_mode_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num, lcamp.cmds_pids['fg_alc_mode_tlm'].des)
        text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['camp_atten_tlm'].num, lcamp.cmds_pids['camp_atten_tlm'].des)
        if 'opa_lin_atten_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['opa_lin_atten_tlm'].num, lcamp.cmds_pids['opa_lin_atten_tlm'].des)
        if 'mute_on_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
        if 'input_pwr_mon_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['input_pwr_mon_tlm'].num,
                                               lcamp.cmds_pids['input_pwr_mon_tlm'].des)
        if 'output_pwr_mon_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['output_pwr_mon_tlm'].num,
                                               lcamp.cmds_pids['output_pwr_mon_tlm'].des)
        text += 'REPORT ================================================================\n'
        text += 'REPORT\n'
        if shared_tl_off:
            on = unit.cmds_pids['on_cmd'].des[:-3].replace(' ', '_').replace(',', '')
        else:
            on = unit.name.replace(' ', '_')
        if 'bus_curnt_tlm' in unit.cmds_pids:
            text += '\tSTAAR_TREND %s %s epcA\t\t\t;# %s\n' % (on, unit.cmds_pids['bus_curnt_tlm'].num,
                                                               unit.cmds_pids['bus_curnt_tlm'].des)
            text += 'REPORT\n'
        text += '\tif {$::ReqPwrCheck} {\n'
        text += '\t\tDevicePower %s\n' % on
        text += 'REPORT\n'
        text += '\t}\n'
        if 'off_cmd' in unit.cmds_pids.keys():
            text += '\tCMD -m %s\t\t\t;# %s\n' % (unit.cmds_pids['off_cmd'].num, unit.cmds_pids['off_cmd'].des)
        else:
            text += '\tCMD -m %s\t\t\t;# %s\n' % (self.twta0.cmds_pids['off_cmd'].num, self.twta0.cmds_pids['off_cmd'].des)
        text += 'REPORT\n'
        text += 'REPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        text += 'REPORT ~~~~~~~~ %s OFF State ~~~~~~~~\n' % unit.name
        text += 'REPORT\n'
        if 'on_tlm' in unit.cmds_pids.keys():
            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        if 'anode_volt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['anode_volt_tlm'].num, unit.cmds_pids['anode_volt_tlm'].des)
        if 'helix_curnt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['helix_curnt_tlm'].num, unit.cmds_pids['helix_curnt_tlm'].des)
        if 'aru_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num, unit.cmds_pids['aru_tlm'].des)
        elif 'aru_ena_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num, unit.cmds_pids['aru_ena_tlm'].des)
        if 'bus_curnt_tlm' in unit.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (unit.cmds_pids['bus_curnt_tlm'].num, unit.cmds_pids['bus_curnt_tlm'].des)
        if 'fg_alc_mode_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num, lcamp.cmds_pids['fg_alc_mode_tlm'].des)
        text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['camp_atten_tlm'].num, lcamp.cmds_pids['camp_atten_tlm'].des)
        if 'opa_lin_atten_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['opa_lin_atten_tlm'].num, lcamp.cmds_pids['opa_lin_atten_tlm'].des)
        if 'mute_on_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
        if 'input_pwr_mon_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['input_pwr_mon_tlm'].num,
                                               lcamp.cmds_pids['input_pwr_mon_tlm'].des)
        if 'output_pwr_mon_tlm' in lcamp.cmds_pids.keys():
            text += '\tTLM %s\t\t\t;# %s\n' % (lcamp.cmds_pids['output_pwr_mon_tlm'].num,
                                               lcamp.cmds_pids['output_pwr_mon_tlm'].des)
        text += 'REPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        return text
    
    def _write_sc_setup(self):
        """ Write one time setup section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once before looping
        through each unit in the script is written here. Overrides BaseScript _write_istc_setup function.
        """
        # Setup
        text = ''
        if self.spacecraft.omega == '2':
            side_pid = 'DH01200'
            side_value = 'DHE1'
        else:
            side_pid = 'DH50200'
            side_value = 'GSP1'
        self.band = self.spacecraft.twtas[self.u_names[0]].cmds_pids['on_tlm'].num[:2]
        
        # Power check
        text += '\t;# Require power check only when in Reference Performance and on side 1\n'
        text += '\tset ::ReqPwrCheck false\n'
        text += '\tif {[DBASE VEHICLE PHASENUM] == 13 && [TLM -q %s] == "%s"} {\n' % (side_pid, side_value)
        text += '\t\tset ::ReqPwrCheck true\n'
        text += '\t}\n'
        text += '\tset ::ReqPwrCheck true\t\t\t;# Force power check - pending STIM357 updates\n'
        
        # Dialog
        text += 'REPORT\n'
        text += '\tif { ![info exists ::%s_CfComTWT_Prompts] } {\n' % self.band
        text += '\t\tif {$::ReqPwrCheck} {\n'
        text += '\t\t\tset action [DIALOG select -justify left -title "Verify OK to Proceed" -values {Continue Abort} -text \\\n'
        text += '\t\t\t"This script may use any two Com TWTAs as a sub-bus load, but most likely\\n\\\n'
        text += '\t\t\tthose in the same sub-system / band (%s, in this case).\\n\\n\\\n' % self.band
        text += '\t\t\tVerify there is no parallel RF testing taking place.\\n\\\n'
        text += '\t\t\t\\nAcknowledge by entering Continue or Abort."]\n'
        text += '\t\t\tif {"$action" == "Abort"} {exit}\n'
        text += '\t\t}\n'
        text += '\t}\n'
        
        # Dialog
        text += 'REPORT\n'
        text += '\tif { ![info exists ::%s_CfComTWT_Prompts]} {\n' % self.band
        text += '\t\tset action [DIALOG select -justify left -title "Verify OK to Proceed" -values \\\n'
        text += '\t\t{Continue Abort {Acknowledge All}} -text \\\n'
        text += '\t\t"This script will test the following TWTAs and associated LCamps:\\n\\n\\\n'
        for u_name in self.u_names:
            text += '\t\t' + u_name + '\\n\\\n'
        text += '\t\t\\nVerify this is okay before proceeding.\\n\\\n'
        text += '\t\t\\nAcknowledge by entering Continue, Abort, or Acknowledge All.\\n\\n\\\n'
        text += '\t\tSelecting \\"Acknowledge All\\" will suppress future warning prompts\\n\\\n'
        text += '\t\tfor all other %s CfComTWT run from this ICL2 Script GUI instance.\\n\\\n' % self.band
        text += '\t\tDo so ONLY if you are certain that no other RF testing will\\n\\\n'
        text += '\t\ttake place while these tests are being run.\\n"]\n'
        text += '\t\tif {"$action" == "Abort"} {exit}\n'
        text += '\t\tif { [ string match -nocase *all* $action ] } {\n'
        text += '\t\t\tset ::%s_CfComTWT_Prompts false\n' % self.band
        text += '\t\t}\n'
        text += 'REPORT\n'
        text += '\t}\n'
        
        # Cleanup
        text += '\tkwproc cleanup {args} {\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT IV. Cleanup Procedure\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tif { [ llength $args ] == 0 } {\n'
        text += '\t\tunset -nocomplain ::%s_CfComTWT_Prompts\n' % self.band
        text += 'REPORT\n'
        text += '\t}\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Turn Off any TWTAs that were turned on by Sub-Bus loading procedures\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += '\tif {$::ReqPwrCheck} {\n'
        
        # Turn off twtas
        for u_name in self.u_names:
            twta_off = self.spacecraft.twtas[u_name].cmds_pids['on_tlm']
            text += '\t\tglobal return%s\n' % (twta_off.num)
            text += '\t\tif { [info exists return%s] } {\n'  % (twta_off.num)
            text += '\t\t\tforeach cmd [lrange $return%s 1 end] {\n'  % (twta_off.num)
            text += '\t\t\t\tCMD $cmd\n'
            text += '\t\t\t}\n'
            text += '\t\t}\n'
        text += '\t}\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Verify that the units tested are OFF\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        for u_name in self.u_names:
            unit = self.spacecraft.twtas[u_name].lcamp
            if 'off_cmd' in unit.cmds_pids.keys():
                unit_off = unit.cmds_pids['off_cmd']
                text += 'REPORT\n'
                text += '\tCMD -m %s\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
                if 'on_tlm' in unit.cmds_pids.keys():
                    unit_off = unit.cmds_pids['on_tlm']
                    text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
        for u_name in self.u_names:
            unit = self.spacecraft.twtas[u_name]
            unit_off = unit.cmds_pids['off_cmd']
            text += 'REPORT\n'
            text += '\tCMD -m %s\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
            unit_off = unit.cmds_pids['on_tlm']
            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
        
        # Dwell
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\t}\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT II. S/C Setup\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tif {$::ReqPwrCheck} {\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Dwell on PCU Sub-Bus\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        twta0 = self.spacecraft.twtas[self.u_names[0]]
        self.twta0 = twta0
        if self.spacecraft.omega == '2':
            text += '\t\tRELEASE DWELLWORD 4\n'
            text += '\t\tINSTALL DWELLWORD %s\n' % (twta0.subbus.num)
        else:
            text += '\t\tREQUIRE DWELLWORD %s\n' % (twta0.subbus.num)
        text += 'REPORT\n'
        text += '\t}\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Verify that the units about to be tested are OFF\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        
        # Verify units off: LCamp, TWT
        for u_name in self.u_names:
            unit = self.spacecraft.twtas[u_name].lcamp
            if 'off_cmd' in unit.cmds_pids.keys():
                unit_off = unit.cmds_pids['off_cmd']
                text += 'REPORT\n'
                text += '\tCMD -m %s\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
                if 'on_tlm' in unit.cmds_pids.keys():
                    unit_off = unit.cmds_pids['on_tlm']
                    text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
        for u_name in self.u_names:
            unit = self.spacecraft.twtas[u_name]
            unit_off = unit.cmds_pids['off_cmd']
            text += 'REPORT\n'
            text += '\tCMD -m %s\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
            unit_off = unit.cmds_pids['on_tlm']
            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit_off.num, unit_off.des)
        
        # Load subbus
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Load Sub-Bus in Prep for Power Measurements later on\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += '\tif {$::ReqPwrCheck} {\n'
        demote_list = []
        for u_name in self.u_names:
            twta = self.spacecraft.twtas[u_name]
            twta_off = twta.cmds_pids['on_tlm']
            demote_list.append(twta_off.num)
            if twta.linked_twta in self.spacecraft.twtas.keys():
                linked_twta = self.spacecraft.twtas[twta.linked_twta]
                twta_off = linked_twta.cmds_pids['on_tlm']
                demote_list.append(twta_off.num)
        text += '\t\tvariable return%s [ SUBBUS Comm_LOAD %s ' % (twta0.cmds_pids['on_tlm'].num, twta0.cmds_pids['on_tlm'].num)
        text += '{ ' + ' '.join(demote_list) + ' } ]\n'
        text += '\t\tif {![lindex $return%s 0 ]} {\n'  % (twta0.cmds_pids['on_tlm'].num)
        text += '\t\t\tDIALOG acknowledge -priority warning -text \\\n'
        text += '\t\t\t"The Sub-bus (%s, %s) may not be loaded to a full 2 amps.\\n\\n\\\n' % (twta0.subbus.des,
                                                                                               twta0.subbus.num)
        text += '\t\t\tThe script has turned on two TWTAs to attempt to do so, but based\\n\\\n'
        text += '\t\t\ton the expected power consumption, this may not be high enough,\\n\\\n'
        text += '\t\t\tonce those TWTAs time-in.\\n\\n\\\n'
        text += '\t\t\tYou may either load the Sub-Bus manually or continue as is.\\n\\\n'
        text += '\t\t\t\\nContinue when ready."\n'
        text += '\t\t} elseif {[lindex $return%s 0] == -1 } {\n'  % (twta0.cmds_pids['on_tlm'].num)
        text += '\t\t\tcleanup\n'
        text += '\t\t\texit 1\n'
        text += '\t\t}\n'
        text += '\t}\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT III. Body of Test\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT Command Verification\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Turn units on
        for u_name_temp in self.u_names:
            text += self._unit_on(unit=self.spacecraft.twtas[u_name_temp])
        
        # Write
        self.f.write(text)
    
    def _write_unit_body(self, u_name):
        """ Write body for specified unit
        
        Description: Called for each unit by _write_body function inherited from BaseScript. Overrides BaseScript 
        _write_unit_body function.
        Arguments: u_name -- Unit name string
        """
        # Front matter
        unit = self.spacecraft.twtas[u_name]
        lcamp = unit.lcamp
        text = ''
        
        # Twta command verification: ARU ena/dis
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT TWTA Command Verification for %s\n' % unit.name
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        if 'aru_ena_cmd' in unit.cmds_pids.keys():
            text += 'REPORT -------- TWTA ARU Ena/Dis --------\n'
            text += 'REPORT\n'
            text += '\tCMD %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_cmd'].num, unit.cmds_pids['aru_ena_cmd'].des)
            if 'aru_ena_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_ena_tlm'].format_key][0],
                                                         unit.cmds_pids['aru_ena_tlm'].des)
            elif 'aru_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_tlm'].format_key][0],
                                                         unit.cmds_pids['aru_tlm'].des)
            text += '\tCMD %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_dis_cmd'].num, unit.cmds_pids['aru_dis_cmd'].des)
            if 'aru_ena_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_ena_tlm'].format_key][1],
                                                         unit.cmds_pids['aru_ena_tlm'].des)
            elif 'aru_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_tlm'].format_key][1],
                                                         unit.cmds_pids['aru_tlm'].des)
            text += '\tCMD %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_cmd'].num, unit.cmds_pids['aru_ena_cmd'].des)
            if 'aru_ena_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_ena_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_ena_tlm'].format_key][0],
                                                         unit.cmds_pids['aru_ena_tlm'].des)
            elif 'aru_tlm' in unit.cmds_pids:
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (unit.cmds_pids['aru_tlm'].num,
                                                         self.dbase.tlm_format[unit.cmds_pids['aru_tlm'].format_key][0],
                                                         unit.cmds_pids['aru_tlm'].des)
        elif unit.linked_twta in self.spacecraft.twtas.keys():
            linked_twta = self.spacecraft.twtas[unit.linked_twta]
            if 'aru_ena_cmd' in linked_twta.cmds_pids.keys():
                text += 'REPORT -------- %s ARU Ena/Dis tested with %s\n' % (unit.name, linked_twta.name)                
                text += '\tCMD -m %s\t\t\t;# %s\n' % (linked_twta.cmds_pids['aru_ena_cmd'].num,
                                                      linked_twta.cmds_pids['aru_ena_cmd'].des)
                text += '\tTLM EQ %s ENA\t\t\t;# %s\n' % (linked_twta.cmds_pids['aru_ena_tlm'].num,
                                                          linked_twta.cmds_pids['aru_ena_tlm'].des)
            else:
                text += 'REPORT -------- %s does not have ARU Ena/Dis\n' % unit.name
        else:
            text += 'REPORT -------- %s does not have ARU Ena/Dis\n' % unit.name
        text += 'REPORT\n'
        
        # LCamp command verification : on/off
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT LCamp Command Verification for %s\n' % lcamp.name
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        if unit.test_lcamp:
            if 'mute_on_cmd' in lcamp.cmds_pids.keys():
                text += 'REPORT -------- LCamp Mute On/Off --------\n'
                text += 'REPORT\n'
                text += '\tCMD %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_cmd'].num, lcamp.cmds_pids['mute_on_cmd'].des)
                text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
                text += 'REPORT\n'
                text += '\tCMD %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_off_cmd'].num, lcamp.cmds_pids['mute_off_cmd'].des)
                text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
                text += 'REPORT\n'
                text += '\tCMD %s\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_cmd'].num, lcamp.cmds_pids['mute_on_cmd'].des)
                text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (lcamp.cmds_pids['mute_on_tlm'].num, lcamp.cmds_pids['mute_on_tlm'].des)
            else:
                text += 'REPORT -------- %s does not have Mute\nREPORT\n' % lcamp.name
            text += 'REPORT\n'
            
            # LCamp command verification : fixed gain mode
            if 'fg_alc_mode_tlm' in lcamp.cmds_pids.keys():
                text += 'REPORT -------- Verify that Fixed Gain Mode is selected by default --------\n'
                text += 'REPORT\n'
                text += '\tTLM EQ %s FGM\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                          lcamp.cmds_pids['fg_alc_mode_tlm'].des)
                text += 'REPORT\n'
                text += 'REPORT -------- LCamp FG/ALC Mode Select --------\n'
                text += 'REPORT\n'
                text += '\tCMD -m %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_mode_cmd'].num, lcamp.cmds_pids['fg_mode_cmd'].des)
                text += '\tTLM EQ %s FGM\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                          lcamp.cmds_pids['fg_alc_mode_tlm'].des)
                text += 'REPORT\n'
                text += '\tCMD %s\t\t\t;# %s\n' % (lcamp.cmds_pids['alc_mode_cmd'].num, lcamp.cmds_pids['alc_mode_cmd'].des)
                text += '\tTLM EQ %s ALC\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                          lcamp.cmds_pids['fg_alc_mode_tlm'].des)
                text += 'REPORT\n'
                text += '\tCMD %s\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_mode_cmd'].num, lcamp.cmds_pids['fg_mode_cmd'].des)
                text += '\tTLM EQ %s FGM\t\t\t;# %s\n' % (lcamp.cmds_pids['fg_alc_mode_tlm'].num,
                                                          lcamp.cmds_pids['fg_alc_mode_tlm'].des)
            else:
                text += 'REPORT -------- %s does not have FGM/ALC Mode\n' % lcamp.name
            text += 'REPORT\n'
            
            # LCamp command verification : camp gain step
            atten = lcamp.camp_incr
            atten_tlm = lcamp.cmds_pids['camp_atten_tlm']
            incr_cmd_arg = lcamp.cmds_pids['camp_incr_cmd_arg']
            decr_cmd_arg = lcamp.cmds_pids['camp_decr_cmd_arg']
            if 'camp_decr_cmd_one' in lcamp.cmds_pids.keys():
                incr_cmd_one = lcamp.cmds_pids['camp_incr_cmd_one']
                decr_cmd_one = lcamp.cmds_pids['camp_decr_cmd_one']
                step_arg = ''
            else:
                incr_cmd_one = lcamp.cmds_pids['camp_incr_cmd_arg']
                decr_cmd_one = lcamp.cmds_pids['camp_decr_cmd_arg']
                step_arg = ' 0'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Gain Step Commanding for %s\n' % lcamp.name
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT -------- Verify Max Attenuation by default --------\n'
            text += 'REPORT\n'
            text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten, atten_tlm.des)
            text += 'REPORT\n'
            text += 'REPORT -------- Decrement Attenuation by 11 steps, then by 1 step --------\n'
            text += 'REPORT\n'
            text += '\tCMD %s 10\t\t\t;# %s\n' % (decr_cmd_arg.num, decr_cmd_arg.des)
            text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-11, atten_tlm.des)
            text += 'REPORT\n'
            text += '\tCMD %s%s\t\t\t;# %s\n' % (decr_cmd_one.num, step_arg, decr_cmd_one.des)
            text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-12, atten_tlm.des)
            text += 'REPORT\n'
            text += 'REPORT -------- Increment Attenuation by 1 step, then by 11 steps --------\n'
            text += 'REPORT\n'
            text += '\tCMD %s%s\t\t\t;# %s\n' % (incr_cmd_one.num, step_arg, incr_cmd_one.des)
            text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-11, atten_tlm.des)
            text += 'REPORT\n'
            text += '\tCMD %s 10\t\t\t;# %s\n' % (incr_cmd_arg.num, incr_cmd_arg.des)
            text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten, atten_tlm.des)
            text += 'REPORT\n'
            
            # LCamp command verification : lin/opa gain step
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT OPA/LIN Step Commanding for %s\n' % lcamp.name
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            if 'opa_lin_atten_tlm' in lcamp.cmds_pids.keys():
                atten = lcamp.opa_lin_incr
                atten_tlm = lcamp.cmds_pids['opa_lin_atten_tlm']
                incr_cmd_arg = lcamp.cmds_pids['opa_lin_incr_cmd_arg']
                decr_cmd_arg = lcamp.cmds_pids['opa_lin_decr_cmd_arg']
                if 'opa_lin_incr_cmd_one' in lcamp.cmds_pids.keys():
                    incr_cmd_one = lcamp.cmds_pids['opa_lin_incr_cmd_one']
                    decr_cmd_one = lcamp.cmds_pids['opa_lin_decr_cmd_one']
                    step_arg = ''
                else:
                    incr_cmd_one = lcamp.cmds_pids['opa_lin_incr_cmd_arg']
                    decr_cmd_one = lcamp.cmds_pids['opa_lin_decr_cmd_arg']
                    step_arg = ' 0'
                text += 'REPORT -------- Verify Max Attenuation by default --------\n'
                text += 'REPORT\n'
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten, atten_tlm.des)
                text += 'REPORT\n'
                text += 'REPORT -------- Decrement Attenuation by 10 steps, then by 1 step --------\n'
                text += 'REPORT\n'
                text += '\tCMD %s 9\t\t\t;# %s\n' % (decr_cmd_arg.num, decr_cmd_arg.des)
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-10, atten_tlm.des)
                text += 'REPORT\n'
                text += '\tCMD %s%s\t\t\t;# %s\n' % (decr_cmd_one.num, step_arg, decr_cmd_one.des)
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-11, atten_tlm.des)
                text += 'REPORT\n'
                text += 'REPORT -------- Increment Attenuation by 1 step, then by 10 steps --------\n'
                text += 'REPORT\n'
                text += '\tCMD %s%s\t\t\t;# %s\n' % (incr_cmd_one.num, step_arg, incr_cmd_one.des)
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten-10, atten_tlm.des)
                text += 'REPORT\n'
                text += '\tCMD %s 9\t\t\t;# %s\n' % (incr_cmd_arg.num, incr_cmd_arg.des)
                text += '\tTLM EQ %s %s\t\t\t;# %s\n' % (atten_tlm.num, atten, atten_tlm.des)
            else:
                text += 'REPORT -------- %s does not have OPA/LIN gain stepping\n' % lcamp.name
        else:
            text += 'REPORT -------- %s is not tested on %s. It is tested on %s\n' % (lcamp.name, unit.name, lcamp.testing_twta)
        text += 'REPORT\n'
        
        # Write
        self.f.write(text)
    
    def _write_footer(self):
        """ Write one time footer section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once after looping
        through each unit in the script is written here. Overrides BaseScript _write_footer function.
        """
        text = ''
        
        # Perform unit power measurement
        text += 'REPORT\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT Power Measurement\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tif {$::ReqPwrCheck} {\n'
        text += 'REPORT -------- Delay to allow TWTAs to time in --------\n'
        text += 'REPORT\n'
        text += '\t\tset DelayTime [expr {int(261 - ( [clock seconds] - $StartTime) ) } ]\n'
        text += '\t\tDELAY $DelayTime\n'
        text += 'REPORT\n'
        text += '\t}\n'
        
        # Off and verification
        for u_name_temp in self.u_names:
            text += self._unit_measure(unit=self.spacecraft.twtas[u_name_temp])
        
        # Write
        text += 'REPORT --------------------------------\n'
        text += 'REPORT -------- End of Test --------\n'
        text += 'REPORT --------------------------------\n'
        text += 'REPORT\n'
        text += '\tcleanup -normal\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT V. TlmCH\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tTlmCH\n'
        text += 'REPORT\n'
        text += '\tPUBLISH CfComTWT\n'
        text += 'REPORT\n'
        text += '############################### End of Script #########################################\n'
        
        # Write and close
        self.f.write(text)
        self.f.close()
