import scipy


GRID_POINTS = 25
x_min = XYZ[:,0].min()
x_max = XYZ[:,0].max()
y_min = XYZ[:,1].min()
y_max = XYZ[:,1].max()
xi = np.linspace(x_min, x_max, GRID_POINTS)
yi = np.linspace(y_min, y_max, GRID_POINTS)
XI, YI = np.meshgrid(xi, yi)

from scipy.interpolate import Rbf
rbf = Rbf(XYZ[:,0],XYZ[:,1],XYZ[:,2],function='thin-plate',smooth=0.0)
ZI = rbf(XI,YI)