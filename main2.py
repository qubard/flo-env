from src.env import Environment

env = Environment(scale=1, fov_size=10)
while not env.finished:
    env.take_action(9)
    print(env.finished, env.fitness, env.hash)