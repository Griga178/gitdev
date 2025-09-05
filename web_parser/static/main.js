
// в html подключаем static/form-builder.js и static/parser.js

buildForm();
// кнопка сформировать словарь - > замена на активацию по изменению формы
document.getElementById('buildDictBtn').addEventListener('click', () => {
  const dict = buildDictFromForm();
  document.getElementById('dictOutput').textContent = JSON.stringify(dict, null, 2);
  if (window.loadedDoc) {
    runParsing(dict, window.loadedDoc);
  }
});

document.getElementById('loadHtmlBtn').addEventListener('click', () => {
  document.getElementById('htmlFileInput').click();
});

// загрузка html-файла
document.getElementById('htmlFileInput').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    const parser = new DOMParser();
    window.loadedDoc = parser.parseFromString(ev.target.result, 'text/html');
    document.getElementById('parseResult').textContent = 'HTML загружен. Нажмите "Сформировать словарь d" для вывода результата парсинга.';
  };
  reader.readAsText(file);
});
