import math
import tkinter as tk
from tkinter import messagebox

# Game settings
BOARD_SIZE = 3  # Change this for larger boards (e.g., 4 for 4x4)
AI_PLAYER = "O"
HUMAN_PLAYER = "X"

# Initialize board
board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Check if moves are left
def is_moves_left():
    return any(" " in row for row in board)

# Check winner
def evaluate():
    # Check rows and columns
    for i in range(BOARD_SIZE):
        if all(board[i][j] == AI_PLAYER for j in range(BOARD_SIZE)):
            return 1
        if all(board[i][j] == HUMAN_PLAYER for j in range(BOARD_SIZE)):
            return -1
        if all(board[j][i] == AI_PLAYER for j in range(BOARD_SIZE)):
            return 1
        if all(board[j][i] == HUMAN_PLAYER for j in range(BOARD_SIZE)):
            return -1

    # Check diagonals
    if all(board[i][i] == AI_PLAYER for i in range(BOARD_SIZE)):
        return 1
    if all(board[i][i] == HUMAN_PLAYER for i in range(BOARD_SIZE)):
        return -1
    if all(board[i][BOARD_SIZE - 1 - i] == AI_PLAYER for i in range(BOARD_SIZE)):
        return 1
    if all(board[i][BOARD_SIZE - 1 - i] == HUMAN_PLAYER for i in range(BOARD_SIZE)):
        return -1

    return 0  # No winner

# Minimax algorithm with Alpha-Beta Pruning
def minimax(depth, is_max, alpha, beta):
    score = evaluate()

    if score == 1:
        return score - depth
    if score == -1:
        return score + depth
    if not is_moves_left():
        return 0

    if is_max:  # AI (O) is maximizing
        best = -math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == " ":
                    board[i][j] = AI_PLAYER
                    best = max(best, minimax(depth + 1, False, alpha, beta))
                    board[i][j] = " "
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:  # Human (X) is minimizing
        best = math.inf
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == " ":
                    board[i][j] = HUMAN_PLAYER
                    best = min(best, minimax(depth + 1, True, alpha, beta))
                    board[i][j] = " "
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

# Find best AI move
def find_best_move():
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == " ":
                board[i][j] = AI_PLAYER
                move_val = minimax(0, False, -math.inf, math.inf)
                board[i][j] = " "
                
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    
    return best_move

# GUI using tkinter
class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe AI")
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j] = tk.Button(master, text=" ", font=("Arial", 24), width=5, height=2,
                                               command=lambda row=i, col=j: self.human_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def human_move(self, row, col):
        if board[row][col] == " ":
            board[row][col] = HUMAN_PLAYER
            self.buttons[row][col].config(text=HUMAN_PLAYER, state=tk.DISABLED)
            if evaluate() == -1:
                messagebox.showinfo("Game Over", "You win!")
                self.master.quit()
            elif not is_moves_left():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.master.quit()
            else:
                self.ai_move()

    def ai_move(self):
        row, col = find_best_move()
        board[row][col] = AI_PLAYER
        self.buttons[row][col].config(text=AI_PLAYER, state=tk.DISABLED)

        if evaluate() == 1:
            messagebox.showinfo("Game Over", "AI wins!")
            self.master.quit()
        elif not is_moves_left():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.master.quit()

# Run the GUI
def play_gui():
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

# Run the game
play_gui()
