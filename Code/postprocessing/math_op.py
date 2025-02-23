import sys
import os
import importlib
import importlib.util
import SimpleITK as sitk
import numpy as np


def math_op(math_argument):
    # check file path
    if not (os.path.isfile(math_argument['Math_input_file']) or math_argument['Math_input_file'].lower().endswith('.mhd')):
        raise Exception('Input file does not exist or is not a .mhd file! Please specify a correct input path.')
    
    # get image from file path
    image = sitk.ReadImage(math_argument['Math_input_file'])
    if image is None:
        raise Exception('Input reading failed!')
    image_array = sitk.GetArrayFromImage(image)

    # check file path
    if not (os.path.isfile(math_argument['Math_operations_file']) or math_argument['Math_operations_file'].lower().endswith('.py')):
        raise Exception('Transform operations file does not exist or is not a python file! Please specify a correct file for the transform operations to be done.')


    # get module name from math_op path
    module_name = os.path.splitext(os.path.basename(math_argument['Math_operations_file']))[0]
    
    # load module from file 
    spec = importlib.util.spec_from_file_location(module_name, math_argument['Math_operations_file'])
    if spec is None or spec.loader is None:
        raise Exception('Reading transform module failed!')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # check for the function
    if not hasattr(module, 'do_math'):
        raise Exception('do_math function not specified in transform file!')

    math_function = getattr(module, 'do_math')

    # call function
    math_array = math_function(image_array)

    ## Write the transformed_image to the specified output file
    if not math_argument['Math_output_file'].lower().endswith('.npz'):
        raise Exception('Output file is not a .npz file! Please specify a correct output path.')

    if os.path.isfile(math_argument['Math_output_file']):
        user_choice = input(f'{math_argument['Math_output_file']} already exists! Do you want to overwrite the file (y/n, default: yes)? ').strip().lower()
        if user_choice == 'n':
            math_argument['Math_output_file'] = input('Enter the new path for the .npz file: ')


    try:
        np.savez(math_argument['Math_output_file'], **math_array)
    except Exception as e:
        print(f'A problem with writing the math_image to the output path occurred: {e}')
        exit()

        

