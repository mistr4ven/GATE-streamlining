import numpy as np   

def do_transform(image_array):
    print(image_array.shape)
    cropped_image_array = image_array[:, :, 375:]
    print(cropped_image_array.shape)
    return cropped_image_array 
