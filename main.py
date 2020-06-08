import numpy as np
import plotting
import global_code


def is_within_radius(xc, yc, x, y, radius):
    return (xc - x)**2 + (yc - y)**2 < radius**2

def get_random_direction():
    return np.random.uniform() * np.pi * 2

def get_left_direction_bias():
    return np.random.normal(0.06, 0.05)

def get_right_direction_bias():
    return np.random.normal(-0.06, 0.05)

def random_bool():
    return np.random.uniform() < 0.5

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

    def get_random_edge_position(self):
        x = int(np.random.uniform() * self.n)
        y = int(np.random.uniform() * self.m)
        if random_bool():
            #trim to left or right edge
            return (0,y) if random_bool() else (self.n-1,y)
        else:
            #trim to top or bottom edge
            return (x,0) if random_bool() else (x, self.m-1)

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
        self.steps = 0

    def set_new_direction(self):
        self.direction += np.random.normal(0.0, 0.07)


    def perform_step(self):
        self.x += np.cos(self.direction) * self.radius
        self.y += np.sin(self.direction) * self.radius
        self.set_new_direction()
        self.steps += 1
        return self.x,self.y

    def split_possible(self):
        return self.radius > 3

    def split_equal(self):
        new_radius = self.radius - 1
        left_dir = self.direction + get_left_direction_bias()
        right_dir = self.direction + get_right_direction_bias()
        runner1 = Runner(self.color, (self.x, self.y), direction=left_dir, radius=new_radius)
        runner2 = Runner(self.color, (self.x, self.y), direction=right_dir, radius=new_radius)
        return runner1, runner2

def draw_n_lines(n, board):
    for i in range(n):
        runner = Runner(i+1, board.get_random_position(), radius=i+1)
        while board.assign_a_step(runner):
            pass
    board.plot()

def draw_splitting_lines(board, radius_mean=7, radius_std=3, split_mean=30, split_std=10,number_start_runner = 7):
    runners = []
    painted_steps = 0
    for i in range(number_start_runner):
        radius =  max(1, np.random.normal(radius_mean, radius_std))
        runners.append( Runner(i+1, board.get_random_edge_position(), radius=radius) )
    while len(runners) > 0:
        runner = runners.pop()
        painted_steps += 1
        if board.assign_a_step(runner):
            #check for splitting
            if runner.steps > np.random.normal(split_mean, split_std) and runner.split_possible():
                    r1, r2 = runner.split_equal()
                    runners.append(r1)
                    runners.append(r2)
            else:
                runners =  [runner] + runners
        if painted_steps % 100 == 0:
            print(len(runners))
    board.plot()
    print(board.name)
    #draw_n_lines(50, board)



board = Board(1600, 2560)
draw_splitting_lines(board, radius_mean=12, radius_std=2, split_mean=25, split_std=10,number_start_runner = 5)