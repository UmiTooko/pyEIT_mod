import numpy as np
import matplotlib.pyplot as plt
from scikitlearn.linear_model import LinearRegression

a = np.array([[1, 1],
              [2, 2],
              [3, 8]])
model = LinearRegression()
model.fit(a)
print(model._coef)

#plt.scatter(a[:,0:1], a[:,1:2])
#plt.plot()