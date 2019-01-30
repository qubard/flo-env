from src.env import Environment

import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import block_reduce

fov = 100
env = Environment(scale=5, fov_size=fov)
lasthash = None


while not env.finished:
    env.take_action(3)
    print(env.finished, env.age, env.fitness, env.hash)

    if env.hash != lasthash:
        lasthash = env.hash
        raster = np.reshape(env.raster_array, (fov * 2, fov * 2))

        # 40,000 = 200x200 needs to be reduced by 5x5 to size 1600 (40x40)
        raster = block_reduce(raster, block_size=(5,5), func=np.mean)
        plt.imshow(raster, cmap='gray', interpolation='nearest')
        plt.show()