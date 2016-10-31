import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
np.random.seed(1977)

x, y, z = np.random.random((3, 10))

interp = scipy.interpolate.Rbf(x, y, z, function='thin_plate')

yi, xi = np.mgrid[0:1:100j, 0:1:100j]

zi = interp(xi, yi)

plt.plot(x, y, 'ko')
plt.imshow(zi, extent=[0, 1, 1, 0], cmap='gist_earth')
plt.colorbar()

plt.show()