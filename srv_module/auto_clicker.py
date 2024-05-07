import pyautogui as pt
import time


# кнопка "Ознакомлен"
# eye_x, eye_y = (1806, 373) # строка № 1
eye_x, eye_y = (1806, 487) # строка № 2
# eye_r, eye_g, eye_b = (88, 158, 213) # 1 вариант цвета
eye_r, eye_g, eye_b = (144, 191, 227) # 2 вариант цвета

def click_one():
    # pt.moveTo(1806, 486, duration = 0.25)

    current_color = pt.pixel(eye_x, eye_y)
    # if current_color == (88, 158, 213): # 1 вариант цвета
    if current_color == (eye_r, eye_g, eye_b): # 2 вариант цвета
        pt.click(eye_x, eye_y)
        time.sleep(0.5)
    else:
        time.sleep(1)
        print("Ждем... 'ознакомлен'")
        print(f'цвет: {current_color} должен быть - {(eye_r, eye_g, eye_b)}')
        click_one()

# кнопка подтвердить
cnf_x, cnf_y = (1123, 632)
cnf_r, cnf_g, cnf_b = (99, 172, 99)

def click_two():
    current_color = pt.pixel(cnf_x, cnf_y)
    if current_color == (99, 172, 99):
        pt.click(cnf_x, cnf_y)
        time.sleep(1)
    else:
        time.sleep(1)
        print("Ждем... 'подтверждение'")
        click_two()

# сообщает ткущие координаты мыши и цвет пикселя
def print_position_info():
    coord = pt.position()
    px = pt.pixel(coord[0], coord[1])
    print(px, coord, end = '\r')
    # print()

def just_do(amount):
    start_time = time.time()
    errors_counter = 0
    counter = 0
    for step in range(amount + 1):
        try:
            click_one()
            click_two()
            counter += 1
            print(f"Закрыли: {counter}")
        except:
            errors_counter += 1
            print(f"Ошибка №: {errors_counter}")
        pt.moveTo(1, 1)
    cur_sec = round((time.time() - start_time), 2)
    print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
    print(f'Закрыто документов: {counter}\nКол-во ошибок: {errors_counter}')


just_do(44)
# print(pt.pixel(eye_x, eye_y))

# while True:
#     print_position_info()
#     time.sleep(0.5)
