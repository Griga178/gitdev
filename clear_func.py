def stand_clear(xval):
    # созздается список значений, которые нам нужны
    # послепервого добавления добавятся '.' ',' '0'
    signs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    # создаем пустой список, в который вставим только значения из signs
    clear_num_1 = []

    if 'Старая' in xval:
        # на сайте xcom встречается 'Старая цена 123 руб. новая цена 20 руб.' перед новой
        # тут мы отсекаем все до первого 'руб.'
        old_rub = xval.index('руб')
        xval = (xval[old_rub+5:])

    elif 'экономии' in xval: # специально для сайта videoglaz
        xval = xval.split('\n')[2]
    elif 'product-buy__price' in xval:
        xval = xval.split('buy__prev')[0]

    for i in xval:
        if i in signs:          # работает, но надо отредактировать (есть бесполезные действия)
            if (i == '.' or i == ','):
                if i in clear_num_1: # что бы вставить только одну "." или ","
                    break
            clear_num_1.append(i)
            signs.append('.')
            signs.append(',')
            signs.append('0')
    a = ''.join(clear_num_1).replace(',', '.')
    try:
        a = float(a)
        return a
    except:
        print(f'ERROR in standart {xval}')
        return 'no price'
