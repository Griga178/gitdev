let py_json_output_str = `{
  "1":{"contract_number": "1",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "2":{"contract_number": "2",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "3":{"contract_number": "3",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "4":{"contract_number": "4",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "5":{"contract_number": "5",  "product_name": "Монитор 25",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"6":{"contract_number": "6",  "product_name": "Монитор 85",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"7":{"contract_number": "7",  "product_name": "Монитор 75",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"8":{"contract_number": "8",  "product_name": "Монитор 75",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"9":{"contract_number": "9",  "product_name": "Монитор 15",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"10":{"contract_number": "10",  "product_name": "Монитор 45",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"11":{"contract_number": "11",  "product_name": "Монитор 35",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"12":{"contract_number": "12",  "product_name": "Монитор 21",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"13":{"contract_number": "13",  "product_name": "Монитор 22",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"14":{"contract_number": "14",  "product_name": "Монитор 23",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"15":{"contract_number": "15",  "product_name": "Монитор 24",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},"16":{"contract_number": "16",  "product_name": "Монитор 26",
  "product_category": "Мониторы",  "company_name": "ООО ЛАЙТКОМ"},
  "columns_info":{"contract_number": "Номер Контракта",  "product_name": "Название товара",
  "company_name": "Название компании",  "product_category": "Категория"}
}`

// Кнопка для показа json строки
let btn_show_json = document.createElement('button')
btn_show_json.textContent = "принимаемая Json строка"
btn_show_json.addEventListener('click', function (){alert(py_json_output_str)})


json_table_div.appendChild(btn_show_json)

// ОБЩИЕ ПЕРЕМЕННЫЕ:
// СЛОВАРЬ ДАННЫХ с данными по названия колонок
let json_dict = JSON.parse(py_json_output_str);
// СПИСОК НАИМЕНОВАНИЙ колонок. Заполняется в draw_table_base
let culumns_name_list = [];
// проверяем на наличие настроек, формируем список
let list_of_keys = []
if ("columns_info" in json_dict) {
  for (culumns_name in json_dict["columns_info"]) {
    culumns_name_list.push(culumns_name);
  }
  // вес ок запускаем функцию отрисовки
  draw_table_base()
}
// если нет названий колонок алерт
else alert('НЕТ ИНФОРМАЦИИ ПО ТАБЛИЦЕ!')

// выбор КОЛИЧЕСТВА ОТОБРАЖАЕМЫХ СТРОК
select_row_number.addEventListener('change', set_amount_rows);
document.addEventListener('click', push_btns);
function push_btns(events) {
  if ([...events.target.classList].includes("pb")) {
    // количество выводимых строк
    let rows_amount = select_row_number.value;
    // номер выбранной страницы
    let y = events.target.textContent;
    let start = rows_amount * (y - 1);
    let end = rows_amount * y;
    draw_table(end, start);
    }
  }

function set_amount_rows(row_amount = 10) {
  let choice = select_row_number.value;
  row_amount = select_row_number.value
  // отрисовка содержимого
  draw_table(row_amount)
  // draw_btn()
}

function draw_btn() {
  // Считает нужное количество кнопок пагинации:
  let rows_amount = select_row_number.value;
  let count = Math.ceil(list_of_keys.length / rows_amount);
  let button_tags = ''
  if (count > 1){
    for (i = 1; i <= count; i++) {
      button_tags += `<button class = "pb" id = "page_num_btn">${i}</button>`
    }
    btns_div.innerHTML = button_tags
  }else btns_div.innerHTML = ''
}

function draw_table_base() {
  // Преобразование в объект (.py словарь)
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
  // *** дополнительно нумерация + в draw_table
  let row_number_head = document.createElement("th")
  tr_head.appendChild(row_number_head);
  row_number_head.textContent = "№"
  // ***
  for (culumns_name in culumns_name_list) {
    let td_head_1 = document.createElement("th")
    tr_head.appendChild(td_head_1);
    td_head_1.textContent = json_dict["columns_info"][culumns_name_list[culumns_name]];
  }
  delete json_dict['columns_info']
  // заполняем список из ключей словаря (номера контрактов)
  for (contr_id in json_dict) {
    list_of_keys.push(contr_id)
  }

  // формируем форму количества выводимых строк
  let label_text = document.createElement('label')
  label_text.setAttribute('for', 'select_row_number');
  label_text.textContent = "Показать по: ";
  let select_tag = document.createElement('select');
  select_tag.setAttribute('id', "select_row_number")
  json_table_div.appendChild(label_text);
  json_table_div.appendChild(select_tag);
  let page_set_ar = [5, 10, 15, 30, 50]
  for (num in page_set_ar) {
    let optinon = document.createElement('option');
    optinon.setAttribute('value', `${page_set_ar[num]}`);
    optinon.textContent = page_set_ar[num];
    select_tag.appendChild(optinon);
  }
  // блок для кнопок
  btns_div = document.createElement('div')
  json_table_div.appendChild(btns_div)
  // ПЕРВИЧНАЯ ОТРИСОВКА ТАБЛИЦЫ
  draw_table(5)
}

function draw_table (step = 5, start = 0) {
    // заполняем содержимое таблицы на основе шапки
    // создаем список всех ключей (для вывода постранично)
    let list_of_rows = ''
    // перебор списка "номеров контрактов"
    let = current_list_slice = list_of_keys.slice(start, step)
    for (contract in current_list_slice) {
      // СОЗДАЕМ СТРОКУ
      // let current_row = `<tr id = "${current_list_slice[contract]}">`
      // + нумерация
      let current_row = `<tr id = "${current_list_slice[contract]}"><td>${list_of_keys.indexOf(current_list_slice[contract]) + 1}</td>`
      // перебор списка "названий колонок"
      for (column_name in culumns_name_list) {
        // перебор списка содержимого контракта
        for (contr_data in json_dict[current_list_slice[contract]]) {
          // Если у ячейки название колонки совпадает с указанными в шапке - вставляем
          if (culumns_name_list[column_name] === contr_data) {
            current_row += `<td> ${json_dict[current_list_slice[contract]][contr_data]}</td>`
          }
        }
        // если не удалось определить столбец, то создаем новую колонку и в шапку новую строку + алерт
        // if !(json_dict[contract] in culumns_name_list)
      }
      current_row += '</tr>'
      list_of_rows += current_row
    }


  // выводим таблицу
  current_table.innerHTML = list_of_rows
  // рисуем кнопки
  draw_btn()
  }


// ЕСЛИ ЯЧЕЙКА ПУСТА ПИШЕТСЯ "-"
// ЕСЛИ ДОП СВОЙСТВО НЕ УКАЗАНННОЕ В ШАПКЕ АЛЕРТ
