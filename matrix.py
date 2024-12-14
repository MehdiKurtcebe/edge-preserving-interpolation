# NOTE:
# a 1 by n matrix should be in form [[1, 2, 3, ...]]
# the following form is NOT accepted: [1, 2, 3, ...]

def summation(a: list, b: list) -> list:
    return [[x + y for x, y in zip(rowa, rowb)] for rowa, rowb in zip(a, b)]


def multiply(a: list | int | float, b: list) -> list:
    if type(a) is int or type(a) is float:
        return [[a * x for x in row] for row in b]

    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a: list) -> list:
    return list(map(list, zip(*a)))


def determinant_2x2(a: list) -> float:
    return (a[0][0] * a[1][1]) - (a[0][1] * a[1][0])


def determinant_3x3(a: list) -> float:
    return (
        (a[0][0] * a[1][1] * a[2][2])
        + (a[0][1] * a[1][2] * a[2][0])
        + (a[0][2] * a[1][0] * a[2][1])
        - (a[0][2] * a[1][1] * a[2][0])
        - (a[0][0] * a[1][2] * a[2][1])
        - (a[0][1] * a[1][0] * a[2][2])
    )
    
    
def inverse_3x3(a: list) -> list:
    det = determinant_3x3(a)
    if det == 0:
        return None

    adj = [
        [determinant_2x2([[a[1][1], a[1][2]], [a[2][1], a[2][2]]]), determinant_2x2([[a[0][2], a[0][1]], [a[2][2], a[2][1]]]), determinant_2x2([[a[0][1], a[0][2]], [a[1][1], a[1][2]]])],
        [determinant_2x2([[a[1][2], a[1][0]], [a[2][2], a[2][0]]]), determinant_2x2([[a[0][0], a[0][2]], [a[2][0], a[2][2]]]), determinant_2x2([[a[0][2], a[0][0]], [a[1][2], a[1][0]]])],
        [determinant_2x2([[a[1][0], a[1][1]], [a[2][0], a[2][1]]]), determinant_2x2([[a[0][1], a[0][0]], [a[2][1], a[2][0]]]), determinant_2x2([[a[0][0], a[0][1]], [a[1][0], a[1][1]]])]
    ]

    return multiply(1 / det, adj)