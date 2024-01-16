import math


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def is_valid_move(board, move):
    row, col = move
    return 1 <= row <= 3 and 1 <= col <= 3 and board[row - 1][col - 1] == " "


def apply_move(board, move, player):
    row, col = move
    board[row - 1][col - 1] = "X" if player == 1 else "O"


def get_empty_moves(board):
    return [(i, j) for i in range(1, 4) for j in range(1, 4) if board[i - 1][j - 1] == " "]


def check_for_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]  # Winner in a row
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]  # Winner in a column

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]  # Winner in the main diagonal

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]  # Winner in the other diagonal

    return None  # No winner


def evaluate(board):
    winner = check_for_winner(board)
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif " " not in [cell for row in board for cell in row]:
        return 0  # Draw
    else:
        return None  # Game still in progress


def minimax(board, depth, alpha, beta, maximizing_player):
    score = evaluate(board)

    if score is not None:
        return score

    empty_moves = get_empty_moves(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in empty_moves:
            board[move[0] - 1][move[1] - 1] = "O"
            eval_score = minimax(board, depth + 1, alpha, beta, False)
            board[move[0] - 1][move[1] - 1] = " "
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in empty_moves:
            board[move[0] - 1][move[1] - 1] = "X"
            eval_score = minimax(board, depth + 1, alpha, beta, True)
            board[move[0] - 1][move[1] - 1] = " "
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board):
    best_move = None
    best_eval = -math.inf

    for move in get_empty_moves(board):
        board[move[0] - 1][move[1] - 1] = "O"
        eval_score = minimax(board, 0, -math.inf, math.inf, False)
        board[move[0] - 1][move[1] - 1] = " "
        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

    return best_move


def main():
    print("Welcome to Tic-Tac-Toe!")
    print("Player is 'X', Computer is 'O'")
    print("Enter 'row col' to make a move.")

    # Decide who goes first
    first_player = input("Who goes first? (P for player, C for computer): ").upper()

    player_turn = 1 if first_player == "P" else 2
    board = initialize_board()

    while True:
        print_board(board)

        if player_turn == 1:
            move = tuple(map(int, input("Your move (row col): ").split()))
            if is_valid_move(board, move):
                apply_move(board, move, player_turn)
            else:
                print("Invalid move. Try again.")
                continue
        else:
            print("Computer's move:")
            move = get_best_move(board)
            apply_move(board, move, player_turn)

        winner = check_for_winner(board)
        if winner:
            print_board(board)
            print(f"Player '{winner}' wins!")
            break
        elif " " not in [cell for row in board for cell in row]:
            print_board(board)
            print("It's a draw!")
            break

        # Switch player turn
        player_turn = 3 - player_turn  # Toggle between 1 and 2


if __name__ == "__main__":
    main()
