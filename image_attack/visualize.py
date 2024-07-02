import numpy as np
from PIL import Image

# After image sampling, generate images
sample_path = 'saved/samples/samples_50x256x256x3.npz'
im = np.load(sample_path)
print( (im.f.arr_0).shape)
for i in range(im.f.arr_0.shape[0]):
    img = Image.fromarray(im.f.arr_0[i])
    img.save("./3500000_{}.png".format(i))
