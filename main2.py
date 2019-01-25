from src.env import Environment

env = Environment(render=False, scale=10)
while not env.finished:
    env.take_action(5)
    print(env.finished, env.fitness, env.hash)