import numpy as np   

def do_transform(image_array):
    print(image_array.shape)
    start_index = 450
    end_index = 550
    cropped_image_array = image_array[start_index:end_index, start_index:end_index, start_index:end_index]
    print(cropped_image_array.shape)
    return cropped_image_array 
