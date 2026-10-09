*This project has been created as part of the 42 curriculum by: lelouren*

# Description
Fly-in is a drone routing simulation. It reads a map of connected zones and moves a fleet of drones from a start zone to an end zone in as few turns as possible, while respecting zone and connection capacities. Paths are found with Dijkstra's algorithm, written from scratch.

# Instructions
1. Clone the repository: <br> 
`git clone https://github.com/educate-llourens/Fly_in.git`

2. Install the necessary packages and dependencies: <br>
`make install`

3. Activate the virtual environment: <br>
`activate .venv/bin/activate`

4. Run the program with the default map with: <br>
`make`

5. Run the program with a custom map using: <br>
`make MAP="folders/map_path.txt"`

# Resources
## Documentation
[Pydantic Documentation](https://pydantic.dev/docs/validation/latest/get-started/)<br>
[Rich documentation](https://rich.readthedocs.io)<br>
## Articles and other research
[Graph theory](https://en.wikipedia.org/wiki/Graph_theory) <br>
[Adjacency Medium article](https://medium.com/@ging.m.louie/easy-python-implementation-of-a-graph-as-an-adjacency-list-ced5ff4fecc8) <br>
[Implement adjacency matrix in Python](https://ssojet.com/data-structures/implement-adjacency-matrix-in-python#adding-edges-to-the-matrix) <br>
[Dijkstra's algorithm, Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) <br>
[Path finding, Wikipedia](https://en.wikipedia.org/wiki/Pathfinding) <br>

## AI Usage
- Creating lessons for parts of the project using a combination of scaffolding and demonstration first teaching methods. No code answers that I can copy into my project.
- Q & A sessions about topics throughout the project
- Creating quizzes and notes for learning
*The goal is long term learning and retention built around repition and how I learn best*

# Algorithm explanation
## Pathfinding: Dijkstra's algorithm

### What it does

Finds the cheapest route from the start hub to the end hub. The cost of a route is the sum of the costs of the hubs a drone enters along the way. Blocked hubs are never entered.

### Why Dijkstra

- Hub costs are not all equal (restricted zones take 2 turns), so a plain breadth-first search would not find the cheapest route.
- Costs are never negative, which Dijkstra requires.
- It is simple to write ourselves, since graph libraries are forbidden.

### Data structures

| Name | Type | Purpose |
|---|---|---|
| `cost` | `dict[str, int]` | Cheapest known cost to reach each hub |
| `previous` | `dict[str, str]` | For each hub, which hub we came from on the cheapest route |
| `working_list` | min-heap of `(cost, name)` | Hubs still to explore, cheapest first |
| `visited` | `set[str]` | Hubs whose cheapest cost is final |

### How it works

1. Start with the start hub at cost 0.
2. Take the cheapest hub from the heap.
3. If we have seen it already, skip it.
4. If it is the goal, stop.
5. For each connection of the current hub, look at the hub at its end. Skip it if it is blocked or already visited.
6. Work out the cost of reaching that hub through the current hub. If it is cheaper than the best known cost, record it and push it onto the heap.
7. After the loop, follow `previous` from the goal back to the start, then reverse the list to get the path.

### How connections are read

A connection is stored as a start hub and an end hub, in the order written in the map file. The algorithm moves from the start hub of a connection to its end hub. Maps are therefore expected to list each connection in the direction drones travel (towards the goal).

### Spreading drones across paths

One cheapest path would send every drone the same way. After each drone gets its path, every hub on that path (except start and goal) gets a penalty added to its cost. The next drone sees that route as more expensive and may pick another one. This spreads drones over the available routes, and it is the main reason the turn counts are low.

### Complexity

With V hubs and E connections:

- **Time:** O((V + E) log V) per drone.
- **Memory:** O(V + E) for the graph, plus O(V) for the tables above.
- **Paths are calculated once** per drone before the simulation starts, not every turn.

### Results

| Map | Drones | Target (turns) | My result |
|---|---|---|---|
| 01 Linear path | 2 | ≤ 6 | 4 |
| 02 Simple fork | 4 | ≤ 8 | 4 |
| 03 Basic capacity | 4 | ≤ 6 | 4 |
| Dead end trap | 5 | ≤ 12 | 8 |
| Circular loop | 6 | ≤ 15 | 12 |
| Priority puzzle | 5 | ≤ 12 | 8 |
| Maze nightmare | 8 | ≤ 30 | 14 |
| Capacity hell | 12 | ≤ 35 | 16 |
| Ultimate challenge | 15 | ≤ 45 | 27 |

### Limitations

- The congestion penalty is a heuristic. It does not guarantee the minimum number of turns on every map.
- Connections are followed in the direction they are written in the map file.
- If the goal cannot be reached, path reconstruction fails.

# Visual representation and how it enhances the user experience
## What I did
The program prints the settings information that it collected from the map file. This makes it easy to check if there has been a mistake. During each turn the drone prints it's movement in the form of:
drone id: start_hub -> end hub | number of drones / maximum allowed at the hub | number of drones on the connection / maximum number allowed and finally the status of the drone if it is waiting and how many turns it has been waiting on the connection.
## What I would have liked to do with more time
I would have loved to play with pygame to create a visual represenation of the simulation. This would have made understanding a lot clearer.

# Challenges faced
## Challenges faced

### Pathfinding

- **No path found.** Dijkstra compared the new cost to the current hub's cost instead of the next hub's, so no route was ever recorded. Comparing against the next hub fixed it.
- **Wrong hub explored first.** The heap sorted by hub name instead of cost. Storing `(cost, name)` tuples made the cheapest hub come out first.
- **Negative costs.** Hub cost was `turn_cost - priority`, which went below zero and breaks Dijkstra. Costs are now always positive, with priority zones only slightly cheaper than normal ones.
- **All drones took the same route.** Every drone had the same cheapest path. Adding a penalty to the hubs of each assigned path pushes the next drone towards another route.
- **Penalties kept growing.** Paths were recalculated every turn. They are now calculated once, before the simulation starts.

### Simulation

- **Wrong turn count.** `move_drones()` was called inside a loop over the drones, so one printed turn held several real ones. It is now called once per turn.
- **Hard-to-read movement code.** One long function did everything. It was split into small methods with one job each.
- **Finding a connection in both directions.** Comparing start to start and end to end only worked in the file's order. Comparing the set of both end names fixed it.
- **Restricted zones.** The 2-turn counter was never reset after crossing, so a second restricted zone would be crossed instantly. It now resets on arrival.

### Parsing and display

- **Unknown colour names.** `rich` rejects names like `brown`, but the brief allows any colour word. Known names are mapped to `rich` equivalents, and anything else falls back to the default style.
- **Colour never applied.** A comparison (`==`) was used where an assignment (`=`) was needed. mypy caught it.

### Typing and tooling

- **Optional type in a nested function.** mypy forgets a `None` check inside a nested function. Declaring a plain type after the check solved it.
- **`heappush` type error.** A list was pushed where the hint said tuple. Pushing a tuple fixed it.
- **Validator return type.** A typo in the nested class name caused an error. `Self` removed the need to name the class.
- **Makefile lint error.** A missing closing quote in the mypy command.
- **mypy "file found twice".** Mixed import styles for one module. Adding `__init__.py` to `src/` and using one style fixed it.

# Testing strategy
Visual testing as I went. Again with more time I would have liked to do a test first approach with pytest.

## Moulinette
N/A

# New Tools
[rich](https://rich.readthedocs.io/en/latest/logging.html)