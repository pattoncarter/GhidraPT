# @Author: Carter Patton and Daxton Gilliam
# @Functionality: This script utilizes chatGPT to analyze the highlighted recompiled code given by Ghidra.
import json
import re
import textwrap
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
from ghidra.program.flatapi import FlatProgramAPI
import json
import logging
import httplib
import os
from datetime import datetime

# Set your API key
api_key = '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'

# setting up writing to file
cwd = currentProgram.getExecutablePath()
name_size = len(currentProgram.getName())
filepath = cwd[:-(name_size)]
fm = currentProgram.getFunctionManager()

# setting up FlatProgram
# state = getState()
# program = state.getCurrentProgram()
# fp = FlatProgramAPI(program)
# fd = FlatDecompilerAPI(fp)

# TODO: make file for all folders to go into, rn errno 22 for inaccess, at
# to run right now, make GhidraPT folder in project folder
# os.mkdir(filepath + "GhidraPT")

#### INFORMATION GATHERING HELPER FUNCTIONS ####

# adds all function names for program to a text file
# TODO: filter out thunk functions
def get_function_names():
    fnc = getFirstFunction()
    with open(filepath + "GhidraPT/functionNames.txt", 'w') as file:
        while fnc is not None:
            if not fnc.isThunk():
                file.write(fnc.getName() + '\n')
            fnc = getFunctionAfter(fnc)

# returns all functions the current function (at the current address) calls
# currently rewrites file every time it's run, so it's specific to the function in the file
def get_called_functions():
    fnc = fm.getFunctionContaining(currentAddress)
    with open(filepath + "GhidraPT/functionsCalledBy - " + fnc.getName() + ".txt", 'w') as file:
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
    with open(filepath + "GhidraPT/functionsCalling - " + fnc.getName() + ".txt", 'w') as file:
        all_fncs = fnc.getCallingFunctions(monitor)
        for f in all_fncs:
            file.write(f.toString() + '\n')

# return all variables in the current function
# NOTE: gets the local variable names, not meaningful names
# tried to get from decompile, however it outs in a string, so there's not a parser for fncs in a string
def get_variables_in_function():
    fnc = getFunctionContaining(currentAddress)
    with open(filepath + "GhidraPT/variables - " + fnc.getName() + ".txt", 'w') as file:
        all_vars = fnc.getVariables(None)
        for v in all_vars:
            file.write(v.getName() + '\n')

# writes the global namespace to a file
# NOTE: how helpful is this in the grand scheme of things?
# program wide, so it rewrites every time it's called in order to avoid duplicates
def get_namespaces():
    namespaces = getCurrentProgram().getNamespaceManager().getGlobalNamespace()
    with open(filepath + "GhidraPT/namespaces.txt", 'w') as file:
        file.write(namespaces)

# Function to get the highlighted text from the decompile panel in Ghidra
def get_highlighted_text():
    # get highlighted text
    # decompile that highlighted text?
    # currentProgram = getCurrentProgram()
    # currhighlight = getState().getCurrentHighlight()
    # testhigh = getState().getCurrentHighlight().iterator()
    # print("current highlight")
    # print(currhighlight.toString())
    # for i in testhigh:
        # print(i)
    # print("current highlight")
    # print(currhighlight.toString())
    # print(currhighlight)
    # decompiler = FlatDecompilerAPI()
    # decompiler.openProgram(currentProgram)
    # fnc = getFunctionContaining(currentAddress)
    # print(fd.getDecompiler().decompileFunction(fnc, 5, monitor))

    # highlighted_text = currentLocation.getDecompile()
    # highlight1 = state.getCurrentHighlight().toString()
    # print("code decompile")
    # # print(decompiler.decompileFunction(currentLocation, 5, monitor))
    # print("highlighted text")
    # print(highlight1)
    # return highlighted_text
    currentProgram = getCurrentProgram()
    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)

    highlighted_text = currentLocation.getDecompile().getCCodeMarkup()
    return highlighted_text


recompiled_code = get_highlighted_text()
if recompiled_code:
    PROMPT = (
            "Please analyze the following recompiled code from Ghidra and provide a "
            "summary of its functionality. Include information about the main "
            "functions and important variables. Give the name of the function in at the start in the format"
	    "'function=FUNCTION_NAME'"
            "Rewrite the code, changing the variable names to have more meaning,"
            "also apply standard coding procedures, format the code to look good."
            "\n\nRecompiled code:\n\n" + str(recompiled_code) + "\n\nAnalysis:"
    )

ENGINE = "text-davinci-003"

MAX_TOKENS = 2048


def openai_query(prompt=PROMPT, temperature=0.19, max_tokens=MAX_TOKENS, engine=ENGINE):
    data = {
        "model": engine,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    endpoint_url = "api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_api_key}".format(openai_api_key=api_key)
    }
    connection = httplib.HTTPSConnection("api.openai.com")
    json_req_data = json.dumps(data)
    connection.request("POST", "/v1/completions", json_req_data, headers)
    connection_response = connection.getresponse()
    response_data = connection_response.read()
    connection.close()
    parsed_data = json.loads(response_data)
    logging.info("OpenAI request succeeded!")
    logging.info("Response: {data}".format(data=parsed_data))
    return parsed_data


def format_response(api_response, max_width=80):
    # # Pull function name
    # functino
    # Split the response into sentences
    sentences = re.split('(?<=[.!?]) +', api_response)

    # Initialize the formatted response string
    formatted_response = ""

    # Iterate through the sentences, wrapping and adding them to the formatted response
    for sentence in sentences:
        wrapped_sentence = textwrap.fill(sentence, width=max_width)
        formatted_response += wrapped_sentence + "\n\n"

    return "\n" + formatted_response.strip() + "\n"


# response = openai_query()
# result_text = response['choices'][0]['text']
result_text = "didn't run chatGPT"
print("Prompt:\n\n"+PROMPT)
print(result_text)

get_function_names()
# write results to file
with open(filepath + "GhidraPT/results.txt", 'a+') as file:
    file.write("Run at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    file.write(result_text)
    file.write("\n\n---------------------------\n\n")


# sort by function name, or have one file that compiles all the rewritten functions together?

