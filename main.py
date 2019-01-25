from __future__ import print_function
from src.env import Environment

import os
import neat

from numpy import argmax


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        env = Environment(render=False, scale=5, fov_size=25)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        while not env.finished and env.fitness < 100000:
            arr = env.raster_array
            output = net.activate(arr)
            env.take_action(argmax(output)) # Take the action and update the game state (tick)
        genome.fitness = env.fitness
        print("Fitness: %s" % genome.fitness)


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

    # Run for up to 30 generations.
    winner = p.run(eval_genomes, 30)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    print(winner_net)

    p = neat.Checkpointer.restore_checkpoint('checkpoints/neat-checkpoint')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation i
    # here so that the script will run successfully regardless of the
    # current working directory.s
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)