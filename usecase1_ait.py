import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import inf
from typing import List, Tuple

random.seed(1)
np.random.seed(1)

# --------------------
# Generate Scheduling Problem Instance
# --------------------
def generate_jobs(n_jobs, proc_mean=10, due_mean=50, slack=20):
    processing = np.random.poisson(proc_mean, size=n_jobs) + 1
    due_dates = np.maximum(1, np.random.normal(due_mean, slack, size=n_jobs).astype(int))
    return list(processing), list(due_dates)

# --------------------
# Evaluation of Sequence
# --------------------
def evaluate(seq, p, d):
    t = 0
    total_C = 0
    total_T = 0
    for j in seq:
        t += p[j]
        total_C += t
        total_T += max(t - d[j], 0)
    return total_C, total_T

# --------------------
# Genetic Operators
# --------------------
def order_crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    def ox(a1, a2):
        c = [-1]*n
        c[a:b+1] = a1[a:b+1]
        fill = [x for x in a2 if x not in c]
        pos = [i for i in range(n) if c[i] == -1]
        for i, v in zip(pos, fill):
            c[i] = v
        return c
    return ox(p1, p2), ox(p2, p1)

def mutation(seq, rate):
    s = seq[:]
    for i in range(len(s)):
        if random.random() < rate:
            j = random.randrange(len(s))
            s[i], s[j] = s[j], s[i]
    return s

# --------------------
# NSGA-II Components
# --------------------
def dominates(u, v):
    return (u[0] <= v[0] and u[1] <= v[1]) and (u[0] < v[0] or u[1] < v[1])

def fast_sort(values):
    S = [[] for _ in values]
    n = [0]*len(values)
    rank = [0]*len(values)
    fronts = [[]]

    for p in range(len(values)):
        for q in range(len(values)):
            if dominates(values[p], values[q]):
                S[p].append(q)
            elif dominates(values[q], values[p]):
                n[p] += 1
        if n[p] == 0:
            rank[p] = 0
            fronts[0].append(p)

    f = 0
    while fronts[f]:
        next_front = []
        for p in fronts[f]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = f+1
                    next_front.append(q)
        f += 1
        fronts.append(next_front)
    fronts.pop()
    return fronts

def crowding(values, front):
    dist = {i: 0 for i in front}
    if len(front) <= 2:
        return dist

    for m in range(2):
        f = sorted(front, key=lambda x: values[x][m])
        dist[f[0]] = dist[f[-1]] = inf
        mn = values[f[0]][m]
        mx = values[f[-1]][m]
        for i in range(1, len(front)-1):
            dist[f[i]] += (values[f[i+1]][m] - values[f[i-1]][m]) / (mx-mn+1e-9)
    return dist

# --------------------
# NSGA-II Main Algorithm
# --------------------
def nsga2(p, d, popsize=60, gen=100, cx=0.9, mut=0.1):
    jobs = len(p)
    pop = [random.sample(range(jobs), jobs) for _ in range(popsize)]
    objs = [evaluate(ind, p, d) for ind in pop]

    for g in range(gen):
        fronts = fast_sort(objs)
        cd = {}
        for f in fronts:
            cd.update(crowding(objs, f))

        def select():
            a, b = random.randrange(popsize), random.randrange(popsize)
            ra = next(i for i, fr in enumerate(fronts) if a in fr)
            rb = next(i for i, fr in enumerate(fronts) if b in fr)
            if ra < rb: return pop[a]
            if rb < ra: return pop[b]
            return pop[a] if cd[a] > cd[b] else pop[b]

        newpop = []
        while len(newpop) < popsize:
            p1, p2 = select(), select()
            if random.random() < cx:
                c1, c2 = order_crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]
            newpop.append(mutation(c1, mut))
            if len(newpop) < popsize:
                newpop.append(mutation(c2, mut))

        pop = newpop
        objs = [evaluate(ind, p, d) for ind in pop]

    fronts = fast_sort(objs)
    return pop, objs, fronts[0]

# --------------------
# RUN Example
# --------------------
if __name__ == "__main__":
    n = 10
    p, d = generate_jobs(n, 10, 50, 15)
    pop, vals, pareto_front = nsga2(p, d)

    print("\nPareto Solutions:")
    for idx in pareto_front:
        print(f"Seq:{pop[idx]} -> Completion, Tardiness = {vals[idx]}")

    # Plot
    X = [v[0] for v in vals]
    Y = [v[1] for v in vals]
    plt.figure(figsize=(7,5))
    plt.scatter(X, Y)
    plt.title("Pareto Front: Completion Time vs. Tardiness")
    plt.xlabel("Total Completion Time")
    plt.ylabel("Total Tardiness")
    plt.grid(True)
    plt.show()
