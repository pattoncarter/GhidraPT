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
    with open(filepath + "GhidraPT/variables.txt", 'w') as file:
        all_vars = fnc.getVariables(None)
        for v in all_vars:
            file.write(v.getName() + '\n')

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
        #address_idx = self.targ_addr.selectedIndex
        #print(address_idx)
        #print(self.function_address[self.targ_addr.selectedIndex])
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
        elif self.fun_select.selectedIndex == 1:
            print("howdy")
        elif self.fun_select.selectedIndex == 2:
            print("hello")
        else:
            print("error 404")

    def loadObject(self, event):
        print("ewwo")

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
            with open('GhidraPT/'+self.textBox.text+'.json', 'w') as outfile:
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
            with open('GhidraPT/'+ self.textBox.text+'.json', 'w') as file:
                json.dump(data_list, file, indent=4)
            print("Table information written to" + self.textBox.text + ".json")
    def updateTable(self):
        dataModels = DefaultTableModel(self.tableData, self.colnames)
        self.table = JTable(dataModels)
        self.tablePane.getViewport().setView(self.table)
    def __init__(self):
        self.dataObject = None
        apiFrame = JFrame()
        apiFrame.setSize(400,300)
        apiFrame.setLocation(200,200)
        apiFrame.setLayout(FlowLayout())
        apiFrame.setTitle("Ghidra Datamanager")
        
        # Set up list of functions
        self.function_list = ['Get Variables', 'Get Functions', 'Find Recursion']
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
        self.tableData = [['wip', 'parseme', 'later']
        ,['wip', 'parseme', 'later']]
        colnames = ('Variable Name', 'Count', 'Recursion')
        dataModel = DefaultTableModel(self.tableData, colnames)
        self.table = JTable(dataModel)

        self.tablePane = JScrollPane()
        self.tablePane.setPreferredSize(Dimension(270,150))
        self.tablePane.getViewport().setView(self.table)

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
        apiFrame.add(panel2)
        apiFrame.add(fun_button)
        apiFrame.add(panelTable)
        apiFrame.add(self.textBox)
        apiFrame.add(save)
        apiFrame.add(load)

        apiFrame.setVisible(True)


ScriptGUI()

