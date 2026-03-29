import heapq                      # For priority queues (UCS, A*)
from collections import deque     # For BFS queue

CITY_GRAPH = {
    "A": [("B", 4), ("D", 6)],
    "B": [("A", 4), ("C", 3), ("E", 2)],
    "C": [("B", 3), ("F", 5)],          # ← Hospital C
    "D": [("A", 6), ("E", 1), ("G", 8)],
    "E": [("B", 2), ("D", 1), ("F", 7)],
    "F": [("C", 5), ("E", 7), ("I", 3)],
    "G": [("D", 8), ("H", 2)],
    "H": [("G", 2), ("I", 4)],
    "I": [("F", 3), ("H", 4)],           # ← Hospital I
}

#  HOSPITALS in the city

HOSPITALS = ["C", "I"]
HEURISTIC = {
    # h(node, "C")  — estimated time to Hospital C
    "C": {"A": 7, "B": 3, "C": 0, "D": 8, "E": 5, "F": 5, "G": 14, "H": 11, "I": 8},
    # h(node, "I")  — estimated time to Hospital I
    "I": {"A": 14, "B": 10, "C": 8, "D": 9, "E": 8, "F": 3, "G": 6, "H": 4, "I": 0},
}


def apply_traffic(graph: dict, factor: float) -> dict:
    """
    Returns a NEW graph with all edge weights multiplied by
    the given traffic factor.
    factor=1.0  → normal
    factor=1.5  → moderate traffic (50% slower)
    factor=2.0  → heavy traffic (twice as slow)
    """
    traffic_graph = {}
    for node, neighbours in graph.items():
        traffic_graph[node] = [(nb, round(w * factor, 2)) for nb, w in neighbours]
    return traffic_graph


#  ROAD BLOCKING

def block_roads(graph: dict, blocked: list) -> dict:
    """
    Returns a NEW graph with the listed roads removed.
    blocked: list of (node1, node2) tuples — order does not matter.
    """
    blocked_set = {frozenset(pair) for pair in blocked}
    new_graph = {}
    for node, neighbours in graph.items():
        new_graph[node] = [
            (nb, w) for nb, w in neighbours
            if frozenset((node, nb)) not in blocked_set
        ]
    return new_graph



#  ALGORITHM 1 — BREADTH-FIRST SEARCH (BFS)

def bfs(graph: dict, start: str, goal: str) -> dict:
    """
    Breadth-First Search.
    Returns a dict with keys: path, cost, nodes_explored.
    """
    # Queue stores: (current_node, path_so_far, total_cost)
    queue = deque()
    queue.append((start, [start], 0))

    visited = set()          # Nodes already expanded
    nodes_explored = 0

    while queue:
        current, path, cost = queue.popleft()

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        # ── GOAL CHECK ──
        if current == goal:
            return {
                "path": path,
                "cost": cost,
                "nodes_explored": nodes_explored
            }

        # ── EXPAND neighbours ──
        for neighbour, weight in graph.get(current, []):
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour], cost + weight))

    # No path found
    return {"path": None, "cost": float("inf"), "nodes_explored": nodes_explored}

#  ALGORITHM 2 — UNIFORM COST SEARCH  (UCS / Dijkstra)

def ucs(graph: dict, start: str, goal: str) -> dict:
    """
    Uniform Cost Search (Dijkstra's algorithm).
    Returns a dict with keys: path, cost, nodes_explored.
    """
    # Heap stores: (cumulative_cost, node, path_so_far)
    heap = []
    heapq.heappush(heap, (0, start, [start]))

    visited = set()
    nodes_explored = 0

    while heap:
        cost, current, path = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        # ── GOAL CHECK ──
        if current == goal:
            return {
                "path": path,
                "cost": cost,
                "nodes_explored": nodes_explored
            }

        # ── EXPAND neighbours ──
        for neighbour, weight in graph.get(current, []):
            if neighbour not in visited:
                new_cost = cost + weight
                heapq.heappush(heap, (new_cost, neighbour, path + [neighbour]))

    return {"path": None, "cost": float("inf"), "nodes_explored": nodes_explored}

#  ALGORITHM 3 — A* SEARCH

def astar(graph: dict, start: str, goal: str,
          heuristic: dict) -> dict:
    """
    A* Search.
    heuristic: dict mapping node → estimated cost to goal.
    Returns a dict with keys: path, cost, nodes_explored.
    """
    # h(node) — look up heuristic for the goal
    def h(node):
        return heuristic.get(goal, {}).get(node, 0)

    # Heap stores: (f_cost, g_cost, node, path_so_far)
    heap = []
    g_start = 0
    f_start = g_start + h(start)
    heapq.heappush(heap, (f_start, g_start, start, [start]))

    visited = set()
    nodes_explored = 0

    while heap:
        f, g, current, path = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        # ── GOAL CHECK ──
        if current == goal:
            return {
                "path": path,
                "cost": g,
                "nodes_explored": nodes_explored
            }

        # ── EXPAND neighbours ──
        for neighbour, weight in graph.get(current, []):
            if neighbour not in visited:
                new_g = g + weight
                new_f = new_g + h(neighbour)
                heapq.heappush(heap,
                               (new_f, new_g, neighbour, path + [neighbour]))

    return {"path": None, "cost": float("inf"), "nodes_explored": nodes_explored}

#  NEAREST HOSPITAL FINDER

def find_nearest_hospital(graph: dict, start: str) -> str:
    """
    Runs UCS from `start` to every hospital and returns the
    hospital with the lowest travel cost.
    """
    best_hospital = None
    best_cost = float("inf")

    for hospital in HOSPITALS:
        if hospital == start:
            return hospital        # Already at a hospital
        result = ucs(graph, start, hospital)
        if result["cost"] < best_cost:
            best_cost = result["cost"]
            best_hospital = hospital

    return best_hospital

#  DISPLAY HELPERS

def print_banner():
    print("\n" + "=" * 60)
    print("        EMERGENCY AMBULANCE ROUTING SYSTEM ")
    print("        AI-Powered Fastest Route Finder")
    print("=" * 60)


def print_city_map():
    print("""
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
  Locations : A  B  C  D  E  F  G  H  I
  Hospitals : C  I
""")


def print_result(algo_name: str, result: dict):
    print(f"\n  ┌─ {algo_name} ─────────────────────────────────")
    if result["path"]:
        path_str = " → ".join(result["path"])
        print(f"  │  Route         : {path_str}")
        print(f"  │  Total time    : {result['cost']} minutes")
        print(f"  │  Nodes explored: {result['nodes_explored']}")
    else:
        print(f"  │  No path found!")
        print(f"  │  Nodes explored: {result['nodes_explored']}")
    print("  └─────────────────────────────────────────────")


def print_comparison(results: dict):
    print("\n   ALGORITHM COMPARISON")
    print("  " + "─" * 55)
    print(f"  {'Algorithm':<12} {'Cost (min)':<14} {'Nodes Explored':<16} {'Status'}")
    print("  " + "─" * 55)
    for name, res in results.items():
        status = " Found" if res["path"] else " Not Found"
        cost   = res["cost"] if res["path"] else "N/A"
        print(f"  {name:<12} {str(cost):<14} {str(res['nodes_explored']):<16} {status}")
    print("  " + "─" * 55)

    # Highlight winner
    valid = {n: r for n, r in results.items() if r["path"]}
    if valid:
        winner = min(valid, key=lambda n: valid[n]["nodes_explored"])
        print(f"\n   Most efficient (fewest nodes explored): {winner}")
        fastest = min(valid, key=lambda n: valid[n]["cost"])
        print(f"   Shortest travel time               : {fastest} "
              f"({valid[fastest]['cost']} min)")


# ─────────────────────────────────────────────────────────────
#  INPUT HELPERS
# ─────────────────────────────────────────────────────────────
def get_valid_node(prompt: str, graph: dict) -> str:
    while True:
        node = input(prompt).strip().upper()
        if node in graph:
            return node
        print(f"   '{node}' is not on the map. "
              f"Valid locations: {', '.join(sorted(graph.keys()))}")


def get_algorithm_choice() -> str:
    options = {"1": "BFS", "2": "UCS", "3": "A*", "4": "ALL"}
    while True:
        print("\n  Choose algorithm:")
        print("    1. BFS  (Breadth-First Search)")
        print("    2. UCS  (Uniform Cost Search / Dijkstra)")
        print("    3. A*   (A-Star Search)")
        print("    4. ALL  (Run all three + comparison)")
        choice = input("  Enter choice (1/2/3/4): ").strip()
        if choice in options:
            return options[choice]
        print("   Please enter 1, 2, 3, or 4.")


def get_traffic_factor() -> float:
    print("\n  Traffic conditions:")
    print("    1. Clear roads     (×1.0)")
    print("    2. Moderate traffic (×1.5)")
    print("    3. Heavy traffic    (×2.0)")
    while True:
        choice = input("  Enter choice (1/2/3): ").strip()
        if choice == "1": return 1.0
        if choice == "2": return 1.5
        if choice == "3": return 2.0
        print("    Please enter 1, 2, or 3.")


def get_blocked_roads(graph: dict) -> list:
    print("\n  Block any roads? (e.g. A-B, D-E  or press Enter to skip)")
    raw = input("  Enter roads to block: ").strip()
    if not raw:
        return []
    blocked = []
    nodes = set(graph.keys())
    for pair in raw.replace(" ", "").split(","):
        parts = pair.upper().split("-")
        if len(parts) == 2 and parts[0] in nodes and parts[1] in nodes:
            blocked.append((parts[0], parts[1]))
        else:
            print(f"   Skipping invalid road '{pair}'.")
    return blocked

#  MAIN PROGRAM

def main():
    print_banner()
    print_city_map()

    # 1. Traffic & road conditions 
    factor  = get_traffic_factor()
    blocked = get_blocked_roads(CITY_GRAPH)

    # Build the working graph
    graph = apply_traffic(CITY_GRAPH, factor)
    if blocked:
        graph = block_roads(graph, blocked)
        print(f"\n  Blocked roads: "
              f"{', '.join('-'.join(p) for p in blocked)}")
    if factor != 1.0:
        print(f"  Traffic factor applied: ×{factor}")

    # 2. Start location 
    print()
    start = get_valid_node("  Enter accident location (start): ", graph)

    # 3. Hospital selection 
    print(f"\n  Hospitals available: {', '.join(HOSPITALS)}")
    use_nearest = input("  Auto-select NEAREST hospital? (y/n): ").strip().lower()

    if use_nearest == "y":
        goal = find_nearest_hospital(graph, start)
        if goal is None:
            print("  No hospital is reachable from your location!")
            return
        print(f"  Nearest hospital selected: {goal}")
    else:
        goal = get_valid_node(
            f"  Enter hospital location {HOSPITALS}: ", graph
        )
        if goal not in HOSPITALS:
            print(f"  ⚠  '{goal}' is not a hospital, "
                  f"but routing anyway...")

    if start == goal:
        print("\n  Ambulance is already at the hospital!")
        return

    # 4. Algorithm selection 
    algo = get_algorithm_choice()

    print(f"\n  Routing from  '{start}'  →  '{goal}'  ...")
    print("=" * 60)

    # 5. Run algorithm(s) 
    results = {}

    if algo in ("BFS", "ALL"):
        results["BFS"] = bfs(graph, start, goal)
        print_result("BFS  (Breadth-First Search)", results["BFS"])

    if algo in ("UCS", "ALL"):
        results["UCS"] = ucs(graph, start, goal)
        print_result("UCS  (Uniform Cost Search)", results["UCS"])

    if algo in ("A*", "ALL"):
        results["A*"] = astar(graph, start, goal, HEURISTIC)
        print_result("A*   (A-Star Search)", results["A*"])

    if algo == "ALL" and results:
        print_comparison(results)

    best_result = None
    best_name   = None
    for name in ("A*", "UCS", "BFS"):         # priority order
        if name in results and results[name]["path"]:
            best_result = results[name]
            best_name   = name
            break

    if best_result:
        print(f"\n  DISPATCH ORDER  ({best_name} recommended route)")
        print(f"     Route : {' → '.join(best_result['path'])}")
        print(f"     ETA   : {best_result['cost']} minutes")
    else:
        print("\n  No route found! Check for disconnected graph "
              "or too many blocked roads.")

    again = input("\n  Run another search? (y/n): ").strip().lower()
    if again == "y":
        main()
    else:
        print("\n  Stay safe!  Goodbye.\n")


if __name__ == "__main__":
    main()