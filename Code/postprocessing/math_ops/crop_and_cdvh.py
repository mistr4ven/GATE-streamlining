# Shape of an array: (1000, 1000, 1000)
# TOFO Drop this? would prefer resizing as a transform step 

import numpy as np

def do_math(image_array):
    start_index = 0
    end_index = 0
    cropped_image_array = image_array[start_index:end_index, start_index:end_index, start_index:end_index]

    flat_array = cropped_image_array.flatten()
    num_bins = 10000
    bin_edges = np.linspace(np.min(flat_array), np.max(flat_array), num_bins + 1)
    histogram, _ = np.histogram(flat_array, bins=bin_edges)
    return {'histogram': histogram, 'bins': bin_edges}

