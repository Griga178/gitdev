
def merge_links_tables(max_number, links_set, links_table_data, work_table_data):
    appended_data = []
    new_counter = max_number + 1

    for row in work_table_data:
        if row[3] in links_set:
            pass
        else:
            row[2] = new_counter
            appended_data.append(row)
            new_counter += 1

    print(f'Добавлено: {len(appended_data)} шт. - новых строк/ссылок')
    return appended_data
