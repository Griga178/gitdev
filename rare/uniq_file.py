'''
    если "имя.файл" существует возвращает "имя (1).файл" --> "имя (2).файл" и т.д
    https://stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number
'''
from os.path import splitext, exists

def uniquify(path: str) -> str:
    filename, extension = splitext(path)
    counter = 1
    while exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path



# folder = 'C:/Users/G.Tishchenko/Desktop/test/'
# target_name = 'test.txt' # func() --> 'test (1).txt'
# ff_path = folder + target_name
#
# a = uniquify(ff_path)
# print(a)
#
# with open(a, 'w') as target:
#     pass
