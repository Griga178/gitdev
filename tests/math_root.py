'''
    Да
    Поиск корня числа A, из N степеней

    Пример:
    За 3 года (n = 3), депозит с 1 у.е. вырос до 5 у.е. (a = 5)
    get_root(3, 5) --> 1.71 => 71% годовых
     1 * 1.71 * 1.71 * 1.71 = 5

'''

def get_root(n, a, d = 2):
    ''' Находит корень n-ой степени из числа a
        n - степень корня (кол-во реинвестирований)
        a - число под корнем (реинвестируемая прибыль - итог)
        d - количество знаков после '.' - точность
        m_root - искомый корень
    '''
    step = 1
    d = 15 if d > 15 else d # 17 чисел после '.' - это слишком!

    m_root = 0
    m_root_n = 0

    for i in range(16):
        # print(m_root)
        while m_root_n < a:
            m_root += step
            m_root_n = m_root ** n
        else:
            if m_root ** n == a:
                # НАШЛИ КОРЕНЬ
                break
            else:
                # НАШЛИ целое число округленное в меньш сторону от КОРНЯ
                m_root = m_root - step
                m_root_n = 0
                step = step / 10

    return round(m_root, d)


period = 3
revenue = 5

m_root = get_root(period, revenue)
print('Increase per "period"', m_root)
