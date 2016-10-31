import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
np.random.seed(1977)

x, y, z = np.random.random((3, 10))
yi, xi = np.mgrid[0:1:100j, 0:1:100j]

interp_types = ['multiquadric', 'inverse', 'gaussian', 'linear', 'cubic',
                'quintic', 'thin_plate']

for kind in interp_types:
    interp = scipy.interpolate.Rbf(x, y, z, function=kind)
    zi = interp(xi, yi)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'ko')
    im = ax.imshow(zi, extent=[0, 1, 1, 0], cmap='gist_earth')
    fig.colorbar(im)
    ax.set(title=kind)
    fig.savefig(kind + '.png', dpi=80)

plt.show()