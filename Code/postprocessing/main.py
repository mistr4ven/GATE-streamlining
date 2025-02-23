import sys
import os
from transform import transform_np, transform_image
from math_op import math_op
from interface import visual_interface
from xml_op import create_new_macro, read_macro_data

arguments = []

# Function to check if the user wants to use the visual interface or the command line interface based on the existence of command line arguments 
def commandline_arguments():
    # check, if command line arguments
    if len(sys.argv) == 2:
        # one Argument provided
        argument = sys.argv[1]  
        return argument
    elif len(sys.argv) > 2:        
        raise Exception("Too many arguments! Please only provide a macro file or no arguments for visual mode!")
    else:
        # No arguments provided -> visual mode
        print("Starting visual mode!")
        return None

# The text that is printed when the user calls the program with the -h or help argument
def write_help():
    print("Help:")
    print("Calling this program without an argument opens visual input mode.")
    print("Calling this program with a path to a macro file enabeles you to call your own macros. Please look at documentation to read more about macro files.")

# Function to interact with the user and get the input for the program
def do_input_interactions():
    global arguments
    try:
        # check if the user wants to use the visual interface or the command line interface. In case of the command line interface, the path to the macro file is returned
        commandline_input = commandline_arguments()
    except Exception as e:
        print(f"{e}")
        exit()
    if commandline_input == "h" or commandline_input == "help" or commandline_input == "-h":
        write_help()
        exit()
    elif commandline_input is None:
        try:
            # visual_arguments has the form {'data': window.data, 'xmlpath':window.xmlpath}
            # Visual Mode has been chosen
            visual_arguments = visual_interface()
            if visual_arguments is None:
                raise ValueError("Visual interface returned None")
            # get the data from the visual arguements for further program flow
            arguments = visual_arguments['data']
            # handle XML file creation
            xmlpath = visual_arguments['xmlpath']['XML_path'] if visual_arguments['xmlpath'] != '' else ''
            if xmlpath not in ('', None):
                if os.path.isfile(xmlpath):
                    user_choice = input(f'{xmlpath} already exists! Do you want to overwrite the file (y/n, default: yes)? ').strip().lower()
                    if user_choice == "n":
                        xmlpath = input("Enter the new path for the .xml file: ")

                create_new_macro(xmlpath, visual_arguments['data'])

        except Exception as e:
            print(f"A problem with visual mode occurred: {e}")
            exit()
    else:
        try:
            # The user has provided a macro file, read the data 
            arguments = read_macro_data(commandline_input)
        except Exception as e:
            print(f"An exception occurred while parsing the macro: {e}")

        
def main():
    global arguments
    # get the arguments either from a macro file or from the visual interface
    do_input_interactions()

    # for each branch in the arguments, check if the arguments are valid and execute transform. 
    ## If one is not provided, skip the branch
    for branch_argument in arguments:
        transform_arguments = branch_argument[0]
        if all(transform_arguments[key] != ('' and "" and None) for key in ['Transform_input_file', 'Transform_operations_file', 'Transform_output_file']):
            transform_np(transform_arguments)

    # for each branch in the arguments, check if the arguments are valid and execute do_math. 
    ## If one is not provided, skip the branch
    for branch_argument in arguments:
        math_arguments = branch_argument[1]
        if all(math_arguments[key] != ('' and "" and None)  for key in ['Math_input_file', 'Math_operations_file', 'Math_output_file']):
            math_op(math_arguments)
 
if __name__ == "__main__":
    main()
