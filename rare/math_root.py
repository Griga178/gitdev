'''
    a = i^n
    i = a ** (1/n)
    n = logarifm (base = i, target = a)
    Поиск корня числа A, из N степеней

    Пример:
    За 5 лет (period = 5) депозит без вложений
    вырос в 1024 раза (1 USD → 1024 USD)

    Вопрос
    Как изменяется депозит при тех же условиях за 1 год?

    Решение
    get_root(5, 1024) → 4 — увеличение в 4 раза в год (или 300% годовых)

     1*4*4*4*4*4 = 1024
     4^5 = 1024

'''

def get_root_old(n, a, d = 2):
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

def get_root(n, a, d=2):
    ''' root ^ n = a '''
    if n <= 0:
        raise ValueError("Степень корня n должна быть положительным числом")
    if a < 0 and n % 2 == 0:
        raise ValueError("Нельзя вычислить четный корень из отрицательного числа")

    d = min(d, 15)
    root = a ** (1 / n)
    return round(root, d)


period = 15
revenue = 960000


m_root = get_root(period, revenue, 3)
print(f'Increase per step', m_root)
