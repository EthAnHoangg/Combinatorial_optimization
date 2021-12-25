import json
import numpy as np
import argparse
from ortools.linear_solver import pywraplp
import time

parser = argparse.ArgumentParser("INPUT")
parser.add_argument('--input', type=str, default='sample1.json')

# find the neighbor nodes of node k
def neighbor(k):
	nb = []
	for i in range (1, n+1):
		if i not in visited:
			nb.append(i)
	return nb

# find the driver that have the minimum time-cost and not return to depot yet
def min_route_driver(route_driver):
	min_route = INF
	for i, route in enumerate(route_driver):
		if route == 0:
			return i
		elif len(route) < min_route:
			min_route = len(route)
			index = i
	return index
# find and add a node to the route of driver
# that have minimum time-cost

def add_next_node(k):
	cur_node = route_driver[k][-1]
	min_distance = INF
	next_node = 0
	for i in neighbor(cur_node):
		# traversal all the neighbor of the last node
		if t[cur_node][i] < min_distance:
			min_distance = t[cur_node][i]
			next_node = i
			# find the nearest node to the last node
			# of the driver k
	cost_driver[k] += min_distance
	route_driver[k].append(next_node)
	visited.append(next_node)

if __name__ == '__main__':
	t1 = time.time()
	args = parser.parse_args()
	name = args.input

	#READ INPUT:
	with open(name, 'r') as f:
		input = json.load(f)
	n, k, d, t = input['N'], input['k'], input['d'], input['t']
	print('NUMBER OF HOUSES', n)
	print('NUMBER OF WORKERS', k)
	INF = np.inf
	# broadcasting to combine matrix d
	# to matrix t (size n+1 x n+1), which is assymetric
	print(np.array(t))
	t = np.array(t) + np.array(d)
	for i in range (n+1):
		for j in range (n+1):
			if i == j:
				t[i][j] = 0

	print(t)

	visited = [0]

	# the first place of each driver must be 0
	route_driver = []
	for i in range (k):
		route_driver.append([0])

	# initially the cost of the driver is 0 
	cost_driver = [0] * k

	while len(visited) <= n:
		dr = min_route_driver(route_driver)
		add_next_node(dr)

	for i in range (k):
		cost_driver[i] += t[route_driver[i][-1]][0]
		route_driver[i].append(0)

	objective_value = max(cost_driver)
	for i in range (k):
		print('Route of driver', str(i), 'is')
		print(route_driver[i])
		for city in route_driver[i]:
			print(city, end = ' -> ')
		print('With the cost', cost_driver[i])
		# for j in range (len(route_driver[i]) - 1):
		# 	print('t =', s[route_driver[i][j]][route_driver[i][j+1]], 'd =', d[route_driver[i][j+1]])
		print('-' * 100)

	print('The objective value =', objective_value)

	t2=time.time()
	print(t2-t1)
	

