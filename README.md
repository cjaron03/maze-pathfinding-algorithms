# Maze Pathfinding Algorithms

A Python implementation of classic pathfinding algorithms for solving ASCII mazes. This project demonstrates and compares five different search algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS), Greedy Best-First Search, and A* Search.

## Features

- **Five search algorithms**: BFS, DFS, UCS, Greedy, and A*
- **Multiple heuristics**: Manhattan and Euclidean distance for informed search algorithms
- **Visual output**: Annotated ASCII mazes showing the solution path and explored nodes
- **Performance metrics**: Tracks path cost, nodes expanded, and optimality
- **Flexible input**: Supports any ASCII maze format with walls (`#`), start (`S`), goal (`G`), and open spaces (`.` or space)

## Requirements

- Python 3.7 or higher
- Standard library only (no external dependencies)

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd maze-pathfinding-algorithms
```

No additional installation required - the project uses only Python standard library.

## Usage

### Basic Usage

Run a search algorithm on a maze:

```bash
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo bfs
```

### Available Algorithms

- `bfs` - Breadth-First Search
- `dfs` - Depth-First Search
- `ucs` - Uniform Cost Search
- `greedy` - Greedy Best-First Search
- `astar` - A* Search

### Command-Line Options

```bash
python pumpkin_pie_maze.py --maze <maze_file> --algo <algorithm> [options]
```

**Required arguments:**
- `--maze`: Path to ASCII maze file
- `--algo`: Algorithm to use (`bfs`, `dfs`, `ucs`, `greedy`, `astar`)

**Optional arguments:**
- `--heuristic`: Heuristic for informed search algorithms (`manhattan` or `euclidean`, default: `manhattan`)
- `--outdir`: Output directory for annotated mazes (default: `outputs`)

### Examples

```bash
# Breadth-First Search
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo bfs

# Depth-First Search
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo dfs

# Uniform Cost Search
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo ucs

# Greedy Best-First Search with Manhattan heuristic
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo greedy --heuristic manhattan

# A* Search with Euclidean heuristic
python pumpkin_pie_maze.py --maze data/pumpkin.txt --algo astar --heuristic euclidean
```

## Output Format

The program generates annotated ASCII maze files in the `outputs/` directory. Each output file shows:

- `#` - Walls
- `S` - Start position
- `G` - Goal position
- `+` - Solution path
- ` ` (space) - Explored nodes (closed set)
- `O` - Frontier nodes (when captured)
- `.` - Existing dots in the original maze

The output also includes:
- Path cost
- Number of nodes expanded
- Whether the solution is optimal (for algorithms that guarantee optimality)
- Path length

## Maze File Format

Maze files should be ASCII text files with:
- `#` for walls
- `S` for start position (exactly one)
- `G` for goal position (exactly one)
- `.` or space for open cells
- Rectangular grid (will be padded with walls if needed)

## Project Structure

```
.
├── pumpkin_pie_maze.py    # Main maze solver with all algorithms
├── format_outputs.py       # Utility to format output files
├── data/
│   └── pumpkin.txt        # Example maze file
├── outputs/               # Generated annotated mazes
│   ├── pumpkinpie-BFS.txt
│   ├── pumpkinpie-DFS.txt
│   ├── pumpkinpie-UCS.txt
│   ├── pumpkinpie-Greedy.txt
│   └── pumpkinpie-Astar.txt
└── README.md
```

## Algorithms Overview

### Breadth-First Search (BFS)
- Uses a queue (FIFO)
- Guarantees shortest path (optimal for unweighted graphs)
- Explores all nodes at depth `d` before depth `d+1`

### Depth-First Search (DFS)
- Uses a stack (LIFO)
- Not optimal, but memory efficient
- Explores as deep as possible before backtracking

### Uniform Cost Search (UCS)
- Uses a priority queue ordered by path cost
- Guarantees optimal solution for weighted graphs
- Equivalent to Dijkstra's algorithm

### Greedy Best-First Search
- Uses a priority queue ordered by heuristic value
- Not optimal, but often fast
- Chooses the node closest to the goal (by heuristic)

### A* Search
- Uses a priority queue ordered by `f(n) = g(n) + h(n)`
- Guarantees optimal solution with admissible heuristics
- Balances path cost and heuristic estimate

## Heuristics

- **Manhattan Distance**: `|x1 - x2| + |y1 - y2|` (L1 norm)
- **Euclidean Distance**: `√((x1 - x2)² + (y1 - y2)²)` (L2 norm)

Both heuristics are admissible (never overestimate) for 4-way movement in a grid.

## License

This project is part of a CS445 (Artificial Intelligence) course assignment.
