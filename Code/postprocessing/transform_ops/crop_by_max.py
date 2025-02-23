max_value = (375, 375, 375)
# zero based indexing
## 101 -> 51
def crop_matrix(matrix, max_pos, target_size=100, new_center=50):
    start = [max(0, pos - (new_center - 1)) for pos in max_pos]
    end = [min(dim, pos + (target_size - new_center)) for pos, dim in zip(max_pos, matrix.shape)]
    
    return matrix[start[0]:end[0], start[1]:end[1], start[2]:end[2]]

def do_transform(image_array):
    cropped_matrix = crop_matrix(image_array, max_value)
    print(cropped_matrix.shape)
    return cropped_matrix 