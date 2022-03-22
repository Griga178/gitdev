
def define_main_page(link):
    '''
    Определение главной страницы из строки
    '''
    if type(link) == str:
        split_list = link.split("/")
        main_page = split_list[2]
        h_protocol = split_list[0]
        if 'http' or 'ftp' in h_protocol:
            return main_page
        else:
            return 'ERROR: не похоже на ссылку'
    else:
        return 'ERROR: ссылка не в формате строки'
