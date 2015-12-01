#******************************************************************************************************************************
# File: ScriptUtils.py
# Desc: Base class for scripts
#******************************************************************************************************************************

import os
import datetime

#******************************************************************************************************************************
# BaseScript
#******************************************************************************************************************************

class BaseScript:
    """ Write script data
    
    Description: Base class for script writing. Mostly a template, with children classes overriding much of the content.
    Usage: Template class
    Public Methods: write -- Write script
    """
    extension = ''
    description = ''
    outline = ''
    istc_setup = ''
    
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
        self.author = author
    
    def _write_header(self):
        """ Write header
        
        Description: Writes header info. Called by write.
        """
        # Open file for writing
        fName = self.name + self.extension
        if not os.path.isdir(self.script_dir):
            os.makedirs(self.script_dir)
        self.f = open(self.script_dir + fName,'w')
        
        # Write header
        date = datetime.date.today()
        date = '%02d.%02d.%d' % (date.month, date.day, date.year-2000)
        text = ''
        text += '#\n'
        text += '################################## HEADER #############################################\n'
        text += '#\n'
        text += '#\tFile Name:   %s\n' % fName
        text += '#\tResp Eng:    %s\n' % self.author
        text += '#\tDescription: %s\n' % self.description
        text += '#\n'
        text += '################################## HISTORY ############################################\n'
        text += '#\n'
        text += '#\t%s - %s - Auto-generated script\n' % (date, self.author)
        text += '#\n'
        text += self.outline
        self.f.write(text)
    
    def _write_istc_setup(self):
        """ Write ISTC Setup """
        text = self.istc_setup
        self.f.write(text)
        
    def _write_sc_setup(self):
        """ Write spacecraft Setup - template"""
        text = ''
        self.f.write(text)
        
    def _write_body(self):
        """ Write body for all units """
        for u_name in self.u_names:
            self._write_unit_body(u_name=u_name)
    
    def _write_unit_body(self, u_name):
        """ Write body for inidvidual unit - template """
        text = ''
        self.f.write(text)
    
    def _write_footer(self):
        """ Write footer - template"""
        text = ''
        self.f.write(text)
        self.f.close()
        
    def write(self):
        """ Write script """
        self._write_header()
        self._write_istc_setup()
        self._write_sc_setup()
        self._write_body()
        self._write_footer()
