def manual_cicle():
    for el in range(100):
        print(el)
        a = input('Ввод: ')
        if a == 's':
            break
#manual_cicle()

#global c

'''
# дозаписывает в файл csv значения
# елси файла нет, создает новый
import csv

csv_file_name = 'new_file2.csv'
with open(csv_file_name, mode = "a") as file:
    file_writer = csv.writer(file, delimiter = ";") #, lineterminator="\r"
    for i in range(10):
        file_writer.writerow([i, i*2, i**2])
        print(i)
'''



file = 'C:/Users/G.Tishchenko/Desktop/Аквариус.msg'

print(file.split('/')[-1].replace('.msg', ''))
