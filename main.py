import tkinter as tk
from tkinter import messagebox


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("MKENYADAIMA 3x3 Sudoku Game")

        # Initial Sudoku board
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        self.cells = {}
        self.build_grid()
        self.add_buttons()

    def build_grid(self):
        """Builds a 9x9 grid of Entry widgets"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    entry = tk.Entry(self.master, width=3, font=('Arial', 22), borderwidth=2,
                                     justify='center', fg='black', bg='light grey')
                    entry.insert(tk.END, self.board[i][j])
                    entry.config(state='readonly')
                else:
                    entry = tk.Entry(self.master, width=3, font=('Arial', 22), borderwidth=2,
                                     justify='center', fg='blue')
                entry.grid(row=i, column=j, sticky="nsew", padx=1, pady=1, ipady=5)
                self.cells[(i, j)] = entry

        # Add thicker borders to the 3x3 subgrids
        for i in range(9):
            for j in range(9):
                if i % 3 == 0:
                    self.cells[(i, j)].config(highlightthickness=2, highlightbackground='black')
                if j % 3 == 0:
                    self.cells[(i, j)].config(highlightthickness=2, highlightbackground='black')

    def add_buttons(self):
        """Add Solve and Clear buttons below the Sudoku grid"""
        solve_button = tk.Button(self.master, text='Solve', command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=4, sticky="ew")

        clear_button = tk.Button(self.master, text='Clear', command=self.clear)
        clear_button.grid(row=9, column=5, columnspan=4, sticky="ew")

    def solve(self):
        """Solve the Sudoku puzzle and update the grid"""
        board = self.get_board_from_entries()
        if self.solve_sudoku(board):
            self.update_grid(board)
        else:
            messagebox.showinfo("Sudoku", "No solution exists for this Sudoku.")

    def clear(self):
        """Clear all non-original entries from the Sudoku grid"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.cells[(i, j)].delete(0, tk.END)

    def get_board_from_entries(self):
        """Retrieve the current board state from the Entry widgets"""
        current_board = []
        for i in range(9):
            current_board.append([])
            for j in range(9):
                value = self.cells[(i, j)].get()
                current_board[i].append(int(value) if value.isdigit() else 0)
        return current_board

    def update_grid(self, board):
        """Update the grid with the solved board"""
        for i in range(9):
            for j in range(9):
                if self.cells[(i, j)].get() == '':
                    self.cells[(i, j)].delete(0, tk.END)
                    self.cells[(i, j)].insert(tk.END, board[i][j])

    def solve_sudoku(self, board):
        """Solve the Sudoku board using backtracking"""
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve_sudoku(board):
                    return True

                board[row][col] = 0

        return False

    def find_empty(self, board):
        """Find an empty space in the board"""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def valid(self, board, num, pos):
        """Check if the move is valid"""
        # Check row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()