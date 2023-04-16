import json
import re
import textwrap
from ghidra.app.decompiler.flatapi import FlatDecompilerAPI
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
from ghidra.program.flatapi import FlatProgramAPI
import json
import logging
import httplib
import os
from datetime import datetime
import httplib
import pickle
from javax.swing import *
from java.awt import *
from javax.swing.table import DefaultTableModel


# setting up FlatProgram
state = getState()
program = state.getCurrentProgram()
fp = FlatProgramAPI(program)
fd = FlatDecompilerAPI(fp)

# return all variables in the current function
# NOTE: gets the local variable names, not meaningful names
# tried to get from decompile, however it outs in a string, so there's not a parser for fncs in a string
def get_variables_in_function(ca):
    fnc = getFunctionContaining(ca)
    # decfnc = decompiler.decompileFunction(fnc, 5, monitor).getDecompiledFunction().getC()
    # fnc = currentLocation.getDecompile().getFunction()
    return fnc.getVariables(None)


# returns all functions that call the current function (at the current address)
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_calling_functions():
    fnc = fm.getFunctionContaining(currentAddress)
    all_fncs = fnc.getCallingFunctions(monitor)
    return all_fncs


# writes the global namespace to a file
# NOTE: how helpful is this in the grand scheme of things?
def get_namespaces():
    namespaces = getCurrentProgram().getNamespaceManager().getGlobalNamespace()


# Function to get the highlighted text from the decompile panel in Ghidra
def get_highlighted_text(event):
    # get highlighted text
    # decompile that highlighted text?
    # currentProgram = getCurrentProgram()
    currhighlight = state.getCurrentHighlight()
    print("current highlight")
    print(currhighlight.toString())
    # for i in testhigh:
        # print(i)
    # print("current highlight")
    # print(currhighlight.toString())
    # print(currhighlight)
    decompiler = FlatDecompilerAPI()
    # decompiler.openProgram(currentProgram)
    fnc = getFunctionContaining(currentAddress)
    print(fd.getDecompiler().decompileFunction(fnc, 5, monitor))

    highlighted_text = currentLocation.getDecompile()
    # highlight1 = state.getCurrentHighlight().toString()
    # print("code decompile")
    # # print(decompiler.decompileFunction(currentLocation, 5, monitor))
    # print("highlighted text")
    print(highlight1)

class ScriptGUI:
    def runFunction(self, event):
        # Option for getting variable infromation
        if self.fun_select.selectedIndex == 0:
            var_list = get_variables_in_function(self.function_address[self.targ_addr.selectedIndex])
            self.colnames = ('Name', 'Data Type', 'Length')
            self.tableData = []
            for v in var_list:
                cur = []
                cur.append(v.getName())
                cur.append(v.getDataType())
                cur.append(v.getLength())
                self.tableData.append(cur)
            print(self.tableData)
            self.updateTable()
        # Option for getting all function info
        elif self.fun_select.selectedIndex == 1:
            f = getFirstFunction()
            self.colnames = ('Name', 'Return Type', 'Address', 'Thunk')
            self.tableData = []
            while f is not None:
                row = []
                if (f.isThunk() and self.cb.isSelected()):
                    f = getFunctionAfter(f)
                    continue
                row.append(f.getName())
                row.append(f.getReturnType())
                row.append(f.getEntryPoint())
                row.append(f.isThunk())
                self.tableData.append(row)
                f = getFunctionAfter(f)
            self.updateTable()

        elif self.fun_select.selectedIndex == 2:
            print("hello")
        else:
            print("error 404")

    def loadObject(self, event):
        print("ewwo")

    def saveObject(self, event):
        print("ewwo")

    def updateTable(self):
        dataModels = DefaultTableModel(self.tableData, self.colnames)
        self.table = JTable(dataModels)
        self.tablePane.getViewport().setView(self.table)
    def __init__(self):
        self.dataObject = None
        apiFrame = JFrame()
        apiFrame.setSize(380,350)
        apiFrame.setLocation(200,200)
        apiFrame.setLayout(FlowLayout())
        apiFrame.setTitle("Ghidra Datamanager")
        
        # Set up list of functions
        self.function_list = ['Get Local Variables', 'All Functions', 'Called Functions']
        self.fun_select = JComboBox(self.function_list)

        self.function_address = []
        self.function_names = []
        f = getFirstFunction()
        while f is not None:
            self.function_address.append(f.getEntryPoint())
            self.function_names.append(f.getName())
            f = getFunctionAfter(f)
            

        self.targ_addr = JComboBox(self.function_names)

        # Sets up function execute
        fun_button = JButton("Execute", actionPerformed=self.runFunction)

        # Sets up table
        colnames = ('Name', 'Data Type', 'Length')
        self.tableData = []
        dataModel = DefaultTableModel(self.tableData, colnames)
        self.table = JTable(dataModel)

        self.tablePane = JScrollPane()
        self.tablePane.setPreferredSize(Dimension(320,170))
        self.tablePane.getViewport().setView(self.table)

        self.cb = JCheckBox('parse Thunk?')
        cbPanel = JPanel()
        cbPanel.add(self.cb)

        panelTable = JPanel()
        panelTable.add(self.tablePane)

        # Filename to save to
        self.textBox = JTextField(20)
        self.textBox.text = "Enter Filename"

        # Save / Load Buttons
        save = JButton("Save")
        load = JButton("Load")


        panel = JPanel()
        panel.add(self.fun_select)

        panel2 = JPanel()
        panel2.add(self.targ_addr)
        

        # Adds the objects to the GUI
        apiFrame.add(panel)
        apiFrame.add(cbPanel)
        apiFrame.add(panel2)
        apiFrame.add(fun_button)
        apiFrame.add(panelTable)
        apiFrame.add(self.textBox)
        apiFrame.add(save)
        apiFrame.add(load)

        apiFrame.setVisible(True)


ScriptGUI()

