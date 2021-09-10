import docx
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

x = 'https://python-docx.readthedocs.io/en/latest/'

document = docx.Document()

sections = document.sections
section = sections[0]
new_width, new_height = section.page_height, section.page_width
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = new_width
section.page_height = new_height
section.top_margin = Inches(0.7)
section.left_margin = Inches(0.7)

#document.add_heading('Heading')

'''

section.top_margin = docx.shared.Inches(12) #Верхний отступ

section.left_margin = docx.shared.Inches(12) #Отступ слева

document.add_heading('Heading')
document.add_paragraph('terxt')
'''

source_O ='../devfiles/ales_screenes/Otveti/БИОН ООО/112.jpg'
source_2 ='../devfiles/ales_screenes/Otveti/БИОН ООО/117.jpg'



document.add_picture(source_O, width=docx.shared.Inches(10), height=docx.shared.Inches(7.2))
#document.add_page_break()
document.add_picture(source_2, width=Inches(10), height=docx.shared.Inches(7.2))

document.save('dem22.docx')

#print(section.orientation,section.page_width, section.page_height)
#print(section.left_margin, section.right_margin) # (Inches(1.25), Inches(1.25))
#print(section.top_margin, section.bottom_margin) # (Inches(1), Inches(1))
#print(section.header_distance, section.footer_distance)
