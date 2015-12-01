#******************************************************************************************************************************
# File: AutogenToolGui.py
# Desc: Main frontend file for input/output
#******************************************************************************************************************************

import IOUtils
import Components
import textwrap
from tkinter import ttk
import tkinter
import tkinter.scrolledtext as tkst
import traceback

#******************************************************************************************************************************
# AutogenTool
#******************************************************************************************************************************

class AutogenTool(ttk.Frame):
    """ Display GUI  for script writing
    
    Description: Displays and manipulates GUI.
    Usage: This is the script that is called to run the whole program. From the command line, run: python AutogenToolGui.py
    where python is the name of your python 3 bin file
    """
    def __init__(self, parent):
        """ Constructor
        
        Arguments: parent -- root
        """
        # Inherited constructor
        super(AutogenTool, self).__init__(parent)
        
        # Parental unit
        self.parent = parent
        self.parent.geometry('800x800')
        self.parent.title('Autogen Tool')
        
        # Setup GUI
        self.initialize()
        self.pack(padx=10, pady=10, anchor='nw', fill='both', expand='yes')
        self.output_text_len = 0.0
        
        # Internal stuff
        self.ah_scripts = []
        self.cfh_scripts = []
        self.twta_scripts = []
    
    def get_program_list(self):
        """ Read programs.txt to get list of available programs """
        f = open('programs.txt')
        self.programs = {}
        programs_out = []
        for line in f:
            line = line.strip('\n')
            if 'Program_Name' not in line:
                data = line.split('\t')
                prog_name = data[0]
                script_dir = data[1]
                data_dir = data[2]
                db_dir = data[3] + 'Current\\'
                self.programs[prog_name] = []
                self.programs[prog_name].append(script_dir)
                self.programs[prog_name].append(data_dir)
                self.programs[prog_name].append(db_dir)
                programs_out.append(prog_name)
        return programs_out
    
    def output_text(self, text):
        """ Display text in output window
        
        Description: Displays text in output window. This is used throughout the code for debug/error catching purposes.
        Arguments: text -- text string to display
         """
        self.output_text_len += len(text)
        self.out_text.config(state=tkinter.NORMAL)
        self.out_text.insert('end', text + '\n')
        self.out_text.see(self.output_text_len)
        self.out_text.config(state=tkinter.DISABLED)
    
    def set_program(self, event):
        """ Kick off spacecraft info reading and display script names in windows
        
        Description: Creates Reader and Writer objects, commencing reading of inputs. Then displays script names.
         """
        # Clear output
        self.out_text.config(state=tkinter.NORMAL)
        self.out_text.delete(1.0,self.output_text_len+1.0)
        self.out_text.config(state=tkinter.DISABLED)
        
        # Clear listboxes
        self.a_htr_display.delete(0, len(self.ah_scripts))
        self.cf_htr_display.delete(0, len(self.cfh_scripts))
        self.twta_display.delete(0, len(self.twta_scripts))
        
        # Create spacecraft
        self.spacecraft = Components.Spacecraft()
        self.spacecraft.name = self.program_combo.get()
        self.spacecraft.script_dir = self.programs[self.spacecraft.name][0]
        self.spacecraft.data_dir = self.programs[self.spacecraft.name][1]
        self.spacecraft.db_dir = self.programs[self.spacecraft.name][2]
        self.author = self.author_text.get()
        
        # Create I/O objects
        try:
            self.reader = IOUtils.Reader(gui=self, spacecraft=self.spacecraft)
            self.reader.execute()
            self.writer = IOUtils.Writer(gui=self, dbase=self.reader.dbase, spacecraft=self.spacecraft, author=self.author)
            self.output_text('')
        except Exception as error:
            self.output_text('Failed to read spacecraft info: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def generate_auto_heaters(self):
        """ Create auto_heater scripts
        
        Description: Calls Writer write_script function to write all selected scripts. If no scripts are selected, all are
        generated.
         """
        # Get list of selected scripts
        sel = self.a_htr_display.curselection()
        scripts = []
        for i in sel:
            scripts.append(self.ah_scripts[int(i)])
        if len(scripts) == 0:
            scripts = self.ah_scripts
        
        # Generate
        self.output_text('Writing scripts...')
        try:
            for s_name in scripts:
                self.writer.write_script(s_name=s_name, s_type='AutoHtr')
            self.output_text('Finished writing scripts.\n')
        except Exception as error:
            self.output_text('Failed to generate scripts: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def process_auto_heaters(self):
        """ Process auto_heater scripts
        
        Description: Calls Reader read_auto_heaters function to read auto_heater inputs
         """
        self.a_htr_display.delete(0, len(self.ah_scripts))
        self.ah_scripts = []
        self.output_text('Reading auto heater inputs...')
        try:
            self.reader.read_auto_heaters()
            self.writer.ah_carve = self.reader.auto_heater_reader.carve
            self.output_text('Finished reading auto heater inputs.\n')
        except Exception as error:
            self.output_text('Failed to read auto heater info: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
        
        # Populate list box display
        for i,script_name in enumerate(sorted(self.writer.ah_carve)):
            self.ah_scripts.append(script_name)
            self.a_htr_display.insert(i, script_name)
    
    def generate_cf_heaters(self):
        """ Create cf_heater scripts
        
        Description: Calls Writer write_script function to write all selected scripts. If no scripts are selected, all are
        generated.
         """
        # Get list of selected scripts
        sel = self.cf_htr_display.curselection()
        scripts = []
        for i in sel:
            scripts.append(self.cfh_scripts[int(i)])
        if len(scripts) == 0:
            scripts = self.cfh_scripts
        
        # Generate
        self.output_text('Writing scripts...')
        try:
            for s_name in scripts:
                self.writer.write_script(s_name=s_name, s_type='CfHtr')
            self.output_text('Finished writing scripts.\n')
        except Exception as error:
            self.output_text('Failed to generate scripts: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def process_cf_heaters(self):
        """ Process cf_heater scripts
        
        Description: Calls Reader read_cf_heaters function to read cf_heater inputs
         """
        self.cf_htr_display.delete(0, len(self.cfh_scripts))
        self.cfh_scripts = []
        self.output_text('Reading cf heater inputs...')
        try:
            self.reader.read_cf_heaters()
            self.writer.cfh_carve = self.reader.cf_heater_reader.carve
            self.output_text('Finished reading cf heater inputs.\n')
        except Exception as error:
            self.output_text('Failed to read cf heater info: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
        
        # Populate list box display
        for i,script_name in enumerate(sorted(self.writer.cfh_carve)):
            self.cfh_scripts.append(script_name)
            self.cf_htr_display.insert(i, script_name)
    
    def generate_twtas(self):
        """ Create twta scripts
        
        Description: Calls Writer write_script function to write all selected scripts. If no scripts are selected, all are
        generated.
         """
        # Get list of selected scripts
        sel = self.twta_display.curselection()
        scripts = []
        for i in sel:
            scripts.append(self.twta_scripts[int(i)])
        if len(scripts) == 0:
            scripts = self.twta_scripts
        
        # Generate
        self.output_text('Writing scripts...')
        try:
            for s_name in scripts:
                self.writer.write_script(s_name=s_name, s_type='CfComTWT')
            self.output_text('Finished writing scripts.\n')
        except Exception as error:
            self.output_text('Failed to generate scripts: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def process_twtas(self):
        """ Process twta scripts
        
        Description: Calls Reader read_twtas function to read twta inputs
         """
        self.twta_display.delete(0, len(self.twta_scripts))
        self.twta_scripts = []
        self.output_text('Reading twta inputs...')
        try:
            self.reader.read_twtas()
            self.writer.twta_carve = self.reader.twta_reader.carve
            self.output_text('Finished reading twta inputs.\n')
        except Exception as error:
            self.output_text('Failed to write twta info: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
        
        # Populate list box display
        for i,script_name in enumerate(sorted(self.writer.twta_carve)):
            self.twta_scripts.append(script_name)
            self.twta_display.insert(i, script_name)
    
    def generate_device(self):
        """ Generate device file
        
        Description: Calls Writer write_device function to write device file.
        """
        # Get list of selected scripts
        # Generate
        try:
            self.output_text('Reading device file info...')
            self.reader.read_device()
            self.output_text('Writing device file...')
            self.writer.write_device()
            self.output_text('Finished writing device file.\n')
        except Exception as error:
            self.output_text('Failed to generate device file: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def generate_heater(self):
        """ Generate heater file
        
        Description: Calls Writer write_heater function to write heater file.
        """
        # Get list of selected scripts
        # Generate
        try:
            self.output_text('Reading heater file info...')
            self.reader.read_heater()
            self.output_text('Writing heater file...')
            self.writer.write_heater()
            self.output_text('Finished writing heater file.\n')
        except Exception as error:
            self.output_text('Failed to generate heater file: %s' % error)
            out = traceback.format_exc()
            self.output_text(out)
            print(out)
    
    def display_menu(self):
        """ Display help/instructions menu """
        # Create window
        top = tkinter.Toplevel()
        top.title('Instructions')
        top.geometry('1000x400')
        
        # Write instructions
        textbox = tkinter.Text(top)
        textbox.pack(fill='both', expand='yes')
        textbox.insert(tkinter.INSERT, textwrap.dedent('''\
        
        Autogen Tool 0.9.8
        RE: J.Richardson
        
        Before generating scripts for a new program, a few manual steps must be taken:
        1. Setup your system/Update programs.txt
            a. Add (or modify an existing) line in programs.txt. The first column is the (user choosable) program
               identifier. This is the name that will show up in the drop-down list. The second is the script directory.
               This is where the program will output scripts. It's convenient to make this an svn working copy - that
               way you can immediately commit any changes. The third is where you store input data (see step 2). The last
               column is where the database is located.
        2. Gather inputs - Thermal STIRs App A, C, F, G. This information is needed to populate spacecraft information. 
            a.  Go to http://bus-sys.ssd.loral.com/te/cgi-bin/docs.cgi?Subsystem=TE, search for "app" and select the
                relevant program. Then download the latest Thermal STIRS App A, C, F, and G (4 files total).
            b.  For heater.xml file: http://bus-sys.ssd.loral.com/te/cgi-bin/memos.cgi?Subsystem=TE, search for
                "constraints" and select the relevant program. Then open the Thermal Constraints for Ambient Testing.
                With the file opened (it will be a .docx file), look for the thermistor limits. Sometimes it's contained
                as an attached .xlsx file, sometimes it's a table at the end. Either way, copy that data to an .xlsx file
                and name it limits.xlsx.
            c.  Place the downloaded files in the data directory you just created.
        
        Now, you should be set to generate scripts. On this program's main screen, select the relevant program from the 
        drop-down list. Next, provide the author name (F. Lastname). For each group you wish to generate, press Process.
        To generate all scripts in a group, simply click Generate. By default, with no scripts selected, generate will 
        generate all. Otherwise, to generate specific scripts, multi-select the required scripts and click generate. 
        The scripts will be placed in the appropriate program directories. The bottom window will provide 
        diagnostics should something go wrong.
        
        '''))
        textbox.config(state=tkinter.DISABLED)
        
    def initialize(self):
        """ Create gui objects
        
        Description: Creates and places all gui objects and links actions to functions. 
         """
        # Default author value
        self.author = 'F. Lastname'
        self.author = 'M. Wilk'
        
        # Add menu
        menubar = tkinter.Menu(self.parent)
        menu_file = tkinter.Menu(menubar, tearoff=0)
        menu_file.add_command(label='Quit', command=self.parent.quit)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_help = tkinter.Menu(menubar, tearoff=0)
        menu_help.add_command(label='Instructions', command=self.display_menu)
        menubar.add_cascade(menu=menu_help, label='Help')
        self.parent.config(menu=menubar)
        
        # Add top frame        
        top_frame = ttk.Frame(self)
        top_frame.pack(side='top', fill='both')
        
        # Add spacecraft selection combo box and label
        label = ttk.Label(top_frame, text='Spacecraft: ')
        label.pack(side='left', padx=(10,0))
        self.program_combo = ttk.Combobox(top_frame)
        self.program_combo.pack(side='left')
        self.program_combo.state(['readonly'])
        self.program_combo['values'] = self.get_program_list()
        self.program_combo.bind('<<ComboboxSelected>>', self.set_program)
        
        # Add author line
        label = ttk.Label(top_frame, text='Author: ')
        label.pack(side='left', padx=(10,0))
        self.author_text = ttk.Entry(top_frame, width=20)
        self.author_text.pack(side='left')
        self.author_text.insert(0, self.author)
        
        # Organize and add status output window
        pw = ttk.Panedwindow(self, orient=tkinter.VERTICAL)
        mid_frame = ttk.Frame(pw, height=550)
        mid_frame.pack_propagate(0)
        self.out_text = tkst.ScrolledText(pw)
        self.out_text.config(state=tkinter.DISABLED)
        pw.pack(pady=10, side='bottom', fill='both', expand='yes')
        
        # Auto Heaters
        a_htr_frame = ttk.Labelframe(mid_frame, text='Auto Heater Scripts')
        a_htr_frame.pack(side='left', fill='both', expand='yes')
        self.a_htr_display = tkinter.Listbox(a_htr_frame, selectmode='extended')
        self.a_htr_display.pack(side='top', fill='both', expand='yes', padx=5, pady=5)
        a_htr_scrollbar = tkinter.Scrollbar(self.a_htr_display)
        a_htr_scrollbar.pack(side='right', fill='y')
        a_htr_scrollbar.config(command=self.a_htr_display.yview)
        self.a_htr_display.config(yscrollcommand=a_htr_scrollbar.set)
        a_frame1 = ttk.Frame(a_htr_frame)
        a_frame1.pack(side='left', fill='both', expand='yes')
        b_frame1 = ttk.Frame(a_htr_frame)
        b_frame1.pack(side='left', fill='both', expand='yes')
        button = ttk.Button(a_frame1, text='Process Inputs', command=self.process_auto_heaters)
        button.pack(side='right', padx=(0,5), pady=(0,5), anchor='center')
        button = ttk.Button(b_frame1, text='Generate Scripts', command=self.generate_auto_heaters)
        button.pack(side='left', padx=(5,0), pady=(0,5), anchor='center')
        
        # Cf Heaters
        cf_htr_frame = ttk.Labelframe(mid_frame, text='Cf Heater Scripts')
        cf_htr_frame.pack(side='left', fill='both', expand='yes', padx=10)
        self.cf_htr_display = tkinter.Listbox(cf_htr_frame, selectmode='extended')
        self.cf_htr_display.pack(side='top', fill='both', expand='yes', padx=5, pady=5)
        cf_htr_scrollbar = tkinter.Scrollbar(self.cf_htr_display)
        cf_htr_scrollbar.pack(side='right', fill='y')
        cf_htr_scrollbar.config(command=self.cf_htr_display.yview)
        self.cf_htr_display.config(yscrollcommand=cf_htr_scrollbar.set)
        a_frame2 = ttk.Frame(cf_htr_frame)
        a_frame2.pack(side='left', fill='both', expand='yes')
        b_frame2 = ttk.Frame(cf_htr_frame)
        b_frame2.pack(side='left', fill='both', expand='yes')
        button = ttk.Button(a_frame2, text='Process Inputs', command=self.process_cf_heaters)
        button.pack(side='right', padx=(0,5), pady=(0,5), anchor='center')
        button = ttk.Button(b_frame2, text='Generate Scripts', command=self.generate_cf_heaters)
        button.pack(side='left', padx=(5,0), pady=(0,5), anchor='center')
        
        # TWTAs
        twta_frame = ttk.Labelframe(mid_frame, text='TWTA Scripts')
        twta_frame.pack(side='left', fill='both', expand='yes')
        self.twta_display = tkinter.Listbox(twta_frame, selectmode='extended')
        self.twta_display.pack(side='top', fill='both', expand='yes', padx=5, pady=5)
        twta_scrollbar = tkinter.Scrollbar(self.twta_display)
        twta_scrollbar.pack(side='right', fill='y')
        twta_scrollbar.config(command=self.twta_display.yview)
        self.twta_display.config(yscrollcommand=twta_scrollbar.set)
        a_frame3 = ttk.Frame(twta_frame)
        a_frame3.pack(side='left', fill='both', expand='yes')
        b_frame3 = ttk.Frame(twta_frame)
        b_frame3.pack(side='left', fill='both', expand='yes')
        button = ttk.Button(a_frame3, text='Process Inputs', command=self.process_twtas)
        button.pack(side='right', padx=(0,5), pady=(0,5), anchor='center')
        button = ttk.Button(b_frame3, text='Generate Scripts', command=self.generate_twtas)
        button.pack(side='left', padx=(5,0), pady=(0,5), anchor='center')
        
        # Other stuff
        button = ttk.Button(top_frame, text='Heater File', command=self.generate_heater)
        button.pack(side='right', padx=(5,0), pady=(0,5))
        button = ttk.Button(top_frame, text='Device File', command=self.generate_device)
        button.pack(side='right', padx=(5,0), pady=(0,5))
        
        pw.add(mid_frame)
        pw.add(self.out_text)

#******************************************************************************************************************************
# Execute
#******************************************************************************************************************************

root = tkinter.Tk()
frame = AutogenTool(root)
root.mainloop()
