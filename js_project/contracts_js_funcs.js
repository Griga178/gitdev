let contracts_massiv = [
 ["№", "№ Контракта", "Товар", "Категория", "ККН"],
 ["1", "37812345", 'Моноблок 23"', "Моноблоки", "Моноблок тип 1"],
 ["2", "37812346", 'Моноблок 23"', "Моноблоки", "Моноблок тип 1"],
 ["3", "37812347", 'Моноблок 27"', "Моноблоки", "Моноблок тип 2"],
 ["4", "37812348", 'Моноблок 27"', "Моноблоки", "Моноблок тип 2"],
 ["5", "37812349", 'Моноблок 31"', "Моноблоки", "Моноблок тип 3"],
 ]
 // СОЗДАЕМ ФУНКЦИЮ С 1 АРГУМЕНТОМ
 let tablicza = function (arr) {
   // создание строк заголовка ("<th>№</th><th>№ Контракта</th>")
   // let head = arr[0].map(i=>`<th>${i}</th>`).join("");
   // добавление строк в заголовок
   // let thead = `<thead><tr>${head}</tr></thead>`;
   let body = arr.slice(1).map(i=>`<tr>${i.map(i=>`<th>${i}</th>`).join("")}</tr>`).join("");
   // let tbody = `<tbody>${body}</tbody>`;
   // let table = `<table>${thead}${tbody}</table>`;
   let table = `${body}</table>`;
   return table;
 }

function displayMessage () {
   var html = document.querySelector('html');

   var panel = document.createElement('div');
   panel.setAttribute('class', 'msgBox');
   html.appendChild(panel);

   var msg = document.createElement('p');
   msg.textContent = 'This is a message box';
   panel.appendChild(msg);

   var closeBtn = document.createElement('button');
   closeBtn.textContent = 'x';
   panel.appendChild(closeBtn);

   closeBtn.onclick = function() {
     panel.parentNode.removeChild(panel);
   }}


function launch_btn_upload_table () {
  // let my_btn = document.getElementById('load_table_btn')
  let my_btn = load_table_btn
  my_btn.onclick = function() {
      load_data_to_table();
      }
    }

function load_data_to_table (){
  // НАХОДИМ ТЕКУЩУЮ ТАБЛИЦУ
  let current_table = document.getElementById('contracts_tbl');
  // СОЗДАЕМ РЯД (СТРОКУ) И ДОБАВЯЕМ В ТАБЛИЦУ
  // let table_row = document.createElement('tr');
  // current_table.appendChild(table_row);
  function from_list_to_table (data_list) {
    // создать tr для каждого элемента
    data_list.map(row => {
      new_row = document.createElement('tr');
      new_row.setAttribute('id', row[1]);
      current_table.appendChild(new_row);
      row.map(data => {
        new_data = document.createElement('td');
        new_row.appendChild(new_data);
        new_data.textContent = data;
      })
    })
  }

  from_list_to_table(contracts_massiv.slice(1))
  $('#load_table_btn').hide()
  }

function my_funcs() {
  alert("вызываем функцию добавления в бд")
}
