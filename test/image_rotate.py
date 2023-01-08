"""
from PIL import Image
import matplotlib.pyplot as plt

im = Image.open("pusula.png")
im = im.rotate(155) # Rotates counter clock-wise.
implot = plt.imshow(im)
plt.ylim({800,400})
plt.xlim([800,400])
plt.show()
"""
#aşağıdaki kodda plot eksen sınırlandırma kodu vardır
"""
img = mpimg.imread('pusula.png')
fig,ax = plt.subplots()
ax.set_xticks(np.arange(0,600,50.0))
imgplot = plt.imshow(img,extent=([0,600,0.006,6]),aspect='auto')    
"""

# Aşağıdaki kodumuzda resim pozisyon değiştiriyor
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl

ax = plt.gca()
ax.set_xlim(0, 300)
ax.set_ylim(0, 300)

imageFile = "pusula.png"
img=mpimg.imread(imageFile)
imgplot = ax.imshow(img)
tx, ty = [0,80]
transform = mpl.transforms.Affine2D().translate(tx, ty)
imgplot.set_transform(transform + ax.transData)

plt.show()

"""
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl

ax = plt.gca()
ax.set_xlim(0, 300)
ax.set_ylim(0, 300)


imageFile = "pusula.png"
img=mpimg.imread(imageFile)
tx, ty = [200,200]
ax.imshow(img, extent=(tx, tx + 50, ty, ty + 50))

plt.show()

"""