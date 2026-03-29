# ResQPath : Emergency Ambulance Routing System using AI Search Algorithms

> A command-line Python application that simulates an ambulance finding the fastest route from an accident location to a hospital, using three classic AI search algorithms: **BFS**, **UCS (Dijkstra)**, and **A\***.

---

## Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [City Map](#-city-map)
4. [Algorithms Implemented](#-algorithms-implemented)
5. [Project Structure](#-project-structure)
6. [Prerequisites](#-prerequisites)
7. [Environment Setup](#-environment-setup)
8. [How to Run](#-how-to-run)
9. [Step-by-Step Usage Guide](#-step-by-step-usage-guide)
10. [Sample Output](#-sample-output)
11. [Algorithm Comparison](#-algorithm-comparison)
12. [Time Complexity](#-time-complexity)
13. [Extra Features](#-extra-features)
14. [Troubleshooting](#-troubleshooting)

---

## Project Overview

This project models a city as a **weighted graph** where:

| Graph Element | Real-World Meaning        |
|---------------|---------------------------|
| **Node**      | A location in the city    |
| **Edge**      | A road connecting two locations |
| **Weight**    | Travel time in minutes    |

An ambulance starts at an accident location and must reach the nearest (or chosen) hospital as fast as possible. The program runs three AI search algorithms and lets you compare their efficiency side by side.

**No GUI. No internet. No external libraries.** Everything runs in your terminal.

---

##  Features

-  Three search algorithms: BFS, UCS, A\*
-  Two hospitals in the city — auto-select the nearest one
-  Traffic simulation — scale all road times by a traffic factor
-  Road blocking — close specific roads to simulate accidents or construction
-  Side-by-side algorithm comparison table
-  Full input validation with helpful error messages
-  Run multiple searches without restarting the program

---

## City Map

The city has **9 locations (A–I)** and **2 hospitals (C and I)**:

```
  A ──4── B ──3── C*
  │        │        │
  6        2        5
  │        │        │
  D ──1── E ──7── F
  │                 │
  8                 3
  │                 │
  G ──2── H ──4── I*
```

- `*` marks a **hospital**
- Numbers on edges represent **travel time in minutes**
- Locations: `A  B  C  D  E  F  G  H  I`
- Hospitals: `C` and `I`

---

##  Algorithms Implemented

### 1. Breadth-First Search (BFS)
- Explores nodes **level by level** using a FIFO queue
- Finds the path with the **fewest road segments** (hops)
- Does **not** consider edge weights — may not find the fastest route

### 2. Uniform Cost Search (UCS / Dijkstra)
- Explores nodes by **lowest cumulative travel time** using a min-heap
- Guarantees the **optimal (shortest time) path**
- Explores more nodes than A\* because it has no directional guidance

### 3. A\* Search
- Combines UCS with a **heuristic** estimate of remaining distance
- Formula: `f(n) = g(n) + h(n)`
  - `g(n)` = actual cost from start to node n
  - `h(n)` = estimated cost from n to the goal (hardcoded straight-line estimates)
- Explores the **fewest nodes** while still finding the optimal path

---

## Project Structure

```
emergency-ambulance-routing/
│
└── main.py          ← The entire program (single file, fully self-contained)
```

All logic is in `main.py`, organized into clean, modular functions:

```
main.py
 ├── CITY_GRAPH          — Adjacency list representing the city
 ├── HOSPITALS           — List of hospital nodes
 ├── HEURISTIC           — Pre-computed h(n) values for A*
 ├── apply_traffic()     — Traffic simulation
 ├── block_roads()       — Road closure simulation
 ├── bfs()               — Breadth-First Search algorithm
 ├── ucs()               — Uniform Cost Search algorithm
 ├── astar()             — A* Search algorithm
 ├── find_nearest_hospital() — Auto-select closest hospital
 ├── print_*()           — Display helpers
 └── main()              — Program entry point
```

---

## Prerequisites

| Requirement    | Details                                    |
|----------------|--------------------------------------------|
| **Python**     | Version **3.7 or higher**                  |
| **Libraries**  | None — uses only Python's standard library |
| **OS**         | Windows, macOS, or Linux                   |
| **Terminal**   | Any command prompt / terminal / shell      |

> **No pip install needed.** This project uses only built-in Python modules (`heapq`, `collections`).

---

## Environment Setup

### Step 1 — Check if Python is installed

Open your terminal (Command Prompt, PowerShell, Terminal, or bash) and run:

```bash
python --version
```

You should see something like:

```
Python 3.11.2
```

If you get `command not found` or a version below 3.7, install Python first:

- **Download:** https://www.python.org/downloads/
- During installation on Windows, check **"Add Python to PATH"**

> On some systems you may need to use `python3` instead of `python`. Both work.

---

### Step 2 — Download the project file

**Option A — If you have the file already:**  
Place `main.py` in any folder of your choice.

**Option B — If cloning from a repository:**

```bash
git clone https://github.com/your-username/emergency-ambulance-routing.git
cd emergency-ambulance-routing
```

---

### Step 3 — Navigate to the project folder

```bash
# Example on Windows
cd C:\Users\YourName\Downloads\emergency-ambulance-routing

# Example on macOS / Linux
cd ~/Downloads/emergency-ambulance-routing
```

---

### Step 4 — Verify the file is present

```bash
# Windows
dir

# macOS / Linux
ls
```

You should see `main.py` listed.

---

## How to Run

```bash
python main.py
```

Or, if your system uses `python3`:

```bash
python3 main.py
```

The program will start immediately in your terminal — no additional configuration required.

---

## Step-by-Step Usage Guide

Once the program starts, it will guide you through the following steps:

---

### Step 1 — View the City Map

The map is printed automatically at startup. Study the layout before making choices.

---

### Step 2 — Choose Traffic Conditions

```
Traffic conditions:
  1. Clear roads      (×1.0)
  2. Moderate traffic (×1.5)
  3. Heavy traffic    (×2.0)
Enter choice (1/2/3):
```

- Enter `1` for normal roads (default)
- Enter `2` to simulate moderate traffic (all times ×1.5)
- Enter `3` to simulate heavy traffic (all times ×2.0)

---

### Step 3 — Block Roads (Optional)

```
Block any roads? (e.g. A-B, D-E  or press Enter to skip)
Enter roads to block:
```

- Press **Enter** to skip (no roads blocked)
- Type road pairs separated by commas to block them, e.g.: `A-B, D-E`
- Blocked roads are removed from the graph for this session

---

### Step 4 — Enter the Accident Location

```
Enter accident location (start):
```

Type any valid location: `A`, `B`, `C`, `D`, `E`, `F`, `G`, `H`, or `I`

> Input is case-insensitive — `a` and `A` both work.

---

### Step 5 — Choose Hospital

```
Hospitals available: C, I
Auto-select NEAREST hospital? (y/n):
```

- Enter `y` — the program uses UCS to find and select the closest hospital automatically
- Enter `n` — you will be asked to type a hospital location manually (`C` or `I`)

---

### Step 6 — Choose Algorithm

```
Choose algorithm:
  1. BFS  (Breadth-First Search)
  2. UCS  (Uniform Cost Search / Dijkstra)
  3. A*   (A-Star Search)
  4. ALL  (Run all three + comparison)
Enter choice (1/2/3/4):
```

- Enter `1`, `2`, or `3` to run a single algorithm
- Enter `4` to run all three and see a comparison table (recommended)

---

### Step 7 — View Results

The program displays for each algorithm:
- The full route (e.g., `A → D → E → B → C`)
-  Total travel time in minutes
-  Number of nodes explored (efficiency measure)

---

### Step 8 — Run Again or Exit

```
Run another search? (y/n):
```

- Enter `y` to restart from the beginning
- Enter `n` to exit

---

## Sample Output

**Scenario:** Accident at `A`, road `A-B` blocked, moderate traffic (×1.5), all algorithms

```
============================================================
     EMERGENCY AMBULANCE ROUTING SYSTEM  
        AI-Powered Fastest Route Finder
============================================================

  CITY MAP  (travel times in minutes)
  ─────────────────────────────────────────────────────
   A ──4── B ──3── C*
   │        │        │
   6        2        5
   │        │        │
   D ──1── E ──7── F
   │                 │
   8                 3
   │                 │
   G ──2── H ──4── I*

   * = Hospital   Numbers = travel time (minutes)
  ─────────────────────────────────────────────────────

  Traffic conditions: → 2 (Moderate ×1.5)
  Block roads: → A-B

  Blocked roads: A-B
  Traffic factor applied: ×1.5

  Enter accident location (start): A
  Auto-select NEAREST hospital? (y/n): y
  Nearest hospital selected: C

  Routing from 'A' → 'C' ...
============================================================

  ┌─ BFS  (Breadth-First Search) ───────────────────────
  │  Route         : A → D → E → B → C
  │  Total time    : 18.0 minutes
  │  Nodes explored: 8
  └──────────────────────────────────────────────────────

  ┌─ UCS  (Uniform Cost Search) ────────────────────────
  │  Route         : A → D → E → B → C
  │  Total time    : 18.0 minutes
  │  Nodes explored: 5
  └──────────────────────────────────────────────────────

  ┌─ A*   (A-Star Search) ──────────────────────────────
  │  Route         : A → D → E → B → C
  │  Total time    : 18.0 minutes
  │  Nodes explored: 3
  └──────────────────────────────────────────────────────

  ALGORITHM COMPARISON
  ───────────────────────────────────────────────────────
  Algorithm    Cost (min)     Nodes Explored   Status
  ───────────────────────────────────────────────────────
  BFS          18.0           8                 Found
  UCS          18.0           5                 Found
  A*           18.0           3                 Found
  ───────────────────────────────────────────────────────

  Most efficient (fewest nodes explored): A*
  Shortest travel time: A* (18.0 min)

  DISPATCH ORDER  (A* recommended route)
     Route : A → D → E → B → C
     ETA   : 18.0 minutes

  Run another search? (y/n): n

  Stay safe! Goodbye.
```

---

## Algorithm Comparison

| Property             | BFS         | UCS (Dijkstra) | A\*          |
|----------------------|-------------|----------------|--------------|
| **Uses weights?**    |  No       |  Yes         |  Yes       |
| **Uses heuristic?**  |  No       |  No          |  Yes       |
| **Optimal path?**    |  Not always |  Yes       |  Yes       |
| **Nodes explored**   | Most        | Medium         | Fewest       |
| **Speed in practice**| Slowest     | Medium         | Fastest      |
| **Best for**         | Fewest hops | Guaranteed optimal | Fast + optimal |

**Why A\* wins:** It uses a heuristic `h(n)` — an estimate of the remaining distance to the goal. This guides the search toward the hospital instead of exploring all directions equally. As long as the heuristic never overestimates (admissible), A\* is guaranteed to find the optimal path while exploring fewer nodes than any other algorithm.

---

## Time Complexity

| Algorithm | Time Complexity   | Space Complexity |
|-----------|-------------------|------------------|
| BFS       | O(V + E)          | O(V)             |
| UCS       | O((V + E) log V)  | O(V)             |
| A\*       | O((V + E) log V)  | O(V)             |

- **V** = number of nodes (locations)
- **E** = number of edges (roads)
- A\* has the same worst-case complexity as UCS, but explores far fewer nodes in practice due to heuristic guidance

---

##  Extra Features

###  Traffic Simulation
Multiplies all road weights by a factor to simulate congestion:
- `×1.0` — clear roads
- `×1.5` — moderate traffic
- `×2.0` — heavy traffic

###  Road Blocking
Remove specific roads to simulate closures:
```
Enter roads to block: A-B, D-E
```
Both directions of each road are removed.

### Multiple Hospitals + Auto-Select
The city has two hospitals (`C` and `I`). When auto-select is enabled, the program runs UCS to both and picks the one with the lowest travel cost from the accident location.

---

##  Troubleshooting

| Problem | Solution |
|--------|----------|
| `python: command not found` | Use `python3 main.py` instead |
| `SyntaxError` on startup | Ensure Python version is 3.7 or higher (`python --version`) |
| `No path found` | You may have blocked too many roads or the graph is disconnected — try fewer blocked roads |
| Invalid location entered | Only `A` through `I` are valid. Input is case-insensitive |
| Program closes immediately | Run from terminal/command prompt, not by double-clicking the file |
