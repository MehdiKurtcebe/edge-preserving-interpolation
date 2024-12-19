import numpy as np

def is_in_bounds(x, y, rows, cols):
    return x >= 0 and x < rows and y >= 0 and y < cols


def diagonals(out: list, x: int, y: int):
    rows = len(out)
    cols = len(out[0])
    
    diag_ul = out[x - 1][y - 1] if is_in_bounds(x - 1, y - 1, rows, cols) else [0, 0, 0]
    diag_ur = out[x - 1][y + 1] if is_in_bounds(x - 1, y + 1, rows, cols) else [0, 0, 0]
    diag_dl = out[x + 1][y - 1] if is_in_bounds(x + 1, y - 1, rows, cols) else [0, 0, 0]
    diag_dr = out[x + 1][y + 1] if is_in_bounds(x + 1, y + 1, rows, cols) else [0, 0, 0]
    
    dD_1 = [abs(x - y) for x, y in zip(diag_ul, diag_dr)]
    dD_2 = [abs(x - y) for x, y in zip(diag_ur, diag_dl)]
    dS_1 = [x + y for x, y in zip(diag_ul, diag_dr)]
    dS_2 = [x + y for x, y in zip(diag_ur, diag_dl)]
    
    return dD_1, dD_2, dS_1, dS_2


def inverse_gradient_weight(dD_1, dD_2):
    W = [0, 0, 0]
    for i in range(3):
        if dD_1[i] == dD_2[i] == 0:
            W[i] = 0.5
        elif dD_1[i] > dD_2[i]:
            W[i] = dD_2[i] / (dD_1[i] + dD_2[i])
        else:
            W[i] = dD_1[i] / (dD_1[i] + dD_2[i])
    
    return W
    
    
def weight_near_far(P):
    W_N = (1 / 2) * (P / (P + 2))
    W_F = (1 / 2) * (1 / (P + 2))
    return W_N, W_F


# image is bgr
def edge_preserving_interpolation(image: np.ndarray, P: int):
    rows = image.shape[0]
    cols = image.shape[1]
    out = [[[255, 255, 255] for _ in range(2 * cols)] for _ in range(2 * rows)]
    
    # TODO: add affine transformation
    for i in range(rows):
        for j in range(cols):
            out[(2 * i) + 1][(2 * j) + 1] = image[i][j]
            
    for i in range(rows):
        for j in range(cols):
            dD_1, dD_2, dS_1, dS_2 = diagonals(out, 2 * i, 2 * j)
            W = inverse_gradient_weight(dD_1, dD_2)
            out[2 * i][2 * j] = [(W[i] * dS_1[i] + (1 - W[i]) * dS_2[i]) / 2 for i in range(3)]

    W_near, W_far = weight_near_far(P)
    for i in range(rows):
        for j in range(cols):
            x = 2 * i + 1 # odd
            y = 2 * j # even
            nbor_l = out[x][y - 1] if is_in_bounds(x, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_r = out[x][y + 1] if is_in_bounds(x, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_ul = out[x - 2][y - 1] if is_in_bounds(x - 2, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_ur = out[x - 2][y + 1] if is_in_bounds(x - 2, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_dl = out[x + 2][y - 1] if is_in_bounds(x + 2, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_dr = out[x + 2][y + 1] if is_in_bounds(x + 2, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            out[x][y] = [(W_near * (nbor_l[i] + nbor_r[i])) + (W_far * (nbor_ul[i] + nbor_ur[i] + nbor_dl[i] + nbor_dr[i])) for i in range(3)]
            
            x = 2 * i # even
            y = 2 * j + 1 # odd
            nbor_l = out[x][y - 1] if is_in_bounds(x, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_r = out[x][y + 1] if is_in_bounds(x, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_ul = out[x - 2][y - 1] if is_in_bounds(x - 2, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_ur = out[x - 2][y + 1] if is_in_bounds(x - 2, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_dl = out[x + 2][y - 1] if is_in_bounds(x + 2, y - 1, 2 * rows, 2 * cols) else [0, 0, 0]
            nbor_dr = out[x + 2][y + 1] if is_in_bounds(x + 2, y + 1, 2 * rows, 2 * cols) else [0, 0, 0]
            out[x][y] = [(W_near * (nbor_l[i] + nbor_r[i])) + (W_far * (nbor_ul[i] + nbor_ur[i] + nbor_dl[i] + nbor_dr[i])) for i in range(3)]
            
    return out
            