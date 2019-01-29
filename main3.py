from src.env import Environment

env = Environment(render=True, scale=5, fov_size=100, keyboard=True)
env.run()

# Do a 200x200 (fov_size = 100) field of view, but convert it into a bitmap which is 200x200/(10*10) = 400 (20x20)
# can be generated in O(N) time