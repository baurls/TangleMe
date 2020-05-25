import numpy as np
import plotting
import global_code


def is_within_radius(xc, yc, x, y, radius):
    return (xc - x)**2 + (yc - y)**2 < radius**2

def get_random_direction():
    return np.random.uniform() * np.pi * 2

class Board:
    """
              n
      -------------------
      \                 \
    m \                 \
      \                 \
      -------------------
    """
    def __init__(self, m, n,name=None):
        self.m = m
        self.n = n
        self.field = np.zeros((m,n), dtype=int)
        self.name = name if name is not None else global_code.get_random_name_of_length(5)
        self.iterations = 0

    def get_random_position(self):
        x = int(np.random.uniform() * self.n)
        y = int(np.random.uniform() * self.m)
        return (x,y)

    def is_inside_bounds(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m

    def color_pixel(self, i, j, color):
        self.field[j][i] = color

    def draw_a_step(self, x, y, radius, color):
        for i in range(int(x-radius), int(x+radius)+1):
            for j in range(int(y-radius), int(y+radius)+1):
                if self.is_inside_bounds(i,j) and is_within_radius(x,y,i,j,radius):
                    self.color_pixel(i, j, color)

    def assign_a_step(self, runner):
        x,y = runner.perform_step()
        color = runner.color
        radius = runner.radius
        self.draw_a_step(x,y,radius,color)
        self.iterations += 1
        return self.is_inside_bounds(x,y)

    def plot(self):
        plotting.plot_board(self.field, self.name, self.iterations)


class Runner:
    def __init__(self, color, position, direction=None, radius=1):
        self.color = color
        self.x, self.y = position
        self.radius = radius
        self.direction = direction if direction is not None else get_random_direction()


    def set_new_direction(self):
        self.direction += np.random.normal(0.0, 0.05)

    def perform_step(self):
        self.x += np.cos(self.direction) * self.radius
        self.y += np.sin(self.direction) * self.radius
        self.set_new_direction()
        return self.x,self.y

def draw_n_lines(n, board):
    for i in range(n):
        runner = Runner(i+1, board.get_random_position(), radius=i+1)
        while board.assign_a_step(runner):
            pass
    board.plot()

board = Board(1000,2000)

draw_n_lines(50, board)


