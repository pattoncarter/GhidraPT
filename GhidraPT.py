import openai
import re
import textwrap
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.app.plugin.core.decompile import DecompilePlugin

# Set your API key
openai.api_key = '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'


# Function to call ChatGPT API
def analyze_assembly(recompiled_code):
    prompt = (
        """Please analyze the following recompiled code from Ghidra and provide a 
        summary of its functionality. Include information about the main 
        functions, important variables, and any potential security risks or 
        optimization opportunities you can identify. Also, if possible, 
        speculate on the purpose of the program or the context in which it might be used.\n\n
        Recompiled code:\n\n{recompiled_code}\n\nAnalysis:""".format(recompiled_code=recompiled_code)
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def format_response(response, max_width=80):
    # Split the response into sentences
    sentences = re.split('(?<=[.!?]) +', response)

    # Initialize the formatted response string
    formatted_response = ""

    # Iterate through the sentences, wrapping and adding them to the formatted response
    for sentence in sentences:
        wrapped_sentence = textwrap.fill(sentence, width=max_width)
        formatted_response += wrapped_sentence + "\n\n"

    return formatted_response.strip()
# Function to get the highlighted text from the decompile panel in Ghidra
def get_highlighted_text():
    currentProgram = getCurrentProgram()
    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)


    highlighted_text = currentLocation.getDecompile().getCCodeMarkup()
    return highlighted_text

if __name__ == "__main__":
    analysis = analyze_assembly(get_highlighted_text())
    print("Analysis of the assembly code:")
    print(format_response(analysis))



