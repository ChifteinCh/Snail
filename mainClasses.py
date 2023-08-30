import random
import time
import msvcrt
import enum
import os
from SnakeAI import choose_direction, MoveDirection


def clear():
    os.system('cls')


# class MoveDirection(enum.Enum):
#     Up = 'Up'
#     Down = 'Down'
#     Right = 'Right'
#     Left = 'Left'
#     Pause = 'Pause'


class TileType(enum.Enum):

    Snake = 's'
    Snake_Head = 'S'
    Enemy_Snake = 'e'
    Enemy_Snake_Head = 'E'
    Floor = '.'
    Wall = 'W'
    Collide = '!'
    Fruit = 'f'
    Big_Fruit = 'F'
    Wall_Fruit = 'o'


class FruitType(enum.Enum):
    Normal = 5
    Big = 5
    Wall = 5


def mask(map_, *object_lists):
    body_list = body_list_from_objects(*object_lists)
    cords = [cord for lst in body_list for cord in lst]
    possible_tiles = []
    for i in range(map_.map_dim[1] - 2):
        possible_tiles.append([1] * (map_.map_dim[0] - 2))

    for x in range(map_.map_dim[0] - 2):
        for y in range(map_.map_dim[1] - 2):
            possible_tiles[y][x] = x + 1
    for cord in cords:
        for i in range(len(cords)):
            if cord[0] != 0 and cord[0] != map_.map_dim[0]-1 and cord[1] != 0 and cord[1] != map_.map_dim[1]-1:
                x = cord[0] - 1
                y = cord[1] - 1
                possible_tiles[y][x] = 0

    for i in range(len(possible_tiles)):
        for j in possible_tiles[i].copy():
            if j == 0:
                possible_tiles[i].remove(j)

    possible_rows = []
    for i in range(len(possible_tiles)):
        possible_rows.append(i)

    for i in range(len(possible_tiles)):
        if not possible_tiles[i]:
            possible_rows.remove(i)

    return possible_tiles, possible_rows


# def mask(map_, *object_lists):
#     body_list = body_list_from_objects(*object_lists)
#     cords = [cord for lst in body_list for cord in lst]
#     possible_tiles = []
#     for i in range(map_.map_dim[1]):
#         possible_tiles.append([1] * (map_.map_dim[0]))
#
#     for x in range(map_.map_dim[0]):
#         for y in range(map_.map_dim[1]):
#             possible_tiles[y][x] = x
#     for cord in cords:
#         for i in range(len(cords)):
#             x = cord[0]
#             y = cord[1]
#             possible_tiles[y][x] = 0
#
#     for i in range(len(possible_tiles)):
#         for j in possible_tiles[i].copy():
#             if j == 0:
#                 possible_tiles[i].remove(j)
#
#     for i in range(len(possible_tiles)):
#         for j in possible_tiles[i].copy():
#             if j == map_.map_dim[1]-1:
#                 possible_tiles[i].remove(j)
#
#     possible_tiles[0] = []
#     possible_tiles[map_.map_dim[1]-1] = []
#
#
#     possible_rows = []
#     for i in range(len(possible_tiles)):
#         possible_rows.append(i)
#
#     for i in range(len(possible_tiles)):
#         if not possible_tiles[i]:
#             possible_rows.remove(i)
#
#     return possible_tiles, possible_rows


def pick_rand_point(map_, *objects):
    possible_tiles, possible_rows = mask(map_, *objects)
    y = random.choice(possible_rows) + 1
    x = random.choice(possible_tiles[y - 1])
    return [x, y]


def body_list_from_objects(*objects):
    lst = []
    for obj in objects:
        if isinstance(obj, Snake):
            lst.append(obj.get_body)
        elif isinstance(obj, Fruit):
            lst.append([obj.get_pos])
        elif isinstance(obj, Wall):
            lst.append(obj.get_pos)
    return lst


def print_matrix(matrix):
    print()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')
        print()


class Map:
    def __init__(self, field_length, field_height):
        self.__length = field_length + 2
        self.__height = field_height + 2
        self.__map = [[TileType.Floor] * self.__height for i in range(self.__length)]

    @property
    def map_dim(self):
        return [self.__length, self.__height]

    def get_tile(self, x, y):
        return self.__map[x][y]

    def print(self):
        print()
        for i in range(self.__height):
            for j in range(self.__length):
                print(self.__map[j][i].value, end=' ')
            print()

    def clear(self):
        for j in range(len(self.__map) - 2):
            for i in range(len(self.__map[j]) - 2):
                self.__map[j + 1][i + 1] = TileType.Floor

    def build_walls(self):
        self.__map[0][0:self.__height] = self.__map[self.__length - 1][0:self.__height] = [
                                                                                              TileType.Wall] * self.__height
        for i in range(self.__length - 1):
            self.__map[i][0] = self.__map[i][self.__height - 1] = TileType.Wall

    def build_snake(self, snake):
        for i in range(1, snake.get_length):
            self.__map[snake.get_body[i][0]][snake.get_body[i][1]] = TileType.Snake

    def build_snake_head(self, snake):
        self.__map[snake.get_body[0][0]][snake.get_body[0][1]] = TileType.Snake_Head

    def build_enemy_snake(self, snake):
        for i in range(1, snake.get_length):
            self.__map[snake.get_body[i][0]][snake.get_body[i][1]] = TileType.Enemy_Snake

    def build_enemy_snake_head(self, snake):
        self.__map[snake.get_body[0][0]][snake.get_body[0][1]] = TileType.Enemy_Snake_Head

    def build_fruit(self, fruit):
        self.__map[fruit.get_pos[0]][fruit.get_pos[1]] = fruit.tile

    def place_eog_tile(self, eog_pos):
        self.__map[eog_pos[0]][eog_pos[1]] = TileType.Collide

    def build_fruit_walls(self, wall):
        if wall.get_lifetime > 0:
            for pos in wall.get_pos:
                self.__map[pos[0]][pos[1]] = TileType.Wall

    def remove_fruit_walls(self, wall):
        for pos in wall.get_pos:
            self.__map[pos[0]][pos[1]] = TileType.Floor


class Snake:
    def __init__(self, length=3, is_player=0):
        self.__length = length
        self.__body = [[0, 0] for i in range(self.__length)]
        self.__last_peace = [0, 0]
        self.__move_dir = MoveDirection.Right
        self.__grow_points = 0
        self.__death_tiles = CollideTiles
        if is_player:
            self.__death_tiles.remove(TileType.Snake_Head)
        else:
            self.__death_tiles.remove(TileType.Enemy_Snake_Head)


    @property
    def get_body(self):
        return self.__body

    @property
    def get_dir(self):
        return self.__move_dir

    @property
    def get_length(self):
        return self.__length

    @property
    def get_death_tiles(self):
        return self.__death_tiles

    @property
    def grow_points(self):
        return self.__grow_points

    @grow_points.setter
    def grow_points(self, points):
        self.__grow_points = self.__grow_points + points

    def set_direction(self, dir):
        self.__move_dir = dir



    # def spawn(self, spawn_map):
    #     if self.__length > (spawn_map.map_dim[0] - 2) // 2:
    #         print('Error. Snake is to big to spawn')
    #         return
    #     for i in range(self.__length):
    #         self.__body[i][0] = (spawn_map.map_dim[0] - 2) // 2 + 1 - i
    #         self.__body[i][1] = (spawn_map.map_dim[1] - 2) // 2 + 1

    def spawn(self, map_, *objects):
        self.__body[0] = pick_rand_point(map_, *objects)

    def respawn(self, map_, *objects):
        self.__length = 1
        self.__body = [[0, 0]]
        self.__body[0] = pick_rand_point(map_, *objects)

    def move(self):
        match self.__move_dir:
            case MoveDirection.Up:
                self.__body.insert(0, [self.__body[0][0], self.__body[0][1] - 1])
            case MoveDirection.Right:
                self.__body.insert(0, [self.__body[0][0] + 1, self.__body[0][1]])
            case MoveDirection.Down:
                self.__body.insert(0, [self.__body[0][0], self.__body[0][1] + 1])
            case MoveDirection.Left:
                self.__body.insert(0, [self.__body[0][0] - 1, self.__body[0][1]])
        self.__last_peace = self.__body.pop()

    def change_dir(self, direction):
        if direction == MoveDirection.Right and self.__move_dir != MoveDirection.Left:
            self.__move_dir = direction
        elif direction == MoveDirection.Up and self.__move_dir != MoveDirection.Down:
            self.__move_dir = direction
        elif direction == MoveDirection.Left and self.__move_dir != MoveDirection.Right:
            self.__move_dir = direction
        elif direction == MoveDirection.Down and self.__move_dir != MoveDirection.Up:
            self.__move_dir = direction

    def grow(self):
        if self.__grow_points > 0:
            self.__length += 1
            self.__body.append(self.__last_peace)
            self.__grow_points -= 1


class EnemySnake(Snake):
    pass


class Fruit:
    def __init__(self, map_, *objects):
        self.__pos = [0, 0]
        self.__type = FruitType.Normal
        self.__tile = TileType.Fruit
        self.spawn(map_, *objects)

    @property
    def get_pos(self):
        return self.__pos

    @property
    def tile(self):
        return self.__tile

    @property
    def type(self):
        return self.__type

    def spawn(self, map_, *objects):
        self.__pos = pick_rand_point(map_, *objects)
        r = random.randrange(5)
        if r == 4:
            self.__type = FruitType.Big
            self.__tile = TileType.Big_Fruit
        elif r == 3:
            self.__type = FruitType.Wall
            self.__tile = TileType.Wall_Fruit
        else:
            self.__type = FruitType.Normal
            self.__tile = TileType.Fruit


class Wall:

    def __init__(self, map_, *objects):
        self.__center = [0, 0]
        self.__pos = []
        self.__lifetime = 5
        self.spawn_wall(map_, *objects)

    @property
    def get_pos(self):
        return self.__pos

    @property
    def get_lifetime(self):
        return self.__lifetime

    def spawn_wall(self, map_, *objects):
        self.__center = pick_rand_point(map_, *objects)

        self.__pos.append(self.__center)
        if map_.get_tile(self.__center[0], self.__center[1] - 1) == TileType.Floor:
            self.__pos.append([self.__center[0], self.__center[1] - 1])
        if map_.get_tile(self.__center[0], self.__center[1] + 1) == TileType.Floor:
            self.__pos.append([self.__center[0], self.__center[1] + 1])
        if map_.get_tile(self.__center[0] - 1, self.__center[1]) == TileType.Floor:
            self.__pos.append([self.__center[0] - 1, self.__center[1]])
        if map_.get_tile(self.__center[0] + 1, self.__center[1]) == TileType.Floor:
            self.__pos.append([self.__center[0] + 1, self.__center[1]])

    def low_lifetime(self):
        if self.__lifetime > 0:
            self.__lifetime -= 1


class Manager:

    def __init__(self, map_, pl_snake, *enemy_snakes):
        self.__map = map_
        self.__fruits = []
        self.__snake_list = [pl_snake, *enemy_snakes]
        self.__wall_list = []
        self.__snake_amount = len(self.__snake_list)
        self.__key_bindings = {b'p': MoveDirection.Pause}
        self.__eog = [0, [0, 0]]

    def initialize(self):
        clear()
        self.install_keys()
        clear()
        for snakes in self.__snake_list:
            snakes.spawn(self.__map, *self.__snake_list)
        self.__map.build_walls()
        self.__map.build_snake_head(self.__snake_list[0])
        self.__map.build_enemy_snake_head(self.__snake_list[1])
        self.__map.build_snake(self.__snake_list[0])
        self.__map.build_enemy_snake(self.__snake_list[1])
        self.__fruits = [Fruit(self.__map, *self.__snake_list), Fruit(self.__map, *self.__snake_list)]
        for fruits in self.__fruits:
            self.__map.build_fruit(fruits)
        self.__map.print()

    # def set_snakes_tiles(self):
    #     for i in range(len(self.__snake_list)):
    #         self.__snake_list[i] =

    def install_keys(self):
        print('Press ' + MoveDirection.Up.value + ' button')
        while True:
            if msvcrt.kbhit():
                self.__key_bindings[msvcrt.getch()] = MoveDirection.Up
                break
        print('Press ' + MoveDirection.Down.value + ' button')
        while True:
            if msvcrt.kbhit():
                self.__key_bindings[msvcrt.getch()] = MoveDirection.Down
                break
        print('Press ' + MoveDirection.Right.value + ' button')
        while True:
            if msvcrt.kbhit():
                self.__key_bindings[msvcrt.getch()] = MoveDirection.Right
                break
        print('Press ' + MoveDirection.Left.value + ' button')
        while True:
            if msvcrt.kbhit():
                self.__key_bindings[msvcrt.getch()] = MoveDirection.Left
                break

    def gen_map(self):
        self.__map.clear()
        for fruits in self.__fruits:
            self.__map.build_fruit(fruits)
        self.__map.build_snake_head(self.__snake_list[0])
        self.__map.build_enemy_snake_head(self.__snake_list[1])
        self.__map.build_snake(self.__snake_list[0])
        self.__map.build_enemy_snake(self.__snake_list[1])
        for wall in self.__wall_list:
            self.__map.build_fruit_walls(wall)
        self.__map.build_walls()

    def print_map(self):
        clear()
        self.__map.print()

    def run(self):
        while True:
            time.sleep(0.1)
            # self.read_keyboard()
            for snakes in self.__snake_list:
                sorted_snake_list = self.__snake_list
                sorted_snake_list.remove(snakes)
                sorted_snake_list.insert(0, snakes)
                snakes.set_direction(choose_direction(sorted_snake_list, self.__fruits))
            # self.__snake_list[0].set_direction(choose_direction(self.__snake_list[0], self.__fruits))
            # self.__snake_list[1].set_direction(choose_direction(self.__snake_list[1], self.__fruits))
            # time.sleep(200)
            for snakes in self.__snake_list:
                snakes.move()
                snakes.grow()
            self.check_wall()
            self.gen_map()
            self.check_event(self.__snake_list, self.__fruits)
            self.gen_map()

            if self.__eog[0]:
                self.__map.place_eog_tile(self.__eog[1])
                self.print_map()
                print('Snail is dead')
                time.sleep(1)
                break

            self.print_map()

    def read_keyboard(self):
        start_time = time.time()
        key = ''
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in list(self.__key_bindings.keys()):
                    break
            elif time.time() - start_time > 1 / 5:
                break
        if key in list(self.__key_bindings.keys()):
            if self.__key_bindings[key] == MoveDirection.Pause:
                self.pause()
            else:
                self.__snake_list[0].change_dir(self.__key_bindings[key])

    def pause(self):
        print('Pause')
        print('Press "p" for unpause')
        while True:
            msvcrt.kbhit()
            if self.__key_bindings[msvcrt.getch()] == MoveDirection.Pause:
                print('Unpause...')
                time.sleep(0.5)
                break

    def check_event(self, snake_list, fruits):
        for snake in snake_list:
            # if snake.get_body[0] != snake.get_body[snake.get_length-1]:
            if self.__map.get_tile(snake.get_body[0][0], snake.get_body[0][1]) in snake.get_death_tiles:
                snake.respawn(self.__map, *self.__snake_list, *self.__fruits, *self.__wall_list)
            # if self.__map.get_tile(snake.get_body[0][0], snake.get_body[0][1]) == TileType.Wall:
            #     self.__eog[0] = 1
            #     self.__eog[1] = snake.get_body[0]
            if self.__map.get_tile(snake.get_body[0][0],
                                   snake.get_body[0][1]) == TileType.Fruit or TileType.Big_Fruit or TileType.Wall_Fruit:
                for i in range(len(fruits.copy())):
                    if snake.get_body[0] == fruits[i].get_pos:
                        snake.grow_points = fruits[i].type.value
                        if fruits[i].type == FruitType.Wall:
                            self.__wall_list.append(Wall(self.__map, *self.__snake_list, *self.__fruits, *self.__wall_list))
                        self.__fruits.pop(i)
                        self.__fruits.append(Fruit(self.__map, *self.__snake_list, *self.__fruits, *self.__wall_list))

    def check_wall(self):
        for wall in self.__wall_list:
            wall.low_lifetime()
            if wall.get_lifetime == 0:
                self.__map.remove_fruit_walls(wall)
                self.__wall_list.remove(wall)


CollideTiles = [TileType.Wall, TileType.Snake, TileType.Snake_Head, TileType.Enemy_Snake, TileType.Enemy_Snake_Head]
Game = Manager(Map(20, 20), Snake(3, is_player=1), Snake(3))
Game.initialize()
Game.run()
