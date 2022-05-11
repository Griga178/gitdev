from engine_data_base import check_links_in_db, add_new_link_to_db, check_sett_to_parse

# С САЙТА ПРИШЛА 1 ССЫЛКА ДЛЯ ПАРСИНГА
# проверка на безопасность - пропускаем ... define_links from funcs_parser

# ищем ссылку в БД
link = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'

a = check_links_in_db(link)
if a:
    print(a)
else:
    add_new_link_to_db(a)

# ИЩЕМ ТЕГИ ДЛЯ ПАРСИНГА
find_tags_sett = check_sett_to_parse(main_page_id)
