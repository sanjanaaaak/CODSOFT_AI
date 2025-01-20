import math

# Constants for the game
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Print the board
def print_board(board):
    for row in range(3):
        print(f" {board[row][0]} | {board[row][1]} | {board[row][2]} ")
        if row < 2:
            print("---|---|---")
    print("\n")

# Check if the current player has won
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Check if the board is full
def is_board_full(board):
    return all([board[i][j] != EMPTY for i in range(3) for j in range(3)])

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, is_maximizing, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O

    # Check for terminal conditions (winner or full board)
    if check_winner(board, PLAYER_X):
        return -10 + depth
    if check_winner(board, PLAYER_O):
        return 10 - depth
    if is_board_full(board):
        return 0
    
    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = player
                    eval = minimax(board, depth + 1, alpha, beta, False, player)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = opponent
                    eval = minimax(board, depth + 1, alpha, beta, True, player)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Find the best move for the AI
def best_move(board, player):
    best_score = -math.inf
    move = (-1, -1)
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = player
                score = minimax(board, 0, -math.inf, math.inf, False, player)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    
    return move

# Play the game
def play_game():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    current_player = PLAYER_X  # Human starts first
    
    while True:
        print_board(board)
        
        if current_player == PLAYER_X:
            row = int(input("Enter the row (0-2): "))
            col = int(input("Enter the column (0-2): "))
            if board[row][col] != EMPTY:
                print("Invalid move. Try again.")
                continue
            board[row][col] = PLAYER_X
        else:
            print("AI is making a move...")
            row, col = best_move(board, PLAYER_O)
            board[row][col] = PLAYER_O
        
        # Check if the game is over
        if check_winner(board, PLAYER_X):
            print_board(board)
            print("You win!")
            break
        elif check_winner(board, PLAYER_O):
            print_board(board)
            print("AI wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        # Switch players
        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

# Start the game
if __name__ == "__main__":
    play_game()
