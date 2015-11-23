#!/usr/bin/python

import tkinter as tk
from tkinter import *
from os import path
import sys
import os

def clearLogic(*ignore):
        ent.delete(0, 'end')
        ent1.delete(0, 'end')
        ent2.delete(0, 'end')
        ent3.delete(0, 'end')
        ent5.delete(0, 'end')
        ent6.delete(0, 'end')
        ent7.delete(0, 'end')
        ent8.delete(0, 'end')

def convertLogic(*ignore):

        frequencyHz = freqHz.get()
        frequencykHz = freqkHz.get()
        frequencyMHz = freqMHz.get()
        frequencyGHz = freqGHz.get()
        cycle_s = cycles.get()
        cycle_ms = cyclems.get()
        cycle_us = cycleus.get()
        cycle_ns = cyclens.get()

### Hz Entered         
        if (frequencyHz.isdigit()):               

                frequencyHz = int(freqHz.get())
                
                ent1.delete(0, 'end')
                ent1.insert(0, (frequencyHz / 1000))
                ent2.delete(0, 'end')
                ent2.insert(0, (frequencyHz / 1000000))
                ent3.delete(0, 'end')
                ent3.insert(0, (frequencyHz / 1000000000))

                ent5.delete(0, 'end')
                ent5.insert(0, (1/(frequencyHz)))
                ent6.delete(0, 'end')
                ent6.insert(0, (1/(frequencyHz))*1000)
                ent7.delete(0, 'end')
                ent7.insert(0, (1/(frequencyHz))*1000000)
                ent8.delete(0, 'end')
                ent8.insert(0, (1/(frequencyHz))*1000000000)

### kHz Entered                 
        elif(frequencykHz.isdigit()):

                frequencykHz = int(freqkHz.get())
                
                ent.delete(0, 'end')
                ent.insert(0, (frequencykHz * 1000))
                ent2.delete(0, 'end')
                ent2.insert(0, (frequencykHz / 1000))
                ent3.delete(0, 'end')
                ent3.insert(0, (frequencykHz / 1000000))

                ent5.delete(0, 'end')
                ent5.insert(0, (1/(frequencykHz))/1000)
                ent6.delete(0, 'end')
                ent6.insert(0, (1/(frequencykHz)))
                ent7.delete(0, 'end')
                ent7.insert(0, (1/(frequencykHz))*1000)
                ent8.delete(0, 'end')
                ent8.insert(0, (1/(frequencykHz))*1000000) 

### MHz Entered                  
        elif(frequencyMHz.isdigit()):

                frequencyMHz = int(freqMHz.get())
                
                ent.delete(0, 'end')
                ent.insert(0, (frequencyMHz * 1000000))
                ent1.delete(0, 'end')
                ent1.insert(0, (frequencyMHz * 1000))
                ent3.delete(0, 'end')
                ent3.insert(0, (frequencyMHz / 1000))

                ent5.delete(0, 'end')
                ent5.insert(0, (1/(frequencyMHz))/1000000)
                ent6.delete(0, 'end')
                ent6.insert(0, (1/(frequencyMHz))/1000)
                ent7.delete(0, 'end')
                ent7.insert(0, (1/(frequencyMHz)))
                ent8.delete(0, 'end')
                ent8.insert(0, (1/(frequencyMHz))*1000)

### GHz Entered                 
        elif(frequencyGHz.isdigit()):

                frequencyGHz = int(freqGHz.get())
                
                ent.delete(0, 'end')
                ent.insert(0, (frequencyGHz * 1000000000))
                ent1.delete(0, 'end')
                ent1.insert(0, (frequencyGHz * 1000000))
                ent2.delete(0, 'end')
                ent2.insert(0, (frequencyGHz * 1000))

                ent5.delete(0, 'end')
                ent5.insert(0, (1/(frequencyGHz))/1000000000)
                ent6.delete(0, 'end')
                ent6.insert(0, (1/(frequencyGHz))/1000000)
                ent7.delete(0, 'end')
                ent7.insert(0, (1/(frequencyGHz))/1000)
                ent8.delete(0, 'end')
                ent8.insert(0, (1/(frequencyGHz)))

### cycle s Entered                 
        elif(cycle_s.isdigit()):

                cycle_s = int(cycles.get())
                ##Hz
                ent.delete(0, 'end')
                ent.insert(0, (1/cycle_s))
                ##kHz
                ent1.delete(0, 'end')
                ent1.insert(0, ((1 / (cycle_s)) / 1000))
                ##MHz
                ent2.delete(0, 'end')
                ent2.insert(0, ((1/cycle_s) / 1000000))
                ##GHz
                ent3.delete(0, 'end')
                ent3.insert(0, ((1 / (cycle_s)) / 1000000000))

                ##seconds
                ent5.delete(0, 'end')
                ent5.insert(0, (cycle_s))
                ##milliseconds           
                ent6.delete(0, 'end')
                ent6.insert(0, (cycle_s * 1000))
                ##microseconds
                ent7.delete(0, 'end')
                ent7.insert(0, (cycle_s * 1000000))
                ##nanoseconds
                ent8.delete(0, 'end')
                ent8.insert(0, (cycle_s * 100000000))

### cycle ms Entered                 
        elif(cycle_ms.isdigit()):

                cycle_ms = int(cyclems.get())
                ##Hz
                ent.delete(0, 'end')
                ent.insert(0, (1/cycle_ms) * 1000)
                ##kHz
                ent1.delete(0, 'end')
                ent1.insert(0, (1 / (cycle_ms)))
                ##MHz
                ent2.delete(0, 'end')
                ent2.insert(0, (1/cycle_ms) /1000)
                ##GHz
                ent3.delete(0, 'end')
                ent3.insert(0, ((1 / (cycle_ms)) / 1000000))

                ##seconds
                ent5.delete(0, 'end')
                ent5.insert(0, (cycle_ms)/1000)
                ##milliseconds           
                ent6.delete(0, 'end')
                ent6.insert(0, (cycle_ms))
                ##microseconds
                ent7.delete(0, 'end')
                ent7.insert(0, (cycle_ms) * 1000)
                ##nanoseconds
                ent8.delete(0, 'end')
                ent8.insert(0, (cycle_ms * 1000000))

### cycle us Entered                 
        elif(cycle_us.isdigit()):

                cycle_us = int(cycleus.get())
                ##Hz
                ent.delete(0, 'end')
                ent.insert(0, (1/cycle_us) * 1000000)
                ##kHz
                ent1.delete(0, 'end')
                ent1.insert(0, (1 / (cycle_us)*1000))
                ##MHz
                ent2.delete(0, 'end')
                ent2.insert(0, (1/cycle_us))
                ##GHz
                ent3.delete(0, 'end')
                ent3.insert(0, ((1 / (cycle_us)) / 1000))

                ##seconds
                ent5.delete(0, 'end')
                ent5.insert(0, (cycle_us)/1000000)
                ##milliseconds           
                ent6.delete(0, 'end')
                ent6.insert(0, (cycle_us)/1000)
                ##microseconds
                ent7.delete(0, 'end')
                ent7.insert(0, (cycle_us))
                ##nanoseconds
                ent8.delete(0, 'end')
                ent8.insert(0, (cycle_us * 1000))

### cycle ns Entered                 
        elif(cycle_ns.isdigit()):

                cycle_ns = int(cyclens.get())
                ##Hz
                ent.delete(0, 'end')
                ent.insert(0, (1/cycle_ns) * 1000000000)
                ##kHz
                ent1.delete(0, 'end')
                ent1.insert(0, (1 / (cycle_ns)*1000000))
                ##MHz
                ent2.delete(0, 'end')
                ent2.insert(0, (1/cycle_ns)*1000)
                ##GHz
                ent3.delete(0, 'end')
                ent3.insert(0, (1 / (cycle_ns)))

                ##seconds
                ent5.delete(0, 'end')
                ent5.insert(0, (cycle_ns)/1000000000)
                ##milliseconds           
                ent6.delete(0, 'end')
                ent6.insert(0, (cycle_ns)/1000000)
                ##microseconds
                ent7.delete(0, 'end')
                ent7.insert(0, (cycle_ns)/1000)
                ##nanoseconds
                ent8.delete(0, 'end')
                ent8.insert(0, (cycle_ns))
                
        else:
                print("enter a number")

######################################################################
#
#Main Entry Point
#
######################################################################

root = tk.Tk()
root.title("Enter a Frequency")
freqHz = tk.StringVar()
freqkHz = tk.StringVar()
freqMHz = tk.StringVar()
freqGHz = tk.StringVar()
cycles = tk.StringVar()
cyclems = tk.StringVar()
cycleus = tk.StringVar()
cyclens = tk.StringVar()

label1 = tk.Label(text = "Frequency (Hz) : ")
label2 = tk.Label(text = "Frequency (kHz) : ")
label3 = tk.Label(text = "Frequency (MHz) : ")
label4 = tk.Label(text = "Frequency (GHz) : ")
label5 = tk.Label(text = "      ")
label6 = tk.Label(text = "Cycle (s) : ")
label7 = tk.Label(text = "Cycle (ms) : ")
label8 = tk.Label(text = "Cycle (us) : ")
label9 = tk.Label(text = "Cycle (ns) : ")

ent = tk.Entry(root,textvariable = freqHz)
ent1 = tk.Entry(root,textvariable = freqkHz)
ent2 = tk.Entry(root,textvariable = freqMHz)
ent3 = tk.Entry(root,textvariable = freqGHz)

ent5 = tk.Entry(root,textvariable = cycles)
ent6 = tk.Entry(root,textvariable = cyclems)
ent7 = tk.Entry(root,textvariable = cycleus)
ent8 = tk.Entry(root,textvariable = cyclens)

btn1 = tk.Button(root, text="Convert", command=convertLogic)
btn2 = tk.Button(root, text="Clear", command=clearLogic)

label1.grid(sticky = W, row = 0, column =0, columnspan = 10)
label2.grid(sticky = W, row = 1, column =0, columnspan = 10)
label3.grid(sticky = W, row = 2, column =0, columnspan = 10)
label4.grid(sticky = W, row = 3, column =0, columnspan = 10)
label5.grid(sticky = W, row = 4, column =0, columnspan = 10)
label6.grid(sticky = W, row = 5, column =0, columnspan = 10)
label7.grid(sticky = W, row = 6, column =0, columnspan = 10)
label8.grid(sticky = W, row = 7, column =0, columnspan = 10)
label9.grid(sticky = W, row = 8, column =0, columnspan = 10)

ent.grid(sticky = W, row = 0, column = 10)
ent1.grid(sticky = W, row = 1, column = 10)
ent2.grid(sticky = W, row = 2, column = 10)
ent3.grid(sticky = W, row = 3, column = 10)

ent5.grid(sticky = W, row = 5, column =10)
ent6.grid(sticky = W, row = 6, column =10)
ent7.grid(sticky = W, row = 7, column =10)
ent8.grid(sticky = W, row = 8, column =10)

btn1.grid(row=9, column = 1)
btn2.grid(row=9, column = 2)

root.bind('<Return>', convertLogic)
root.bind('<BackSpace>', clearLogic)

root.mainloop()
