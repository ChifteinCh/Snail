import random
import time
import msvcrt
import enum
import os


def clear():
    os.system('cls')


class MoveDirection(enum.Enum):
    Up = 'Up'
    Down = 'Down'
    Right = 'Right'
    Left = 'Left'
    Pause = 'Pause'


class TileType(enum.Enum):
    Floor = '.'
    Wall = 'W'
    Snake = 's'
    Snake_End = 's'
    Collide = '!'
    Fruit = 'f'
    Big_Fruit = 'F'
    Wall_Fruit = 'w'


class FruitType(enum.Enum):
    Normal = 1
    Big = 3
    Wall = 0


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
        self.__map[0][0:self.__height] = self.__map[self.__length - 1][0:self.__height] = [TileType.Wall] * self.__height
        for i in range(self.__length - 1):
            self.__map[i][0] = self.__map[i][self.__height - 1] = TileType.Wall

    def build_snake(self, snake):
        for i in range(snake.get_length-1):
            self.__map[snake.get_body[i][0]][snake.get_body[i][1]] = TileType.Snake
        self.__map[snake.get_body[snake.get_length-1][0]][snake.get_body[snake.get_length-1][1]] = TileType.Snake_End

    def build_fruit(self, fruit):
        self.__map[fruit.position[0]][fruit.position[1]] = fruit.tile

    def place_eog_tile(self, eog_pos):
        self.__map[eog_pos[0]][eog_pos[1]] = TileType.Collide

    def build_fruit_walls(self, wall):
        if wall.get_lifetime > 0:
            self.__map[wall.get_pos[0]][wall.get_pos[1]] = TileType.Wall
            if self.__map[wall.get_pos[0]][wall.get_pos[1]-1] == TileType.Floor:
                self.__map[wall.get_pos[0]][wall.get_pos[1] - 1] = TileType.Wall
            if self.__map[wall.get_pos[0]][wall.get_pos[1]+1] == TileType.Floor:
                self.__map[wall.get_pos[0]][wall.get_pos[1] + 1] = TileType.Wall
            if self.__map[wall.get_pos[0]-1][wall.get_pos[1]] == TileType.Floor:
                self.__map[wall.get_pos[0] - 1][wall.get_pos[1]] = TileType.Wall
            if self.__map[wall.get_pos[0]+1][wall.get_pos[1]] == TileType.Floor:
                self.__map[wall.get_pos[0] + 1][wall.get_pos[1]] = TileType.Wall


class Snake:
    def __init__(self, length=3):
        self.__length = length
        self.__body = [[0, 0] for i in range(self.__length + 1)]
        self.__move_dir = MoveDirection.Right
        self.__grow_points = 0

    @property
    def get_body(self):
        return self.__body

    @property
    def get_length(self):
        return self.__length

    @property
    def grow_points(self):
        return self.__grow_points

    @grow_points.setter
    def grow_points(self, points):
        self.__grow_points = self.__grow_points + points

    def spawn(self, spawn_map):
        if self.__length > (spawn_map.map_dim[0] - 2) // 2:
            print('Error. Snake is to big to spawn')
            return
        for i in range(self.__length):
            self.__body[i][0] = (spawn_map.map_dim[0] - 2) // 2 + 1 - i
            self.__body[i][1] = (spawn_map.map_dim[1] - 2) // 2 + 1

    def move(self):
        self.grow()
        match self.__move_dir:
            case MoveDirection.Up:
                self.__body.insert(0, [self.__body[0][0], self.__body[0][1] - 1])
            case MoveDirection.Right:
                self.__body.insert(0, [self.__body[0][0] + 1, self.__body[0][1]])
            case MoveDirection.Down:
                self.__body.insert(0, [self.__body[0][0], self.__body[0][1] + 1])
            case MoveDirection.Left:
                self.__body.insert(0, [self.__body[0][0] - 1, self.__body[0][1]])

    def change_dir(self, direction):
        if direction == MoveDirection.Right and self.__move_dir != MoveDirection.Left:
            self.__move_dir = MoveDirection.Right
        elif direction == MoveDirection.Up and self.__move_dir != MoveDirection.Down:
            self.__move_dir = MoveDirection.Up
        elif direction == MoveDirection.Left and self.__move_dir != MoveDirection.Right:
            self.__move_dir = MoveDirection.Left
        elif direction == MoveDirection.Down and self.__move_dir != MoveDirection.Up:
            self.__move_dir = MoveDirection.Down

    def grow(self):
        if self.__grow_points == 0:
            self.__body.pop()
        elif self.__grow_points > 0:
            self.__length += 1
            self.__grow_points -= 1


class Fruit:
    def __init__(self):
        self.__pos = [0, 0]
        self.__type = FruitType.Normal
        self.__tile = TileType.Fruit

    @property
    def position(self):
        return self.__pos

    @property
    def tile(self):
        return self.__tile

    @property
    def type(self):
        return self.__type

    def spawn(self, map_, *snake_list):
        possible_tiles = []
        for i in range(map_.map_dim[1] - 2):
            possible_tiles.append([1] * (map_.map_dim[0] - 2))

        for x in range(map_.map_dim[0] - 2):
            for y in range(map_.map_dim[1] - 2):
                possible_tiles[y][x] = x + 1
        for snake in snake_list:
            for i in range(snake.get_length):
                x = snake.get_body[i][0] - 1
                y = snake.get_body[i][1] - 1
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

        fruit_y = random.choice(possible_rows) + 1
        fruit_x = random.choice(possible_tiles[fruit_y - 1])
        self.__pos = [fruit_x, fruit_y]
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

    def __init__(self, map_, *snakes):
        self.__pos = [0, 0]
        self.__lifetime = 5
        self.spawn_wall(map_, *snakes)

    @property
    def get_pos(self):
        return self.__pos

    @property
    def get_lifetime(self):
        return self.__lifetime

    def spawn_wall(self, map_, *snakes):
        possible_tiles = []
        for i in range(map_.map_dim[1] - 2):
            possible_tiles.append([1] * (map_.map_dim[0] - 2))

        for x in range(map_.map_dim[0] - 2):
            for y in range(map_.map_dim[1] - 2):
                possible_tiles[y][x] = x + 1
        for snake in snakes:
            for i in range(snake.get_length):
                x = snake.get_body[i][0] - 1
                y = snake.get_body[i][1] - 1
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

        wall_y = random.choice(possible_rows) + 1
        wall_x = random.choice(possible_tiles[wall_y - 1])
        self.__pos = [wall_x, wall_y]

    def low_lifetime(self):
        if self.__lifetime > 0:
            self.__lifetime -= 1


class Manager:
    def __init__(self, map_, *snakes):
        self.__map = map_
        self.__fruits = [Fruit(), Fruit()]
        self.__snake_list = snakes
        self.__wall_list = []
        self.__snake_amount = len(self.__snake_list)
        self.__key_bindings = {b'p': MoveDirection.Pause}
        self.__eog = [0, [0, 0]]

    def initialize(self):
        clear()
        self.install_keys()
        clear()
        for snakes in self.__snake_list:
            snakes.spawn(self.__map)
        self.__map.build_walls()
        for snakes in self.__snake_list:
            self.__map.build_snake(snakes)
        for fruits in self.__fruits:
            fruits.spawn(self.__map, *self.__snake_list)
            self.__map.build_fruit(fruits)
        self.__map.print()

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
        clear()
        self.__map.clear()
        for snakes in self.__snake_list:
            self.__map.build_snake(snakes)
        for fruits in self.__fruits:
            self.__map.build_fruit(fruits)
        for wall in self.__wall_list:
            self.__map.build_fruit_walls(wall)

    def print_map(self):
        self.__map.print()

    def run(self):
        while True:
            time.sleep(0.5)
            start_time = time.time()
            key = ''
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key in list(self.__key_bindings.keys()):
                        break
                elif time.time() - start_time > 1/5:
                    break
            if key in list(self.__key_bindings.keys()):
                if self.__key_bindings[key] == MoveDirection.Pause:
                    self.pause()
                else:
                    self.__snake_list[0].change_dir(self.__key_bindings[key])
            for snakes in self.__snake_list:
                snakes.move()
            self.check_wall()
            self.check_event(self.__snake_list[0], self.__fruits)
            self.gen_map()

            if self.__eog[0]:
                self.__map.place_eog_tile(self.__eog[1])
                self.__map.print()
                print('Snail is dead')
                time.sleep(1)
                break

            self.print_map()

    def pause(self):
        print('Pause')
        print('Press "p" for unpause')
        while True:
            msvcrt.kbhit()
            if self.__key_bindings[msvcrt.getch()] == MoveDirection.Pause:
                print('Unpause...')
                time.sleep(0.5)
                break

    def check_event(self, snake, fruits):
        if snake.get_body[0] != snake.get_body[snake.get_length]:
            if self.__map.get_tile(snake.get_body[0][0], snake.get_body[0][1]) == TileType.Snake:
                self.__eog[0] = 1
                self.__eog[1] = snake.get_body[0]
        if self.__map.get_tile(snake.get_body[0][0], snake.get_body[0][1]) == TileType.Wall:
            self.__eog[0] = 1
            self.__eog[1] = snake.get_body[0]
        if self.__map.get_tile(snake.get_body[0][0], snake.get_body[0][1]) == TileType.Fruit or TileType.Big_Fruit or TileType.Wall_Fruit:
            for i in range(len(fruits)):
                if snake.get_body[0] == fruits[i].position:
                    snake.grow_points = fruits[i].type.value
                    if fruits[i].type == FruitType.Wall:
                        self.__wall_list.append(Wall(self.__map, *self.__snake_list))
                    self.__fruits[i].spawn(self.__map, *self.__snake_list)

    def check_wall(self):
        for wall in self.__wall_list:
            wall.low_lifetime()
            if wall.get_lifetime == 0:
                self.__wall_list.remove(wall)


Game = Manager(Map(4, 10), Snake(1))
Game.initialize()
Game.run()
