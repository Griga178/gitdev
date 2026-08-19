document.querySelectorAll('.field-cell').forEach(cell => {
  const dict = JSON.parse(cell.getAttribute('data-dict'));
  const keys = Object.keys(dict);
  // Ищем span
  let span = cell.querySelector('span');
  // выпадающее меню - start
  if (keys.length > 2) {
    // создание блоков меню
    const options = document.createElement('div');
    options.classList.add('field-options');

    const arrow = document.createElement('div');
    arrow.classList.add('arrow');
    arrow.textContent = '▾';

    const dropdown = document.createElement('div');
    dropdown.classList.add('dropdown', 'hidden');
    // добавление блоков меню
    options.appendChild(arrow);
    options.appendChild(dropdown);
    cell.appendChild(options);
    // заполнение выпадающего меню
    keys.forEach(key => {
      const option = document.createElement('div');
      option.textContent = key;
      option.dataset.key = key;
      dropdown.appendChild(option);
    });
    // добавляем переключатель "стрелке"
    arrow.addEventListener('click', e => {
      e.stopPropagation();
      dropdown.classList.toggle('hidden');
    });
    // добавляем обработку пункта выпадающего меню
    dropdown.addEventListener('click', e => {
      if (e.target && e.target.dataset.key) {
        e.stopPropagation() // останавливает клик на общий блок
        const selectedKey = e.target.dataset.key;
        cell.setAttribute('data-key', selectedKey);
        span.textContent = selectedKey;
        dropdown.classList.add('hidden');
        // new_func
        updateDictOutput();
      }
    });
  }; // выпадающее меню - end
  // обработка клика по ячейке формы
  cell.addEventListener('click', () => {
    const input = cell.querySelector('.field-input');
    // если в форме есть - input клик активирует его
    // если нет, простое переключение по дефолтным значениям
    if (input) {
        // навешиваем обработчик blur один раз
        if (!input._blurHandler) {
            input._blurHandler = () => {
                const newValue = input.value.trim();
                if (newValue) {
                    span.textContent = newValue;
                    cell.setAttribute('data-key', newValue);

                    let dict = JSON.parse(cell.getAttribute('data-dict') || '{}');
                    dict[newValue] = newValue;
                    cell.setAttribute('data-dict', JSON.stringify(dict));

                    const dropdown = document.querySelector('.dropdown');
                    // Проверяем, нет ли уже такого ключа, чтобы избежать дубликата
                    if (![...dropdown.children].some(child => child.dataset.key === newValue)) {
                        const option = document.createElement('div');
                        option.textContent = newValue;
                        option.dataset.key = newValue;
                        dropdown.appendChild(option);
                    }
                }
                span.style.display = 'inline';
                input.style.display = 'none';
                // new_func
                updateDictOutput();
            };
            input.addEventListener('blur', input._blurHandler);
        }
        // добавим обработчик Enter для закрытия инпута
        if (!input._enterHandler) {
          input._enterHandler = (e) => {
            if (e.key === 'Enter') {
              input.blur(); // триггерим blur, чтобы закрыть и сохранить
              // new_func
              updateDictOutput();
            } else if (e.key === 'Escape') {
              input.value = cell.dataset.key; // вернуть исходное значение
              input.blur(); // закрыть инпут без сохранения изменений
            }
          };
          input.addEventListener('keydown', input._enterHandler);
        }

        span.style.display = 'none';
        input.style.display = 'inline-block';
        input.focus();
    } else {
        // простое переключение по словарю
        const currentKey = cell.getAttribute('data-key');
        const dict = JSON.parse(cell.getAttribute('data-dict') || '{}');
        const keys = Object.keys(dict);
        const currentIndex = keys.indexOf(currentKey);
        const nextIndex = (currentIndex + 1) % keys.length;
        const nextKey = keys[nextIndex];

        cell.setAttribute('data-key', nextKey);
        span.textContent = nextKey;
        // new_func
        updateDictOutput();
    }
  });

});

// Скрытие всех dropdown при клике вне
document.addEventListener('click', () => {
  document.querySelectorAll('.dropdown').forEach(dropdown => {
    dropdown.classList.add('hidden');
  });
});
