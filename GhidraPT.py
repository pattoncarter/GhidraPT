import openai
import re
import textwrap

# Set your API key
openai.api_key = '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'


# Function to call ChatGPT API
def analyze_assembly(recompiled_code):
    prompt = (
        f"Please analyze the following recompiled code from Ghidra and provide a "
        f"summary of its functionality. Include information about the main "
        f"functions, important variables, and any potential security risks or "
        f"optimization opportunities you can identify. Also, if possible, "
        f"speculate on the purpose of the program or the context in which it might be used.\n\n"
        f"Recompiled code:\n\n{recompiled_code}\n\nAnalysis:"
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


if __name__ == "__main__":
    assembly_code = input("copy and paste assembly code here: ")
    analysis = analyze_assembly(assembly_code)
    print("Analysis of the assembly code:")
    print(format_response(analysis))
