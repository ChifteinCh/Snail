import math
import enum


class MoveDirection(enum.Enum):
    Up = 'Up'
    Down = 'Down'
    Right = 'Right'
    Left = 'Left'
    Pause = 'Pause'


def calculate_distance(cord1, cord2):
    distance = math.sqrt((cord1[0]-cord2[0])**2 + (cord1[1]-cord2[1])**2)
    return distance


def choose_target(snakes, fruits):
    dist = {}
    for fruit in fruits:
        dist2me = calculate_distance(snakes[0].get_body[0], fruit.get_pos)
        dist2enemy = calculate_distance(snakes[1].get_body[0], fruit.get_pos)
        dist[dist2me-dist2enemy] = fruit
    return dist[sorted(list(dist.keys()))[0]]


def choose_direction(snakes, fruits):

    changed_dir = snakes[0].get_dir
    near_fruit = choose_target(snakes, fruits)
    x_shift = snakes[0].get_body[0][0] - near_fruit.get_pos[0]
    y_shift = snakes[0].get_body[0][1] - near_fruit.get_pos[1]
    if x_shift > 0:
        changed_dir = MoveDirection.Left
    elif x_shift < 0:
        changed_dir = MoveDirection.Right
    elif y_shift > 0:
        changed_dir = MoveDirection.Up
    elif y_shift < 0:
        changed_dir = MoveDirection.Down

    if changed_dir == MoveDirection.Left and snakes[0].get_dir == MoveDirection.Right:
        changed_dir = MoveDirection.Up
    elif changed_dir == MoveDirection.Right and snakes[0].get_dir == MoveDirection.Left:
        changed_dir = MoveDirection.Up
    elif changed_dir == MoveDirection.Up and snakes[0].get_dir == MoveDirection.Down:
        changed_dir = MoveDirection.Right
    elif changed_dir == MoveDirection.Down and snakes[0].get_dir == MoveDirection.Up:
        changed_dir = MoveDirection.Right

    return changed_dir
