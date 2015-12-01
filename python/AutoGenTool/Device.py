#******************************************************************************************************************************
# File: Device.py
# Desc: Device file Input/Output for automatic script generation
#******************************************************************************************************************************

import IOUtils
import re

#******************************************************************************************************************************
# Input
#******************************************************************************************************************************

class DeviceReader:
    """ Read device file data
    
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
        
    def _sort_by_on(self, units):
        sorted_device_names = []
        sorter_dict = {} 
        for u_name in sorted(units.keys()):
            unit = units[u_name]
            on_cmd = unit['on_cmd']
            while on_cmd in sorter_dict.keys():
                on_cmd += '0'
            sorter_dict[on_cmd] = u_name
        for sorter in sorted(sorter_dict.keys()):
            sorted_device_names.append(sorter_dict[sorter])
        return sorted_device_names
    
    def _process_heaters(self, u_name, u_name_device):
        unit = self.spacecraft.cf_heaters[u_name]
        processed_unit = {}
        processed_unit['name'] = u_name_device
        processed_unit['on_cmd'] = IOUtils.underscore_it(unit.cmds_pids['on_cmd'].num)
        processed_unit['off_cmd'] = IOUtils.underscore_it(unit.cmds_pids['off_cmd'].num)
        if 'cur_mon_tlm' in unit.cmds_pids.keys():
            processed_unit['cur_mon_tlm'] = IOUtils.underscore_it(unit.cmds_pids['cur_mon_tlm'].num)
        processed_unit['subbus_pid'] = IOUtils.underscore_it(unit.subbus.num)
        processed_unit['power_val'] = float(unit.power_val)
        return processed_unit
    
    def _process_twtas(self, u_name, u_name_device):
        unit = self.spacecraft.twtas[u_name]
        processed_unit = {}
        shared_tl_off = True
        if 'off_cmd' in unit.lcamp.cmds_pids.keys():
            off_cmd =  unit.lcamp.cmds_pids['off_cmd']
            if 'off_cmd' in unit.cmds_pids.keys():
                if off_cmd.num != unit.cmds_pids['off_cmd'].num:
                    shared_tl_off = False
            else:
                shared_tl_off = False
        if shared_tl_off:
            processed_unit['name'] = unit.cmds_pids['on_cmd'].des[:-3].replace(' ', '_').replace(',', '')
        else:
            processed_unit['name'] = unit.name.replace(' ', '_')
        processed_unit['on_cmd'] = IOUtils.underscore_it(unit.cmds_pids['on_cmd'].num)
        processed_unit['off_cmd'] = IOUtils.underscore_it(unit.cmds_pids['off_cmd'].num)
        processed_unit['subbus_pid'] = IOUtils.underscore_it(unit.subbus.num)
        processed_unit['power_val'] = 0.0
        if 'bus_curnt_tlm' in unit.cmds_pids.keys():
            processed_unit['bus_curnt_tlm'] = IOUtils.underscore_it(unit.cmds_pids['bus_curnt_tlm'].num)
        return processed_unit
    
    def _process_lcamps(self, u_name, u_name_device):
        unit = self.spacecraft.twtas[u_name]
        processed_unit = {}
        if 'on_cmd' and 'off_cmd' in unit.lcamp.cmds_pids.keys():
            processed_unit['name'] = unit.lcamp.name.replace(' ', '_')
            processed_unit['on_cmd'] = IOUtils.underscore_it(unit.lcamp.cmds_pids['on_cmd'].num)
            processed_unit['off_cmd'] = IOUtils.underscore_it(unit.lcamp.cmds_pids['off_cmd'].num)
            processed_unit['subbus_pid'] = IOUtils.underscore_it(unit.subbus.num)
            processed_unit['power_val'] = 0.0
        return processed_unit
                
    def _process_misc(self, u_name, u_name_device, cmds, macros, tlm_misc):
        # Find on/off in database
        processed_unit = {}
        processed_unit['name'] = u_name_device.replace('Side_','')
        if re.search('_\d', u_name[-2:]):
            u_name_t = u_name[:-2]
        elif re.search('mro.*side', u_name.lower()):
            u_name_t = u_name + ' dc'
        else:
            u_name_t = u_name
        cmd = self.dbase.get_cmd_pid(cmds,'%s on' % u_name_t)
        if len(cmd) == 0:
            cmd = self.dbase.get_cmd_pid(macros,'%s on' % u_name_t)
        if len(cmd) == 1:
            cmd = cmd[next(iter(cmd))].num
        else:
            self.gui.output_text('    Warning - ON cmd mixed up for %s' % u_name)
            return 0
        processed_unit['on_cmd'] = IOUtils.underscore_it(cmd)
        cmd = self.dbase.get_cmd_pid(cmds,'%s off' % u_name_t)
        if len(cmd) == 0:
            cmd = self.dbase.get_cmd_pid(macros,'%s on' % u_name_t)
        if len(cmd) == 1:
            cmd = cmd[next(iter(cmd))].num
        else:
            self.gui.output_text('    Warning - OFF cmd mixed up for %s' % u_name)
            return 0
        processed_unit['off_cmd'] = IOUtils.underscore_it(cmd)
        processed_unit['power_val'] = 0.0
        processed_unit['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses[u_name].num)
        if u_name_t in self.dbase.mmdc_assoc.keys():
            master_unit = self.dbase.mmdc_assoc[u_name_t]
            if 'MMDC' in master_unit:
                tlm_search = 'MMDC ' + master_unit[4:] + ' Side ' + u_name_device[-1] + ' Curnt Sense'
            elif 'CPSU' in master_unit:
                if u_name_device[-1] == '1':
                    tlm_search = 'CPSU ' + master_unit[4:] + ' EPC P Output Shunt Curnt'
                else:
                    tlm_search = 'CPSU ' + master_unit[4:] + ' EPC R Output Shunt Curnt'
            else:
                tlm_search = 'do not search, blerg'
            cmd = self.dbase.get_cmd_pid(tlm_misc, tlm_search)
            if len(cmd) == 1:
                cmd = cmd[next(iter(cmd))].num
                processed_unit['bus_curnt_tlm'] = IOUtils.underscore_it(cmd)
        return processed_unit
    
    def _process_tcnr(self, u_name, u_name_device, cmds):
        # Find on/off in database
        processed_unit = {}
        
#         num = re.search('\d+.*', u_name).group(0)
        num = IOUtils.get_rd(u_name)
        if re.search('bcn|beacon', u_name.lower()):
            search_str = 'xmtr'
            u_name_device = 'BcnXmtr_' + num
        elif re.search('tlm', u_name.lower()):
            search_str = 'xmtr'
            if '(2' in u_name: # Corrections for old RD schema
                num = re.search('\d\d\d', u_name)
                if num:
                    num = num.group(0)
                else:
                    num = '22' + re.search('\d', u_name).group(0)
            u_name_device = 'TlmXmtr_' + num
        elif re.search('twt', u_name.lower()):
            search_str = 'twt'
        processed_unit['name'] = u_name_device
        
        cmds_t = self.dbase.get_cmd_pid(cmds,'%s' % num)
        cmds_t = self.dbase.get_cmd_pid(cmds_t, search_str)
        cmds_t = self.dbase.get_cmd_pid(cmds_t, 'rang', '!=')
        cmds_tt = {}
        for cmd in cmds_t.values(): # Filter out linked commands
            if ',' not in cmd.des:
                cmds_tt[cmd.num] = cmd
        cmd = self.dbase.get_cmd_pid(cmds_tt,'on')
        if len(cmd) == 1:
            cmd = cmd[next(iter(cmd))].num
        else:
            self.gui.output_text('    Warning - ON cmd mixed up for %s' % u_name)
            return 0
        processed_unit['on_cmd'] = IOUtils.underscore_it(cmd)
        cmd = self.dbase.get_cmd_pid(cmds_tt,'off')
        if len(cmd) == 1:
            cmd = cmd[next(iter(cmd))].num
        else:
            self.gui.output_text('    Warning - OFF cmd mixed up for %s' % u_name)
            return 0
        processed_unit['off_cmd'] = IOUtils.underscore_it(cmd)
         
        processed_unit['power_val'] = 0.0
        processed_unit['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses[u_name].num)
        return processed_unit
    
    def _process_acs_misc(self):
        processed_units = {}
        processed_units_sort = []
        
        # ACE
        processed_units['ACE_1'] = {}
        processed_units['ACE_1']['name'] = 'ACE_1'
        processed_units['ACE_1']['on_cmd'] = 'AC_00100'
        processed_units['ACE_1']['off_cmd'] = 'AC_00105'
        processed_units['ACE_1']['power_val'] = 0.0
        processed_units['ACE_1']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ACE_1'].num)
        processed_units_sort.append('ACE_1')
        processed_units['ACE_2'] = {}
        processed_units['ACE_2']['name'] = 'ACE_2'
        processed_units['ACE_2']['on_cmd'] = 'AC_00200'
        processed_units['ACE_2']['off_cmd'] = 'AC_00205'
        processed_units['ACE_2']['power_val'] = 0.0
        processed_units['ACE_2']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ACE_2'].num)
        processed_units_sort.append('ACE_2')
        
        # ICU units: BA_GSP, Encoder
        if 'ICU_1' in self.dbase.carved_subbuses.keys():
            processed_units['BA_GSP_1'] = {}
            processed_units['BA_GSP_1']['name'] = 'BA_GSP_1'
            processed_units['BA_GSP_1']['on_cmd'] = 'HW_03570'
            processed_units['BA_GSP_1']['off_cmd'] = 'HW_03575'
            processed_units['BA_GSP_1']['power_val'] = 0.0
            processed_units['BA_GSP_1']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ICU_1'].num)
            processed_units_sort.append('BA_GSP_1')
            processed_units['BA_GSP_2'] = {}
            processed_units['BA_GSP_2']['name'] = 'BA_GSP_2'
            processed_units['BA_GSP_2']['on_cmd'] = 'HW_04010'
            processed_units['BA_GSP_2']['off_cmd'] = 'HW_04015'
            processed_units['BA_GSP_2']['power_val'] = 0.0
            processed_units['BA_GSP_2']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ICU_2'].num)
            processed_units_sort.append('BA_GSP_2')
            processed_units['Encoder_1'] = {}
            processed_units['Encoder_1']['name'] = 'Encoder_1'
            processed_units['Encoder_1']['on_cmd'] = 'DH_01800'
            processed_units['Encoder_1']['off_cmd'] = 'DH_01805'
            processed_units['Encoder_1']['power_val'] = 0.0
            processed_units['Encoder_1']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ICU_1'].num)
            processed_units_sort.append('Encoder_1')
            processed_units['Encoder_2'] = {}
            processed_units['Encoder_2']['name'] = 'Encoder_2'
            processed_units['Encoder_2']['on_cmd'] = 'DH_01850'
            processed_units['Encoder_2']['off_cmd'] = 'DH_01855'
            processed_units['Encoder_2']['power_val'] = 0.0
            processed_units['Encoder_2']['subbus_pid'] = IOUtils.underscore_it(self.dbase.carved_subbuses['ICU_2'].num)
            processed_units_sort.append('Encoder_2')
        
        # ST
        if 'AC26100' in self.dbase.cmd.keys():  # AC26100 - ST 1 ON Seq
            processed_units['ST_1'] = {}
            processed_units['ST_1']['name'] = 'ST_1'
            processed_units['ST_1']['on_cmd'] = 'AC_26110'
            processed_units['ST_1']['off_cmd'] = 'AC_26115'
            processed_units['ST_1']['power_val'] = 4.5
            processed_units['ST_1']['subbus_pid'] = 'PWD90065'
            processed_units_sort.append('ST_1')
            processed_units['ST_2'] = {}
            processed_units['ST_2']['name'] = 'ST_2'
            processed_units['ST_2']['on_cmd'] = 'AC_26210'
            processed_units['ST_2']['off_cmd'] = 'AC_26215'
            processed_units['ST_2']['power_val'] = 4.5
            processed_units['ST_2']['subbus_pid'] = 'PWD90065'
            processed_units_sort.append('ST_2')
        
        # ES
        processed_units['ES_1'] = {}
        processed_units['ES_1']['name'] = 'ES_1'
        processed_units['ES_1']['on_cmd'] = 'AC_21000'
        processed_units['ES_1']['off_cmd'] = 'AC_21005'
        processed_units['ES_1']['power_val'] = 4.7
        processed_units['ES_1']['subbus_pid'] = 'PWD90065'
        processed_units_sort.append('ES_1')
        processed_units['ES_2'] = {}
        processed_units['ES_2']['name'] = 'ES_2'
        processed_units['ES_2']['on_cmd'] = 'AC_22000'
        processed_units['ES_2']['off_cmd'] = 'AC_22005'
        processed_units['ES_2']['power_val'] = 4.7
        processed_units['ES_2']['subbus_pid'] = 'PWD90065'
        processed_units_sort.append('ES_2')
        
        # TEC
        processed_units['TECpri'] = {}
        processed_units['TECpri']['name'] = 'TECpri'
        processed_units['TECpri']['on_cmd'] = 'AC_24100'
        processed_units['TECpri']['off_cmd'] = 'AC_24080'
        processed_units['TECpri']['power_val'] = 4.8
        processed_units['TECpri']['subbus_pid'] = 'PWD90065'
        processed_units_sort.append('TECpri')
        processed_units['TECstby'] = {}
        processed_units['TECstby']['name'] = 'TECstby'
        processed_units['TECstby']['on_cmd'] = 'AC_25100'
        processed_units['TECstby']['off_cmd'] = 'AC_25080'
        processed_units['TECstby']['power_val'] = 4.8
        processed_units['TECstby']['subbus_pid'] = 'PWD90065'
        processed_units_sort.append('TECstby')
        
        # Gyro
        if 'AC14350' in self.dbase.cmd.keys():  # AC_14350 - RLG 1 ON Seq
            processed_units['RLG_1'] = {}
            processed_units['RLG_1']['name'] = 'RLG_1'
            processed_units['RLG_1']['on_cmd'] = 'AC_14360'
            processed_units['RLG_1']['off_cmd'] = 'AC_14365'
            processed_units['RLG_1']['power_val'] = 23.0
            processed_units['RLG_1']['subbus_pid'] = 'PWD90065'
            processed_units_sort.append('RLG_1')
            processed_units['RLG_2'] = {}
            processed_units['RLG_2']['name'] = 'RLG_2'
            processed_units['RLG_2']['on_cmd'] = 'AC_15360'
            processed_units['RLG_2']['off_cmd'] = 'AC_15365'
            processed_units['RLG_2']['power_val'] = 23.0
            processed_units['RLG_2']['subbus_pid'] = 'PWD90065'
            processed_units_sort.append('RLG_2')
            if 'AC16350' in self.dbase.cmd.keys():  # AC16350 - RLG 3 ON Seq
                processed_units['RLG_3'] = {}
                processed_units['RLG_3']['name'] = 'RLG_3'
                processed_units['RLG_3']['on_cmd'] = 'AC_16360'
                processed_units['RLG_3']['off_cmd'] = 'AC_16365'
                processed_units['RLG_3']['power_val'] = 23.0
                processed_units['RLG_3']['subbus_pid'] = 'PWD90065'
                processed_units_sort.append('RLG_3')
        
        return processed_units_sort, processed_units
    
    def add_units(self):
        # Heaters
        devices_t = {}
        for u_name in self.spacecraft.cf_heaters.keys():
            u_name_device = u_name.replace(' ','_').replace(',','')
            processed_unit = self._process_heaters(u_name, u_name_device)
            if 'battery' in u_name.lower():
                u_name_device = 'Bat' + u_name_device[7:]
                processed_unit_flight = processed_unit.copy()
                processed_unit_flight['name'] = u_name_device + '_flight'
                devices_t[processed_unit_flight['name']] = processed_unit_flight
                processed_unit['name'] = u_name_device + '_batsim'
                processed_unit['power_val'] = 50.0
            devices_t[processed_unit['name']] = processed_unit
        self.spacecraft.sorted_device_names = self._sort_by_on(devices_t)
        self.spacecraft.devices = dict(self.spacecraft.devices,**devices_t)
        
        # TWTAs
        devices_t = {}
        twtas_t = [] # Needed for grouped twta subbus carving
        for u_name in sorted(self.spacecraft.twtas.keys()):
            if re.search('[a-z|A-Z]\d',u_name[-2:]):
                twtas_t.append(u_name[:-2])
            twtas_t.append(u_name)
            u_name_device = u_name.replace(' ','_').replace(',','')
            processed_unit = self._process_twtas(u_name, u_name_device)
            devices_t[processed_unit['name']] = processed_unit
            processed_unit = self._process_lcamps(u_name, u_name_device)
            if len(processed_unit.keys()) > 0:
                devices_t[processed_unit['name']] = processed_unit
        self.spacecraft.sorted_device_names.extend(self._sort_by_on(devices_t))
        self.spacecraft.devices = dict(self.spacecraft.devices,**devices_t)
         
        # Other stuff
        devices_t_misc = {}
        devices_t_tcnr = {}
        misc_search = 'lna|cnvtr|mlo|mro|mmdc|mini|rcvr|cpsu'
        cmds_misc = self.dbase.get_cmd_pid(self.dbase.cmd, misc_search)
        tlm_misc = self.dbase.get_cmd_pid(self.dbase.tlm, misc_search)
        cmds_misc = self.dbase.get_cmd_pid(cmds_misc,',','!=') # Get rid of ganged commands
        macs_misc = self.dbase.get_cmd_pid(self.dbase.mac, misc_search)
        cmds_tcnr = self.dbase.get_cmd_pid(self.dbase.cmd,'xmtr|twt')
        for u_name in sorted(self.dbase.carved_subbuses.keys()):
            u_name_device = u_name.replace(' ','_').replace(',','')
            if u_name_device not in self.spacecraft.devices.keys() and 'htr' not in u_name_device.lower():
                if re.search(misc_search, u_name.lower()):
                    processed_unit = self._process_misc(u_name, u_name_device, cmds_misc, macs_misc, tlm_misc)
                    if processed_unit != 0:
                        devices_t_misc[processed_unit['name']] = processed_unit
                elif re.search('xmtr|twt', u_name.lower()) and u_name not in twtas_t and u_name[:-1] not in twtas_t:
                    processed_unit = self._process_tcnr(u_name, u_name_device, cmds_tcnr)
                    if processed_unit != 0:
                        devices_t_tcnr[processed_unit['name']] = processed_unit
        self.spacecraft.sorted_device_names.extend(self._sort_by_on(devices_t_misc))
        self.spacecraft.devices = dict(self.spacecraft.devices,**devices_t_misc)
        self.spacecraft.sorted_device_names.extend(self._sort_by_on(devices_t_tcnr))
        self.spacecraft.devices = dict(self.spacecraft.devices,**devices_t_tcnr)
         
        # Unchanging stuff (ACS, etc)
        sorted_acs_misc, devices_t_acs_misc = self._process_acs_misc()
        self.spacecraft.sorted_device_names.extend(sorted_acs_misc)
        self.spacecraft.devices = dict(self.spacecraft.devices,**devices_t_acs_misc)

#******************************************************************************************************************************
# Output
#******************************************************************************************************************************

class DeviceScript:
    
    def __init__(self, gui, dbase, spacecraft):
        """ Constructor
         
        Arguments: gui -- GUI object
                   dbase -- Database object
                   spacecraft -- Spacecraft object
                   author -- Author name string 
        """
        self.gui = gui
        self.dbase = dbase
        self.spacecraft = spacecraft
        self.script_name = spacecraft.script_dir + 'textsrc\\device2.xml'
        
    def write(self):
        # Write file: init
        f = open(self.script_name,'w')
        text = '<DEVICES>\n'
        text += '  <Defaults tolerance="0.1" samples="200" />\n'
        
        # Write file
        for u_name in self.spacecraft.sorted_device_names:
            unit = self.spacecraft.devices[u_name]
            on_cmd = unit['on_cmd']
            off_cmd = unit['off_cmd']
            subbus_pid = unit['subbus_pid']
            power_val = unit['power_val']
            if 'Htr' in u_name:
                if power_val > 15 or 'cur_mon_tlm' in unit.keys():
                    if 'cur_mon_tlm' in unit:
                        # For heaters with current monitor pids (which are prop line heaters only),
                        # the current monitor is on a 100 volt bus. Even though these heaters are 
                        # actually on a 31.6 volt bus, they are measured on a 100 volt bus and thus
                        # the excpected value must be adjusted. 
                        power_val *= 100/31.6
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" expected="%0.1f">\n' % \
                    (u_name, on_cmd, off_cmd, power_val)
                    text += '    <Subbus pid="%s"/>\n' % subbus_pid
                    if 'cur_mon_tlm' in unit:
                        text += '    <Optional type="monA" pid="%s"/>\n' % unit['cur_mon_tlm']
                else:
                    min_req = 1/power_val
                    rpt_req = max([0.2, min_req])
                    gen_req = max([0.75, min_req])
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" tolerance="%0.2f" expected="%0.1f">\n' % \
                    (u_name, on_cmd, off_cmd, gen_req, power_val)
                    text += '    <Subbus pid="%s"/>\n' % subbus_pid
                    text += '    <Override tolerance="%0.2f" phase="13" test="true"/>\n' % rpt_req
            elif re.search('ES_|ST_|TEC', u_name):
                if 'ST_' in u_name:
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" tolerance="0.3" samples="1000" expected="%0.1f">\n' % (u_name, on_cmd, off_cmd, power_val)
                else:
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" tolerance="0.3" expected="%0.1f">\n' % (u_name, on_cmd, off_cmd, power_val)
                text += '    <Subbus pid="%s"/>\n' % subbus_pid
                text += '    <Override tolerance="0.5" phase="14" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="15" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="16" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="17" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="18" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="19" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="20" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="21" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="22" test="true"/>\n'
                text += '    <Override tolerance="0.5" phase="24" test="true"/>\n'
            else:
                if 'Mini' in u_name:
                    power_val = 4.2
                elif 'DCnvtr' in u_name:
                    power_val = 4.4
                elif 'LNA' in u_name:
                    power_val = 2.1
#                 power_val = 0.0
#                 if 'TWT_' in u_name:
#                     u_name = u_name.replace('TWT_', self.spacecraft.t+'_')
                if 'RLG_' in u_name:
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" samples="1000" expected="%0.1f">\n' % (u_name, on_cmd, off_cmd, power_val)
                else:
                    text += '  <Device name="%s" oncmd="%s" offcmd="%s" expected="%0.1f">\n' % (u_name, on_cmd, off_cmd, power_val)
                text += '    <Subbus pid="%s"/>\n' % subbus_pid
                if 'bus_curnt_tlm' in unit:
                    text += '    <Optional type="monA" pid="%s"/>\n' % unit['bus_curnt_tlm']
#             if 'twt' not in u_name.lower():
            text += '  </Device>\n'
        
        # Finalize and close
        text += '</DEVICES>\n'
        f.write(text)        
        f.close()
