let py_json_output_str = `{
  "12345":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "12346":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "12347":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "12348":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "12349":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"12341":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123429":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"1234269":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"12342679":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"12342349":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"12343439":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123439":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123449":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123459":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123469":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"123479":{"contract_number": "12345",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "columns_info":{"contract_number": "Номер Контракта",  "product_name": "Название товара",
  "company_name": "Название компании",  "product_category": "Категория"}
}`


function draw_table_base(json_string) {
  // Преобразование в объект (.py словарь)
  let json_dict = JSON.parse(py_json_output_str);

  if ("columns_info" in json_dict) {
    // СОЗДАЕМ НЕСМЕНЯЕМЫЕ ТЕГИ ТАБЛИЦЫ

    let table = document.createElement("table");
    table.setAttribute('class', 'smart_table my_table');
    json_table_div.appendChild(table);
    let table_head = document.createElement("thead");
    table.appendChild(table_head);
    let tr_head = document.createElement("tr");
    table_head.appendChild(tr_head);
    t_body = document.createElement('tbody');
    t_body.setAttribute('id', 'current_table');
    table.appendChild(t_body);

    // Создаем шапку и список колонок - формируем порядок вставки данных
    // ЗАГОЛОВКИ
    let culumns_name_list = [];
    for (culumns_name in json_dict["columns_info"]) {
      culumns_name_list.push(culumns_name);
      let td_head_1 = document.createElement("th")
      tr_head.appendChild(td_head_1);
      td_head_1.textContent = json_dict["columns_info"][culumns_name];
    }

    // формируем настройку количества выводимых строк
    let label_text = document.createElement('label')
    label_text.setAttribute('for', 'select_row_number');
    label_text.textContent = "Сколько страниц: ";
    let select_tag = document.createElement('select');
    json_table_div.appendChild(label_text);
    json_table_div.appendChild(select_tag);
    let page_set_ar = [5, 10, 15, 30, 50]
    for (num in page_set_ar) {
      let optinon = document.createElement('option');
      optinon.setAttribute('value', `${page_set_ar[num]}`);
      optinon.textContent = page_set_ar[num];
      select_tag.appendChild(optinon);
    }
    // ЗАКОНЧИЛИ С ШАПКОЙ
    // Удаляем инфу о таблицце из объекта
    delete json_dict['columns_info']
    alert(Object.keys(json_dict).length + '<  -- ' + '\n -- >' + culumns_name_list)
    return [json_dict, culumns_name_list]
  } else {alert('НЕТ ИНФОРМАЦИИ ПО ТАБЛИЦЕ!')}
}

let json_dict_data = draw_table_base(py_json_output_str)
let json_dict_data = draw_table_base(py_json_output_str)

let list_columns_name = draw_table_base(py_json_output_str)

function draw_table (json_dict_data, columns_name) {
    // заполняем содержимое таблицы на основе шапки
    // создаем список всех ключей (для вывода постранично)
    let list_of_rows = ''
    for (contract in list_of_keys.slice(0, 5)) {
      // СОЗДАЕМ СТРОКУ
      // let current_row = `<tr id = "${contract}">`
      let current_row = `<tr id = "${list_of_keys[contract]}">`
      for (column_name in culumns_name_list) {
        for (contr_data in json_dict[list_of_keys[contract]]) {
          // Если у ячейки название колонки совпадает с указанными в шапке - вставляем
          if (culumns_name_list[column_name] === contr_data) {
            // current_row += `<td> ${json_dict[contract][contr_data]}</td>`
            current_row += `<td> ${json_dict[list_of_keys[contract]][contr_data]}</td>`
          }
        }
        // если не удалось определить столбец, то создаем новую колонку и в шапку новую строку + алерт
        // if !(json_dict[contract] in culumns_name_list)
      }
      current_row += '</tr>'
      list_of_rows += current_row
    }
  current_table.innerHTML = list_of_rows
  // return list_of_keys = list_of_keys
  }

// первичная отрисовка таблицы
// draw_table(json_dict_data, list_columns_name)

// ЕСЛИ ЯЧЕЙКА ПУСТА ПИШЕТСЯ "-"
// ЕСЛИ ДОП СВОЙСТВО НЕ УКАЗАНННОЕ В ШАПКЕ АЛЕРТ
