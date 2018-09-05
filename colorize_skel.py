# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio
from aligners import alignMain, SearchMode, MatchMode, printMeOut, ColorMode
from utils import *
import datetime
from enum import Enum

### OPTIONS
# print matched matrixes
debugPrintMatch = False
# name of the input file
imname = 'emir.tif'

# read in the image
im = skio.imread(imname)

# convert to double (might want to do this later on to save memory)    
im = sk.img_as_float(im)
    
# compute the height of each part (just 1/3 of total)
height = int(np.floor(im.shape[0] / 3.0))

# separate color channels
b = im[:height]
g = im[height: 2*height]
r = im[2*height: 3*height]

# align the images
# functions that might be useful for aligning the images include:
# np.roll, np.sum, sk.transform.rescale (for multiscale)

# trim
trimSize = 400
trimR = trimAllSide(r, trimSize)
trimG = trimAllSide(g, trimSize)
trimB = trimAllSide(b, trimSize)

alignMode = MatchMode.NCC
mode = SearchMode.PYR

print("===== 1ST MATCH =====")
mat1A = trimG
mat1B = trimB
ag, agCoord = alignMain(mode, alignMode, mat1A, mat1B)
agCoord = ",".join([str(x) for x in agCoord])

print("===== 2ND MATCH =====")
mat2A = trimR
mat2B = trimB
ar, arCoord = alignMain(mode, alignMode, mat2A, mat2B)
arCoord = ",".join([str(x) for x in arCoord])

if debugPrintMatch:
    printMeOut(ag, ColorMode.G)
    printMeOut(ar, ColorMode.R)
    printMeOut(trimB, ColorMode.B)

# zg = np.full(g.shape, 0)
# zr = np.full(r.shape, 0)
# zb = np.full(r.shape, 0)

# create a color image
im_out = np.dstack([ar, ag, trimB])

# save the image
imname_no_format = imname.split(".")[0]
currTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

fname = 'out_path/%s_%s_%s_%s_g%s_r%s_trim%d.jpg' % (imname_no_format, currTime, alignMode, mode, agCoord, arCoord, trimSize)
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()