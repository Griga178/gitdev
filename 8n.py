# РАБОТА С DOC
'''
    Создать папки: images, otveti, ekranki
    Из папки ales_screenes otveti   название папки = doc_name
                                    содержимое папки doc_name.add_picture

'''
import docx
from docx.enum.section import WD_ORIENT
import os

name_file = 'new_file.docx'
name_name_file = 'new_file_2.docx'
#doc = docx.Document(name_file)
#all_paras = doc.paragraphs # doc list к элементам нужен .text
#paras_2 = doc.paragraphs[1].text # doc str
#print(paras_2)

dir_name_O = '../devfiles/images/Otveti'
dir_name_E = '../devfiles/images/Ekranki'
def create_dirs():
    try:
        os.mkdir(dir_name_O)
        os.mkdir(dir_name_E)
    except:
        print('Папки не создавалась')

#create_dirs()

source_O ='../devfiles/ales_screenes/Otveti'
source_E ='../devfiles/ales_screenes/Ekranki'

dir_source = source_O # где берем картинки и названия папок
dir_destiny = dir_name_O # куда сохраняем word.doc с картинками

list_comp_name = os.listdir(dir_source)

for el in list_comp_name[:1]:
    doc_file_name = dir_destiny + '/' + el + '.docx'
    new_doc = docx.Document().sections.orientation
    page =
    print('\n', doc_file_name, '\n')
    for image in (os.listdir(dir_source + '/' + el))[:5]:
        name_image = dir_source + '/' + el + '/' +  image
        new_doc.add_picture(name_image, width=docx.shared.Inches(6.69), height=docx.shared.Inches(4.33))
        print(name_image)
    new_doc.save(doc_file_name)
#my_doc = docx.Document(name_name_file)
#my_doc.add_paragraph("This is first paragraph of a MS Word file.")
#third_para = my_doc.add_paragraph("This is the third paragraph.")
#third_para.add_run(" this is a section at the end of third paragraph")


#name_picture = '../devfiles/scr/new/1.jpg'
#my_doc.add_picture(name_picture, width=docx.shared.Inches(6.69), height=docx.shared.Inches(4.33)) #width=docx.shared.Inches(6.69), height=docx.shared.Inches(4.33)
#my_doc.save(name_name_file)
