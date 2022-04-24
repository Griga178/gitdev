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
]

// СОЗДАНИЕ ЭЛЕМЕНТОВ
let body_tag = document.querySelector("body");
// Главный DIV для результатов пагинации
let pagDiv = document.createElement("div");
pagDiv.setAttribute("class", "pagDiv");
body_tag.appendChild(pagDiv)
// Заголовок
let pagH1 = document.createElement("h2");
pagH1.textContent = "Товары на странице"
pagDiv.appendChild(pagH1);
// Блок для отрисовки результатов
let result = document.createElement("div");
result.setAttribute("class", "result");
pagDiv.appendChild(result)
// Линия КНОПКИ
let bl2 = document.createElement("div");
bl2.setAttribute("class", "bl2");
pagDiv.appendChild(bl2)
// ВВОД КОЛИЧЕСТВА ОТОБРАЖАЕМЫХ СТРОК
let quantityforselection = 7;
// ВЫВОД СТРОК
function paintResult(arr) {
  for (item = 0, r = ""; item < arr.length; item++) {
    r += `<li class="result-item">${arr[item]}</li>`
  }
  return "<ul>" + r + "</ul>"
}

let ul_block = paintResult(goods)

// Считает нужное количество кнопок пагинации:
function numberofbuttons(arr, num) {
  return Math.ceil(arr.length / num)
}
// РИСУЕМ КНОПКИ
function paintPaginationButton(count) {
  for (i = 1, r = ""; i <= count; i++) {
    r += `<button class="pb">${i}</button>`
  }
  return r
}
let btn_number = numberofbuttons(goods, quantityforselection)
let btn_string = paintPaginationButton(btn_number)
bl2.innerHTML = btn_string

// Первичная отрисовка результата
result.innerHTML = paintResult(goods.slice(0, quantityforselection))

// НАЖАТИЯ НА КНОПИК
document.addEventListener('click', function(event) {
  if ([...event.target.classList].includes("pb")) {
    var y = event.target.textContent;
    var start = quantityforselection * (y - 1);
    var end = quantityforselection * y;
    result.innerHTML = paintResult(goods.slice(start, end));
  } else {
    console.log(event.target)
  }
});