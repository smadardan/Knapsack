"""
tests.population
~~~~~~~~~~~~~~~~
here we will write all of the unit test for the population class
"""

import numpy as np

from src.population import Population
from tests.test_chromosome import LoggerMock
import config.conf_file as cnf

# initialize for all tests
logger = LoggerMock()
inst = Population(2, cnf.KNAPSACK_FILE_NAME, 5, logger)


def test_natural_population():
    pop = inst.natural_population(np.array([[6, 6], [2, 2], [9, 9], [7, 7]]), 1)
    assert np.array_equal(pop, [np.array([2, 2])])


def test_calc_scores():
    score = inst.calc_scores([np.array([[2, 2], [2, 2]]), np.array([2, 2])])
    assert np.array_equal(score, np.array([[4, 4], [2, 2]]))


def test_rank_and_find_best():
    rank, best = inst.rank_and_find_best(np.array([[4, 4], [2, 2]]), [np.array([[2, 2], [2, 2]]), np.array([2, 2])])
    assert np.array_equal(rank, np.array([1, 0]))
    assert np.array_equal(best, [np.array([[2, 2], [2, 2]])])


def test_find_best_score():
    inst.find_best_score(np.array([[8, 8], [5, 5]]), np.array([0, 1]))
    assert np.array_equal(np.array([8, 8]), inst.max_score_for_run)


def test_create_new_population():
    pop = inst.create_new_population(np.array([[8, 8]]), np.array([[2, 2]]))
    assert np.array_equal(pop, [np.array([2, 2]), np.array([2, 2])])


def test_create_parents_and_mutants():
    parents, mutants = inst.create_parents_and_mutants([np.array([[8, 8]]), np.array([[3, 3], [2, 2]])])
    assert np.array_equal(parents, [np.array([[8, 8]])])
    assert np.array_equal(mutants, [np.array([[3, 3], [2, 2]])])
