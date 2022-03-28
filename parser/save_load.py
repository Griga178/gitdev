'''
ФУНКЦИИ
СОХРАНЯЕМ
ЗАГРУЖАЕМ
PICKLE
EXCEL
WORD
PDF
SQL?
'''
import pickle

def pkl_saver(file_name, variable_name):
    with open(file_name, 'wb') as f:
        pickle.dump(variable_name, f, pickle.HIGHEST_PROTOCOL)
        
def pkl_set_reader(file_name):
    with open(file_name, 'rb') as f:
        pickle_set = pickle.load(f)
    return pickle_set
