import numpy as np
from PIL import Image

# BOA major revision startsLinkΩ_b/samples/samples_50x256x256x3.npz'
sample_path = 'saved/samples/samples_50x256x256x3.npz'
im = np.load(sample_path)
print( (im.f.arr_0).shape)
for i in range(im.f.arr_0.shape[0]):
    print("img shape ", im.f.arr_0[i].shape)
    img = Image.fromarray(im.f.arr_0[i])
    img.save("./logo_mr_out/logo_HSBC_out/3400000_{}.png".format(i))
