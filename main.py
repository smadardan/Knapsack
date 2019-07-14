#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main
~~~~~

the purpose of this code is to solve the knapsack problem.
the code will read the input (the items in the knapsack) and will hopefully
solve the problem (find the best fit to the restrictions) by using genetic algorithm
"""

import logging
import click
import pytest

from src.population import Population
import config.conf_file as cnf


@click.command()
@click.option('--population_size', type=click.IntRange(cnf.MIN_POP_SIZE, cnf.MAX_POP_SIZE, clamp=True),
              prompt="Please choose population size between {} to {}".format(cnf.MIN_POP_SIZE, cnf.MAX_POP_SIZE),
              default='20')
@click.option('--max_weight', type=click.IntRange(cnf.MIN_MAX_WEIGHT, cnf.MAX_MAX_WEIGHT, clamp=True),
              prompt="Please choose maximum weight between {} to {}".format(
                  cnf.MIN_MAX_WEIGHT, cnf.MAX_MAX_WEIGHT),
              default='15')
@click.option('--num_iterations', type=click.IntRange(cnf.MIN_ITERATIONS, cnf.MAX_ITERATIONS, clamp=True),
              prompt="Please choose number of iterations between {} to {}".format(
                  cnf.MIN_ITERATIONS, cnf.MAX_ITERATIONS), default='15')
def main(population_size, max_weight, num_iterations):
    """
    starts logging and insert data to population to initiate the genetic algorithm
    :param population_size: int, how many items are allowed in the knapsack
    :param max_weight: int, what is the maximum weight allowed in the knapsack
    :param num_iterations: how many iterations can the genetic algorithm perform
    :return:
    """
    pytest.main()
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info('## Started ##')

    try:
        pop = Population(population_size, cnf.KNAPSACK_FILE_NAME, max_weight, logger)
        pop.circle_of_life(num_iterations)

    except IOError:
        logger.error('Failed to open file', exc_info=True)

    logger.info('## Finished ##')
    return


def configure_logging():
    """
    initialize the logging process
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler(cnf.LOG_FILE_NAME)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)


if __name__ == "__main__":
    main()
