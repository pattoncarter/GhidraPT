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
def get_variables_in_function(event):
    # currentProgram = getCurrentProgram()
    # decompiler = DecompInterface()
    # decompiler.openProgram(currentProgram)
    fnc = getFunctionContaining(currentAddress)
    # decfnc = decompiler.decompileFunction(fnc, 5, monitor).getDecompiledFunction().getC()
    # fnc = currentLocation.getDecompile().getFunction()
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
    # return highlighted_text


class ScriptGUI:
    def __init__(self):
        apiFrame = JFrame()
        apiFrame.setSize(400,300)
        apiFrame.setLocation(200,200)
        apiFrame.setLayout(FlowLayout())
        apiFrame.setTitle("Enter API Key")
        
        # Set up list of functions
        self.function_list = ('Get Variables', 'Get Functions', 'Find Recursion')
        self.fun_select = JComboBox(self.function_list)

        # Sets up function execute
        fun_button = JButton("Execute", actionPerformed=get_variables_in_function)

        # Sets up table
        self.tableData = [['wip', 'parseme', 'later']
        ,['wip', 'parseme', 'later']]
        colnames = ('Variable Name', 'Count', 'Recursion')
        dataModel = DefaultTableModel(self.tableData, colnames)
        self.table = JTable(dataModel)

        tablePane = JScrollPane()
        tablePane.setPreferredSize(Dimension(270,150))
        tablePane.getViewport().setView(self.table)

        panelTable = JPanel()
        panelTable.add(tablePane)

        # Filename to save to
        self.textBox = JTextField(25)
        self.textBox.text = "Enter Filename"

        # Save / Load Buttons
        save = JButton("Save")
        load = JButton("Load")


        panel = JPanel()
        panel.add(self.fun_select)

        
        apiFrame.add(panel)
        apiFrame.add(fun_button)
        apiFrame.add(panelTable)
        apiFrame.add(self.textBox)
        apiFrame.add(save)
        apiFrame.add(load)

        apiFrame.setVisible(True)

'''
textBox = JTextField(25)
def saveKey(event):
    string = textBox.text
    f = open("api_key", "wb")
    pickle.dump(string, f)

def loadAPIFrame():
    apiFrame = JFrame()
    apiFrame.setSize(300,300)
    apiFrame.setLocation(200,200)
    apiFrame.setTitle("Enter API Key")
    apiFrame.setLayout(FlowLayout())
    title = JLabel("Enter API Key")
    submit = JButton("Save", actionPerformed=saveKey)
    apiFrame.add(title)
    apiFrame.add(textBox)
    apiFrame.add(submit)
    apiFrame.setVisible(True)

def loadMainMenu():
    frame = JFrame()
    frame.setSize(200,350)
    frame.setLocation(200,200)
    frame.setTitle("Test 2")

    frame.setLayout(FlowLayout())

    title = JLabel("GhidraPT")
    promptlabel = JLabel("API Key")
    txt = JTextField(30)

    b1 = JButton("Analyze Code Segment")
    b2 = JButton("Exit")

    frame.add(title)
    frame.add(promptlabel)
    frame.add(txt)

    frame.add(b1)
    frame.add(b2)

    frame.setVisible(True)

# Set your API key
try:
    fopen = open("api_key", "rb")
    api_key = pickle.load(fopen)
    print(api_key)
except:
    loadAPIFrame()
'''
ScriptGUI()

def send_https_request(address, path, data, headers):
    try:
        conn = httplib.HTTPSConnection(address)
        json_req_data = json.dumps(data)
        conn.request("POST", path, json_req_data, headers)
        response = conn.getresponse()
        json_data = response.read()
        conn.close()
        try:
            data = json.loads(json_data)
            return data
        except ValueError:
            logging.error("Could not parse JSON response from OpenAI!")
            logging.debug(json_data)
            return None
    except Exception as e:
        logging.error("Error sending HTTPS request: {e}".format(e=e))
        return None


'''
if recompiled_code:
    PROMPT = (
        "Please analyze the following recompiled code from Ghidra and provide a "
        "summary of its functionality. Include information about the main "
        "functions and important variables."
	"Rewrite the code, changing the variable names to have more meaning,"
	"also apply standard coding procedures."
        "\n\nRecompiled code:\n\n" + str(recompiled_code) + "\n\nAnalysis:"
    )

ENGINE = "text-davinci-003"

MAX_TOKENS = 512


def openai_request(prompt=PROMPT, temperature=0.19, max_tokens=MAX_TOKENS, engine=ENGINE):
    data = {
        "model": engine,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    # The URL is "https://api.openai.com/v1/completions"
    host = "api.openai.com"
    path = "/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_api_key}".format(openai_api_key=api_key)
    }
    data = send_https_request(host, path, data, headers)
    if data is None:
        logging.error("OpenAI request failed!")
        return None
    logging.info("OpenAI request succeeded!")
    logging.info("Response: {data}".format(data=data))
    return data


def format_response(response, max_width=80):
    # Split the response into sentences
    sentences = re.split('(?<=[.!?]) +', response)

    # Initialize the formatted response string
    formatted_response = ""

    # Iterate through the sentences, wrapping and adding them to the formatted response
    for sentence in sentences:
        wrapped_sentence = textwrap.fill(sentence, width=max_width)
        formatted_response += wrapped_sentence + "\n\n"

    return "\n" + formatted_response.strip() + "\n"

response = openai_request()
result_text = response['choices'][0]['text']
print(result_text)
'''
