
def find_document_from_main(driver, number_element):
    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops'
    driver.get(main_page)

    tag = 'input'
    atribute = 'type'
    atr_val = 'text'
    find_element =  driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    find_element.send_keys(number_element)

    tag = 'div'
    atribute = 'class'
    atr_val_btn = 'WbForm_ButtonIcon buttonSearch searchButtonCtl'
    driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val_btn}']").click() # поиск в поисковике сайта

    if number_element in driver.title:
        print(driver.title)
