# GhidraPT
This is a Ghidra script written in Python that takes decompiled functions and summarizes their purpose via ChatGPT's API.

The Ghidra-ChatGPT Script is a script for the Ghidra reverse engineering tool that integrates the ChatGPT language model in order to gain more insight into code. ChatGPT is an Artificial Intelligence (AI) model that is capable of generating text based on prompts given to it. By integrating ChatGPT into Ghidra, you can get AI-generated insights about the code you're analyzing, helping you to understand the code more deeply and quickly.

Installation

To install the GhidraPT script, simply download the latest release from the releases page and extract it into the Ghidra scripts directory. You can then launch Ghidra and use the script from the scripts menu.

Usage

Once you have the GhidraPT script installed, you can use it to generate AI-generated insights about the code you're analyzing. Simply highlight the code you're interested in and run the GhidraPT.py script from the scripts menu. From there, you can see the interpretation of the code + a reinterpretation of the function's variables to contextualized names within the function. This will be displayed in the Ghidra console. Functionality for exporting the function's description and reformatted code is coming in the future.
