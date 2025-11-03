import matplotlib.pyplot as plt
from heapq import heappush, heappop

# --------------------------
# A* Pathfinding Algorithm
# --------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan distance

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heappush(open_set, (0, start))
    
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        _, current = heappop(open_set)
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                new_cost = g_score[current] + 1
                if (nx, ny) not in g_score or new_cost < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = new_cost
                    f = new_cost + heuristic((nx, ny), goal)
                    heappush(open_set, (f, (nx, ny)))
                    came_from[(nx, ny)] = current
    
    return None  # No path found

# --------------------------
# Example Map
# --------------------------
grid = [
    [0,0,0,0,0,0],
    [0,1,1,1,0,0],
    [0,0,0,1,0,0],
    [0,1,0,0,0,0],
    [0,0,0,1,1,0],
    [0,0,0,0,0,0]
]
start = (0,0)
goal  = (5,5)

# Find Path
path = astar(grid, start, goal)
print("Shortest Path:", path)

# --------------------------
# Plot
# --------------------------
plt.figure(figsize=(6,6))
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 1:
            plt.scatter(j, i, marker="s", c="black")
        else:
            plt.scatter(j, i, marker=".", c="lightgray")

# Draw path
if path:
    px = [p[1] for p in path]
    py = [p[0] for p in path]
    plt.plot(px, py, linewidth=3)
    plt.scatter(start[1], start[0], c="green", s=100, label="Start")
    plt.scatter(goal[1], goal[0], c="red", s=100, label="Goal")

plt.title("A* Pathfinding Navigation")
plt.gca().invert_yaxis()
plt.grid(True)
plt.legend()
plt.show()
