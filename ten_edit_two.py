
from bs4 import BeautifulSoup

def get_uploaded_files(driver):

    soup = BeautifulSoup(driver.page_source, 'lxml')

    tag = 'table'
    atribute = 'id'
    atr_val = 'grid_1h2vd8eofi9a2l2bfs4'

    print(soup)
'table'
'class'
'WbWidget_Content'

"//div[@id='wb_control_contentPane_1h2veqeu2nfl57dpplf']"

def is_doc_uploaded(driver, doc_name):

    web_elem = driver.find_element("xpath", f"//span[contains(text(), '{doc_name}')]")
    # //div[contains(text(), '{doc_name}')]
    # //span[contains(text(), '4105_ОНЛАЙН_ТРЕЙД_ООО_БЫТОВОЕ_ОБОРУДОВАНИЕ.docx')]
    # //div[contains(text(), '4105_ОНЛАЙН_ТРЕЙД_ООО_БЫТОВОЕ_ОБОРУДОВАНИЕ.docx')]
    print(f'{doc_name} - ЗАГРУЖЕН')
    return web_elem
