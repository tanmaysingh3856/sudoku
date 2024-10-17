from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class SudokuSolver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(600, 700)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.grid_layout = QGridLayout()
        self.cells = [[QLineEdit(self) for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                self.cells[i][j].setFixedSize(50, 50)
                self.cells[i][j].setFont(QFont("Arial", 20))
                self.cells[i][j].setAlignment(Qt.AlignCenter)
                self.cells[i][j].setStyleSheet(self.get_cell_style(i, j))
                self.grid_layout.addWidget(self.cells[i][j], i, j)
        
        self.solve_button = QPushButton("Solve")
        self.solve_button.setFixedSize(100, 50)
        self.solve_button.setStyleSheet("background-color: #555; color: #fff;")
        self.solve_button.clicked.connect(self.solve_sudoku)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedSize(100, 50)
        self.reset_button.setStyleSheet("background-color: #f00; color: #fff;")
        self.reset_button.clicked.connect(self.reset_sudoku)
        
        self.layout.addLayout(self.grid_layout)
        self.layout.addWidget(self.solve_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)
        
        self.setStyleSheet("background-color: #222;")
    
    def get_cell_style(self, row, col):
        style = "background-color: #333; color: #fff; border: 1px solid #555;"
        if row % 3 == 0 and row != 0:
            style += "border-top: 2px solid #fff;"
        if col % 3 == 0 and col != 0:
            style += "border-left: 2px solid #fff;"
        if row == 8:
            style += "border-bottom: 2px solid #fff;"
        if col == 8:
            style += "border-right: 2px solid #fff;"
        return style
    
    def solve_sudoku(self):
        board = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                text = self.cells[i][j].text()
                board[i][j] = int(text) if text.isdigit() else 0
        
        if self.solve(board):
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].setText(str(board[i][j]))
    
    def reset_sudoku(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].clear()
    
    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, num, row, col):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, board, num, row, col):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        
        box_x = col // 3
        box_y = row // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num:
                    return False
        
        return True

if __name__ == "__main__":
    app = QApplication([])
    window = SudokuSolver()
    window.show()
    app.exec()