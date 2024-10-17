import tkinter as tk
from tkinter import messagebox

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_safe(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_board()
        self.create_buttons()

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=450, height=450)
        self.canvas.grid(row=0, column=0, columnspan=9, rowspan=9)

        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(5 + i * 50, 5, 5 + i * 50, 455, width=width)
            self.canvas.create_line(5, 5 + i * 50, 455, 5 + i * 50, width=width)

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry
            
    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=3, columnspan=3, pady=10)

        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        reset_button.grid(row=10, column=3, columnspan=3, pady=10)

    def solve(self):
        self.read_board()
        if solve_sudoku(self.board):
            self.update_board()
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku")

    def read_board(self):
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                self.board[row][col] = int(value) if value else 0

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.board[row][col]))

    def reset_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()