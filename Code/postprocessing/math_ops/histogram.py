import numpy as np

def do_math(image_array):
    histograms = {0: [], 1: [], 2: []}
    bins = {0: [], 1: [], 2: []}


    # Dimension 0: should be axial
    for i in range(image_array.shape[0]):
        hist, bin_edges = np.histogram(image_array[i, :, :].ravel(), bins=image_array.shape[0])
        histograms[0].append(hist)
        bins[0].append(bin_edges)
    
    # Dimension 1: should be coronal
    for i in range(image_array.shape[1]):
        hist, bin_edges = np.histogram(image_array[:, i, :].ravel(), bins=image_array.shape[1])
        histograms[1].append(hist)
        bins[1].append(bin_edges)
    
    # Dimension 2: should be sagittal
    for i in range(image_array.shape[2]):
        hist, bin_edges = np.histogram(image_array[:, :, i].ravel(), bins=image_array.shape[2])
        histograms[2].append(hist)
        bins[2].append(bin_edges)
    
    # return the data in a way that np.savez does not need to know about the structure of the data
    return {'histograms': histograms, 'bins': bins}
