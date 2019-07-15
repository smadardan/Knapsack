# Knapsack

Knapsack solves the knapsack problem using genetic algorithm.

* more about the knapsack problem can be found [here](https://en.wikipedia.org/wiki/Knapsack_problem)
* Explanation about genetic algorithm is present [here](https://en.wikipedia.org/wiki/Genetic_algorithm) 


## Usage

1. clone the repository
2. insert items in config/items.txt in the form of:
```
6 2
5 3
8 6
9 7
6 5
7 9
3 4
```
where the **left** int is the **value** of each item and the **right** int is the **weight**
3. open the console. change directory to this repository
4. write:
```
python main.py
```
5. then you will need to insert 3 variables:
   - population size between 10 to 50 - how many chromosomes - possible solutions will be in each set of solutions
   - maximum weight between 10 to 20 - what is the maximum allowed weight for the knapsack (remember we want to maximize value and minimize weight)
   - number of iterations between 10 to 30 - how many iterations that creates population should execute? it is important to find the optimum of this hyperparameter

6. in the end we will receive the best solution with the exact items in the logs\log_file.log. (an example is already present there)


## License
[MIT](https://choosealicense.com/licenses/mit/)
