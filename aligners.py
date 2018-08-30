import numpy as np

def padCut(mat, x, y, constant):
    finalMat = mat

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

SSD = "ssd"
NCC = "ncc"


def fnSsd(mat1, mat2):
    return np.sum((mat2 - mat1) ** 2) / mat1.size

def fnNcc(mat1, mat2):
    return -1 * np.dot(mat2 / np.linalg.norm(mat2), mat1 / np.linalg.norm(mat1))

keywordToAlignFunction = {
    SSD: fnSsd,
    NCC: fnNcc
}

def align(keyword, mat1, mat2):

    evaluatorTypes = {SSD, NCC}

    assert mat1.size == mat2.size

    # matSize = mat1.size
    displRangeStart = -15
    displRangeEnd = 15
    vectMat2 = mat2.flatten()
    # print(vectMat2)

    curMin = 1
    curMat = None
    displacements = ()

    for displX in range(displRangeStart, displRangeEnd):
        for displY in range(displRangeStart, displRangeEnd):
            shiftedMat1 = padCut(mat1, displX, displY, -1)
            vectShiftedMat1 = shiftedMat1.flatten()
            matMask = vectShiftedMat1 != -1
            maskedVect1 = vectShiftedMat1[matMask]

            # result = np.sum((vectMat2[matMask] - maskedVect1) ** 2) / maskedVect1.size

            # result = -1 * np.dot(vectMat2[matMask] / np.linalg.norm(vectMat2[matMask]), maskedVect1 / np.linalg.norm(maskedVect1))

            result = keywordToAlignFunction[keyword](vectMat2[matMask], maskedVect1)

            if curMin > result:
                curMin = result
                curMat = padCut(mat1, displX, displY, 0)
                displacements = (displX, displY)

    print(curMat, curMin)
    print(displacements)

    return curMat