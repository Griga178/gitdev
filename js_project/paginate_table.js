let goods = [
  'Элемент 1', 'Элемент 2', 'Элемент 3', 'Элемент 4',
  'Элемент 5', 'Элемент 6', 'Элемент 7', 'Элемент 8',
  'Элемент 9', 'Элемент 10', 'Элемент 11', 'Элемент 12',
  'Элемент 13', 'Элемент 14', 'Элемент 15', 'Элемент 16',
  'Элемент 17', 'Элемент 18', 'Элемент 19', 'Элемент 20',
  'Элемент 21', 'Элемент 22', 'Элемент 23', 'Элемент 24',
  'Элемент 25', 'Элемент 26', 'Элемент 27', 'Элемент 28',
  'Элемент 29', 'Элемент 30', 'Элемент 31', 'Элемент 32',
  'Элемент 33', 'Элемент 34', 'Элемент 35', 'Элемент 36',
  'Элемент 37', 'Элемент 38', 'Элемент 39', 'Элемент 40',
  'Элемент 41', 'Элемент 42', 'Элемент 43', 'Элемент 44',
  'Элемент 45', 'Элемент 46', 'Элемент 47', 'Элемент 48',
  'Элемент 49', 'Элемент 50', 'Элемент 51', 'Элемент 52',
]

// СОЗДАНИЕ ЭЛЕМЕНТОВ
let body_tag = document.querySelector("body");

// ВЫВОД СТРОК
function paintResult(arr) {
  for (item = 0, r = ""; item < arr.length; item++) {
    r += `<tr class="result-item"><td>${arr[item]}</td></tr>`
  }
  return "<thead><th>Заголовок таблицы</th></thead>" + r
}

// выбор КОЛИЧЕСТВА ОТОБРАЖАЕМЫХ СТРОК
select_row_number.addEventListener('change', set_amount_rows);

function set_amount_rows(quantityforselection = 10) {
  let choice = select_row_number.value;
  quantityforselection = select_row_number.value
  table_for_data.innerHTML = paintResult(goods.slice(0, quantityforselection));
  // num_page_btns.innerHTML = paintPaginationButton(numberofbuttons(goods, quantityforselection));
  num_page_btns.innerHTML = paintPaginationButton(goods);
}

// РАСЧЕТЫ:
// Считает нужное количество кнопок пагинации:
// function numberofbuttons(arr, nums = select_row_number.value) {
//   return Math.ceil(arr.length / nums)
// }
// РИСУЕМ КНОПКИ
function paintPaginationButton(data_array) {
  let nums = select_row_number.value;
  let count = Math.ceil(data_array.length / nums);
  // alert(count)
  for (i = 1, r = ""; i <= count; i++) {
    r += `<button class="pb">${i}</button>`
  }
  return r
}

// Первичная отрисовка результата
table_for_data.innerHTML = paintResult(goods.slice(0, 10))
// num_page_btns.innerHTML = paintPaginationButton(numberofbuttons(goods, 10))
num_page_btns.innerHTML = paintPaginationButton(goods)

// НАЖАТИЯ НА КНОПКи
document.addEventListener('click', push_btns);

function push_btns(events) {
  if ([...events.target.classList].includes("pb")) {
    let rows_amount = select_row_number.value;
    let y = events.target.textContent;
    let start = rows_amount * (y - 1);
    let end = rows_amount * y;
    table_for_data.innerHTML = paintResult(goods.slice(start, end));

    num_page_btns.innerHTML = paintPaginationButton(goods)
  } else {
    console.log(events.target)
  }
}
