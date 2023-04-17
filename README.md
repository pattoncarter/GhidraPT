# The Data Manager
The Ghidra Data Manager is a tool for collecting and organizing data from throughout a file in order to provide context for API calls outside of Ghidra.
![image](https://user-images.githubusercontent.com/83371509/232357833-d7bd8542-afd6-4e54-a315-773cfd73afad.png)
![image](https://user-images.githubusercontent.com/83371509/232357847-710ffb85-1d48-4c96-b0df-3dc251e8f0d7.png)


## Usage
The Data Manager will scan through your file and create data tables with the selected values for selected functions. These values include variable names and types within the functions, all of the functions in the file, what functions are called by a specific function, what functions call a specific function, and what functions are recursive within the file. This can all be accessed through a GUI that is executed by the script. Within this GUI you can select what funcitons to examine and what about them you'd like to see. We also have the option for you to export all of this data in JSON format to a file of your naming convention. These files will be stored within your GhidraPT foler wherver your executable is housed.

## Executable Placement
This script is meant to be run on an executable within a folder that has a subfolder named GhirdaPT. To complete this process follow these steps:
- Create a folder somewhere on your machine that will house the executable which you will be analyzing. 
- Move your executable to this folder. 
- Within this folder create a subfolder called GhidraPT
- In your Ghidra project, import your executable from its current location.

NOTE: If your executable was already imported into your Ghidra project, you need to create the GhidraPT folder wherever the executable is currently housed. If the GhidraPT folder and the executable are not within the same directory, you will get permission issues.

## Installation
- Download the latest version of the DataManager.py file.
- Display the Script Manager within Ghidra
- Click the three dots list in the top right corner to display the list of script locations.
- Click the green + to add a new location.
- Find the location of the DataManager.py file and select it.
- Find the script within the script manager to run it on your project.

# GhidraPT
This is a Ghidra script written in Python that takes decompiled functions and summarizes their purpose via ChatGPT's API.

The Ghidra-ChatGPT Script is a script for the Ghidra reverse engineering tool that integrates the ChatGPT language model in order to gain more insight into code. ChatGPT is an Artificial Intelligence (AI) model that is capable of generating text based on prompts given to it. By integrating ChatGPT into Ghidra, you can get AI-generated insights about the code you're analyzing, helping you to understand the code more deeply and quickly.

## Installation

To install the GhidraPT script, simply download the latest release from the releases page and extract it into the Ghidra scripts directory. You can then launch Ghidra and use the script from the scripts menu.

## Usage

Once you have the GhidraPT script installed, you can use it to generate AI-generated insights about the code you're analyzing. Simply highlight the code you're interested in and run the GhidraPT.py script from the scripts menu. From there, you can see the interpretation of the code + a reinterpretation of the function's variables to contextualized names within the function. This will be displayed in the Ghidra console. Functionality for exporting the function's description and reformatted code is coming in the future.

