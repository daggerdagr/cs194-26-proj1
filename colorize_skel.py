# CS194-26 (CS294-26): Project 1 starter Python code

# these are just some suggested libraries
# instead of scikit-image you could use matplotlib and opencv to read, write, and display images

import numpy as np
import skimage as sk
import skimage.io as skio
from aligners import align
from utils import *

# name of the input file
imname = 'cathedral.jpg'

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

### ag = align(g, b)
### ar = align(r, b)

trimSize = 50
r = trimAllSide(r, trimSize)
g = trimAllSide(g, trimSize)
b = trimAllSide(b, trimSize)

ag = align(g, b)
ar = align(r, b)

# zg = np.full(g.shape, 0)
# zr = np.full(r.shape, 0)
# zb = np.full(r.shape, 0)

# create a color image
im_out = np.dstack([ar, ag, b])

# save the image
fname = 'out_path/out_fname2.jpg'
skio.imsave(fname, im_out)

# display the image
skio.imshow(im_out)
skio.show()