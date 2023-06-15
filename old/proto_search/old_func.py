# первый вариант парсинга таблицы очень долгий из за часты запросов к странице
def table_pars():### Заменяем Эту Часть!
    # Создаем список наименований с вложенными словарями
    list_name_char = []
    row_range = 0
    number_g = 0
    row_path = '//*[@id="contract_subjects"]/tbody/tr'
    list_of_rows = driver.find_elements_by_xpath(row_path)
    row_range = len(list_of_rows)
    for row_num in range(1, row_range, 2):
        number_g += 1
        # Создаем словарь Наименование - Характеристика
        char_value = {}
        for cell_num in [2, 3, 4, 5, 6]:
            # Создаем словарь Характеристика - Значение;
            #   список словарей: имя товара характеристики
            x_path = f'//*[@id="contract_subjects"]/tbody/tr[{row_num}]/td[{cell_num}]'
            value = driver.find_element_by_xpath(x_path).text

            if cell_num == 2:
                # Наименование товара (+ страна происхождения Россия: 2 div)
                value_list = value.split("\n")
                # Наименование = ключ к словаре
                goods_name = value_list[0]
                if len(value_list) == 2:
                    # характеристика страны
                    value_country = value_list[1].replace('Страна происхождения: ', '')
                    char_value = char_value | {'Country': value_country}

            elif cell_num == 3:
                # ОКПД2 и КТРУ (ВОЗМОЖНО)
                value_list = value.split("\n")
                if len(value_list) == 3:
                    # характеристика КТРУ
                    ktru_val = value_list[1].replace('(', '').replace(')', '')
                    char_value = char_value | {'KTRU': ktru_val}
                okpd_val = value_list[-1].replace('(', '').replace(')', '')
                char_value = char_value | {'OKPD2': okpd_val}

            elif cell_num == 4:
                # Тип объекта (прим. Товар)
                char_value = char_value | {'Type': value}

            elif cell_num == 5:
                # Количество
                '''
                amount_val = []
                for el in value:
                    if el in {'1', '2', '3', '4', '5', '6', '7', '8','9', '0'}:
                        amount_val.append(el)
                '''
                try:
                    char_value = char_value | {'Amount': string_to_float(value)} #''.join(amount_val)
                except:
                    char_value = char_value | {'Amount': value}
                    print('\n\n', [value], 'ВНИМАНИИЕЕЕ\n\n')

            elif cell_num == 6:
                # Цена за ед
                char_value = char_value | {'Price': float(value.replace(',', '.').replace(' ', ''))}

        # Упаковываем словари в список
        list_name_char.append({goods_name: char_value})
        #print(number_g, goods_name)

    return list_name_char
