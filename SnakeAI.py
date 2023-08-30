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


def choose_nearest(snake, fruits):
    dist = {}
    for fruit in fruits:
        dist[calculate_distance(snake.get_body[0], fruit.get_pos)] = fruit
    # print('I see this fruits: ', dist)
    return dist[sorted(list(dist.keys()))[0]]


def choose_direction(snake, fruits):
    # print('old dir = ', snake.get_dir)
    changed_dir = snake.get_dir
    near_fruit = choose_nearest(snake, fruits)
    # print('nearest fruit at ', near_fruit.get_pos)
    x_shift = snake.get_body[0][0] - near_fruit.get_pos[0]
    y_shift = snake.get_body[0][1] - near_fruit.get_pos[1]
    # print('x axis shift = ', x_shift)
    # print('y axis shift = ', y_shift)
    if x_shift > 0:
        # print('changing dir to left')
        changed_dir = MoveDirection.Left
        # print('changing dir to right')
    elif x_shift < 0:
        changed_dir = MoveDirection.Right
    elif y_shift > 0:
        changed_dir = MoveDirection.Up
        # print('changing dir to up')
    elif y_shift < 0:
        changed_dir = MoveDirection.Down
        # print('changing dir to down')

    # print('old dir = ', snake.get_dir)
    # print('new dir = ', changed_dir)
    # print(changed_dir == MoveDirection.Left)
    # print(snake.get_dir == MoveDirection.Right)

    if changed_dir == MoveDirection.Left and snake.get_dir == MoveDirection.Right:
        changed_dir = MoveDirection.Up
        # print('rechanging dir to up')
    elif changed_dir == MoveDirection.Right and snake.get_dir == MoveDirection.Left:
        changed_dir = MoveDirection.Up
        # print('rechanging dir to up')
    elif changed_dir == MoveDirection.Up and snake.get_dir == MoveDirection.Down:
        changed_dir = MoveDirection.Right
        # print('rechanging dir to right')
    elif changed_dir == MoveDirection.Down and snake.get_dir == MoveDirection.Up:
        changed_dir = MoveDirection.Right
        # print('rechanging dir to right')
    # else:
        # print('no need in rechanging dir')
    # print('changed_dir = ', changed_dir)

    return changed_dir
