#!/usr/bin/env python3
"""
pumpkin pie maze- search algorithms

run examples:
    python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo bfs
    python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo astar --heuristic manhattan (or euclidean)
    if on macOS, you can do: python3 pumpkin_pie_maze.py --maze data/pumpkin.txt --algo bfs

outputs an annotated ASCII maze to files like:
    outputs/pumpkinpie-BFS.txt

legend in annotated files:
    # = wall
    S = start
    G = goal
    * = final path
    x = explored/closed set
    o = frontier when captured (optional)

assuming:
- 4-way movement (up, down, left, right)
- Unit step cost unless otherwise noted (we stick to 1)
"""
from __future__ import annotations

import argparse # for command-line argument parsing
import heapq # for priority queue
import os 
from collections import deque
from typing import Dict, Iterable, List, Optional, Set, Tuple # type hints

Coord = Tuple[int, int] # coordinate type
Grid = List[List[str]] # grid type

WALL = "#"
START = "S"
GOAL = "G"
OPEN = "."  # also treat space as open when reading

READABLE_MAP = {
    WALL: WALL,
    START: START,
    GOAL: GOAL,
    '*': '+',
    'x': ' ',
    'o': 'O',
    '.': '.',
}

LEGEND_LINES = [
    'legend:',
    '# = wall',
    "space = explored/open space (was 'x')",
    "+ = solution path (was '*')",
    '. = existing dots',
    "O = special item (was 'o')",
    'S = start',
    'G = goal',
]

# -----------------------------
# grid readings & neighbors
# -----------------------------

def read_grid(path: str) -> Tuple[Grid, Coord, Coord]: 
    """read an ASCII maze file into a grid.

    Allowed symbols: '#', 'S', 'G', '.', space.
    Returns (grid, start, goal)
    """
    with open(path, "r", encoding="utf-8") as f: # read lines from file
        lines = [line.rstrip("\n") for line in f] # strip newlines
    if not lines:
        raise ValueError("Maze file is empty")

    width = max(len(line) for line in lines) # find max width for padding
    grid: Grid = []
    start: Optional[Coord] = None
    goal: Optional[Coord] = None
    for r, line in enumerate(lines): # pad each line to the max width
        row: List[str] = []
        for c in range(width):
            ch = line[c] if c < len(line) else WALL  # pad to rectangle with walls
            if ch == " ":
                ch = OPEN
            if ch == START: # only one start allowed
                start = (r, c)
            if ch == GOAL:
                goal = (r, c)
            row.append(ch)
        grid.append(row)

    if start is None or goal is None:
        raise ValueError("Maze must contain exactly one 'S' and one 'G'")
    return grid, start, goal # (grid, start, goal)


def neighbors(grid: Grid, cell: Coord) -> Iterable[Coord]: # 4-way neighbors
    r, c = cell # current cell
    H, W = len(grid), len(grid[0]) # grid dimensions
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # up, down, left, right
        nr, nc = r + dr, c + dc # neighbor cell
        if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] != WALL: # within bounds and not a wall
            yield (nr, nc) # yield valid neighbor


# -----------------------------
# path reconstruction & annotation
# -----------------------------

def reconstruct(parent: Dict[Coord, Coord], start: Coord, goal: Coord) -> List[Coord]: # backtrack from goal to start
    """reconstruct path from start to goal using parent map."""
    path: List[Coord] = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()  # backtrack
    return path  # from start to goal 


def annotate_and_write(  # annotate the maze and write to file
    grid: Grid,
    start: Coord,
    goal: Coord,
    path: Optional[List[Coord]],
    explored: Set[Coord],
    out_path: str,
    frontier: Optional[Iterable[Coord]] = None,
) -> None:
    """writes an annotated ASCII maze to out_path."""
    H, W = len(grid), len(grid[0])
    out = [row[:] for row in grid]

    explored = set(explored)
    path_set = set(path) if path else set()
    frontier_set = set(frontier) if frontier else set()

    for r in range(H): # annotate the grid
        for c in range(W):
            pt = (r, c)
            ch = out[r][c]
            if pt == start:
                out[r][c] = START
            elif pt == goal:
                out[r][c] = GOAL
            elif pt in path_set:
                out[r][c] = "*"
            elif ch != WALL and pt in explored:
                out[r][c] = "x"
            elif ch != WALL and pt in frontier_set:
                out[r][c] = "o"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    readable_lines = []
    for r in range(H):
        raw_line = "".join(out[r])
        readable_line = "".join(READABLE_MAP.get(ch, ch) for ch in raw_line)
        readable_lines.append(readable_line)

    legend_block = "\n".join(LEGEND_LINES)
    contents = legend_block + "\n\n" + "\n".join(readable_lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(contents)


# -----------------------------
# heuristics
# -----------------------------

def manhattan(a: Coord, b: Coord) -> int: # function for heuristic manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Manhattan distance


def euclidean(a: Coord, b: Coord) -> float: # function for heuristic euclidean distance
    dx, dy = a[0] - b[0], a[1] - b[1] # Euclidean distance
    return (dx * dx + dy * dy) ** 0.5 


# -----------------------------
# search algorithms
# -----------------------------

def bfs(grid: Grid, start: Coord, goal: Coord): 
    q: deque[Coord] = deque([start])
    parent: Dict[Coord, Coord] = {}
    visited: Set[Coord] = {start}  
    closed: Set[Coord] = set()     
    expanded = 0

    while q: # queue
        u = q.popleft()  
        closed.add(u)   
        expanded += 1
        if u == goal:
            path = reconstruct(parent, start, goal) # reconstruct path
            return path, len(path) - 1, expanded, True, closed, list(q) # return all nodes in queue
        for v in neighbors(grid, u):
            if v not in visited: # if not yet visited
                visited.add(v) # mark as visited
                parent[v] = u # set parent
                q.append(v) 
    return None, float("inf"), expanded, False, closed, [] # no path found


def dfs(grid: Grid, start: Coord, goal: Coord):
    stack: List[Coord] = [start]
    parent: Dict[Coord, Coord] = {}
    visited: Set[Coord] = {start}
    expanded = 0

    while stack: 
        u = stack.pop()
        expanded += 1
        if u == goal:
            path = reconstruct(parent, start, goal)
            return path, len(path) - 1, expanded, False, visited, stack
        for v in neighbors(grid, u):
            if v not in visited: # if not yet visited
                visited.add(v) # mark as visited
                parent[v] = u # set parent
                stack.append(v) # add to stack
    return None, float("inf"), expanded, False, visited, [] # no path found


def ucs(grid: Grid, start: Coord, goal: Coord): # uniform cost search
    pq: List[Tuple[int, Coord]] = [(0, start)]
    parent: Dict[Coord, Coord] = {}
    best_g: Dict[Coord, int] = {start: 0}
    closed: Set[Coord] = set()
    expanded = 0 # sets number of nodes to 0 

    while pq: # priority queue
        g, u = heapq.heappop(pq)
        if u in closed:
            continue # if already expanded, skip
        closed.add(u)
        expanded += 1
        if u == goal:
            path = reconstruct(parent, start, goal)
            return path, g, expanded, True, closed, [v for _, v in pq]
        for v in neighbors(grid, u):
            ng = g + 1
            if v not in best_g or ng < best_g[v]:
                best_g[v] = ng # update best cost to reach v
                parent[v] = u # set parent
                heapq.heappush(pq, (ng, v)) # push new cost and node to priority queue
    return None, float("inf"), expanded, False, closed, []


def greedy(grid: Grid, start: Coord, goal: Coord, h=manhattan): # greedy best-first search
    pq: List[Tuple[float, Coord]] = [(h(start, goal), start)]
    parent: Dict[Coord, Coord] = {}
    visited: Set[Coord] = set()
    expanded = 0

    while pq: # priority queue
        _, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u) # mark as visited
        expanded += 1 # increment expanded nodes
        if u == goal: 
            path = reconstruct(parent, start, goal) # reconstruct path
            return path, len(path) - 1, expanded, False, visited, [v for _, v in pq] 
        for v in neighbors(grid, u): # for each neighbor
            if v not in visited: # if not yet visited
                parent.setdefault(v, u)  # set parent if not already set
                heapq.heappush(pq, (h(v, goal), v)) # push heuristic cost and node to priority queue
    return None, float("inf"), expanded, False, visited, []


def astar(grid: Grid, start: Coord, goal: Coord, h=manhattan): # A* search
    pq: List[Tuple[float, Coord]] = [(h(start, goal), start)]
    parent: Dict[Coord, Coord] = {} 
    best_g: Dict[Coord, float] = {start: 0}
    closed: Set[Coord] = set()
    expanded = 0

    while pq:
        f, u = heapq.heappop(pq)
        if u in closed: # if already expanded, skip
            continue 
        closed.add(u) # mark as expanded
        expanded += 1 # increment expanded nodes
        if u == goal: # if goal reached
            path = reconstruct(parent, start, goal)
            return path, int(best_g[u]), expanded, True, closed, [v for _, v in pq]
        for v in neighbors(grid, u): # for each neighbor
            ng = best_g[u] + 1 
            if v not in best_g or ng < best_g[v]: # if new cost is better
                best_g[v] = ng # update best cost to reach v
                parent[v] = u # set parent
                heapq.heappush(pq, (ng + h(v, goal), v)) 
    return None, float("inf"), expanded, False, closed, [] 


# -----------------------------
# flag definitions & main
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="Solve the Pumpkin Pie Maze with various searches.") # argument parser
    parser.add_argument("--maze", required=True, help="Path to ASCII maze file") # maze file path
    parser.add_argument("--algo", required=True, choices=["bfs", "dfs", "ucs", "greedy", "astar"], help="Algorithm")
    parser.add_argument("--heuristic", choices=["manhattan", "euclidean"], default="manhattan")
    parser.add_argument("--outdir", default="outputs", help="Directory for annotated outputs")
    args = parser.parse_args() 

    grid, start, goal = read_grid(args.maze)
    heuristic = manhattan if args.heuristic == "manhattan" else euclidean

    if args.algo == "bfs":
        path, cost, expanded, optimal, explored, frontier = bfs(grid, start, goal)
        outname = "pumpkinpie-BFS.txt"
    elif args.algo == "dfs":
        path, cost, expanded, optimal, explored, frontier = dfs(grid, start, goal)
        outname = "pumpkinpie-DFS.txt"
    elif args.algo == "ucs":
        path, cost, expanded, optimal, explored, frontier = ucs(grid, start, goal)
        outname = "pumpkinpie-UCS.txt"
    elif args.algo == "greedy":
        path, cost, expanded, optimal, explored, frontier = greedy(grid, start, goal, heuristic)
        outname = "pumpkinpie-Greedy.txt"
    else:  
        path, cost, expanded, optimal, explored, frontier = astar(grid, start, goal, heuristic)
        outname = "pumpkinpie-Astar.txt"

    print(f"Algorithm: {args.algo.upper()}")
    print(f"Path cost: {cost}")
    print(f"Nodes expanded: {expanded}")
    print(f"Optimal (claimed): {optimal}")
    if path:
        print(f"Path length: {len(path)} (including start+goal)")
    else:
        print("No path found.")

    annotate_and_write( # annotate the maze and write to file
        grid,
        start,
        goal,
        path,
        explored,
        os.path.join(args.outdir, outname),
        frontier,
    )
    print(f"Annotated maze written to {os.path.join(args.outdir, outname)}")


if __name__ == "__main__": # main entry point
    main()
