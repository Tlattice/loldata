import matplotlib.pyplot as plt
import matplotlib.patches as patches


img = plt.imread("assets/minimap.png")
champ = plt.imread('assets/champions/Aatrox.png')


#fig, ax = plt.subplots()
#ax.imshow(img)
fig, ax = plt.subplots()
x = range(300)
ax.imshow(img, extent=[0, 400, 0, 300])
ax.axis('off')

ax2 = plt.axes([0.1, 0.1, 0.05, 0.05], frameon=True)
im = ax2.imshow(champ)
patch = patches.Circle((60, 60), radius=60, transform=ax2.transData)
im.set_clip_path(patch)
ax2.axis('off')
#plotImage([0], [0], champ)

#ax.show()
plt.show()
