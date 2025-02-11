import numpy as np
from skimage.transform import rescale
import skimage.io as skio
from enum import Enum

DEBUG = False
DEBUG2 = False

# match mode
class MatchMode(Enum):
    SSD = "ssd"
    NCC = "ncc"

# search mode
class SearchMode(Enum):
    NONP = "non-pyramid"
    PYR = "pyramid"

def padCut(mat, x, y, constant):

    finalMat = mat
    if abs(x) > mat.shape[1]:
        if x < 0:
            x = -1 * mat.shape[1]
        else:
            x = mat.shape[1]
    if abs(y) > mat.shape[0]:
        if y < 0:
            y = -1 * mat.shape[0]
        else:
            y = mat.shape[0]

    if x < 0:
        # cut left side of mat X times
        # add right side of mat X times
        shiftDistX = -1 * x

        finalMat = finalMat[:, shiftDistX:]
        padderMat = np.full((finalMat.shape[0], shiftDistX), constant)
        finalMat = np.hstack([finalMat, padderMat])
    elif x > 0:
        # cut right side of finalMat X times
        # add left side of finalMat X times
        shiftDistX = x

        finalMat = finalMat[:, :-shiftDistX]
        padderMat = np.full((finalMat.shape[0], shiftDistX), constant)
        finalMat = np.hstack([padderMat, finalMat])

    if y < 0:
        # cut top side of finalMat X times
        # add bottom side of finalMat X times
        shiftDistY = -1 * y

        finalMat = finalMat[shiftDistY:, :]
        padderMat = np.full((shiftDistY, finalMat.shape[1]), constant)
        finalMat = np.vstack([finalMat, padderMat])
    elif y > 0:
        # cut bottom side of finalMat X times
        # add top side of finalMat X times
        shiftDistY = y

        finalMat = finalMat[:-shiftDistY, :]
        padderMat = np.full((shiftDistY, finalMat.shape[1]), constant)
        finalMat = np.vstack([padderMat, finalMat])

    return finalMat

MIN_SIZE = 100

def fnSsd(mat1, mat2):
    return np.sum((mat2 - mat1) ** 2) / mat1.size

def fnNcc(mat1, mat2):
    return -1 * np.dot(mat2 / np.linalg.norm(mat2), mat1 / np.linalg.norm(mat1))

keywordToAlignFunction = {
    MatchMode.SSD: fnSsd,
    MatchMode.NCC: fnNcc
}

"""

def FN(mat1, mat2, alignKeyWord):

    if matrices is at the smallest possib level (2x2 OR our max depth level):
        [start algo]
        
        do align, get back the displacement coords
        return up the displacement coords
    else:
        [as in you need to go deeper recursion wise AND do something w the info gotten back]
        
        RESIZE_MAT1, RESIZE_MAT2 = 0.5x resized matrices
        RESULT = call FN w on RESIZE_MAT1 and RESIZE_MAT2
        
        NEW STARTING POSITION, RESULT * 2
        do align
        return displacement coords
        

"""

def alignMain(mode, alignFnKey, mat1, mat2, level = 4):
    if mode == SearchMode.NONP:
        displX, displY = align(alignFnKey, mat1, mat2)
    elif mode == SearchMode.PYR:
        displX, displY = helper(alignFnKey, mat1, mat2, level)
    else:
        raise Exception("unrecognizable mode: " + mode)
    print(displX, displY)
    res = padCut(mat1, displX, displY, 0)
    if DEBUG:
        printMeOut(mat2, ColorMode.G)
        printMeOut(res, ColorMode.R)
    return res, (displX, displY)

def helper(alignFnKey, mat1, mat2, level = 10):
    if level == 0 or mat1.shape[0] < MIN_SIZE or mat1.shape[1] < MIN_SIZE:
        return align(alignFnKey, mat1, mat2)
    else:
        resizeMat1 = rescale(mat1, 0.5)
        resizeMat2 = rescale(mat2, 0.5)

        result = helper(alignFnKey, resizeMat1, resizeMat2, level - 1)
        result2 = (result[0] * 2, result[1] * 2)


        if DEBUG2:
            print()
            print("++ RESULTS FOR", level, result, "++")

            printMeOut(padCut(mat1, result[0], result[1], 0), ColorMode.R)
            printMeOut(mat2, ColorMode.G)

            print("next step for ", result2)

        return align(alignFnKey, mat1, mat2, result2, (-5, 5))


def align(alignFnKey, mat1, mat2, center = (0, 0), displRange = (-30, 30)):

    assert mat1.size == mat2.size

    # matSize = mat1.size
    displRangeStart, displRangeEnd = displRange
    centerX, centerY = center
    vectMat2 = mat2.flatten()
    # print(vectMat2)

    curMin = 1
    displacements = ()

    for displX in range(displRangeStart, displRangeEnd):
        for displY in range(displRangeStart, displRangeEnd):
            newDisplX = displX + centerX
            newDisplY = displY + centerY
            shiftedMat1 = padCut(mat1, newDisplX, newDisplY, 0.5)
            vectShiftedMat1 = shiftedMat1.flatten()
            # matMask = vectShiftedMat1 != -1
            # maskedVect1 = vectShiftedMat1 # [matMask]

            result = keywordToAlignFunction[alignFnKey](vectMat2, vectShiftedMat1)

            if DEBUG:
                print()
                print("Result:", result)
                print("Current coord:", (newDisplX, newDisplY))

            if curMin > result:
                if DEBUG:
                    print("beat current min of", displacements, curMin)
                curMin = result
                displacements = (newDisplX, newDisplY)

                # if DEBUG:
                #     printMeOut(mat2, R, "mat2")
                #     shiftedMat1_SUB = padCut(mat1, displX + centerX, displY + centerY, 0)
                #     printMeOut(shiftedMat1_SUB, G, "possible mat1")

    return displacements

class ColorMode(Enum):
    B = "blue"
    R = "red"
    G = "green"

def printMeOut(mat1, mode, savePath = ""):
    empty = np.full(mat1.shape, 0)
    color_stack = [empty, empty, empty]
    if mode == ColorMode.R:
        color_stack[0] = mat1
    elif mode == ColorMode.G:
        color_stack[1] = mat1
    elif mode == ColorMode.B:
        color_stack[2] = mat1
    else:
        raise Exception("unrecognizable print mode", mode)

    im_out = np.dstack(color_stack)
    if savePath != "":
        skio.imsave(savePath, im_out)
    skio.imshow(im_out)
    skio.show()