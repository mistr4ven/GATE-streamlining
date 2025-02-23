import sys
import os
import importlib
import importlib.util
import SimpleITK as sitk


def transform_np(transform_argument):

    print(transform_argument['Transform_input_file'])
    # check file path
    if not (os.path.isfile(transform_argument['Transform_input_file']) or transform_argument['Transform_input_file'].lower().endswith('.mhd')):
        raise Exception('Input file does not exist or is not a .mhd file! Please specify a correct input path.')
    
    # get image from file path
    image = sitk.ReadImage(transform_argument['Transform_input_file'])

    # get image as array from file
    if image is None:
        raise Exception('Input reading failed!')
    image_array = sitk.GetArrayFromImage(image)

    # check file path
    if not (os.path.isfile(transform_argument['Transform_operations_file']) or transform_argument['Transform_operations_file'].lower().endswith('.py')):
        raise Exception('Transform operations file does not exist or is not a python file! Please specify a correct file for the transform operations to be done.')

    # get module name from transform path
    module_name = os.path.splitext(os.path.basename(transform_argument['Transform_operations_file']))[0]
    
    # load module from file 
    spec = importlib.util.spec_from_file_location(module_name, transform_argument['Transform_operations_file'])
    if spec is None or spec.loader is None:
        raise Exception('Reading transform module failed!')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # check for the function
    if not hasattr(module, 'do_transform'):
        raise Exception('do_transform function not specified in transform file!')

    transform_function = getattr(module, 'do_transform')

    # call function
    transformed_image_array = transform_function(image_array)

    ## Write the transformed_image to the specified output file
    if not transform_argument['Transform_output_file'].lower().endswith('.mhd'):
        raise Exception('Output file is not a .mhd file! Please specify a correct output path.')

    if os.path.isfile(transform_argument['Transform_output_file']):
        user_choice = input(f'{transform_argument['Transform_output_file']} already exists! Do you want to overwrite the file (y/n, default: yes)? ').strip().lower()
        if user_choice == 'n':
            transform_argument['Transform_output_file'] = input('Enter the new path for the .mhd file: ')


    try:
        # get the image from the transformed array 
        transformed_image = sitk.GetImageFromArray(transformed_image_array)
        # transfer the metadata from image to transformed_image
        transformed_image.SetOrigin(image.GetOrigin())
        transformed_image.SetSpacing(image.GetSpacing())
        transformed_image.SetDirection(image.GetDirection())
    except Exception as e:
        print(f'A problem with getting transformed image from array or the metadata from the original image occurred: {e}')
        exit()

    try:
        sitk.WriteImage(transformed_image, transform_argument['Transform_output_file'])
    except Exception as e:
        print(f'A problem with writing the transformed_image to the output path occurred: {e}')
        exit()

        
def transform_image(transform_argument):
    # check file path
    if not (os.path.isfile(transform_argument['Transform_input_file']) or transform_argument['Transform_input_file'].lower().endswith('.mhd')):
        raise Exception('Input file does not exist or is not a .mhd file! Please specify a correct input path.')
    
    # get image from file path
    image = sitk.ReadImage(transform_argument['Transform_input_file'])

    if image is None:
        raise Exception('Input reading failed!')

    # check file path
    if not (os.path.isfile(transform_argument['Transform_operations_file']) or transform_argument['Transform_operations_file'].lower().endswith('.py')):
        raise Exception('Transform operations file does not exist or is not a python file! Please specify a correct file for the transform operations to be done.')

    # get module name from transform path
    module_name = os.path.splitext(os.path.basename(transform_argument['Transform_operations_file']))[0]
    
    # load module from file 
    spec = importlib.util.spec_from_file_location(module_name, transform_argument['Transform_operations_file'])
    if spec is None or spec.loader is None:
        raise Exception('Reading transform module failed!')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # check for the function
    if not hasattr(module, 'do_transform'):
        raise Exception('do_transform function not specified in transform file!')

    transform_function = getattr(module, 'do_transform')

    # call function
    transformed_image = transform_function(image)

    ## Write the transformed_image to the specified output file
    if not transform_argument['Transform_output_file'].lower().endswith('.mhd'):
        raise Exception('Output file is not a .mhd file! Please specify a correct output path.')

    if os.path.isfile(transform_argument['Transform_output_file']):
        user_choice = input(f'{transform_argument['Transform_output_file']} already exists! Do you want to overwrite the file (y/n, default: yes) ?').strip().lower()
        if user_choice == 'n':
            transform_argument['Transform_output_file'] = input('Enter the new path for the .mhd file: ')

    try:
        sitk.WriteImage(transformed_image, transform_argument['Transform_output_file'])
    except Exception as e:
        print(f'A problem with writing the transformed_image to the output path occurred: {e}')
        exit()

