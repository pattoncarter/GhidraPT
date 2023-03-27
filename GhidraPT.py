import json

import re
import textwrap
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin
import json
import logging
import httplib

# Set your API key
api_key = 'API-Key'


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
            "functions and important variables."
            "Rewrite the code, changing the variable names to have more meaning,"
            "also apply standard coding procedures."
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
    # The open ai api link is "https://api.openai.com/v1/completions"
    host = "api.openai.com"
    path = "/v1/completions"
    key_file = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {openai_api_key}".format(openai_api_key=api_key)
    }
    httpconn = httplib.HTTPSConnection(host)
    json_req_data = json.dumps(data)
    httpconn.request("POST", path, json_req_data, key_file)
    httpconn_response = httpconn.getresponse()
    json_data = httpconn_response.read()
    httpconn.close()
    data = json.loads(json_data)
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


response = openai_query()
result_text = response['choices'][0]['text']
print(result_text)
