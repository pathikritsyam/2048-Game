from tkinter import Frame, Label, CENTER
import random
import constants as c
import AI
import time


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.placeholder = []
        self.state = "not over"
        self.master.title('2048')
        self.score = 0
        self.total_moves = 0
        self.grid_cells = []
        self.init_grid()
        self.matrix = new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()
        self.timer = 0

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update()

    def reset_grid(self):
        self.matrix.clear()
        self.matrix = new_game(c.GRID_LEN)
        self.state = "not over"

    def direction(self):
        AI.BEST_SCORE = 0
        AI.GRIDS.clear()
        grids = []

        grids = AI.bestmove(self.matrix, 0, [], self.score, [])

        for i in range(0, len(grids)):
            self.matrix = grids[i]
            self.update_grid_cells()
        self.score = AI.getScore(self.matrix)


# print(self.placeholder)
# print(self.matrix)
        self.state = game_state(self.matrix)
        if self.placeholder == self.matrix:
            print(self.timer)
            self.timer += 0.3
            if self.timer > 10:
                self.state = "lose"
        else:
            self.timer = 0
# return
##
        self.placeholder = self.matrix

        if self.state == 'lose':
            self.grid_cells[1][1].configure(
                text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(
                text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            return

        self.total_moves += 1
        self.update_grid_cells()

    def high_tile(self):
        maxt = 0
        for i in range(0, c.GRID_LEN):
            for j in range(0, c.GRID_LEN):
                if self.matrix[i][j] > maxt:
                    maxt = self.matrix[i][j]
        return maxt

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat


def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


def game_state(mat):
    # check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # check for same cells that touch each other
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

    return game, done


def gen():
    return random.randint(0, c.GRID_LEN - 1)


def main():

    game_grid = GameGrid()
   # time.sleep(5)
    for i in range(0, 100):
        start = time.time()
        while not game_grid.state == "lose":
            game_grid.direction()
        f = open("results.txt", "a")

        string = ("score: " + str(game_grid.score) + " highest tile " +
                  str(game_grid.high_tile()) + " time: " + str(round(time.time()-start, 2))+"s")
        f.write(string)
        f.write('\n')
        f.close()
        game_grid.reset_grid()


main()
#AI.graph(game_grid.score, game_grid.total_moves, start)
