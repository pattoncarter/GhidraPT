import json
import re
import textwrap
import os
from ghidra.app.decompiler.flatapi import FlatDecompilerAPI
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
from ghidra.program.flatapi import FlatProgramAPI
import json
import logging
import httplib
from datetime import datetime
import httplib
import pickle
from javax.swing import *
from java.awt import *
from javax.swing.table import DefaultTableModel
from ghidra.app.decompiler import DecompInterface

# setting up FlatProgram
state = getState()
program = state.getCurrentProgram()
fp = FlatProgramAPI(program)
fd = FlatDecompilerAPI(fp)
fm = currentProgram.getFunctionManager()
cwd = currentProgram.getExecutablePath()
name_size = len(currentProgram.getName())
filepath = cwd[:-(name_size)]

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


# returns all functions the current function (at the current address) calls
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_called_functions(ca):
    fnc = fm.getFunctionContaining(ca)
    all_fncs = fnc.getCalledFunctions(monitor)
    funcs = []
    for f in all_fncs:
        try:
            pfnc = re.search("::(.*)", f.toString()).group(1)
            funcs.append(f)
        except Exception as e:
            funcs.append(f)
    return funcs

# returns all functions that call the current function (at the current address)
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_calling_functions(ca):
    fnc = fm.getFunctionContaining(ca)
    all_fncs = fnc.getCallingFunctions(monitor)
    return all_fncs

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

def find_recursive_functions():
    recursive_functions = []
    f = getFirstFunction()
    while f is not None:
        fnc = fm.getFunctionContaining(f.getEntryPoint())
        all_fncs = fnc.getCalledFunctions(monitor)
        for func in all_fncs:
            try:
                if func.getEntryPoint() == f.getEntryPoint():
                    recursive_functions.append(f)
                    break
            except Exception as e:
                print(e)
                pass
        f = getFunctionAfter(f)
    return recursive_functions

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
                if (f.isExternal() and self.cb2.isSelected()):
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
            self.colnames = ('Name', 'Return Type', 'Address', 'Thunk')
            self.tableData = []
            call_func = get_called_functions(self.function_address[self.targ_addr.selectedIndex])
            for f in call_func:
                row = []
                if (f.isThunk() and self.cb.isSelected()):
                    continue
                if (f.isExternal() and self.cb2.isSelected()):
                    continue
                row.append(f.getName())
                row.append(f.getReturnType())
                row.append(f.getEntryPoint())
                row.append(f.isThunk())   
                self.tableData.append(row)
            self.updateTable()
        elif self.fun_select.selectedIndex == 3:
            self.colnames = ('Name', 'Return Type', 'Address', 'Thunk')
            self.tableData = []
            calling_func = get_calling_functions(self.function_address[self.targ_addr.selectedIndex])
            for f in calling_func:
                row = []
                if ((not f.isThunk()) or (not self.cb.isSelected())):
                    row.append(f.getName())
                    row.append(f.getReturnType())
                    row.append(f.getEntryPoint())
                    row.append(f.isThunk())   
                    self.tableData.append(row)
            self.updateTable()
        elif self.fun_select.selectedIndex == 4:
            fun_list = find_recursive_functions()
            self.colnames = ('Name', 'Return Type', 'Address', 'Thunk')
            self.tableData = []
            for f in fun_list:
                row = []
                row.append(f.getName())
                row.append(f.getReturnType())
                row.append(f.getEntryPoint())
                row.append(f.isThunk())
                self.tableData.append(row)
            self.updateTable()
        else:
            print("error 404")

    def saveObject(self, event):
        if self.fun_select.selectedIndex == 0:
                # Get the current program and function being viewed
            current_function = getFunctionContaining(currentAddress)

            # Initialize the decompiler
            decomp_interface = DecompInterface()
            decomp_interface.openProgram(program)
            # Decompile the function
            function_decompilation = decomp_interface.decompileFunction(current_function, 0, monitor)

            # Get the high-level function representation
            high_function = function_decompilation.getHighFunction()

            # Extract the names and types of the local variables and add them to a dictionary
            variable_info = {}
            for var_symbol in high_function.getLocalSymbolMap().getSymbols():
                variable_name = var_symbol.getName()
                variable_type = var_symbol.getDataType().getName()
                variable_info[variable_name] = variable_type


            # Write the dictionary as a JSON object to a text file
            with open(filepath + 'GhidraPT/'+self.textBox.text+'.json', 'w') as outfile:
                json.dump(variable_info, outfile, indent=4)

            print("Variable information written to GhidraPT/" + self.textBox.text + ".json")
        else:
            # Get the row and column counts
            row_count = self.table.getRowCount()
            col_count = self.table.getColumnCount()
            col_names = ('Name', 'Return Type', 'Address', 'Thunk')
            # Create a list of dictionaries to hold the data
            data_list = {}

            # Iterate over the rows and columns of the table
            for i in range(row_count):
                data_dict = {}
                for j in range(col_count):
                    value = self.table.getValueAt(i, j)
                    key = col_names[j]
                    data_dict[key] = str(value)
                data_list[i]=(data_dict)

            # Write the data to a JSON file
            with open(filepath + 'GhidraPT/'+ self.textBox.text+'.json', 'w') as file:
                json.dump(data_list, file, indent=4)
            print("Table information written to" + self.textBox.text + ".json")

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
        self.function_list = ['Get Local Variables', 'All Functions', 'Called Functions', 'Caller Functions', 'Recursive Functions']
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

        self.cb2 = JCheckBox('parse Extern?')
        cbPanel2 = JPanel()
        cbPanel2.add(self.cb2)

        panelTable = JPanel()
        panelTable.add(self.tablePane)

        # Filename to save to
        self.textBox = JTextField(30)
        self.textBox.text = "Enter Filename"

        # Save / Load Buttons
        save = JButton("Save", actionPerformed=self.saveObject)

        panel = JPanel()
        panel.add(self.fun_select)

        panel2 = JPanel()
        panel2.add(self.targ_addr)
        

        # Adds the objects to the GUI
        apiFrame.add(panel)
        apiFrame.add(cbPanel)
        apiFrame.add(cbPanel2)
        apiFrame.add(panel2)
        apiFrame.add(fun_button)
        apiFrame.add(panelTable)
        apiFrame.add(self.textBox)
        apiFrame.add(save)

        apiFrame.setVisible(True)


ScriptGUI()

