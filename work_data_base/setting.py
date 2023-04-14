import sys
import getpass

SQL_FILE_NAME = 'work_db_v1.db'

user_name = getpass.getuser()

if user_name == 'G.Tishchenko':
    # вставка файла с любого места диска
    # sys.path.insert(1, 'C:/Users/G.Tishchenko/Desktop/myfiles')
    # import set
    DATA_BASE_PATH = f'sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/{SQL_FILE_NAME}'
