"""
    не программа! 
    Тут тестирование добавления скриншотов в word
"""

import docx
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

source_info_docx = 'https://python-docx.readthedocs.io/en/latest/'

document = docx.Document()

section = document.sections[0]
#section = sections[0]
# Горизонтальный формат листа
new_width, new_height = section.page_height, section.page_width
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = new_width
section.page_height = new_height
# отступы на странице
section.top_margin = Inches(0.75)
section.left_margin = Inches(0.7)

# добавление верхнего колониткула
header = section.header
paragraph = header.paragraphs[0]
paragraph.text = "Title of my document"

footer = section.footer
paragraph = footer.paragraphs[0]
paragraph.text = "my footer"

#document.add_heading('Heading')

'''

section.top_margin = docx.shared.Inches(12) #Верхний отступ

section.left_margin = docx.shared.Inches(12) #Отступ слева

document.add_heading('Heading')
document.add_paragraph('terxt')
'''


sources =  ['../devfiles/ales_screenes/Otveti/БИОН ООО/112.jpg', '../devfiles/ales_screenes/Otveti/БИОН ООО/117.jpg']

for pic_name in sources:
    document.add_picture(pic_name, width=docx.shared.Inches(9.3), height=docx.shared.Inches(6.5))

#document.add_picture(source_2, width=Inches(9.3), height=docx.shared.Inches(9.3))


document.save('dem22.docx')

#print(section.orientation,section.page_width, section.page_height)
#print(section.left_margin, section.right_margin) # (Inches(1.25), Inches(1.25))
#print(section.top_margin, section.bottom_margin) # (Inches(1), Inches(1))
#print(section.header_distance, section.footer_distance)
