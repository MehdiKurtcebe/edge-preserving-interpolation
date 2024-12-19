import numpy as np

def is_in_bounds(x, y, rows, cols):
    return x >= 0 and x < rows and y >= 0 and y < cols


def diagonals(out: list, x: int, y: int):
    rows = len(out)
    cols = len(out[0])
    
    diag_ul = out[x - 1][y - 1] if is_in_bounds(x - 1, y - 1, rows, cols) else 0
    diag_ur = out[x - 1][y + 1] if is_in_bounds(x - 1, y + 1, rows, cols) else 0
    diag_dl = out[x + 1][y - 1] if is_in_bounds(x + 1, y - 1, rows, cols) else 0
    diag_dr = out[x + 1][y + 1] if is_in_bounds(x + 1, y + 1, rows, cols) else 0
    
    dD_1 = abs(diag_ul - diag_dr)
    dD_2 = abs(diag_ur - diag_dl)
    dS_1 = diag_ul + diag_dr
    dS_2 = diag_ur + diag_dl
    
    return dD_1, dD_2, dS_1, dS_2


def inverse_gradient_weight(dD_1, dD_2):
    if dD_1 == dD_2 == 0:
        return 0.5
    elif dD_1 > dD_2:
        return dD_2 / (dD_1 + dD_2)
    else:
        return dD_1 / (dD_1 + dD_2)
    
    
def weight_near_far(P):
    W_N = (1 / 2) * (P / (P + 2))
    W_F = (1 / 2) * (1 / (P + 2))
    return W_N, W_F


# image is grayscale
def edge_preserving_interpolation(image: np.ndarray, P: int):
    rows = image.shape[0]
    cols = image.shape[1]
    out = [[255 for _ in range(2 * cols)] for _ in range(2 * rows)]
    
    # TODO: add affine transformation
    for i in range(rows):
        for j in range(cols):
            out[(2 * i) + 1][(2 * j) + 1] = image[i][j]
            
    for i in range(rows):
        for j in range(cols):
            dD_1, dD_2, dS_1, dS_2 = diagonals(out, 2 * i, 2 * j)
            W = inverse_gradient_weight(dD_1, dD_2)
            out[2 * i][2 * j] = (W * dS_1 + (1 - W) * dS_2) / 2

    W_near, W_far = weight_near_far(P)
    for i in range(rows):
        for j in range(cols):
            x = 2 * i + 1 # odd
            y = 2 * j # even
            nbor_l = out[x][y - 1] if is_in_bounds(x, y - 1, 2 * rows, 2 * cols) else 0
            nbor_r = out[x][y + 1] if is_in_bounds(x, y + 1, 2 * rows, 2 * cols) else 0
            nbor_ul = out[x - 2][y - 1] if is_in_bounds(x - 2, y - 1, 2 * rows, 2 * cols) else 0
            nbor_ur = out[x - 2][y + 1] if is_in_bounds(x - 2, y + 1, 2 * rows, 2 * cols) else 0
            nbor_dl = out[x + 2][y - 1] if is_in_bounds(x + 2, y - 1, 2 * rows, 2 * cols) else 0
            nbor_dr = out[x + 2][y + 1] if is_in_bounds(x + 2, y + 1, 2 * rows, 2 * cols) else 0
            out[x][y] = (W_near * (nbor_l + nbor_r)) + (W_far * (nbor_ul + nbor_ur + nbor_dl + nbor_dr))
            
            x = 2 * i # even
            y = 2 * j + 1 # odd
            nbor_l = out[x][y - 1] if is_in_bounds(x, y - 1, 2 * rows, 2 * cols) else 0
            nbor_r = out[x][y + 1] if is_in_bounds(x, y + 1, 2 * rows, 2 * cols) else 0
            nbor_ul = out[x - 2][y - 1] if is_in_bounds(x - 2, y - 1, 2 * rows, 2 * cols) else 0
            nbor_ur = out[x - 2][y + 1] if is_in_bounds(x - 2, y + 1, 2 * rows, 2 * cols) else 0
            nbor_dl = out[x + 2][y - 1] if is_in_bounds(x + 2, y - 1, 2 * rows, 2 * cols) else 0
            nbor_dr = out[x + 2][y + 1] if is_in_bounds(x + 2, y + 1, 2 * rows, 2 * cols) else 0
            out[x][y] = (W_near * (nbor_l + nbor_r)) + (W_far * (nbor_ul + nbor_ur + nbor_dl + nbor_dr))
            
    return out
            