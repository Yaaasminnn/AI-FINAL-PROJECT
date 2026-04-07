import heapq
import time
from collections import deque

# Goal state
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Possible moves
moves = ['U', 'D', 'L', 'R']


# Puzzle State Class
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


# Heuristic (Manhattan Distance)
def heuristic(board):
    distance = 0
    for i in range(9):
        if board[i] == 0:
            continue
        goal_pos = board[i] - 1
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_pos, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


# Move Tile
def move_tile(board, move, blank_pos):
    new_board = board[:]
    swap = blank_pos

    if move == 'U':
        swap = blank_pos - 3
    elif move == 'D':
        swap = blank_pos + 3
    elif move == 'L':
        swap = blank_pos - 1
    elif move == 'R':
        swap = blank_pos + 1

    new_board[blank_pos], new_board[swap] = new_board[swap], new_board[blank_pos]
    return new_board


# Print Board
def print_board(board):
    for i in range(0, 9, 3):
        print(board[i:i+3])
    print()


# Get Solution Path
def get_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    return path[::-1]


# BFS
def bfs(start_state):
    queue = deque([PuzzleState(start_state, None, None, 0, 0)])
    visited = set()
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        if current.board == goal_state:
            return current, nodes_expanded

        visited.add(tuple(current.board))
        blank_pos = current.board.index(0)

        for move in moves:
            if move == 'U' and blank_pos < 3: continue
            if move == 'D' and blank_pos > 5: continue
            if move == 'L' and blank_pos % 3 == 0: continue
            if move == 'R' and blank_pos % 3 == 2: continue

            new_board = move_tile(current.board, move, blank_pos)

            if tuple(new_board) not in visited:
                queue.append(PuzzleState(new_board, current, move, current.depth + 1, 0))

    return None, nodes_expanded


# DFS (Depth-Limited)
def dfs(start_state, limit=50):
    stack = [PuzzleState(start_state, None, None, 0, 0)]
    visited = set()
    nodes_expanded = 0

    while stack:
        current = stack.pop()
        nodes_expanded += 1

        if current.board == goal_state:
            return current, nodes_expanded

        if current.depth > limit:
            continue

        visited.add(tuple(current.board))
        blank_pos = current.board.index(0)

        for move in moves:
            if move == 'U' and blank_pos < 3: continue
            if move == 'D' and blank_pos > 5: continue
            if move == 'L' and blank_pos % 3 == 0: continue
            if move == 'R' and blank_pos % 3 == 2: continue

            new_board = move_tile(current.board, move, blank_pos)

            if tuple(new_board) not in visited:
                stack.append(PuzzleState(new_board, current, move, current.depth + 1, 0))

    return None, nodes_expanded


# A* Search
def a_star(start_state):
    open_list = []
    closed_list = set()
    nodes_expanded = 0

    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic(start_state)))

    while open_list:
        current = heapq.heappop(open_list)
        nodes_expanded += 1

        if current.board == goal_state:
            return current, nodes_expanded

        closed_list.add(tuple(current.board))
        blank_pos = current.board.index(0)

        for move in moves:
            if move == 'U' and blank_pos < 3: continue
            if move == 'D' and blank_pos > 5: continue
            if move == 'L' and blank_pos % 3 == 0: continue
            if move == 'R' and blank_pos % 3 == 2: continue

            new_board = move_tile(current.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue

            new_state = PuzzleState(
                new_board,
                current,
                move,
                current.depth + 1,
                current.depth + 1 + heuristic(new_board)
            )

            heapq.heappush(open_list, new_state)

    return None, nodes_expanded


# Solvability Check
def is_solvable(board):
    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if board[i] and board[j] and board[i] > board[j]:
                inv_count += 1
    return inv_count % 2 == 0


# Run All Algorithms
def run_all(initial_state):
    print("Initial State:")
    print_board(initial_state)

    if not is_solvable(initial_state):
        print("❌ This puzzle is NOT solvable.")
        return

    # BFS
    print("=== BFS ===")
    start = time.time()
    solution, nodes = bfs(initial_state)
    end = time.time()
    print(f"Time: {end - start:.4f}s | Nodes Expanded: {nodes}")

    # DFS
    print("\n=== DFS ===")
    start = time.time()
    solution, nodes = dfs(initial_state)
    end = time.time()
    print(f"Time: {end - start:.4f}s | Nodes Expanded: {nodes}")

    # A*
    print("\n=== A* ===")
    start = time.time()
    solution, nodes = a_star(initial_state)
    end = time.time()
    print(f"Time: {end - start:.4f}s | Nodes Expanded: {nodes}")

    if solution:
        print("\nOptimal Solution Path (using A*):")
        path = get_path(solution)
        for step in path:
            print_board(step)


# Test Cases
test_cases = [
    {
        "name": "Easy Case", # 4 inversions
        "state": [1, 2, 3,
                  4, 0, 5,
                  6, 7, 8]
    },
    {
        "name": "Medium Case", # 8 inversions
        "state": [1, 2, 3,
                  5, 6, 0,
                  7, 8, 4]
    },
    {
        "name": "Unsolvable Case", # odd number of inversions (1)
        "state": [1, 2, 3,
                  4, 5, 6,
                  8, 7, 0]
    }
]


# MAIN
if __name__ == "__main__":
    for test in test_cases:
        print("\n==============================")
        print(f"Test: {test['name']}")
        print("==============================")

        run_all(test["state"])

        # Pausing between tests
        time.sleep(1)