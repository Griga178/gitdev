import time
import threading
from random import randint

def get_query(mes = randint(1,5)):

    print(f'ждем {mes} сек...') #, end = '\r'
    time.sleep(mes)
    print(f'{mes}  Готово')

url_s = [randint(1,5) for el in range(1000)]

threads = []

for el in url_s:
    t = threading.Thread(target = get_query, args = [el])
    t.start()
    threads.append(t)

for el in threads:
    el.join()




print(time.perf_counter(), 'Готово')
