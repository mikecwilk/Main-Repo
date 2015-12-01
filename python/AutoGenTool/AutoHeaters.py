#******************************************************************************************************************************
# File: AutoHeaters.py
# Desc: Auto Heater Input/Output for automatic script generation
#******************************************************************************************************************************

import ScriptUtils
import re
import textwrap

#******************************************************************************************************************************
# Input
#******************************************************************************************************************************

class AutoHeaterReader:
    """ Read auto heater data
    
    Description: Read information from thermal STIRS and database to populate auto heaters
    Usage: Invoked by Reader object in IOUtils.py
    Public Variables: carve -- Dictionary of script names:list of unit names
    Public Methods: add_units -- Populate spacecraft object with auto heaters
    """
    
    # Dictionary of regex:script name for auto heaters
    carve_search = {'Prop|MST[^Tank]':'PROP',
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
                    '^RW|^RLG':'ADCS',
                    '^Star':'STAR_TRACKER',
                    '^N SSM':'N_SSM',
                    '^S SSM':'S_SSM',
                    'h SSM Htr':'SSM',
                    '^N.*Comm H':'N_HIPWR',
                    '^N.*Comm L':'N_LOPWR',
                    '^S.*Comm H':'S_HIPWR',
                    '^S.*Comm L':'S_LOPWR',
#                     '^N Upper Comm H':'N_UPPER_HIPWR',
#                     '^N Upper Comm L':'N_UPPER_LOPWR',
#                     '^S Upper Comm H':'S_UPPER_HIPWR',
#                     '^S Upper Comm L':'S_UPPER_LOPWR',
#                     '^N Lower Comm H':'N_LOWER_HIPWR',
#                     '^N Lower Comm L':'N_LOWER_LOPWR',
#                     '^S Lower Comm H':'S_LOWER_HIPWR',
#                     '^S Lower Comm L':'S_LOWER_LOPWR',
                    '^E Rx':'Rx_EAST',
                    '^W Rx':'Rx_WEST',
                    '[^SPT]EDAPM':'EDAPM',
                    '[^SPT][^EDAPM]DAPM':'DAPM',
                    '^PMA':'PMA',
                    '^DSS|^ES H|^ECASS':'SENSOR',
                    '^Feed':'FEED',
                    'PP':'ANT_PP',
                    'Mtr':'ANT_MTR',           
                    '^Press':'PRESS_TANK',
                    '^Prop Tank':'PROP_TANK',
                    '^Ox Tank':'OX_TANK',
                    '^Fuel Tank':'FUEL_TANK',
                    'LNA':'LNA',
                    'MLHP':'MLHP',
                    'Notch':'NF',}
    
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
    
    def _carve(self, name):
        """ Determine script in which to test unit
        
        Description: Populates relevant carve object with unit name
        Arguments: name -- unit name string
        """
        # Search for regex in heater name
        found = False
        for regex in self.carve_search.keys():
            if re.search(pattern=regex, string=name):
                script_name = self.carve_search[regex] + '_ah'
                found = True
                break
        
        # Carve
        if found:
            if script_name not in self.carve.keys():
                self.carve[script_name] = []
            self.carve[script_name].append(name)
        else:
            self.gui.output_text('    Warning - No matching script found for ' + name)
    
    def _add_lvc_info(self):
        """ Verify LVC/LVDC config
        
        Description: Checks LVC/LVDC config in database against expected config. Ensures LVC_Off and LVC_On in library 
        (DHS-1.0.tm) execute successfully, warning the user if a possible failure could occur. Does not modify any class 
        variables - debug window outputs only.
        """
        # Populate the three known, expected configurations: 2 PCUs; 1 PCU, 1 LVDC; 2 LVDCs
        known_config = True
        if 'PWM53300' in self.dbase.mac.keys() and 'PWM63300' in self.dbase.mac.keys():
            self.gui.output_text('    LVC Configuration: 2 PCUs')
            config_tlm = {'PW50610':'PCU1, LVC A Inp Curnt',
                          'PW50611':'PCU1, LVC B Inp Curnt',
                          'PW60610':'PCU2, LVC A Inp Curnt',
                          'PW60611':'PCU2, LVC B Inp Curnt',
                          'PW50201':'PCU1, LVC A ON/OFF Stat',
                          'PW50202':'PCU1, LVC B ON/OFF Stat',
                          'PW60201':'PCU2, LVC A ON/OFF Stat',
                          'PW60202':'PCU2, LVC B ON/OFF Stat'}
            config_mac = {'PWM53200':'PCU1 LVC A ON / LVC B ON',
                          'PWM63200':'PCU2 LVC A ON / LVC B ON',
                          'PWM53300':'PCU1 LVC A ON / LVC B OFF',
                          'PWM63300':'PCU2 LVC A ON / LVC B OFF',
                          'PWM53400':'PCU1 LVC A OFF / LVC B ON',
                          'PWM63400':'PCU2 LVC A OFF / LVC B ON'}
        elif 'PWM19000' in self.dbase.mac.keys() and 'PWM53300' in self.dbase.mac.keys():
            self.gui.output_text('    LVC Configuration: 1 PCU, 1 LVDC')
            config_tlm = {'PW50610':'PCU1, LVC A Inp Curnt',
                          'PW50611':'PCU1, LVC B Inp Curnt',
                          'PW19020':'LVDC 1 LVC A Curnt Input TLM',
                          'PW19120':'LVDC 1 LVC B Curnt Input TLM',
                          'PW50201':'PCU1, LVC A ON/OFF Stat',
                          'PW50202':'PCU1, LVC B ON/OFF Stat',
                          'PW19000':'LVDC 1 LVC A ON/OFF',
                          'PW19100':'LVDC 1 LVC B ON/OFF'}
            config_mac = {'PWM53200':'PCU1 LVC A ON / LVC B ON',
                          'PWM19010':'LVDC 1 LVC A ON/LVC B ON',
                          'PWM53300':'PCU1 LVC A ON / LVC B OFF',
                          'PWM19000':'LVDC 1 LVC A ON/LVC B OFF',
                          'PWM53400':'PCU1 LVC A OFF / LVC B ON',
                          'PWM19100':'LVDC 1 LVC B ON/LVC A OFF'}
        elif 'PWM19000' in self.dbase.mac.keys() and 'PWM19200' in self.dbase.mac.keys():
            self.gui.output_text('    LVC Configuration: 2 LVDCs')
            config_tlm = {'PW19020':'LVDC 1 LVC A Curnt Input TLM',
                          'PW19120':'LVDC 1 LVC B Curnt Input TLM',
                          'PW19220':'LVDC 2 LVC A Curnt Input TLM',
                          'PW19320':'LVDC 2 LVC B Curnt Input TLM',
                          'PW19000':'LVDC 1 LVC A ON/OFF',
                          'PW19100':'LVDC 1 LVC B ON/OFF',
                          'PW19200':'LVDC 2 LVC A ON/OFF',
                          'PW19300':'LVDC 2 LVC B ON/OFF'}
            config_mac = {'PWM19010':'LVDC 1 LVC A ON/LVC B ON',
                          'PWM19210':'LVDC 2 LVC A ON/LVC B ON',
                          'PWM19000':'LVDC 1 LVC A ON/LVC B OFF',
                          'PWM19100':'LVDC 1 LVC B ON/LVC A OFF',
                          'PWM19200':'LVDC 2 LVC A ON/LVC B OFF',
                          'PWM19300':'LVDC 2 LVC B ON/LVC A OFF'}
        else:
            self.gui.output_text('    LVC Configuration: Unknown')
            config_tlm = {}
            config_mac = {}
            known_config = False
        
        # Query database for 'LVC'
        lvc_cmd = self.dbase.get_cmd_pid(self.dbase.cmd, 'LVC')
        lvc_mac = self.dbase.get_cmd_pid(self.dbase.mac, 'LVC')
        lvc_tlm = self.dbase.get_cmd_pid(self.dbase.tlm, 'LVC')
        
        # Check to make sure config is known
        if known_config:
            for key in config_tlm.keys():
                if key not in self.dbase.tlm.keys():
                    self.gui.output_text('      Mismatched key: ' + key)
                    known_config = False
                    break
                elif config_tlm[key] != self.dbase.tlm[key].des:
                    self.gui.output_text('      Mismatched key: ' + key)
                    self.gui.output_text('        Proc -  ' + config_tlm[key])
                    self.gui.output_text('        DBase - ' + self.dbase.tlm[key].des)
                    known_config = False
                    break
            if known_config:
                for key in config_mac.keys():
                    if key not in self.dbase.mac.keys():
                        self.gui.output_text('      Mismatched key: ' + key)
                        known_config = False
                        break
                    elif config_mac[key] != self.dbase.mac[key].des:
                        self.gui.output_text('      Mismatched key: ' + key)
                        self.gui.output_text('        Proc -  ' + config_mac[key])
                        self.gui.output_text('        DBase - ' + self.dbase.mac[key].des)
                        known_config = False
                        break
        if not known_config:
            self.gui.output_text('      Warning - unknown LVC configuration. LVC_On/Off procedure might fail.')
            self.gui.output_text('        Expected:')
            for key in sorted(config_mac.keys()):
                self.gui.output_text('          %s - %s' % (key, config_mac[key]))
            for key in sorted(config_tlm.keys()):
                self.gui.output_text('          %s - %s' % (key, config_tlm[key]))
            self.gui.output_text('        In database:')
            for key in sorted(lvc_mac.keys()):
                self.gui.output_text('          %s - %s' % (lvc_mac[key].num, lvc_mac[key].des))
            for key in sorted(lvc_tlm.keys()):
                self.gui.output_text('          %s - %s' % (lvc_tlm[key].num, lvc_tlm[key].des))
        
        # Error check commands
        if len(lvc_cmd) > 0:
            for key in sorted(lvc_cmd.keys()):
                self.gui.output_text('      Extra cmd in dbase: %s - %s' % (lvc_cmd[key].num, lvc_cmd[key].des))
        # Error check macros
        for key in sorted(lvc_mac.keys()):
            if key not in config_mac.keys():
                self.gui.output_text('      Extra mac in dbase: %s - %s' % (lvc_mac[key].num, lvc_mac[key].des))
        # Error check telemetry
        for key in sorted(lvc_tlm.keys()):
            if key not in config_tlm.keys():
                self.gui.output_text('      Extra tlm in dbase: %s - %s' % (lvc_tlm[key].num, lvc_tlm[key].des))
    
    def add_units(self, app_a_data, app_c_data, app_f_data, app_g_data):
        """ Populate spacecraft object with auto heaters
        
        Description: Iterates through thermal STIRS appendices to obtain auto heater properties (cmds, tlm, etc.), then
        populates spacecraft object auto heater list.
        Arguments: app_a_data -- Thermisters. Dictionary of RT name:(dictionary of cmd/tlm id:cmd/tlm object)
                   app_c_data -- Heaters. Dictionary of heater name:(dictionary of cmd/tlm id:cmd/tlm object)
                   app_f_data -- Heater sfty relays. Dictionary of htr sfty rly name:(dictionary of cmd/tlm id:cmd/tlm object)
                   app_g_data -- Auto heaters. Dictionary of heater name:heater object
        """
        # Loop through heaters
        for htr_name in sorted(app_g_data.keys()):
            # Get heater and carve
            htr = app_g_data[htr_name];
            if 'batt' not in htr_name.lower():
                self._carve(htr_name)
            
            # Add heater commands, pids
            if 'Sfty Rly' in htr_name:
                # Calculations for grouped heater safety relays. Ex: AEP Prop Line Htr Sfty Rlys
                if ' and ' in htr_name or 'Rlys' in htr_name:
                    # Get regex search string. Ex: ^ES Htr, ^AEP Prop Line Htr
                    sstr = '^' + htr_name.split('Htr')[0] + 'Htr'
                    # Get relevant heater off/dis commands
                    htr.cmds_pids['dis_cmd'] = []
                    htr.cmds_pids['off_cmd'] = []
                    for key in sorted(app_c_data.keys()):
                        if re.search(sstr, key):
                            htr.cmds_pids['dis_cmd'].append(app_c_data[key][0]['dis_cmd'])
                            htr.cmds_pids['off_cmd'].append(app_c_data[key][0]['off_cmd'])
                    # Get all safety relay cmds/pids
                    ctemp = self.dbase.get_cmd_pid(self.dbase.cmd, sstr)
                    ctemp = self.dbase.get_cmd_pid(ctemp, 'Sfty')
                    ctemp = self.dbase.get_cmd_pid(ctemp, 'Seq', '!=')
                    ttemp = self.dbase.get_cmd_pid(self.dbase.tlm, sstr)
                    ttemp = self.dbase.get_cmd_pid(ttemp, 'Sfty')
                    on_cmds = self.dbase.get_cmd_pid(ctemp, 'ON').values()
                    off_cmds = self.dbase.get_cmd_pid(ctemp, 'OFF').values()
                    ena_cmds = self.dbase.get_cmd_pid(ctemp, 'ENA').values()
                    dis_cmds = self.dbase.get_cmd_pid(ctemp, 'DIS').values()
                    on_tlms = self.dbase.get_cmd_pid(ttemp, 'ON/OFF').values()
                    ena_tlms = self.dbase.get_cmd_pid(ttemp, 'ENA/DIS').values()
                    # Sort by command/pid description
                    htr.cmds_pids['on_cmds'] = sorted(on_cmds, key=lambda cmd: cmd.des)
                    htr.cmds_pids['off_cmds'] = sorted(off_cmds, key=lambda cmd: cmd.des)
                    htr.cmds_pids['ena_cmds'] = sorted(ena_cmds, key=lambda cmd: cmd.des)
                    htr.cmds_pids['dis_cmds'] = sorted(dis_cmds, key=lambda cmd: cmd.des)
                    htr.cmds_pids['on_tlms'] = sorted(on_tlms, key=lambda cmd: cmd.des)
                    htr.cmds_pids['ena_tlms'] = sorted(ena_tlms, key=lambda cmd: cmd.des)
                elif htr_name in app_f_data.keys():
                    htr.cmds_pids = app_f_data[htr_name]
                else:
                    self.gui.output_text('    Warning - Mismatched heater name : ' + htr_name)
            else:
                if htr_name in app_c_data.keys():
                    htr.cmds_pids = app_c_data[htr_name][0]
                else:
                    self.gui.output_text('    Warning - Mismatched heater name : ' + htr_name)
            
            # Add thermistor pid
            for thrm in htr.thermisters:
                if thrm.rt in app_a_data.keys():
                    thrm.tlm      = app_a_data[thrm.rt]
                    thrm.name     = thrm.tlm.des
                else:
                    self.gui.output_text('    Warning - Mismatched thermister RT : ' + thrm.rt)
            
            # Add to spacecraft
            self.spacecraft.heaters[htr_name] = htr
        
        # Add LVC/LVDC info
        self._add_lvc_info()

#******************************************************************************************************************************
# Output
#******************************************************************************************************************************

class AutoHeaterScript(ScriptUtils.BaseScript):
    """ Write auto heater data
    
    Description: Write information compiled from AutoHeaterReader to script
    Usage: Invoked by Writer object in IOUtils.py
    Public Variables: None
    Public Methods: None (write inherited from BaseScript)
    """
    
    extension = '.icl'
    description = 'DHS_Cmd Auto Heater Script'
    outline = textwrap.dedent('''\
    ############################## REQUIREMENT OVERVIEW ####################################
    #
    #\tThis script is linked to the following requirement(s) in:
    #
    #\tTRD Exxxx01
    #\tPara 3.5.4.8.1 (Thermal Managment Commandability)
    #\t\tTR791 - Heater ON/OFF controls operate per commanded SET points and default thermistors.
    #\t\tTR792 - Heater ENA/DISABLE status is properly displayed in telemetry.
    #\t\tTR793 - Master ENABLE/DISABLE commands provide control over all autonomous heater operations.
    #
    #
    ############################### OVERVIEW ##############################################
    #
    #\tS/C Feature Description / Addtional Background Info
    #\t\tThe DHS contains a set of firmware that is responsible for providing autonomous
    #\t\tcontrol of DHS-controllable heaters on the spacecraft. Temperature measurements
    #\t\tare collected by the DHS firmware then copied and stored in local memory. The
    #\t\tfirmware uses these temperature measurements to make decisions on whether to
    #\t\tturn heaters on or off.
    #
    #\tTest Philosophy
    #\t\tWrite to memory locations that Flight Software uses to autonomously turn on/off heaters,
    #\t\tafter diverting the real Thrmistor data away from these memory locations.
    #
    ############################### OUTLINE ###############################################
    #
    #\tI. ISTC Setup
    #\t\ta. ITACs - STAAR+_BUS, Stamp, TLMCH, RT_SUB
    #\t\tb. EAGE - MNC: Power, Cmd/Tlm
    #\t\tc. Warnings
    #\t\t\t1. Prompt to verify correct PROM revision
    #
    #\tII. S/C Setup
    #\t\ta. Snapshot of current: Heater Config, Heater auto control config, Master Auto config
    #\t\tb. Verify Nominal S/C Config (per req type only ie. SW, HW, etc)
    #\t\tc. Configure & Verify Test S/C Config (starting config of test)
    #\t\t\t1. Turn off heaters being tested.
    #\t\t\t2. Disable heater auto control for ALL htrs
    #\t\t\t3. Enable Master auto control (rate table)
    #
    #\tIII. Body of Test
    #
    #\tFollow this outline for each heater:
    #\t\ta. Redirect tlm acq to another location (STE ENA keyword)
    #\t\tb. Report default thermal STIRs setpoints
    #\t\tc. Write new temps into thermal mem location (MEM WRITE keyword)
    #\t\t\t1. Write a temp below low limit to turn on heater
    #\t\t\t2. Enable heater auto control
    #\t\t\t3. Verify heater turned ON
    #\t\t\t4. Write a temp above high limit to turn off heater
    #\t\t\t5. Verify heater turned OFF
    #\t\td. Disable heater auto control
    #\t\te. Turn off heater
    #\t\tf. Redirect tlm data acq back to default location (STE DIS keyword)
    #
    #\tIV. Clean Up
    #\t\tDisable Auto Heater Table
    #\t\tVerify all used heaters are turned off
    #
    #\tV. Tlm Check
    #
    #######################################################################################
    ''')
    istc_setup = textwrap.dedent('''\
    REPORT
    REPORT --------------------------------------------------------------------------------
    REPORT --------------------------------------------------------------------------------
    REPORT I. ISTC Setup
    REPORT --------------------------------------------------------------------------------
    REPORT --------------------------------------------------------------------------------
    REPORT
    REPORT
    REPORT ---------- 1a. ITACs ----------
    REPORT
    \tSTAMP STAAR_PLUS_YES
    REPORT
    \tset tlmch_start [ clock seconds ]
    REPORT
    \tset vehicle [VEHICLE]
    REPORT
    \tif {[file exists /taps/veh/$vehicle/memory/$vehicle.BlkOff.xml] !=1} {
    \t\tFEEDBACK Abort Abort IndianRed "
    \t\tThis test requires a file called $vehicle.BlkOff.xml to exist in the following directory:
    \t\t/taps/veh/$vehicle/memory/
    \t\t-
    \t\tThis file is either named wrong, or doesn't exist.
    \t\tThis test will now Abort.
    \t\t-
    \t\tAcknowledge by entering Abort, Abort, or Abort!
    \t\t"
    \t\tGOTO Abort
    \t}
    REPORT
    REPORT
    REPORT ---------- 1b. EAGE ----------
    REPORT
    REPORT
    REPORT
    REPORT ---------- 1c. Warnings ----------
    REPORT
    REPORT
    REPORT
    \tFEEDBACK Continue Abort LightGreen "
    \t********** NOTE **********
    \tAll Auto-heaters will be disabled at the start of this test.
    \tAcknowledge by entering Abort or Continue.
    \t"
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
        if self.spacecraft.omega == '2':
            self.script_dir = spacecraft.script_dir + 'cf\\CfDhsAH\\'
        else:
            self.script_dir = spacecraft.script_dir + 'performance\\DHS\\DHS_Cmd_AH\\'
    
    def _write_sc_setup(self):
        """ Write one time setup section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once before looping
        through each unit in the script is written here. Overrides BaseScript _write_istc_setup function.
        """
        text = ''
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT II. S/C Setup\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        if 'DH63505' in self.dbase.cmd.keys():
            text += 'REPORT -------- Disable ChkSm Region 30 (for Tlm_Ch) --------\n'
            text += '\tCMD DH63505 After\t\t\t;# ChkSm Region 30 DIS\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
        if self.spacecraft.omega == '3':
            text += 'REPORT ---------- Disable all Auto-Heaters ----------\n'
            text += '\tINCLUDE satcf/HtrDisFast.icl\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
        else:
            if 'TC35310' in self.dbase.cmd.keys():
                text += 'REPORT -------- Set Data Acq to RAM --------\n'
                text += '\tCMD TC35310 After\t\t\t;# Sel Data Acq RAM Tbls\n'
                text += 'REPORT\n'
                text += 'REPORT\n'
            else:
                self.gui.output_text('    Warning - TC35310 not in cmd/tlm database')
            text += 'REPORT ---------- Disable all Auto-Heaters ----------\n'
            text += '\tINCLUDE satcf/HTR_DIS.icl\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
        if self.spacecraft.omega == '3':
            if 'TH01001' in self.dbase.cmd.keys() and 'TH01001' in self.dbase.tlm.keys():
                text += 'REPORT  -------- Enable Master Heater Rate Table --------\n'
                text += '\tCMD TH01001 After\t\t\t;# All Htrs Tbl ENA\n'
                text += '\tTLM EQ TH01001 ENA\t\t\t;# All Htrs Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += 'REPORT\n'
            else:
                self.gui.output_text('    Warning - TH01001 not in cmd/tlm database')
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT III. Body of Test\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        self.f.write(text)
    
    def _write_unit_body(self, u_name):
        """ Write body for specified unit
        
        Description: Called for each unit by _write_body function inherited from BaseScript. Overrides BaseScript 
        _write_unit_body function.
        Arguments: u_name -- Unit name string
        """
        # Start test overview
        unit = self.spacecraft.heaters[u_name]
        thrms = unit.thermisters
        n_thrms = len(unit.thermisters)
        text = ''
        text += 'REPORT ================================================================================\n'
        text += 'REPORT ================================================================================\n'
        text += 'REPORT\n'
        text += 'REPORT ------------------------------------------------------------------\n'
        text += 'REPORT START TEST:  %s\n' % unit.name
        text += 'REPORT ------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT -------------------------------------------------------\n'
        text += 'REPORT This Heater is controlled by %s Thermistors:\n' % n_thrms
        # List thermisters
        for t_num, thrm in enumerate(thrms):
            text += 'REPORT %s (%s) is Thermistor %s\n' % (thrm.name, thrm.tlm.num, t_num+1)
            
        # Determine test approach:
        # To turn on, use the first x number of thermisters required to turn on.
        # To turn off, use the next x number of thermisters required to turn off in an attempt to get full coverage
        # Ex: Vote Margins = 1 on, 2 off;
        #    With 2 thermisters - Use T1 to turn on, T1 and T2 to turn off
        #    With 3 thermisters - Use T1 to turn on, T2 and T3 to turn off
        # Ex: Vote Margins = 2 on, 2 off;
        #    With 2 thermisters - Use T1 and T2 to turn on, T1 and T2 to turn off
        #    With 3 thermisters - Use T1 and T2 to turn on, T2 and T3 to turn off
        # The on_trms and off_trms calculations cover this logic if the sum of the voting margins is >= the number of therms.
        # If not, this logic will not work!
        # Ex: Vote Margins = 1 on, 2 off;
        #    With 4 thermisters - Use T1 to turn on, T2 and T3 to turn off => We didn't verify T4!!
        # In such a case, the logic would need to be changed to loop back around. This has not been observed in recent programs
        # and therefor has not been programmed (it'd be a bit more difficult - this simpler way is pretty easy). May the gods
        # be with you if you have to program that functionality - sucka! It's not actually bad.
        v_margs  = unit.vote_marg
        sum_marg = int(v_margs[0]) + int(v_margs[1])
        on_trms  = range(1,int(v_margs[0])+1)
        off_trms = range(n_thrms-int(v_margs[1])+1,n_thrms+1)
        text += 'REPORT Voting Margins are:  %s ON, %s OFF\n' % (v_margs[0], v_margs[1])
        text += 'REPORT\n'
        text += 'REPORT Test approach for this Heater:\n'
        text += 'REPORT Heater ON tripped by Thermistor(s) %s\n' % ', '.join(map(str,on_trms))
        text += 'REPORT Heater OFF tripped by Thermistor(s) %s\n' % ', '.join(map(str,off_trms))
        text += 'REPORT -------------------------------------------------------\n'
        text += 'REPORT\n'
        if sum_marg < n_thrms:
            self.gui.output_text('    Warning - Voting margin testing insufficient')
        
        # Disable and off
        if 'on_cmds' in unit.cmds_pids.keys():
            text += 'REPORT ----- Verify that the Relevant Heaters are Disabled and OFF\n'
            for cmd in unit.cmds_pids['dis_cmd']:
                text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
            for cmd in unit.cmds_pids['off_cmd']:
                text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
            text += 'REPORT\n'
            text += 'REPORT ----- Verify that the Htr Sfty Rlys about to be tested are Disabled and OFF\n'
            for cmd in unit.cmds_pids['dis_cmds']:
                text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
            for cmd in unit.cmds_pids['off_cmds']:
                text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
            text +='REPORT\n'
            for cmd in unit.cmds_pids['ena_tlms']:
                text += '\tTLM EQ %s DIS\t\t\t;# %s\n' % (cmd.num, cmd.des)
            for cmd in unit.cmds_pids['on_tlms']:
                text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (cmd.num, cmd.des)
        else:
            text += 'REPORT ----- Verify that the Heater about to be tested is Disabled and OFF\n'
            text += '\tCMD %s Both\t\t\t;# %s\n' % (unit.cmds_pids['dis_cmd'].num, unit.cmds_pids['dis_cmd'].des)
            text += '\tCMD %s Both\t\t\t;# %s\n' % (unit.cmds_pids['off_cmd'].num, unit.cmds_pids['off_cmd'].des)
            text += 'REPORT\n'
            text += '\tTLM EQ %s DIS\t\t\t;# %s\n' % (unit.cmds_pids['ena_tlm'].num, unit.cmds_pids['ena_tlm'].des)
            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        
        # Tables
        if self.spacecraft.omega == '2':
            text += 'REPORT\n'
            text += 'REPORT ----- %s is in %s table\n' % (unit.name, unit.rate)
            if unit.rate == 'FAST':
                text += 'REPORT ----- Ensure that FAST master is enabled and SLOW master is disabled\n'
                text += '\tCMD TH01011 Before\t\t\t;# All Htrs Fast Rate Tbl ENA\n'
                text += '\tTLM EQ TH01011 ENA\t\t\t;# All Htrs Fast Rate Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += '\tCMD TH01006 Before\t\t\t;# All Htrs Slow Rate Tbl DIS\n'
                text += '\tTLM EQ TH01001 DIS\t\t\t;# All Htrs Slow Rate Tbl ENA/DIS St\n'
            else:
                text += 'REPORT ----- Ensure that SLOW master is enabled and FAST master is disabled\n'
                text += '\tCMD TH01001 Before\t\t\t;# All Htrs Slow Rate Tbl ENA\n'
                text += '\tTLM EQ TH01001 ENA\t\t\t;# All Htrs Slow Rate Tbl ENA/DIS St\n'
                text += 'REPORT\n'
                text += '\tCMD TH01016 Before\t\t\t;# All Htrs Fast Rate Tbl DIS\n'
                text += '\tTLM EQ TH01011 DIS\t\t\t;# All Htrs Fast Rate Tbl ENA/DIS St\n'
        
        # Enable STE
        text += 'REPORT\n'
        text += 'REPORT ----- ENA STE for each %s Thermistor\n' % unit.name
        for thrm in thrms:
            text += '\tSTE ENA %s\n' % thrm.tlm.num
        text += 'REPORT\n'
        text += 'REPORT +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
        
        # Print thermistor info
        for t_num, thrm in enumerate(thrms):
            if t_num != 0:
                text += 'REPORT\n'
            text += 'REPORT Thermistor %s: PID = %s\n' % (t_num+1, thrm.tlm.num)
            text += 'REPORT Thermistor Name: %s\n' % thrm.name
            text += 'REPORT Def Set Points (deg): LOW = %.1f, HIGH = %.1f\n' % (float(thrm.low_sp_dec),
                                                                                float(thrm.high_sp_dec))
            text += 'REPORT Raw Set Points (hex): LOW = %s, HIGH = %s\n' % (thrm.low_sp_hex, thrm.high_sp_hex)
        text += 'REPORT\n'
        text += 'REPORT +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
           
        # Turn on heater
        t_num = 1
        for i in on_trms:
            thrm = thrms[i-1]
            val = '0x%X' % (int(thrm.low_sp_hex,16)-thrm.sp_dir)
            text += 'REPORT ----- Temp %s (%s) < default low limit to turn on heater\n' % (t_num, thrm.tlm.num)
            text += '\tMEM WRITE %s %s\n' % (thrm.tlm.num, val)
            text += 'REPORT\n'
            t_num+=1
        
        # Put the rest to mid
        for i in range(t_num, n_thrms+1):
            thrm = thrms[i-1]
            lv = int(thrm.low_sp_hex,16)
            hv = int(thrm.high_sp_hex,16)
            val = '0x%X' % int((lv+hv)/2)
            text += 'REPORT ----- Temp %s (%s) in mid-range\n' % (t_num, thrm.tlm.num)
            text += '\tMEM WRITE %s %s\n' % (thrm.tlm.num, val)
            text += 'REPORT\n'
            t_num+=1
            
        # Enable & verify
        if self.spacecraft.omega == '3' or unit.rate == 'FAST':
            wait_dur = 100
        else:
            wait_dur = 220
        text += 'REPORT ----- Enable Heater Auto-Control\n'
        if 'on_cmds' in unit.cmds_pids.keys():
            for cmd in unit.cmds_pids['ena_cmds']:
                text += '\tCMD %s After\t\t\t;# %s\n' % (cmd.num, cmd.des)
            for cmd in unit.cmds_pids['ena_tlms']:
                text += '\tTLM EQ %s ENA\t\t\t;# %s\n' % (cmd.num, cmd.des)
        else:
            text += '\tCMD %s After\t\t\t;# %s\n' % (unit.cmds_pids['ena_cmd'].num, unit.cmds_pids['ena_cmd'].des)
            text += '\tTLM EQ %s ENA\t\t\t;# %s\n' % (unit.cmds_pids['ena_tlm'].num, unit.cmds_pids['ena_tlm'].des)
        text += 'REPORT\n'
        if 'on_cmds' in unit.cmds_pids.keys():
            text += '\tTLM WAIT %s ON,%s\t\t\t;# %s - Wait %s secs to change\n' % (unit.cmds_pids['on_tlms'][0].num, wait_dur,
                                                                                   unit.cmds_pids['on_tlms'][0].des, wait_dur)
        else:
            text += '\tTLM WAIT %s ON,%s\t\t\t;# %s - Wait %s secs to change\n' % (unit.cmds_pids['on_tlm'].num, wait_dur,
                                                                                   unit.cmds_pids['on_tlm'].des, wait_dur)
        text += 'REPORT\n'
        text += 'REPORT ----- Verify %s is now ON\n' % unit.name
        if 'on_cmds' in unit.cmds_pids.keys():
            for cmd in unit.cmds_pids['on_tlms']:
                text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (cmd.num, cmd.des)
        else:
            text += '\tTLM EQ %s ON\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        text += 'REPORT\n'
        
        # Put the rest to mid
        t_num = 1
        for i in range(t_num, off_trms[0]):
            thrm = thrms[i-1]
            lv = int(thrm.low_sp_hex,16)
            hv = int(thrm.high_sp_hex,16)
            val = '0x%X' % int((lv+hv)/2)
            text += 'REPORT ----- Temp %s (%s) in mid-range\n' % (t_num, thrm.tlm.num)
            text += '\tMEM WRITE %s %s\n' % (thrm.tlm.num, val)
            text += 'REPORT\n'
            t_num+=1
        
        # Turn off heater
        for i in range(off_trms[0], off_trms[1]+1):
            thrm = thrms[i-1]
            val = '0x%X' % (int(thrm.high_sp_hex,16)+thrm.sp_dir)
            text += 'REPORT ----- Temp %s (%s) > default high limit to turn off heater\n' % (t_num, thrm.tlm.num)
            text += '\tMEM WRITE %s %s\n' % (thrm.tlm.num, val)
            text += 'REPORT\n'
            t_num+=1
        
        # Verify and cleanup
        if 'on_cmds' in unit.cmds_pids.keys():
            text += '\tTLM WAIT %s OFF,%s\t\t\t;# %s - Wait %s secs to change\n' % (unit.cmds_pids['on_tlms'][0].num, wait_dur,
                                                                                    unit.cmds_pids['on_tlms'][0].des, wait_dur)
        else:
            text += '\tTLM WAIT %s OFF,%s\t\t\t;# %s - Wait %s secs to change\n' % (unit.cmds_pids['on_tlm'].num, wait_dur,
                                                                                   unit.cmds_pids['on_tlm'].des, wait_dur)
        text += 'REPORT\n'
        text += 'REPORT ----- Verify %s is now OFF\n' % unit.name
        if 'on_cmds' in unit.cmds_pids.keys():
            for cmd in unit.cmds_pids['on_tlms']:
                text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (cmd.num, cmd.des)
        else:
            text += '\tTLM EQ %s OFF\t\t\t;# %s\n' % (unit.cmds_pids['on_tlm'].num, unit.cmds_pids['on_tlm'].des)
        text += 'REPORT\n'
        text += 'REPORT ---------------- CLEANUP ----------------\n'
        text += 'REPORT\n'
        text += 'REPORT ----- Disable Heater Auto-Control\n'
        if 'on_cmds' in unit.cmds_pids.keys():
            for cmd in unit.cmds_pids['dis_cmds']:
                text += '\tCMD %s After\t\t\t;# %s\n' % (cmd.num, cmd.des)
            for cmd in unit.cmds_pids['ena_tlms']:
                text += '\tTLM EQ %s DIS\t\t\t;# %s\n' % (cmd.num, cmd.des)
        else:
            text += '\tCMD %s After\t\t\t;# %s\n' % (unit.cmds_pids['dis_cmd'].num, unit.cmds_pids['dis_cmd'].des)
            text += '\tTLM EQ %s DIS\t\t\t;# %s\n' % (unit.cmds_pids['ena_tlm'].num, unit.cmds_pids['ena_tlm'].des)
        text += 'REPORT\n'
        if 'Sfty Rly' in unit.name:
            text += 'REPORT ----- Ensure %s is ON\n' % unit.name
            if 'on_cmds' in unit.cmds_pids.keys():
                for cmd in unit.cmds_pids['on_cmds']:
                    text += '\tCMD %s After\t\t\t;# %s\n' % (cmd.num, cmd.des)
            else:
                text += '\tCMD %s After\t\t\t;# %s\n' % (unit.cmds_pids['on_cmd'].num, unit.cmds_pids['on_cmd'].des)
        else:
            text += 'REPORT ----- Ensure %s is OFF\n' % unit.name
            if 'on_cmds' in unit.cmds_pids.keys():
                for cmd in unit.cmds_pids['off_cmds']:
                    text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
            else:
                text += '\tCMD %s Both\t\t\t;# %s\n' % (unit.cmds_pids['off_cmd'].num, unit.cmds_pids['off_cmd'].des)
        text += 'REPORT\n'
        text += 'REPORT ----- DIS STE For each %s Thermistor\n' % unit.name
        
        # Disable STE
        for thrm in thrms:
            text += '\tSTE DIS %s\n' % thrm.tlm.num
        text += 'REPORT\n'
        text += 'REPORT\n'
        
        # Write
        self.f.write(text)
    
    def _write_footer(self):
        """ Write one time footer section of script
        
        Description: Called only once by _write function inherited from BaseScript. Anything that executes once after looping
        through each unit in the script is written here. Overrides BaseScript _write_footer function.
        """
        # Front matter
        text = ''
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT IV. Clean Up\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT -------- Turn Off Heaters --------\n'
        
        # Turn off heaters   
        for u_name in self.u_names:
            unit = self.spacecraft.heaters[u_name]
            if 'Sfty Rly' in unit.name:
                if 'on_cmds' in unit.cmds_pids.keys():
                    for cmd in unit.cmds_pids['on_cmds']:
                        text += '\tCMD %s After\t\t\t;# %s\n' % (cmd.num, cmd.des)
                else:
                    text += '\tCMD %s After\t\t\t;# %s\n' % (unit.cmds_pids['on_cmd'].num, unit.cmds_pids['on_cmd'].des)
            else:
                if 'on_cmds' in unit.cmds_pids.keys():
                    for cmd in unit.cmds_pids['off_cmds']:
                        text += '\tCMD %s Both\t\t\t;# %s\n' % (cmd.num, cmd.des)
                else:
                    text += '\tCMD %s Both\t\t\t;# %s\n' % (unit.cmds_pids['off_cmd'].num, unit.cmds_pids['off_cmd'].des)
        
        # Finish
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += 'REPORT -------- Disable Master Heater Rate Table --------\n'
        if self.spacecraft.omega == '3':
            if 'TH01006' in self.dbase.cmd.keys() and 'TH01001' in self.dbase.tlm.keys():
                text += '\tCMD TH01006 After\t\t\t;# All Htrs Tbl DIS\n'
                text += '\tTLM EQ TH01001 DIS\t\t\t;# All Htrs Tbl ENA/DIS St\n'
        else:
            text += '\tCMD TH01006 After\t\t\t;# All Htrs Slow Rate Tbl DIS\n'
            text += '\tCMD TH01016 After\t\t\t;# All Htrs Fast Rate Tbl DIS\n'
            text += '\tTLM EQ TH01001 DIS\t\t\t;# All Htrs Slow Rate Tbl ENA/DIS St\n'
            text += '\tTLM EQ TH01011 DIS\t\t\t;# All Htrs Fast Rate Tbl ENA/DIS St\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
            text += 'REPORT -------- Set Data Acq to PROM --------\n'
            text += '\tCMD TC35300 After\t\t\t;# Sel Data Acq PROM Tbls\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        if 'DH63500' in self.dbase.cmd.keys():
            text += 'REPORT -------- Enable ChkSm Region 30 --------\n'
            text += '\tCMD DH63500 After\t\t\t;# ChkSm Region 30 ENA\n'
            text += 'REPORT\n'
            text += 'REPORT\n'
        
        # Tlm check
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT V. Tlm Check\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT --------------------------------------------------------------------------------\n'
        text += 'REPORT\n'
        text += 'REPORT\n'
        text += '\tINCLUDE satcf/Tlm_Ch.icl\n'
        text += 'REPORT\n'
        text += '\tLABEL Abort\n'
        text += 'REPORT\n'
        text += '\tEND\n'
        text += '\tPRINT\n'
        text += 'REPORT\n'
        text += '############################### End of Script #########################################\n'
            
        # Write and close
        self.f.write(text)
        self.f.close()
