def frog_puzzle(N):
    start_state = ['>'] * N + ['_'] + ['<'] * N
    final_state = ['<'] * N + ['_'] + ['>'] * N

    def is_valid(state):
        return ''.join(state).find('><') == -1

    def generate_neighbors(state):
        neighbors = []
        for i in range(2 * N + 1):
            if state[i] == '<':
                if i < 2 * N and state[i + 1] == '_':
                    neighbor = state[:]
                    neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
                    neighbors.append(neighbor)
                if i < 2 * N - 1 and state[i + 2] == '_':
                    neighbor = state[:]
                    neighbor[i], neighbor[i + 2] = neighbor[i + 2], neighbor[i]
                    neighbors.append(neighbor)
            elif state[i] == '>':
                if i > 0 and state[i - 1] == '_':
                    neighbor = state[:]
                    neighbor[i], neighbor[i - 1] = neighbor[i - 1], neighbor[i]
                    neighbors.append(neighbor)
                if i > 1 and state[i - 2] == '_':
                    neighbor = state[:]
                    neighbor[i], neighbor[i - 2] = neighbor[i - 2], neighbor[i]
                    neighbors.append(neighbor)
        return neighbors

    def bfs():
        visited = set()
        queue = [start_state]
        visited.add(''.join(start_state))

        while queue:
            current_state = queue.pop(0)

            if current_state == final_state:
                return visited

            for neighbor_state in generate_neighbors(current_state):
                neighbor_str = ''.join(neighbor_state)
                if neighbor_str not in visited:
                    visited.add(neighbor_str)
                    queue.append(neighbor_state)

        return None

    if is_valid(start_state) and is_valid(final_state):
        visited_states = bfs()
        return [''.join(list(state)) for state in visited_states]

    return []

# Example usage:
N = 2
result = frog_puzzle(N)
for state in result:
    print(state)
