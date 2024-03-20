import time

def find_document_from_main(driver, number_element):
    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops'
    driver.get(main_page)

    tag = 'input'
    atribute = 'type'
    atr_val = 'text'
    find_element =  driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    time.sleep(0.5)
    find_element.send_keys(number_element)

    tag = 'div'
    atribute = 'class'
    atr_val_btn = 'WbForm_ButtonIcon buttonSearch searchButtonCtl'
    find_element_btn = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_btn}']")
    find_element_btn.click() # поиск в поисковике сайта

    if number_element in driver.title:
        print(driver.title)
