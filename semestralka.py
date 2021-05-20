from PIL import Image
import numpy as np


Kr = 0.299
Kg = 0.587
Kb = 0.114

#load image
np_im = np.array(Image.open('lena.bmp'))
print ("loaded image shape: ", np_im.shape)

R = np_im[:,:,0]
G = np_im[:,:,1]
B = np_im[:,:,2]



#transform to ycbcr
Y = 16 + 219*(Kr * R + Kg * G + Kb * B)

Cb = 128 + 224 * 0.5 * (B - Y / 1 - Kb)
Cr = 128 + 224 * 0.5 * (R - Y / 1 - Kr)

YCBCR = np.zeros(np_im.shape)

YCBCR[:,:,0] = Y
YCBCR[:,:,1] = Cb
YCBCR[:,:,2] = Cr


#subsampling chromatics components

Cb_x = len(Cb[:, 0])
Cb_y = len(Cb[0, :])

Cb_s_x = int((len(Cb[:,0]) / 2))
Cb_s_y = int((len(Cb[0,:]) / 2))




Cb_s = np.zeros((Cb_s_x, Cb_s_y), dtype=float, order='C')
Cr_s = np.zeros((Cb_s_x, Cb_s_y), dtype=float, order='C')


for y in range(0, Cb_y, 2):
    for x in range(0, Cb_x, 2):
        
        Cb_s[int(x / 2), int(y / 2)] = Cb[x, y]
        Cr_s[int(x / 2), int(y / 2)] = Cr[x, y]



#ycbcr to rgb

YCBCR_s = np.zeros(np_im.shape)

Cb_s_ = np.zeros(Cb.shape)
Cr_s_ =np.zeros(Cr.shape)

for y in range(0, Cb_y, 1):
    for x in range(0, Cb_x, 1):
        
        Cb_s_ [x, y] = Cb_s[int(x / 2), int(y / 2)]
        Cr_s_ [x, y] = Cr_s[int(x / 2), int(y / 2)]


YCBCR_s[:,:,0] = Y
YCBCR_s[:,:,1] = Cb_s_
YCBCR_s[:,:,2] = Cr_s_


R_ = Y + 1.40200 * (Cr_s_ - 128)
G_ = Y - 0.34414 * (Cb_s_ - 128) - 0.71414 * (Cr_s_ - 128)
B_ = Y + 1.77200 * (Cb - 128)

np_im_ = np.zeros(np_im.shape)

np_im_ [:,:,0] = R_
np_im_ [:,:,1] = G_
np_im_ [:,:,2] = B_

print ("final image shape: ", np_im_.shape)

new = np.multiply(np_im_.reshape((240,  240, 3)), 255).astype(np.uint8)


img = Image.fromarray(new)
img.show()