#******************************************************************************************************************************
# File: Components.py
# Desc: Component structure collector
#******************************************************************************************************************************

#******************************************************************************************************************************
# Supporting Structures
#******************************************************************************************************************************

class CmdTlm:
    """ Command/Telem Object Structure """
    
    def __init__(self):
        """ Constructor """
        self.num = ''
        self.des = ''
        self.bin = ''
        self.format_key = ''
        self.sia_add = ''

class Spacecraft:
    """ Spacecraft Object Structure """
    
    def __init__(self):
        """ Constructor """
        self.name = ''
        self.omega = ''
        self.script_dir = ''
        self.data_dir = ''
        self.db_dir = ''
        self.heaters = {}
        self.cf_heaters = {}
        self.twtas = {}
        self.lcamps = {}
        self.devices = {}
        self.measure_camps = False
        self.sorted_htr_names = []
        
#******************************************************************************************************************************
# Component Structures
#******************************************************************************************************************************

class Heater:
    """ Heater Object Structure """
    
    def __init__(self):
        """ Constructor """
        self.name = ''
        self.thermisters = []
        self.vote_marg = []
        self.rate = ''
        self.cmds_pids = {}
        self.subbus = CmdTlm()
        self.tray = ''
        self.sfty_rly = HtrSftyRly()
        self.power_val = ''

class HtrSftyRly:
    """ Heater Safety Relay Object Structure """
    
    def __init__(self):
        """ Constructor """
        self.name = ''
        self.thermisters = []
        self.vote_marg = []
        self.rate = ''
        self.cmds_pids = {}
        self.links = {'on_cmd': False, 'off_cmd': False, 'ena_cmd': False, 'dis_cmd': False}

class Twta:
    """ TWTA Object Structure """
    
    def __init__(self, name=''):
        """ Constructor """
        self.name = name
        self.lcamp = LCamp()
        self.cmds_pids = {}
        self.subbus = CmdTlm()
        self.linked_off = False
        self.linked_twta = ''
        self.test_lcamp = True
        self.power_val = ''
        
#******************************************************************************************************************************
# Subunit Structures
#******************************************************************************************************************************

class Thermistor:
    """ Thermistor Object Structure """
    
    def __init__(self,):
        """ Constructor """
        self.name = ''
        self.tlm = CmdTlm()
        self.low_sp_dec = ''
        self.high_sp_dec = ''
        self.low_sp_hex = ''
        self.high_sp_hex = ''
        self.lower_limit = None
        self.upper_limit = None
        self.sp_dir = 1

class LCamp:
    """ LCamp Object Structure """
    
    def __init__(self, name=''):
        """ Constructor """
        self.name = name
        self.testing_twta = ''
        self.opa_lin_incr = 0
        self.opa_lin_decr = 0
        self.camp_incr = 0
        self.camp_decr = 0
        self.cmds_pids = {}
        self.power_val = ''
