# get data
import numpy as np
data = np.loadtxt(fname='inflammation-01.csv',delimiter=',')
# plot matrix
import matplotlib.pyplot as plt
image = plt.imshow(data)
plt.savefig('heatmap.png', dpi = 300)
