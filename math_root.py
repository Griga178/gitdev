'''
    Поиск корня числа A, из N степеней
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



period = 3# * 12
period = 1392/365
inc = 0

m_root = get_root(period, 4.56)
print('rasp', m_root)
print((m_root - 1)*2000)
# inc += (m_root - 1)*2000 * 95
# m_root = get_root(period, 2.61)
# print('sberp', m_root)
# print((m_root - 1)*75000)
# inc += (m_root - 1)*75000
m_root = get_root(period, 5.05)
print('sber', m_root)
print((m_root - 1)*100000)
inc += (m_root - 1)*100000
m_root = get_root(period, 15.14)
print('bane', m_root)
print((m_root - 1)*100000)
inc += (m_root - 1)*100000
m_root = get_root(period, 4.56)
print('trmk', m_root)
print((m_root - 1)*100000)
inc += (m_root - 1)*100000

print(inc)
# m_root = get_root(6, 28.14)
# print(m_root)

# m_root = get_root(4, 150.0625, 3)
# print(m_root)
