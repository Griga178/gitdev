from srv_helper import *





name = 'Tishchenko_GL'
passe = 'cmec789'


driver.get(page_enter)


if authorization_func(name, passe):
    print('All is OK')


considering = 'На рассмотрении'
my_reports = 'Мои отчеты'
new_project = 'Новый проект исходящего'


#link_by_wbtitle(new_project)
#driver.get(main_page)
find_document_by_number('04-8712/21-0-0')

driver.close()
