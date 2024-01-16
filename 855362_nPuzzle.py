from copy import deepcopy
import math
import time

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "R": [0, -1], "L": [0, 1]} # as per the instructions, otherwise it would be
#DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

def is_solvable(board):
    board_list = [num for row in board for num in row if num != 0]
    inversions = 0

    for i in range(len(board_list) - 1):
        for j in range(i + 1, len(board_list)):
            if board_list[i] > board_list[j]:
                inversions += 1

    return inversions % 2 == 0

# Node class to store each state of the puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

# getting the position of an element in the current state
def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

# manhattan distance heuristic
def manhattanCost(current_state, GOAL):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            if current_state[row][col] == 0:
                continue
            pos = get_pos(GOAL, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

# get adjacent nodes
def getAdjNode(node, GOAL):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, manhattanCost(newState, GOAL), dir))

    return listNode

# getting the best node available among nodes
def getBestNode(openSet):
    firstIter = True
    bestF = 0

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

# creating the smallest path
def buildPath(closedSet, GOAL):
    node = closedSet[str(GOAL)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

# A* search
def main(puzzle, GOAL):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, manhattanCost(puzzle, GOAL), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == GOAL:
            return buildPath(closed_set, GOAL)

        adj_node = getAdjNode(test_node, GOAL)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

def has_integer_square_root(number):
    # Calculate the square root of the number
    sqrt = math.isqrt(number)

    # Check if the square of the square root is equal to the original number
    return sqrt * sqrt == number

def create_goal(N, i, j):
    goal = [[0] * N for _ in range(N)]
    num = 1
    for row in range(N):
        for col in range(N):
            goal[row][col] = num
            num += 1
    goal[i][j] = 0
    return goal

def input_puzzle(dim):
    puzzle = []
    for _ in range(dim):
        row = input().strip().split()
        if len(row) != dim:
            print("Error: Each row should contain exactly N numbers.")
        try:
            row = [int(num) for num in row]
        except ValueError:
            print("Error: Please enter only integers.")
        puzzle.append(row)
    return puzzle

def generate_goal(ind, dim):
    i = int(ind/dim) # coordinate for 0
    j = int(ind%dim) # coordinate for 0

    matrix = [[-1] * dim for _ in range(dim)]
    matrix[i][j] = 0
    current_value = 1 # to start from 1

    for x in range(dim):
        for y in range(dim):
            if  matrix[x][y] == 0:
                continue
            matrix[x][y] = current_value
            current_value += 1
    return matrix

if __name__ == '__main__':

    N = int(input("Enter the size of the puzzle (N): "))
    I = int(input("Enter index of 0 (I): "))

    if not has_integer_square_root(N+1):
        print("Entered N not valid")
        exit()

    dimension = math.isqrt(N+1)
    puzzle = []
    goal = []

    puzzle = input_puzzle(dimension)

    if I<0:
        I += N + 1

    goal = generate_goal(I, dimension)

    if not is_solvable(puzzle):
        print(-1)
        exit()

    start_time = time.time()
    board = main(puzzle, goal)
    end_time = time.time()  # Record the end time

    print(len(board) - 1)  # Printing total steps
    for tile in board:
        if tile['dir'] != '':
            move = ''
            if tile['dir'] == 'U':
                move = 'up'
            elif tile['dir'] == 'R':
                move = 'right'
            elif tile['dir'] == 'L':
                move = 'left'
            elif tile['dir'] == 'D':
                move = 'down'
            print(move)

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")