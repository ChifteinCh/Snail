
import random
#import keyboard
import time
import msvcrt
# a

# todo пока задания такие:
#  0. Напиши мне по комменту на 85 строке
#  1. Все замечания исправить
#  2. Добавить паузу по нажатию какой-то кнопки
#  3. Добавить ещё один вид фруктов, который будет добавлять 3 ячейки к змейке (как - на твоё усмотрение)
#  4. Добавить победное сообщение (когда змейка всё поле заполняет)
#  5. Выпили все комменты ненужные

# todo твёрдо и чётко, имя функции должно начинаться с глагола, исправь везде, много где гавно
def matrix_print(matrix):
    print()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')
        print()


def snail_spawn(snail_length, dimensions_xy):
    if snail_start_length > dimensions_xy[0]//2:
        print('Error. Snake is to big to spawn')
        return
    snail_body = []
    for i in range(snail_length):
        snail_body.append([dimensions_xy[1]//2+1, dimensions_xy[0]//2+1-i])
    return snail_body


def build_walls(map, corn_wall_tile, vert_wall_tile, hor_wall_tile):
    x = len(map[1])
    y = len(map)
    map[0][0] = map[y-1][0] = map[0][x-1] = map[y-1][x-1] = corn_wall_tile
    map[0][1:x-1] = map[y-1][1:x-1] = hor_wall_tile*(x-2)
    for i in range(y-2):
        map[i+1][0] = map[i+1][x-1] = vert_wall_tile
    return map


def build_snail(map, snail_body, snail_tile):
    for i in range(len(snail_body)):
        map[snail_body[i][0]][snail_body[i][1]] = snail_tile
    return map


def build_fruit(map, fruit_pos, fruit_tile):
    map[fruit_pos[0]][fruit_pos[1]] = fruit_tile
    return map


def map_generator(dimensions_xy, snail_body, fruit_pos):
    map_size_xy = [dimensions_xy[0]+2, dimensions_xy[1]+2]
    map = [['.']*map_size_xy[0] for i in range(map_size_xy[1])]
    map = build_walls(map, 'C', 'V', 'H')
    map = build_fruit(map, fruit_pos, 'o')
    map = build_snail(map, snail_body, 's')

    return map


def snail_is_growing():
    # todo можно append заюзать, вообще не стесняйся после нажатия точки рассматривать, какие там есть методы и их описания
    snail_body.insert(len(snail_body), tail)


# todo не до конца прозрачное название. сейчас тут по сути проверяется взаимодействие с фруктом либо стеной, поэтому я бы написал что-то типа check_collision
def snail_is_checking():
    # todo пучарм подсказывает, что вот след. строка нахуй не нужна
    event = ''
    if snail_body[0] == fruit_pos:
        snail_is_growing()
        event = 'f'
        return event

    for i in range(len(snail_body)-1):

        if snail_body[0] == snail_body[i+1]:
            event = 'd'
            return event
    # todo чо тут происходит, напиши в личку, нихуя не понял
    if snail_body[0][0] == 0 or snail_body[0][1] == 0:
        event = 'd'
        return event
    if snail_body[0][0] > dimensions_xy[1] or snail_body[0][1] > dimensions_xy[0]:
        event = 'd'
        return event

# todo есть такой "принцип" - dry (don`t repeat yourself), то есть не повторять один и тот же код (иногда это уместно
#  но редко) а в следующих 4 методах ты пишешь один и тот же код, отличающийся двумя плюсами/минусами. конкретно тут
#  я написал бы также, но в большинстве случаев лучше так не писать, поэтому исправим. нужно вместо этих 4ёх функций,
#  сделать одну (соответственно, там ещё аргументы добавятся).
#  Нажимай иногда ctrl-alt-L, он тебе пофиксит стиль в файле, будешь видить как правильно должно всё выглядеть
def snail_moves_right(snail_body):
    snail_body.pop()
    snail_body.insert(0, [snail_body[0][0], snail_body[0][1]+1])
    return snail_body


def snail_moves_up(snail_body):
    snail_body.pop()
    snail_body.insert(0, [snail_body[0][0]-1, snail_body[0][1]])
    return snail_body


def snail_moves_down(snail_body):
    snail_body.pop()
    snail_body.insert(0, [snail_body[0][0]+1, snail_body[0][1]])
    return snail_body


def snail_moves_left(snail_body):
    snail_body.pop()
    snail_body.insert(0, [snail_body[0][0], snail_body[0][1]-1])
    return snail_body


def snail_saves_direction(snail_body, snail_direction):
    # todo if-elif в петухоне писать вполне одобряемо (а в c# кстати в таком случае нет). Но для общего развития
    #  давай используем тут вместо ифов конструкцию match-case
    if snail_direction == 'R':
        snail_body = snail_moves_right(snail_body)
    if snail_direction == 'L':
        snail_body = snail_moves_left(snail_body)
    if snail_direction == 'U':
        snail_body = snail_moves_up(snail_body)
    if snail_direction == 'D':
        snail_body = snail_moves_down(snail_body)
    return snail_body


def fruit_generation(dimensions_xy, snail_body):
    possible_tiles = []
    for i in range(dimensions_xy[1]):
        possible_tiles.append([1] * dimensions_xy[0])

    for x in range(dimensions_xy[0]):
        for y in range(dimensions_xy[1]):
            possible_tiles[y][x] = x+1

    for i in range(len(snail_body)):
        x = snail_body[i][1]-1
        y = snail_body[i][0]-1
        possible_tiles[y][x] = 0

    #matrix_print(possible_tiles)

    for i in range(len(possible_tiles)):
        for j in possible_tiles[i].copy():
            if j == 0:
                possible_tiles[i].remove(j)

    #matrix_print(possible_tiles)

    fruit_y = random.randrange(1, dimensions_xy[1]+1)
    fruit_x = random.choice(possible_tiles[fruit_y-1])
    fruit_pos = [fruit_y, fruit_x]
    print(fruit_pos)
    return fruit_pos


def snail_is_moving(snail_body, snail_direction, key, key_bindings):
    # todo думаю лучше использовать if-elif-else, у тебя же только одно действие возможно, а не несколько,
    #  лишние проверки пропустятся
    #  + давай посмотрим, что такое enum и заюзаем его (вместо букв для направления)
    if key == key_bindings[2] and snail_direction != 'L':
        snail_body = snail_moves_right(snail_body)
        snail_direction = 'R'

    if key == key_bindings[0] and snail_direction != 'D':
        snail_body = snail_moves_up(snail_body)
        snail_direction = 'U'

    if key == key_bindings[3] and snail_direction != 'R':
        snail_body = snail_moves_left(snail_body)
        snail_direction = 'L'

    if key == key_bindings[1] and snail_direction != 'U':
        snail_body = snail_moves_down(snail_body)
        snail_direction = 'D'

    #else:
    #    snail_body = snail_saves_direction(snail_body, snail_direction)
    #    break
    return snail_body, snail_direction


# todo вот тут хорошее название функции
def install_keys():
    print('Prepare for the game!')
    i = 0
    #todo давай попробуем не два массива использовать, а словарь, он здесь лучше подходит
    key_bindings = [0, 0, 0, 0]
    button_names = ['Up', 'Down', 'Right', 'Left']
    while i < 4:
        print('Press '+button_names[i]+' button')
        while True:
            if msvcrt.kbhit():
                key_bindings[i] = msvcrt.getche()
                i = i + 1
                break
    return(key_bindings)


key_bindings = install_keys()

dimensions_xy = [10, 10]
snail_start_length = 3
snail_direction = 'R'
#fruit_is_eaten = 0
time_delay = 1/5

snail_body = snail_spawn(snail_start_length, dimensions_xy)

fruit_pos = fruit_generation(dimensions_xy, snail_body)

map = map_generator(dimensions_xy, snail_body, fruit_pos)
matrix_print(map)
print('')
print('')

while True:
    time.sleep(0.5)
    key = ''
    #key = keyboard.read_key()
    #if key == 'q':
    #    print('exit')
    #    time.sleep(1)
    #    break

    tail = snail_body[len(snail_body)-1]

    start_time = time.time()
#    print(msvcrt.kbhit())
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getche()
#            print(key)
#            if key == 'w':
#                print(True)
#            else:
#                print(False)
            break
        elif time.time() - start_time > time_delay:
            break

    if key:
        snail_body, snail_direction = snail_is_moving(snail_body, snail_direction, key, key_bindings)
    else:
        snail_body = snail_saves_direction(snail_body, snail_direction)

    event = snail_is_checking()
    if event == 'f':
        fruit_pos = fruit_generation(dimensions_xy, snail_body)
    elif event == 'd':
        print('snail is dead')
        time.sleep(2)
        break

    map = map_generator(dimensions_xy, snail_body, fruit_pos)
    matrix_print(map)

    #print(snail_body[0])

print('end of game')
