import time
def setup_site_filter(DRIVER):
    # Настройка параметров поиска
        # Клики по "квадратикам"
        # завершенные контракты + Настройка на количество страниц 50 шт.

    param_list = [
        '//*[@id="contractStageListTag"]/div/div[2]/div[1]/label',
        '//*[@id="contractStageListTag"]/div/div[2]/div[3]/label',
        '//*[@id="contractStageListTag"]/div/div[2]/div[4]/label',
        '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/span',
        '//*[@id="_50"]'
        ]

    [DRIVER.find_element_by_xpath(el).click() for el in param_list]

        # Выбор Города
    citi_chose = '//*[@id="customerPlaceAnchor"]'
    DRIVER.find_element_by_xpath(citi_chose).click()
    print('Два *')
    citi_input = '//*[@id="goodssearch"]'
    DRIVER.find_element_by_xpath(citi_input).send_keys('Санкт-Петербург')
    aply_btn = '//*[@id="btn-floating"]/button'
    print('вставили спб *')
    time.sleep(1) # Нужно подождать пока найдет СПБ
    spb_cell = '//*[@id="mCSB_2_container"]/ul/li[1]/span'
    DRIVER.find_element_by_xpath(spb_cell).click()
    print('кликнули спб *')
    aply_btn = '//*[@id="modal-okdp-okved"]/div/div[4]/div/div/button[2]'
    DRIVER.find_element_by_xpath(aply_btn).click()
    print('Применили')
