let student = {
  name: 'John',
  age: 30,
  isAdmin: false,
  courses: ['html', 'css', 'js'],
  wife: null
};


let py_json_output_str = `{
  "12345":{"contract_number": "12345",
  "product_name": "Монитор 25",
  "product_category": "Мониторы",
  "company_name": "ООО ЛАЙТКОМ"},
  "columns_info":{"contract_number": "Номер Контракта",
  "product_name": "Название товара",
  "company_name": "Название компании",
  "product_category": "Категория"
}
}`

function my_btn_funcs () {
  let json = JSON.stringify(student, null, 2);
  alert("JSON-строка в объект:" + JSON.parse(py_json_output_str));
};

function my_btn_funcs_2 () {
  let json = JSON.stringify(py_json_output_str, null, 2);
  alert(py_json_output_str);
};

// ОБЪЕКТ/МАССИВ В JSON == СТРОКА
// JSON.stringify()
// преобразование строки в JSON затем в объект javascript
// JSON.parse()

// ВЫВОДИМ ОБЪЕКТ(словарь) в ТАБЛИЦУ - HTML
// парсим строку в объект
let object_from_py_dict = JSON.parse(py_json_output_str);

function create_table_with_3_keys (object_dict) {
  // создаем таблицу помещаем в html-body
  let html_body = document.querySelector('body');
  let table = document.createElement("table");
  table.setAttribute('class', 'my_table');
  html_body.appendChild(table);
  let tr_head = document.createElement("tr");
  table.appendChild(tr_head);
  let td_head_1 = document.createElement("th");
  let td_head_2 = document.createElement("th");
  let td_head_3 = document.createElement("th");
  tr_head.appendChild(td_head_1);
  tr_head.appendChild(td_head_2);
  tr_head.appendChild(td_head_3);
  td_head_1.textContent = 'Номер контракта';
  td_head_2.textContent = 'Наименовение Товара';
  td_head_3.textContent = 'Категория';

  for (contract in object_dict) {
    let tr_for_data = document.createElement("tr");
    tr_for_data.setAttribute('id', contract);
    table.appendChild(tr_for_data);
    for (contr_data in object_dict[contract]) {
      let td_for_data = document.createElement("td");
      tr_for_data.appendChild(td_for_data);
      td_for_data.textContent = object_dict[contract][contr_data];
      }
    }
  }

function create_table_with_columns_info (json_dict) {
  // выделяем информацию о таблице
  if ("columns_info" in json_dict) {
    let culumns_name_list = [];
    let html_body = document.querySelector('body');
    let table = document.createElement("table");
    table.setAttribute('class', 'smart_table my_table');
    html_body.appendChild(table);
    let tr_head = document.createElement("tr");
    table.appendChild(tr_head);
    // Создаем шапку и список колонок - порядок вставки данных
    for (culumns_name in json_dict["columns_info"]) {
      culumns_name_list.push(culumns_name);
      let td_head_1 = document.createElement("th")
      tr_head.appendChild(td_head_1);
      td_head_1.textContent = json_dict["columns_info"][culumns_name];
    }
    // Удаляем инфу о таблицце из объекта
    delete json_dict['columns_info']
    // alert(Object.keys(json_dict))
    // заполняем содержимое таблицы на основе шапки
    for (contract in json_dict) {
      let tr_for_data = document.createElement("tr");
      tr_for_data.setAttribute('id', contract);
      table.appendChild(tr_for_data);
       for (column_name in culumns_name_list){
        for (contr_data in json_dict[contract]) {
          // Если у ячейки название колонки совпадает с указанными в шапке - вставляем
          if (culumns_name_list[column_name] === contr_data){
            let td_for_data = document.createElement("td");
            tr_for_data.appendChild(td_for_data);
            td_for_data.textContent = json_dict[contract][contr_data];
            // alert(`Сравнение: ${culumns_name_list[column_name]} - ${contr_data} ${json_dict[contract][contr_data]}`)
          }
        }
        // если не удалось определить столбец, то создаем новую колонку и в шапку новую строку + алерт
        // if !(json_dict[contract] in culumns_name_list)
        }
      }
  }
  else {
    alert('НЕТ ИНФОРМАЦИИ ПО ТАБЛИЦЕ!')
  }
  }
