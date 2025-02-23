import numpy as np 

def do_math(image_array):
    flat_image = image_array.flatten()
    sorted_image = np.sort(flat_image)
    cumsum_image = np.cumsum(sorted_image)

    return {'flat_image': flat_image, 'sorted_image': sorted_image, 'cumsum_image': cumsum_image}
