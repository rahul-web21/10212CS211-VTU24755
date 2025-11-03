#Task 5:Implementation of Ant Colony Optimization to Optimize Ride-Sharing Trip Duration using Python by following constraints.

import numpy as np
from numpy import inf
d = np.array([
    [0, 10, 12, 11, 14],
    [10, 0, 13, 15, 8],
    [12, 13, 0, 9, 14],
    [11, 15, 9, 0, 16],
    [14, 8, 14, 16, 0]
])
iteration = 100
n_ants = 5
n_citys = 5
m = n_ants
n = n_citys
e = 0.5   
alpha = 1 
beta = 2  
d_safe = np.where(d == 0, np.inf, d)
visibility = 1 / d_safe
visibility[visibility == inf] = 0
pheromone = 0.1 * np.ones((n, n))
rute = np.ones((m, n+1))
for ite in range(iteration):
    rute[:, 0] = 1
    for i in range(m):
        temp_visibility = np.array(visibility)
        for j in range(n-1):
            combine_feature = np.zeros(n)
            cur_loc = int(rute[i, j] - 1)
            temp_visibility[:, cur_loc] = 0
            p_feature = np.power(pheromone[cur_loc, :], beta)
            v_feature = np.power(temp_visibility[cur_loc, :], alpha)
            combine_feature = p_feature * v_feature
            total = np.sum(combine_feature)
            probs = combine_feature / total
            cum_prob = np.cumsum(probs)
            r = np.random.random_sample()
            city = np.nonzero(cum_prob > r)[0][0] + 1
            rute[i, j+1] = city
        left = list(set([i for i in range(1, n+1)]) - set(rute[i, :-2]))[0]
        rute[i, -2] = left
    rute_opt = np.array(rute)
    dist_cost = np.zeros((m, 1))
    for i in range(m):
        s = 0
        for j in range(n-1):
            s += d[int(rute_opt[i, j]) - 1, int(rute_opt[i, j+1]) - 1]
        dist_cost[i] = s
    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = rute[dist_min_loc, :]
    pheromone = (1 - e) * pheromone
    for i in range(m):
        for j in range(n-1):
            dt = 1 / dist_cost[i].item()
            a = int(rute_opt[i, j]) - 1
            b = int(rute_opt[i, j+1]) - 1
            pheromone[a, b] += dt

print("Final Routes of all Ants:")
print(rute_opt)
print()
print("Best Route (Ride-Sharing Path):", best_route)
print("Optimal Trip Duration (minutes):", int(dist_min_cost[0]) + d[int(best_route[-2]) - 1, 0])


#Output:

#Final Routes of all Ants:
# [[1. 2. 5. 4. 3. 1.]
#  [1. 2. 5. 4. 3. 1.]
#  [1. 2. 5. 4. 3. 1.]
#  [1. 2. 5. 4. 3. 1.]
#  [1. 2. 5. 4. 3. 1.]]

# Best Route (Ride-Sharing Path): [1. 2. 5. 4. 3. 1.]
# Optimal Trip Duration (minutes): 55
