# @Author: Carter Patton and Daxton Gilliam
# @Functionality: This script utilizes chatGPT to analyze the highlighted recompiled code given by Ghidra.

import json
import re
import textwrap
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
import json
import logging
import httplib
import os
from datetime import datetime

# Set your API key
api_key = 


# Function to get the highlighted text from the decompile panel in Ghidra
def get_highlighted_text():
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
    # Pull function name
    functino
    # Split the response into sentences
    sentences = re.split('(?<=[.!?]) +', api_response)

    # Initialize the formatted response string
    formatted_response = ""

    # Iterate through the sentences, wrapping and adding them to the formatted response
    for sentence in sentences:
        wrapped_sentence = textwrap.fill(sentence, width=max_width)
        formatted_response += wrapped_sentence + "\n\n"

    return "\n" + formatted_response.strip() + "\n"


response = openai_query()
result_text = response['choices'][0]['text']
print("Prompt:\n\n"+PROMPT)
print(result_text)

# append results to the end of a file for future use
#get file path for file containing the executable - results are stored in the same folder
cwd = currentProgram.getExecutablePath()
name_size = len(currentProgram.getName())
filepath = cwd[:-(name_size)]
with open(filepath + "results.txt", 'a+') as file:
    file.write("Run at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    file.write(result_text)
    file.write("\n\n---------------------------\n\n")

# append all functions together - running the script multiple times on the same function will add that function multiple times to the file
# function = re.search("Rewritten code:\\n\\n+(.*)$", result_text).group(1)
# print(function)
# with open(filepath + "functions.c", "a+") as file:
#     file.write(function)


# sort by function name, or have one file that compiles all the rewritten functions together?
