import pyautogui as pt
import time


# Координаты
# кнопка "Ознакомлен"
eye_x, eye_y = (1806, 373) # строка № 1
# eye_x, eye_y = (1806, 487) # строка № 2
# eye_x, eye_y = (1806, 520) # строка № 2 - после сдвига кнопок вниз
# кнопка подтвердить
cnf_x, cnf_y = (1123, 632)

# Цвета кнопок
view_btn_clrs = [
    (235, 141, 59),
    (232, 124, 31),
    (241, 176, 120),
]
confirm_btn_clrs = [(99, 172, 99), (109, 177, 109)]

view_btn_clr = confirm_btn_clr = None

def click_one():
    pt.moveTo(eye_x, eye_y, duration = 0.25)
    current_color = pt.pixel(eye_x, eye_y)
    # print(current_color)
    if current_color in view_btn_clrs:
        view_btn_clr = current_color
        pt.click(eye_x, eye_y)
        time.sleep(0.5)
    else:
        time.sleep(1)
        print("Ждем... 'ознакомлен'")
        print(f'цвет: {current_color} должен быть - {view_btn_clr}')
        click_one()

def click_two():
    current_color = pt.pixel(cnf_x, cnf_y)
    # pt.moveTo(cnf_x, cnf_y, duration = 0.25)
    print(current_color)
    if current_color in confirm_btn_clrs:
        confirm_btn_clr = current_color
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
    for step in range(amount):
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


just_do(5)
# print(pt.pixel(eye_x, eye_y))

# while True:
#     print_position_info()
#     time.sleep(0.5)
