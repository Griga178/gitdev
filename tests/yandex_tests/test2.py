
# def str_to_coord(coord_string):
#     a, b = coord_string.split(' ')
#     return int(a), int(b)
#
# def get_chess_coord_s(chess_size):
#     # все клетки, на которых могут стоять шашки
#     chess_coord_s = set()
#     max_x, max_y = chess_size
#     ny = 1
#     st = 1
#     for x in range(1, max_x + 1, 1):
#         for y in range(ny, max_y + ny, 2):
#             chess_coord_s.add((x, y))
#             # print((x, y))
#         ny = ny + st
#         st = st * (-1)
#     return chess_coord_s
#
# def define_move_cells(coord, chess_coord_s):
#     # Определяем координаты клеток, куда может сходить шашка
#     move_cells = set()
#     # max_x, max_y = chess_size
#     x, y = coord
#
#     neighbour_coord = {
#         (x + 1, y - 1), # вверх + лево
#         (x + 1, y + 1), # вверх + право
#         (x - 1, y + 1), # вниз + лево
#         (x - 1, y - 1), # вниз + право
#     }
#     ns = neighbour_coord & chess_coord_s
#     # print(ns)
#
#     # for i_coord in neighbour_coord:
#     #     i_x, i_y = i_coord
#     #     if i_x >= 1 and i_y >= 1:
#     #         if i_x <= max_x and i_y <= max_y:
#     #             move_cells.add(i_coord)
#     #
#     # print(move_cells)
#
#     return ns
#
# def get_near_enemies(move_cells, enemy_cels):
#     enemies = move_cells & enemy_cels
#     return enemies
#
# def can_eat(figure, enemies, all_figures, chess_coord_s):
#     for enem_coord in enemies:
#         # ячейка, на которую встанет шашка после обеда
#         delta_x = enem_coord[0] - figure[0]
#         delta_y = enem_coord[1] - figure[1]
#
#         target_cell = (enem_coord[0] + delta_x, enem_coord[1] + delta_y)
#         # print('target', target_cell)
#
#         if target_cell in chess_coord_s:
#             # print('target', target_cell)
#
#             if target_cell not in all_figures:
#                 # print('clear target', target_cell)
#                 return True
#     else:
#         return False






# chess_size = str_to_coord('8 8')
#
# white_amount = 3
# w_pos = ['1 1', '2 6', '6 6']
#
# black_amount = 3
# b_pos = ['2 2', '7 7', '8 8']
# turn = 'white'
#
# white_pos = set()
# for i in range(white_amount):
#     white_pos.add(str_to_coord(w_pos[i]))
#
# black_pos = set()
# for i in range(black_amount):
#     black_pos.add(str_to_coord(b_pos[i]))
#
# turn = 'white'
# turn = 'black'

# процесс
# строки --> в [int, int]
# Определяем координаты клеток, куда может сходить шашка
# Проверяем есть ли в этих клетках шашки соперника (Ш-С)
# если есть:
# Ш-С проверяем следующую клетку на возможность перемещения
# если есть --> Yes
# если нет, проверяем следующую шашку
# else --> No

def str_to_coord(coord_string):
    a, b = coord_string.split(' ')
    return int(a), int(b)

def get_chess_coord_s(chess_size):
    # все клетки, на которых могут стоять шашки
    chess_coord_s = set()
    max_x, max_y = chess_size
    ny = 1
    st = 1
    for x in range(1, max_x + 1, 1):
        for y in range(ny, max_y + ny, 2):
            chess_coord_s.add((x, y))
        ny = ny + st
        st = st * (-1)
    return chess_coord_s

def define_move_cells(coord, chess_coord_s):
    # Определяем координаты клеток, куда может сходить шашка
    move_cells = set()
    x, y = coord

    neighbour_coord = {
        (x + 1, y - 1), # вверх + лево
        (x + 1, y + 1), # вверх + право
        (x - 1, y + 1), # вниз + лево
        (x - 1, y - 1), # вниз + право
    }
    ns = neighbour_coord & chess_coord_s
    return ns

def get_near_enemies(move_cells, enemy_cels):
    enemies = move_cells & enemy_cels
    return enemies

def can_eat(figure, enemies, all_figures, chess_coord_s):
    for enem_coord in enemies:
        # ячейка, на которую встанет шашка после обеда
        delta_x = enem_coord[0] - figure[0]
        delta_y = enem_coord[1] - figure[1]
        target_cell = (enem_coord[0] + delta_x, enem_coord[1] + delta_y)
        # эта ячейка на доске?
        if target_cell in chess_coord_s:
            # Эта ячейка свободна?
            if target_cell not in all_figures:
                return True
    else:
        return False

# Ввод
chess_size = str_to_coord(input())

white_amount = int(input())
white_pos = set()
for i in range(white_amount):
    white_pos.add(str_to_coord(input()))

black_pos = set()
black_amount = int(input())
for i in range(black_amount):
    black_pos.add(str_to_coord(input()))
turn = input()

if turn == 'white':
    friend_cells = white_pos
    enemy_cells = black_pos
else:
    friend_cells = black_pos
    enemy_cells = white_pos

chess_coord_s = get_chess_coord_s(chess_size)

for figure in friend_cells:
    move_cells = define_move_cells(figure, chess_coord_s)
    near_enemies = get_near_enemies(move_cells, enemy_cells)
    if near_enemies:
        if can_eat(figure, near_enemies, enemy_cells|friend_cells, chess_coord_s):
            print("Yes")
            break
else:
    print("No")
