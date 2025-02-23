max_value = (49, 49, 49)

def crop_matrix(matrix, max_pos, target_size, new_center):

    start = [max(0, pos - (new_center - 1)) for pos in max_pos]
    end = [start[i] + size for i, size in enumerate(target_size)]
    for i in range(len(end)):
        if end[i] > matrix.shape[i]:
            end[i] = matrix.shape[i]
            start[i] = end[i] - target_size[i]
            start[i] = max(0, start[i])  

    return matrix[start[0]:end[0], start[1]:end[1], start[2]:end[2]]

def do_transform(image_array):
    target_size = (10, 99, 99)  
    new_center = 5              
    cropped_matrix = crop_matrix(image_array, max_value, target_size, new_center)
    print(cropped_matrix.shape)
    return cropped_matrix