#******************************************************************************************************************************
# File: CfHeaters.py
# Desc: Cf Heater Input/Output for automatic script generation
#******************************************************************************************************************************

import IOUtils
import Components
import ScriptUtils
import re
import textwrap

#******************************************************************************************************************************
# Input
#******************************************************************************************************************************

class CfHeaterReader:
    """ Read cf heater data
    
    Description: Read information from thermal STIRS and database to populate cf heaters
    Usage: Invoked by Reader object in IOUtils.py
    Public Variables: carve -- Dictionary of script names:list of unit names
    Public Methods: add_units -- Populate spacecraft object with cf heaters
    """
    
    # Dictionary of regex:script name for cf heaters
    carve_search = {'Prop [^Tank]|MST':'PROP',
                    '^AEP.*A Htr':'AEP_TH_A',
                    '^AEP.*B Htr':'AEP_TH_B',
                    '^EP.*A Htr':'EP_TH_A',
                    '^EP.*B Htr':'EP_TH_B',
                    '^East T':'E_TH',
                    '^West T':'W_TH',
                    'Xe':'XENON',
                    'SPT Rad':'SPT',
                    'XFC':'XFC',
                    'SPT DAPM':'SPT_DAPM',
                    '^RW |RLG':'ADCS',
                    '^Star':'STAR_TRACKER',
                    '^N SSM':'N_SSM',
                    '^S SSM':'S_SSM',
                    'SSM Htr':'SSM',
                    '^N Comm H':'NHIPWR',
                    '^N Comm L':'NLOPWR',
                    '^S Comm H':'SHIPWR',
                    '^S Comm L':'SLOPWR',
                    '^N Upper Comm H':'N_UPPER_HIPWR',
                    '^N Upper Comm L':'N_UPPER_LOPWR',
                    '^S Upper Comm H':'S_UPPER_HIPWR',
                    '^S Upper Comm L':'S_UPPER_LOPWR',
                    '^N Lower Comm H':'N_LOWER_HIPWR',
                    '^N Lower Comm L':'N_LOWER_LOPWR',
                    '^S Lower Comm H':'S_LOWER_HIPWR',
                    '^S Lower Comm L':'S_LOWER_LOPWR',
                    '^Upper.*Res':'UPPER_RES',
                    '^Mid.*Res':'MID_RES',
                    '^Lower.*Res':'LOWER_RES',
                    'Boom':'BOOM',
                    'Reflector':'REFL',
                    'Rx Panel':'RX_PANEL',
                    '[^SPT]EDAPM':'EDAPM',
                    '[^SPT][^EDAPM]DAPM':'DAPM',
                    '^PMA':'PMA',
                    '^DSS|^ES H|^ECASS':'SENSOR',
                    '^FEED':'FEED',
                    'Mtr':'MTR',
                    'Damper':'DAMPER_HTR',
                    '^Press':'PRESS_TANK',
                    '^Prop Tank':'PROP_TANK',
                    '^Ox Tank':'OX_TANK',
                    '^Fuel Tank':'FUEL_TANK',
                    '^LNA':'LNA',
                    '^S LNA':'S_LNA',
                    '^N LNA':'N_LNA',
                    'MLHP':'MLHP',
                    '^Notch':'NF',
                    '^S Notch':'S_NF',
                    '^N Notch':'N_NF'}
    
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
        
        Description: Get script name prefix using subbus identifier. Ex: LVC_, SA_, NX3_, etc.
        Arguments: name -- unit name string
        Output: prefix -- subbus prefix string
        """
        htr = self.spacecraft.cf_heaters[name]
        subbus = htr.subbus
        if 'PW5' in subbus.num or 'PW6' in subbus.num:
            prefix = ''
            if int(subbus.num[2:]) < 60000:
                prefix = 'N'
            else:
                prefix = 'S'
            prefix += subbus.des[subbus.des.find('Bus')+4:subbus.des.find('Out')-1]
            prefix += htr.tray + '_'
        else:
            prefix = 'LVC_'
        return prefix
    
    def _carve(self, name):
        """ Determine script in which to test unit
        
        Description: Populates relevant carve object with unit name
        Arguments: name -- unit name string
        """
        # Search for regex in heater name
        found = False
        for regex in self.carve_search.keys():
            if re.search(pattern=regex, string=name):
                script_name = self._get_carve_prefix(name) + self.carve_search[regex]
                found = True
                break
        
        # Carve
        if found:
            if script_name not in self.carve:
                self.carve[script_name] = []
            self.carve[script_name].append(name)
        else:
            self.gui.output_text('    Warning - No matching script found for ' + name)
    
    def add_units(self, app_c_data, app_f_data):
        """ Populate spacecraft object with cf heaters
        
        Description: Iterates through thermal STIRS appendices to obtain cf heater properties (cmds, tlm, etc.), then
        populates spacecraft object cf heater list.
        Arguments: app_c_data -- Heaters. Dictionary of heater name:(dictionary of cmd/tlm id:cmd/tlm object)
                   app_f_data -- Heater sfty relays. Dictionary of htr sfty rly name:(dictionary of cmd/tlm id:cmd/tlm object)
        """
        for htr_name in sorted(app_c_data.keys()):
            if 'Htr' in htr_name and 'Side' not in htr_name:
                htr = Components.Heater()
                htr.name = htr_name
                htr.cmds_pids = app_c_data[htr_name][0]
                htr.power_val = app_c_data[htr_name][1]
                # Standardize naming convention
                htr_name = IOUtils.adjust_htr_name(htr_name)
                if htr_name in self.dbase.carved_subbuses.keys():
                    htr.subbus = self.dbase.carved_subbuses[htr_name]
                    htr.tray = self.dbase.carved_prefixes[htr_name]
                else:
                    # See if not exact match, but simply 'contained in'
                    print_error = True
                    for htr_name_t in self.dbase.carved_subbuses.keys():
                        if re.search('^'+htr_name, htr_name_t):
                            htr.subbus = self.dbase.carved_subbuses[htr_name_t]
                            htr.tray = self.dbase.carved_prefixes[htr_name_t]
                            print_error = False
                            break
                    if print_error:
                        self.gui.output_text('    Warning - Subbus not associated for ' + htr.name + '. Assuming LVC.')
                        htr.subbus = self.dbase.subbuses['LVC']
                        htr.tray = ''
                for sfty_rly_name in app_f_data.keys():
                    if re.search('^'+htr.name,sfty_rly_name):
                        htr.sfty_rly.name = sfty_rly_name
                        htr.sfty_rly.cmds_pids = app_f_data[sfty_rly_name]
                        break
                self.spacecraft.cf_heaters[htr.name] = htr
                if 'batt' not in htr_name.lower():
                    self._carve(htr.name)
    
    def check_for_links(self):
        # Look for sequence commands. Assume a sequence if shared between two heaters, but also check for some keywords
        # in the description just to be safe.
        linked_sfty_rly = Components.HtrSftyRly()
        pids = linked_sfty_rly.links.keys()
        for htr_name in sorted(self.spacecraft.cf_heaters.keys()):
            sfty_rly = self.spacecraft.cf_heaters[htr_name].sfty_rly
            for pid in pids:
                if pid in sfty_rly.cmds_pids and pid in linked_sfty_rly.cmds_pids:
                    if sfty_rly.cmds_pids[pid].num == linked_sfty_rly.cmds_pids[pid].num:
                        linked_sfty_rly.links[pid] = True
                        if not re.search('seq|rlys|relays', sfty_rly.cmds_pids[pid].des.lower()):
                            self.gui.output_text('    Found linked Sfty Rly commands, but mismatching des: %s - %s ' %
                                                 (sfty_rly.cmds_pids[pid].num, sfty_rly.cmds_pids[pid].des))
            linked_sfty_rly = sfty_rly
            
    
#******************************************************************************************************************************
# Output
#******************************************************************************************************************************

class CfHeaterScript(ScriptUtils.BaseScript):
    """ Write cf heater data
    
    Description: Write information compiled from CfHeaterReader to script
    Usage: Invoked by Writer object in IOUtils.py
    Public Variables: None
    Public Methods: None (write inherited from BaseScript)
    """
    extension = '.icl2'
    ddir = 'scripts\\cf\\CfHtr\\'
    description = 'Heater Command Functional'
    outline = textwrap.dedent('''\
    ############################### OUTLINE ###############################################
    #
    #\tI. ISTC Setup
    #\t\t- STAMP
    #\t\t- Request required packages
    #\t\t- Set Config
    #\t\t- Prompt which heaters will be tested
    #
    #\tII. S/C Setup
    #\t\t- Turn off 2 of the 4 Low Voltage Converters for cleaner power measuremnets (if testing Low Voltage Heaters)
    #\t\t- Use snap procedure to record current state of Heater ON/OFF, ENA/DIS states to restore later
    #\t\t- Verify any Heaters with Auto Control are Disabled
    #\t\t- Verify that all relevant Htr Sfty Rlys are ON
    #
    #\tIII. Body of Test
    #\t\t- Verify Htr Ena/Dis Cmd/Tlm (if auto-controlled)
    #\t\t- Make sure Heaters are OFF before testing Sfty Rlys
    #\t\t- Verify Htr Sfty Rly ON/OFF Cmd/Tlm (if applicable)
    #\t\t- Load Sub-Bus in Prep for Htr Power Measurements in following section
    #\t\t- Perform Power Measurements (autonomously loading Sub-Bus first, if necessary)
    #
    #\tIV. Clean Up
    #\t\t- Turn LVCs back ON, if necessary
    #\t\t- Turn Off any Heaters that were turned on by Sub-Bus loading procedures
    #\t\t- Restore previously snapped Htr ENA/DIS and ON/OFF states
    #
    #\tV. Tlm_Ch
    #
    #######################################################################################
    ''')
    istc_setup = textwrap.dedent('''\
    \tpackage require STO
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
        self.script_dir = spacecraft.script_dir + 'cf\\CfHtr\\'
    
    # Function to write Spacecraft Setup
    def _write_sc_setup(self):
        """ Write one time setup section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once before looping
        through each unit in the script is written here. Overrides BaseScript _write_istc_setup function.
        """
        # Additional initializations
        if 'LVC' in self.name:
            self.voltage = '30'
            self.prefix = 'LVC'
        else:
            self.voltage = '100'
            self.prefix = self.name[:2]
        
        # Htr prompt
        text = ''
        text += 'REPORT -------- Prompt the Operator about which heaters will be tested --------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tif {![info exists ::%sV_CfHtr_Prompts]} {\n' % self.voltage        
        text += '\t\tset action [DIALOG select -justify left -title "Verify OK to Proceed" \\\n'
        text += '\t\t-values {Continue Abort {Acknowledge All}} -text \\\n'
        text += '\t\t"This script will test the following heaters:\\n\\n\\\n'
        for u_name in self.u_names:
            text += '\t\t' + u_name + '\\n\\\n'
        text += '\t\t\\nThe Auto Heater Table will also be disabled.\\n\\\n'
        text += '\t\t\\nAcknowledge by entering Continue, Abort, or Acknowledge All.\\n\\n\\\n'
        text += '\t\tSelecting \\"Acknowledge All\\" will suppress future warning prompts\\n\\\n'
        text += '\t\tfor all other %sV CfHtr scripts run from this ICL2 Script GUI instance.\\n\\\n' % self.voltage
        text += '\t\tDo so ONLY if you are certain that it is safe to do so."]\n'
        text += '\t\tif {"$action" == "Abort"} {exit}\n'
        text += '\t\tif { [ string match -nocase *all* $action ] } {\n'
        text += '\t\t\tset ::%sV_CfHtr_Prompts false\n' % self.voltage
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
        text += '\t\tunset -nocomplain ::%sV_CfHtr_Prompts\n' % self.voltage
        text += 'REPORT\n'
        text += '\t}\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Turn Off any Heaters that were turned on by Sub-Bus loading procedures\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Turn off heaters
        for u_name in self.u_names:
            twta_off = self.spacecraft.cf_heaters[u_name].cmds_pids['on_tlm']
            text += '\tglobal return%s\n' % (twta_off.num)
            text += '\tif { [info exists return%s] } {\n'  % (twta_off.num)
            text += '\t\tforeach cmd [lrange $return%s 1 end] {\n'  % (twta_off.num)
            text += '\t\t\tCMD [string range $cmd 0 end-1]5\n'
            text += '\t\t}\n'
            text += '\t}\n'
        
        # Finish setup
        if 'LV' in self.name:
            text += 'REPORT\n'
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Return LVC to nominal state\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            text += '\tLVC_On\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Restore previously snapped Htr ENA/DIS and ON/OFF states\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tcatch {restore}\t\t\t;# Restore Previously snapped Tlm States\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Kill Heater/Thermistor Triggers created during script run\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tKILL_temp_triggers\n'
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
        if 'LV' in self.name:
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Dwell and Turn OFF 2 of the 4 LVCs for cleaner power measurements\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            text += '\tLVC_Off\n'
        else:
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Dwell on PCU Sub-Bus\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            htr0 = self.spacecraft.cf_heaters[self.u_names[0]]
            if self.spacecraft.omega == '2':
                text += '\tRELEASE DWELLWORD 4\n'
                text += '\tINSTALL DWELLWORD %s\n' % (htr0.subbus.num)
            else:
                text += '\tREQUIRE DWELLWORD %s\n' % (htr0.subbus.num)
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Use snap procedure to record current state of Heater ON/OFF, ENA/DIS states to restore later\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Record current heater states
        for u_name in self.u_names:
            on_cmd = self.spacecraft.cf_heaters[u_name].cmds_pids['on_cmd']
            off_cmd = self.spacecraft.cf_heaters[u_name].cmds_pids['off_cmd']
            on_tlm = self.spacecraft.cf_heaters[u_name].cmds_pids['on_tlm']
            text += '\tsnap %s %s\t\t\t;# %s\n' % (on_cmd.num, off_cmd.num, on_tlm.des)
        text += 'REPORT\n'
        ena_present = False
        for u_name in self.u_names:
            htr = self.spacecraft.cf_heaters[u_name]
            if 'ena_cmd' in htr.cmds_pids:
                ena_present = True
                ena_cmd = htr.cmds_pids['ena_cmd']
                dis_cmd = htr.cmds_pids['dis_cmd']
                ena_tlm = htr.cmds_pids['ena_tlm']
                text += '\tsnap %s %s\t\t\t;# %s\n' % (ena_cmd.num, dis_cmd.num, ena_tlm.des)
        if ena_present:
            text += 'REPORT\n'
        
        # Record current heater safety relay states
        sfty_rlys_present = False
        sfty_rly_ons_present = False
        sfty_rly_offs_present = False
        sfty_rly_tlm_present = False
        for u_name in self.u_names:
            htr = self.spacecraft.cf_heaters[u_name]
            if 'ena_cmd' in htr.sfty_rly.cmds_pids.keys():
                sfty_rlys_present = True
                ena_cmd = htr.sfty_rly.cmds_pids['ena_cmd']
                dis_cmd = htr.sfty_rly.cmds_pids['dis_cmd']
                ena_tlm = htr.sfty_rly.cmds_pids['ena_tlm']
                if not htr.sfty_rly.links['ena_cmd']:
                    text += '\tsnap %s %s\t\t\t;# %s\n' % (ena_cmd.num, dis_cmd.num, ena_tlm.des[:-3])
            if 'on_cmd' in htr.sfty_rly.cmds_pids.keys() or 'on_mac' in htr.sfty_rly.cmds_pids.keys():
                sfty_rly_ons_present = True
            if 'off_cmd' in htr.sfty_rly.cmds_pids.keys() or 'off_mac' in htr.sfty_rly.cmds_pids.keys():
                sfty_rly_offs_present = True
            if 'on_tlm' in htr.sfty_rly.cmds_pids.keys():
                sfty_rly_tlm_present = True
        if sfty_rlys_present:
            text += 'REPORT\n'
        
        # Auto control
        if ena_present:
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Verify any heaters with Auto Control are Disabled\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            for u_name in self.u_names:
                htr = self.spacecraft.cf_heaters[u_name]
                if 'dis_cmd' in htr.cmds_pids:
                    dis_cmd = htr.cmds_pids['dis_cmd']
                    text += '\tCMD -m %s\t\t\t;# %s\n' % (dis_cmd.num, dis_cmd.des)
            text += 'REPORT\n'
        
        # Disable table
        text += 'REPORT\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT Disable Auto Heater Table\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        if self.spacecraft.omega == '3':
            if 'TH01006' in self.dbase.cmd.keys() and 'TH01001' in self.dbase.tlm.keys():
                text += '\tCMD -m TH01006\t\t\t;# All Htrs Tbl DIS\n'
                text += '\tTLM EQ TH01001 DIS\t\t\t;# All Htrs Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += 'REPORT\n'
            else:
                self.gui.output_text('    Warning - TH01001 not in cmd/tlm database')
        elif self.spacecraft.omega == '2': 
            if 'TH01006' in self.dbase.cmd.keys() and 'TH01001' in self.dbase.tlm.keys() and \
            'TH01011' in self.dbase.cmd.keys() and 'TH01011' in self.dbase.tlm.keys():
                text += '\tCMD -m TH01016\t\t\t;# All Htrs Fast Rate Tbl DIS\n'
                text += '\tTLM EQ TH01011 DIS\t\t\t;# All Htrs Fast Rate Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += '\tCMD -m TH01006\t\t\t;# All Htrs Slow Rate Tbl DIS\n'
                text += '\tTLM EQ TH01001 DIS\t\t\t;# All Htrs Slow Rate Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += 'REPORT\n'
            else:
                self.gui.output_text('    Warning - TH01001/11 not in cmd/tlm database')
        
        # Start body - turn on safety relays
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT III. Body of Test\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        if sfty_rly_tlm_present:
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Verify that all relevant Htr Sfty Rlys are ON\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            skip = False
            for ind in range(0,len(self.u_names)):
                htr = self.spacecraft.cf_heaters[self.u_names[ind]]
                if not skip:
                    if htr.sfty_rly.links['on_cmd']:
                        skip = True
                        htr2 = self.spacecraft.cf_heaters[self.u_names[ind+1]]
                        htr_off_cmd = htr.cmds_pids['off_cmd']
                        htr2_off_cmd = htr2.cmds_pids['off_cmd']
                        rly_on_cmd = htr.sfty_rly.cmds_pids['on_cmd']
                        text += '\tCMD -v {} %s\t\t\t;# %s\n' % (htr_off_cmd.num, htr_off_cmd.des)
                        text += '\tCMD -v {} %s\t\t\t;# %s\n' % (htr2_off_cmd.num, htr2_off_cmd.des)
                        text += '\tCMD -m %s\t\t\t;# %s\n' % (rly_on_cmd.num, rly_on_cmd.des)
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        rly_on_tlm = htr2.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr2.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr2.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        text += 'REPORT\n'
                    elif 'on_cmd' in htr.sfty_rly.cmds_pids.keys():
                        htr_off_cmd = htr.cmds_pids['off_cmd']
                        rly_on_cmd = htr.sfty_rly.cmds_pids['on_cmd']
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tCMD -v {} %s\t\t\t;# %s\n' % (htr_off_cmd.num, htr_off_cmd.des)
                        text += '\tCMD -m %s\t\t\t;# %s\n' % (rly_on_cmd.num, rly_on_cmd.des)
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        text += 'REPORT\n'
                    elif 'on_mac' in htr.sfty_rly.cmds_pids.keys():
                        htr_off_cmd = htr.cmds_pids['off_cmd']
                        rly_on_cmd = htr.sfty_rly.cmds_pids['on_mac']
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tCMD -v {} %s\t\t\t;# %s\n' % (htr_off_cmd.num, htr_off_cmd.des)
                        text += '\tCMD -m %s\t\t\t;# %s\n' % (rly_on_cmd.num, rly_on_cmd.des)
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        text += 'REPORT\n'
                    elif 'on_tlm' in htr.sfty_rly.cmds_pids.keys():
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        text += 'REPORT\n'
                else:
                    skip = False
        
        # Ena/dis cmd/tlm
        if ena_present:
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Verify Htr Ena/Dis Cmd/Tlm\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            for u_name in self.u_names:
                htr = self.spacecraft.cf_heaters[u_name]
                if 'ena_cmd' in htr.cmds_pids:
                    ena_cmd = htr.cmds_pids['ena_cmd']
                    ena_tlm = htr.cmds_pids['ena_tlm']
                    dis_cmd = htr.cmds_pids['dis_cmd']
                    text += '\tCMD %s\t\t\t;# %s\n' % (ena_cmd.num, ena_cmd.des)
                    text += '\tTLM EQ %s ENA\t\t\t;# %s\n' % (ena_tlm.num, ena_tlm.des)
                    text += '\tCMD %s\t\t\t;# %s\n' % (dis_cmd.num, dis_cmd.des)
                    text += '\tTLM EQ %s DIS\t\t\t;# %s\n' % (ena_tlm.num, ena_tlm.des)
                    text += 'REPORT\n'
        
        # Turn off heaters
        if sfty_rly_ons_present and sfty_rly_offs_present:
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Make sure Heaters are OFF before testing Sfty Rlys, to avoid hot-switching\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            for u_name in self.u_names:
                htr = self.spacecraft.cf_heaters[u_name]
                if htr.sfty_rly.name != '':
                    if 'off_cmd' in htr.cmds_pids.keys():
                        htr_off_cmd = htr.cmds_pids['off_cmd']
                        text += '\tCMD -m %s\t\t\t;# %s\n' % (htr_off_cmd.num, htr_off_cmd.des)
                    elif 'off_mac' in htr.cmds_pids.keys():
                        htr_off_cmd = htr.cmds_pids['off_mac']
                        text += '\tCMD -m %s\t\t\t;# %s\n' % (htr_off_cmd.num, htr_off_cmd.des)
        
        # Safety relay on/off cmd/tlm
        if sfty_rly_ons_present and sfty_rly_offs_present:
            text += 'REPORT\n'
            text += 'REPORT\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT Verify Htr Sfty Rly ON/OFF Cmd/Tlm\n'
            text += 'REPORT --------------------------------------------------------------------------------\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            skip = False
            for ind in range(0,len(self.u_names)):
                htr = self.spacecraft.cf_heaters[self.u_names[ind]]
                if not skip:
                    if htr.sfty_rly.links['on_cmd']:
                        skip = True
                        htr2 = self.spacecraft.cf_heaters[self.u_names[ind+1]]
                        off_cmd = htr.sfty_rly.cmds_pids['off_cmd']
                        text += '\tCMD %s\t\t\t;# %s\n' % (off_cmd.num, off_cmd.des)
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        rly_on_tlm = htr2.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr2.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr2.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        on_cmd = htr.sfty_rly.cmds_pids['on_cmd']
                        text += '\tCMD %s\t\t\t;# %s\n' % (on_cmd.num, on_cmd.des)
                        rly_on_tlm = htr.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        rly_on_tlm = htr2.sfty_rly.cmds_pids['on_tlm']
                        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        if 'on2_tlm' in htr2.sfty_rly.cmds_pids.keys():
                            rly_on_tlm = htr2.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (rly_on_tlm.num, rly_on_tlm.des)
                        text += 'REPORT\n'
                    elif 'on_cmd' in htr.sfty_rly.cmds_pids.keys() or 'on_mac' in htr.sfty_rly.cmds_pids.keys():
                        if 'off_cmd' in htr.sfty_rly.cmds_pids.keys():
                            off_cmd = htr.sfty_rly.cmds_pids['off_cmd']
                            text += '\tCMD %s\t\t\t;# %s\n' % (off_cmd.num, off_cmd.des)
                        elif 'off_mac' in htr.sfty_rly.cmds_pids.keys():
                            off_cmd = htr.sfty_rly.cmds_pids['off_mac']
                            text += '\tCMD %s\t\t\t;# %s\n' % (off_cmd.num, off_cmd.des)
                        if 'on_tlm' in htr.sfty_rly.cmds_pids.keys():
                            on_tlm1 = htr.sfty_rly.cmds_pids['on_tlm']
                            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (on_tlm1.num, on_tlm1.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            on_tlm2 = htr.sfty_rly.cmds_pids['on2_tlm']
                            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (on_tlm2.num, on_tlm2.des)
                        if 'on_cmd' in htr.sfty_rly.cmds_pids.keys():
                            on_cmd = htr.sfty_rly.cmds_pids['on_cmd']
                            text += '\tCMD %s\t\t\t;# %s\n' % (on_cmd.num, on_cmd.des)
                        elif 'on_mac' in htr.sfty_rly.cmds_pids.keys():
                            on_cmd = htr.sfty_rly.cmds_pids['on_mac']
                            text += '\tCMD %s\t\t\t;# %s\n' % (on_cmd.num, on_cmd.des)
                        if 'on_tlm' in htr.sfty_rly.cmds_pids.keys():
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (on_tlm1.num, on_tlm1.des)
                        if 'on2_tlm' in htr.sfty_rly.cmds_pids.keys():
                            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (on_tlm2.num, on_tlm2.des)
                        text += 'REPORT\n'
                else:
                    skip = False
        
        # Load subbus and setup rest of body
        text += 'REPORT\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT Perform Power Measurements\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Write
        self.f.write(text)
    
    def _write_unit_body(self, u_name):
        """ Write body for specified unit
        
        Description: Called for each unit by _write_body function inherited from BaseScript. Overrides BaseScript 
        _write_unit_body function.
        Arguments: u_name -- Unit name string
        """
        # Load subbus
        unit = self.spacecraft.cf_heaters[u_name]
        text = ''
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT ------------------------ %s ------------------------\n' % unit.name
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT -------- Load the Sub-Bus --------\n'
        demote_list = []
        for u_name in self.u_names:
            htr = self.spacecraft.cf_heaters[u_name]
            on_tlm = htr.cmds_pids['on_tlm']
            demote_list.append(on_tlm.num)
        text += '\tvariable return%s [ SUBBUS Heater_LOAD ' % (unit.cmds_pids['on_tlm'].num)
        text += '%s { ' % (unit.cmds_pids['on_tlm'].num) + ' '.join(demote_list) + ' } ]\n'
        text += '\tif {![lindex $return%s 0]} {\n'  % (unit.cmds_pids['on_tlm'].num)
        text += '\t\tDIALOG acknowledge -priority warning -text \\\n'
        text += '\t\t"The Sub-Bus (%s, %s) may not be loaded to a full 2 Amps.\\n\\n\\\n' % (self.prefix, unit.subbus.num)
        text += '\t\tYou may either load the Sub-Bus manually or continue as is.\\n\\\n'
        text += '\t\t\\nContinue when ready."\n'
        text += '\t} elseif {[lindex $return%s 0] == -1 } {\n'  % (unit.cmds_pids['on_tlm'].num)
        text += '\t\tcleanup\n'
        text += '\t\texit 1\n'
        text += '\t}\n'
        text += 'REPORT\n'
        
        # Perform measurement and verify status
        on_cmd = unit.cmds_pids['on_cmd']
        off_cmd = unit.cmds_pids['off_cmd']
        on_tlm = unit.cmds_pids['on_tlm']
        text += 'REPORT ---- Take Power Measurement for %s ----\n' % (unit.name)
        text += 'REPORT\n'
        text += '\tCMD -m %s\t\t\t;# %s\n' % (on_cmd.num, on_cmd.des)
        text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (on_tlm.num, on_tlm.des)
        if 'cur_mon_tlm' in unit.cmds_pids.keys():
            cur_mon_tlm = unit.cmds_pids['cur_mon_tlm']
            text += '\tDELAY 30\n'
            text += '\tTLM %s\t\t\t;# %s\n' % (cur_mon_tlm.num, cur_mon_tlm.des)
        text += 'REPORT\n'
        text += '\tDevicePower %s\n' % (unit.name.replace(' ','_'))
        text += 'REPORT\n'
        text += '\tCMD -m %s\t\t\t;# %s\n' % (off_cmd.num, off_cmd.des)
        text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (on_tlm.num, on_tlm.des)
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Write
        self.f.write(text)
    
    def _write_footer(self):
        """ Write one time footer section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once after looping
        through each unit in the script is written here. Overrides BaseScript _write_footer function.
        """
        text = ''
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
        text += '\tPUBLISH CfHtr\n'
        text += 'REPORT\n'
        text += '############################### End of Script #########################################\n'
        
        # Write and close
        self.f.write(text)
        self.f.close()
