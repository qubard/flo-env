from src.env import Environment

#env = Environment(render=True, scale=5, fov_size=100, keyboard=True)
#env.run()

fov = 100
env = Environment(scale=5, max_projectiles=100, fov_size=fov, render=True, keyboard=True)
env.run()

print(env.fitness)
# Do a 200x200 (fov_size = 100) field of view, but convert it into a bitmap which is 200x200/(10*10) = 400 (20x20)
# can be generated in O(N) time