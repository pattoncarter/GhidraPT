from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin

# Function to get the highlighted text from the decompile panel in Ghidra
def get_highlighted_text():
    currentProgram = getCurrentProgram()
    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)


    highlighted_text = currentLocation.getDecompile().getCCodeMarkup()
    return highlighted_text

# Example usage
recompiled_code = get_highlighted_text()
if recompiled_code:
    print("Highlighted text from the decompile panel:")
    print(recompiled_code)
# @Author: Carter Patton and Daxton Gilliam
# @Functionality: This script utilizes chatGPT to analyze the highlighted recompiled code given by Ghidra.
import json
import re
import textwrap
import os
import ghidra.util.filechooser as filechooser
from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
import json
import logging
import httplib
import os
from datetime import datetime

# Set your API key
api_key = ''

# setting up writing to file
cwd = currentProgram.getExecutablePath()
name_size = len(currentProgram.getName())
filepath = cwd[:-(name_size)]
fm = currentProgram.getFunctionManager()
# TODO: make file for all folders to go into, rn errno 22 for inaccess, at
# to run right now, make GhidraPT folder in project folder
# os.mkdir(filepath + "GhidraPT")

#### INFORMATION GATHERING HELPER FUNCTIONS ####

# adds all function names for program to a text file
# TODO: filter out thunk functions
def get_function_names():
    function = getFirstFunction()
    with open(filepath + "GhidraPT/functions.txt", 'w') as file:
        while function is not None:
            file.write(function.getName() + '\n')
            function = getFunctionAfter(function)

# returns all functions the current function (at the current address) calls
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_called_functions():
    fnc = fm.getFunctionContaining(currentAddress)
    with open(filepath + "GhidraPT/called_functions.txt", 'w') as file:
        all_fncs = fnc.getCalledFunctions(monitor)
        for f in all_fncs:
            try:
                pfnc = re.search("::(.*)", f.toString()).group(1)
                file.write(pfnc + '\n')
            except Exception as e:
                file.write(f.toString())

# returns all functions that call the current function (at the current address)
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_calling_functions():
    fnc = fm.getFunctionContaining(currentAddress)
    with open(filepath + "GhidraPT/calling_functions.txt", 'w') as file:
        all_fncs = fnc.getCallingFunctions(monitor)
        for f in all_fncs:
            file.write(f.toString() + '\n')

# return all variables in the current function
# NOTE: gets the local variable names, not meaningful names
# tried to get from decompile, however it outs in a string, so there's not a parser for fncs in a string
def get_variables_in_function():
    # currentProgram = getCurrentProgram()
    # decompiler = DecompInterface()
    # decompiler.openProgram(currentProgram)
    fnc = fm.getFunctionContaining(currentAddress)
    # decfnc = decompiler.decompileFunction(fnc, 5, monitor).getDecompiledFunction().getC()
    # fnc = currentLocation.getDecompile().getFunction()
    with open(filepath + "GhidraPT/variables.txt", 'w') as file:
        all_vars = fnc.getVariables(None)
        for v in all_vars:
            file.write(v.getName() + '\n')

# writes the global namespace to a file
# NOTE: how helpful is this in the grand scheme of things?
def get_namespaces():
    namespaces = getCurrentProgram().getNamespaceManager().getGlobalNamespace()
    with open(filepath + "GhidraPT/namespaces.txt", 'a+') as file:
        file.write(namespaces)

def get_JSON_variables():
        # Get the current program and function being viewed
    current_program = state.getCurrentProgram()
    current_function = getFunctionContaining(currentAddress)
    projectDir = current_program.getProjectLocator().getProjectDir()

    folderName = current_function.getName()
    folderPath = os.path.join(projectDir.getAbsolutePath(), folderName)

    if not os.path.exists(folderPath):
        chooser = filechooser.DirectoryChooser("Select parent directory")
        parentDir = chooser.getSelectedFile()

        if parentDir != None:
            newFolder = os.path.join(parentDir.getAbsolutePath(), folderName)
            os.makedirs(newFolder)
            print("Folder created:", newFolder)
    else:
        print("Folder already exists:", folderPath)

    # Initialize the decompiler
    decomp_interface = DecompInterface()
    decomp_interface.openProgram(current_program)

    # Set the decompilation options
    decomp_options = DecompileOptions()
    decomp_options.grabFromProgram(current_program)

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
    with open(current_function.getName() +'/variable_info.json', 'w') as outfile:
        json.dump(variable_info, outfile, indent=4)

    print("Variable information written to variable_info.json")


# Function to get the highlighted text from the decompile panel in Ghidra
# def get_highlighted_text():
#     currentProgram = getCurrentProgram()
#     decompiler = DecompInterface()
#     decompiler.openProgram(currentProgram)

#     highlighted_text = currentLocation.getDecompile().getCCodeMarkup()
#     # highlight1 = state.getCurrentHighlight().toString()
#     # print("code decompile")
#     # # print(decompiler.decompileFunction(currentLocation, 5, monitor))
#     # print("highlighted text")
#     # print(highlight1)
#     return highlighted_text


# recompiled_code = get_highlighted_text()
# if recompiled_code:
#     PROMPT = (
#             "Please analyze the following recompiled code from Ghidra and provide a "
#             "summary of its functionality. Include information about the main "
#             "functions and important variables. Give the name of the function in at the start in the format"
# 	    "'function=FUNCTION_NAME'"
#             "Rewrite the code, changing the variable names to have more meaning,"
#             "also apply standard coding procedures, format the code to look good."
#             "\n\nRecompiled code:\n\n" + str(recompiled_code) + "\n\nAnalysis:"
#     )

# ENGINE = "text-davinci-003"

# MAX_TOKENS = 2048


# def openai_query(prompt=PROMPT, temperature=0.19, max_tokens=MAX_TOKENS, engine=ENGINE):
#     data = {
#         "model": engine,
#         "prompt": prompt,
#         "max_tokens": max_tokens,
#         "temperature": temperature
#     }
#     endpoint_url = "api.openai.com/v1/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer {openai_api_key}".format(openai_api_key=api_key)
#     }
#     connection = httplib.HTTPSConnection("api.openai.com")
#     json_req_data = json.dumps(data)
#     connection.request("POST", "/v1/completions", json_req_data, headers)
#     connection_response = connection.getresponse()
#     response_data = connection_response.read()
#     connection.close()
#     parsed_data = json.loads(response_data)
#     logging.info("OpenAI request succeeded!")
#     logging.info("Response: {data}".format(data=parsed_data))
#     return parsed_data


# def format_response(api_response, max_width=80):
#     # # Pull function name
#     # functino
#     # Split the response into sentences
#     sentences = re.split('(?<=[.!?]) +', api_response)

#     # Initialize the formatted response string
#     formatted_response = ""

#     # Iterate through the sentences, wrapping and adding them to the formatted response
#     for sentence in sentences:
#         wrapped_sentence = textwrap.fill(sentence, width=max_width)
#         formatted_response += wrapped_sentence + "\n\n"

#     return "\n" + formatted_response.strip() + "\n"


# response = openai_query()
# result_text = response['choices'][0]['text']
# print("Prompt:\n\n"+PROMPT)
# print(result_text)

# append results to the end of a file for future use
#get file path for file containing the executable - results are stored in the same folder
# cwd = currentProgram.getExecutablePath()
# name_size = len(currentProgram.getName())
# filepath = cwd[:-(name_size)]

# get_highlighted_text()
with open(filepath + "GhidraPT/results.txt", 'a+') as file:
    file.write("Run at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    #file.write(result_text)
    file.write("\n\n---------------------------\n\n")
get_called_functions()
get_function_names()
get_variables_in_function()
get_JSON_variables()
# append all functions together - running the script multiple times on the same function will add that function multiple times to the file
# function = re.search("Rewritten code:\\n\\n+(.*)$", result_text).group(1)
# print(function)
# with open(filepath + "functions.c", "a+") as file:
#     file.write(function)


# sort by function name, or have one file that compiles all the rewritten functions together?
