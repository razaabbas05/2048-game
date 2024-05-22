# ui.py
import tkinter as tk
from game_logic import start_game, move_left, move_right, move_up, move_down, add_2, get_curr_state
from constants import *

class Game2048GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master.title("2048 Game")
        self.master.resizable(False, False)
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.master.bind("<Key>", self.key_down)

    def init_grid(self):
        background = tk.Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid(padx=(GRID_PADDING, 0), pady=(GRID_PADDING, 0))
        self.grid_cells = []
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = tk.Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = start_game()

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT.get(new_number, "#cdc1b4"), fg=CELL_COLOR_DICT.get(new_number, "#776e65"))
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == KEY_UP:
            self.matrix, changed = move_up(self.matrix)
        elif key == KEY_DOWN:
            self.matrix, changed = move_down(self.matrix)
        elif key == KEY_LEFT:
            self.matrix, changed = move_left(self.matrix)
        elif key == KEY_RIGHT:
            self.matrix, changed = move_right(self.matrix)
        else:
            return

        if changed:
            add_2(self.matrix)
            self.update_grid_cells()
            if get_curr_state(self.matrix) == "You won":
                self.show_game_over("You won!")
            if get_curr_state(self.matrix) == "You lost":
                self.show_game_over("Game over!")

    def show_game_over(self, message):
        game_over_frame = tk.Frame(self.master, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(game_over_frame, text=message, bg="#ffcc00", fg="#ffffff", font=FONT, width=10, height=5).pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048GUI(master=root)
    game.mainloop()
