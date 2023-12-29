from db_search.aone import read_query_xlsx, read_work_table

file_path = 'C:/Users/G.Tishchenko/Desktop/test.xlsx'
fpath =  'C:/Users/G.Tishchenko/Desktop/test2.xlsx'

wt_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/19 Бытовые приборы.xlsx'
с_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/19 Контракты.xlsx'

wt_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/26 Оборудование для театрально.xlsx'
с_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/26 Контракты.xlsx'

wt_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/3 компьютерное.xlsx'
с_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/3 Контракты.xlsx'

wt_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/3 Нормирование.xlsx'
с_path = 'C:/Users/G.Tishchenko/Desktop/1 кв 2024/3Н Контракты.xlsx'
# read_query_xlsx(file_path, sheet_name = 'Лист1', fpath = fpath)

read_work_table(wt_path, fpath = с_path)
