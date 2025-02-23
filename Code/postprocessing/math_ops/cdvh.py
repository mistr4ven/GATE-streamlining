import numpy as np

def do_math(image_array):
    flat_array = image_array.flatten()
    num_bins = 10000
    bin_edges = np.linspace(np.min(flat_array), np.max(flat_array), num_bins + 1)
    histogram, _ = np.histogram(flat_array, bins=bin_edges)
    return {'histogram': histogram, 'bins': bin_edges}

