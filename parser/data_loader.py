import pickle
import os

'''
Загрузчик Базы данных
'''
# путь до файла PICKLE
cmec_path_name_settings = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/parser/Data_Folder/Sites_settings.pkl'
home_path_name_settings = False
current_path_name_settings = cmec_path_name_settings
current_path_name_settings = 'Data_Folder/Sites_settings.pkl'

cmec_path_name_links = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/parser/Data_Folder/Links_examples.pkl'



'''
В ПРОГРАММЕ НАПИСАТЬ:
my_dict = load_pkl_file()
if not my_dict:
    ФАЙЛА НЕ СУЩЕСТВУЕТ
'''
def save_pkl(variable_name, file_name):
    try:
        with open(file_name, 'wb') as f:
            pickle.dump(variable_name, f, pickle.HIGHEST_PROTOCOL)
    except:
        print(f'Проверь путь: {file_name}')


def load_pkl_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as f:
            pickle_file = pickle.load(f)
        return pickle_file
    else:
        return False
