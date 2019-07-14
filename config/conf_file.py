"""
config.conf_file
~~~~~~~~~~~~~~~~~

this file will keep all of the constant
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE_NAME = os.path.join(BASE_DIR, "logs", "log_file.log")
KNAPSACK_FILE_NAME = os.path.join(BASE_DIR, "config", 'items.txt')
POPULATION_MODULE = os.path.join(BASE_DIR, "src", 'population.py')

MAX_POP_SIZE = 50
MIN_POP_SIZE = 10

MAX_MAX_WEIGHT = 20
MIN_MAX_WEIGHT = 10

MAX_ITERATIONS = 30
MIN_ITERATIONS = 10

WEIGHT = 1
VALUE = 0

TOP_PERCENT = 0.5
CUT_BY = int(1 / TOP_PERCENT)
