param_for_parser = {
    "links": ['', ''],
    "base": {
        "parse": True, # zakupki, всякие конфигураторы = False
        "unknown_defend": False, # у прим.: Ozone: True - делаем только скрин
        "js_content": True,
        "screenshot": 'C:/Users/G.Tishchenko/Desktop/screens_2_2022/', # False - не делать
        "screenshot_sleep": 5,
        },
    "tags": {
        "price": ['div', 'class', 'price'],
        "name": ['div', 'class', 'name'],
        },
    "xpath": {
        "price": "//div[@class = что то там][5]"
        },
    "check_push": [['id', 'chouse_city', 'button']] # нажать на кнопку если появится элемент


}

return_dict = {
    "link": {
        "price": 100.50,
        "name": "Нож",
        "screenshot_name": "1.jpg"
        }
    }


''' 0 - где проверка наличие указанных папок? создавать новые?
    0 - все настройки переданы
        если в "tags", ничего нет - делаем только скриншоты 1.2

    1 - (parse:true, tags):
            unknown_defend: => идем сразу 1.2
            получение html - данных проверка на response(200)
    1.1 - нахождение искомого по тегам
    1.2 - делаем скриншот
        unknown_defend:
            открываем webbrowser - скрин

    2 - выдача yield - что бы сразу в БД сохранить

Способы делать скрины:
    1 webbrowser (ctr + w) - проверка раскладки клавиатуры (eng)? (хз почему)
      pyautogui - скрин
    2 selenium
      pyautogui - скрин
      selenium - скрин - без панели задач (не все сайты, пока что)

    ps сохранение meta данных в jpg файле

Настройки selenium:
    - полный экран
    - убрать автоматический режим
    - смена прокси, на определенных сайтах
'''
