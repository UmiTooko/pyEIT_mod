import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

x, y = np.meshgrid(np.linspace(0,50,51), np.linspace(0,50,51))
z = np.linspace(-2,4,50*50).reshape(50,50)

norm = TwoSlopeNorm(vcenter=0)
pc = plt.pcolormesh(x,y,z, norm=norm, cmap="RdBu_r")
plt.colorbar(pc)

plt.show()