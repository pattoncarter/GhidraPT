# GhidraPT
The Ghidra Data Manager is a tool for collecting and organizing data from throughout a file in order to provide context for API calls outside of Ghidra.

## Usage
The Data Manager will scan through your file and create data tables with the selected values for selected functions. These values include variable names and types within the functions, all of the functions in the file, what functions are called by a specific function, what functions call a specific function, and what functions are recursive within the file. This can all be accessed through a GUI that is executed by the script. Within this GUI you can select what functions to examine and what about them you'd like to see. We also have the option for you to export all of this data in JSON format to a file of your naming convention. These files will be stored within your GhidraPT folder wherever your executable is housed.

GhidraPT extends the data manager functionality to include an option for code analysis and suggested rewritten variable names using the ChatGPT API. ChatGPT is an Artificial Intelligence (AI) model that is capable of generating text based on prompts given to it. By integrating ChatGPT into Ghidra, you can get AI-generated insights about the code you're analyzing, helping you to understand the code more deeply and quickly.

## Installation
- Download the latest version of the GhidraPT.py file.
- Display the Script Manager within Ghidra
- Click the three dots list in the top right corner to display the list of script locations.
- Click the green + to add a new location.
- Find the location of the GhidraPT.py file and select it.
- Find the script within the script manager to run it on your project.
