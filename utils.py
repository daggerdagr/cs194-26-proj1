def trimAllSide(matr, size):
    return trimEachSide(matr, size, size, size, size)

def trimEachSide(matr, left = 0, right = 0, up = 0, down = 0):
    assert left >= 0 and right >= 0 and up >= 0 and down >= 0
    res = matr
    if up > 0:
        res = res[up:]
    if down > 0:
        res = res[:-1 * down]
    if left > 0:
        res = res[:, left:]
    if right > 0:
        res = res[:, :-1 * right]
    return res