import random
import time

def nqueens(n):
	show(min_conflicts(list(range(n)), n), n)

def show(solution, n):
    # If no solution is found, print -1
    if solution==-1:
        print(-1)
    # Print the board solution if N is less than or equal to 100
    elif N <= 100:
        for i in range(n):
            # The double commented parts are for testing with ai-hw-02.exe
            # For printing the positions from right to left as per the task output example
            ## positions = [N - 1 - i for i in combo]
            # print(f"Solution {sol}: ")
            ## print(f"{positions}\n")

            row = [' _ '] * n
            for column in range(n):
                if solution[column] == n - 1 - i:
                    row[column] = ' * '
            print(''.join(row))

def min_conflicts(solution, n, iterations=1000):
    # Helper function to get a random position in a list based on a filter
	def random_pos(li, filt):
		return random.choice([i for i in range(n) if filt(li[i])])

    # Iterate for a maximum number of iterations (default is 1000)
	for k in range(iterations):
        # Find conflicts for each column
		conflicts = find_conflicts(solution, n)

        # If there are no conflicts, the solution is found
		if sum(conflicts) == 0:
			return solution

        # Select a column with conflicts randomly
		column = random_pos(conflicts, lambda elt: elt > 0)

        # Calculate vertical conflicts for the selected column
		vertical_conflicts = [hits(solution, n, column, row) for row in range(n)]

        # Move the queen to a new position with minimum vertical conflicts
		solution[column] = random_pos(vertical_conflicts, lambda elt: elt == min(vertical_conflicts))

    # If no solution is found within the specified iterations, return -1
	return -1

def find_conflicts(solution, n):
    # Count the number of hits (conflicts) for each column
	return [hits(solution, n, column, solution[column]) for column in range(n)]

def hits(solution, n, column, row):
    # Count the total number of conflicts for a queen in a given column and row
	total = 0
	for i in range(n):
		if i == column:
			continue
		if solution[i] == row or abs(i - column) == abs(solution[i] - row):
			total += 1
	return total


N = int(input("Enter the number of queens (N): "))

start_time = time.time()
nqueens(N)
end_time = time.time()

# Calculate and print the elapsed time if N is greater than 100
if N > 100:
    elapsed_time = end_time - start_time
    print(f"Time elapsed: {elapsed_time:.2f} seconds")