from __future__ import print_function
from src.env import Environment

import os
import neat

import numpy as np

import random

from skimage.measure import block_reduce

def eval_genomes(genomes, config):
    genome_seed = random.randrange(0, 99999999)
    print("Selected seed", genome_seed)
    for genome_id, genome in genomes:
        genome.fitness = 0
        fov = 100
        env = Environment(render=False, max_projectiles=100, seed=genome_seed, scale=5, fov_size=fov)
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        while not env.finished:
            raster = np.reshape(env.raster_array, (fov * 2, fov * 2))

            # 40,000 = 200x200 needs to be reduced by 5x5 to size 1600 (40x40)
            raster = block_reduce(raster, block_size=(5, 5), func=np.mean)
            output = net.activate(raster.flatten())
            env.take_action(np.argmax(output)) # Take the action and update the game state (tick)
        genome.fitness = env.fitness


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 30)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation i
    # here so that the script will run successfully regardless of the
    # current working directory.s
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)