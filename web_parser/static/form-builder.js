
// Создание блока target_point рекурсивно
function createTargetPointBlock(level = 0) {
  const wrapper = document.createElement('div');
  wrapper.className = 'nested';

  wrapper.innerHTML = `
    <label>search_index <input type="number" name="search_index" value="0" /></label>
    <label>recursive
      <select name="recursive">
        <option value="true">True</option><option value="false" selected>False</option>
      </select>
    </label>
    <label>expected_amount (null если нет) <input type="text" name="expected_amount" value="" /></label>
    <label>Название тега <input type="text" name="tag_name" value="" /></label>
    <label>Название аттрибута<input type="text" name="attr_name" value="" /></label>
    <label>Значение аттрибута<input type="text" name="attr_value" value="" /></label>
    <label>target_point
      <select name="target_point_select">
        <option value="true">True</option>
        <option value="false" selected>Нет (null)</option>
        <option value="object">Объект (рекурсия)</option>
      </select>
    </label>
  `;

  const nestedContainer = document.createElement('div');
  nestedContainer.style.marginLeft = '15px';
  wrapper.appendChild(nestedContainer);

  const targetPointSelect = wrapper.querySelector('select[name="target_point_select"]');
  targetPointSelect.addEventListener('change', () => {
    if (targetPointSelect.value === 'object') {
      nestedContainer.innerHTML = '';
      nestedContainer.appendChild(createTargetPointBlock(level + 1));
    } else {
      nestedContainer.innerHTML = '';
    }
  });

  return wrapper;
}

function buildForm() {
  const form = document.getElementById('settingsForm');
  form.innerHTML = `
    <label>name <input type="text" name="name" value="price"/></label>
    <label>type
      <select name="type">
        <option>float</option><option>int</option><option>str</option><option>bool</option>
      </select>
    </label>
    <label>is_expected
      <select name="is_expected">
        <option value="true">True</option><option value="false" selected>False</option>
      </select>
    </label>
    <fieldset style="border:1px solid #ccc; padding:10px; margin-top:10px;">
      <legend>rules</legend>
    </fieldset>
  `;

  const fieldset = form.querySelector('fieldset');
  fieldset.appendChild(createTargetPointBlock());
}

function parseTargetPointDiv(div) {
  const obj = {};
  obj.search_index = Number(div.querySelector('input[name="search_index"]').value);
  obj.recursive = div.querySelector('select[name="recursive"]').value === 'true';
  const expVal = div.querySelector('input[name="expected_amount"]').value.trim();
  obj.expected_amount = expVal === '' || expVal.toLowerCase() === 'null' ? null : Number(expVal);
  obj.tag_name = div.querySelector('input[name="tag_name"]').value || null;
  const attrName = div.querySelector('input[name="attr_name"]').value.trim();
  obj.attr_name = attrName ? attrName : null;
  const attrValue = div.querySelector('input[name="attr_value"]').value.trim();
  obj.attr_value = attrValue ? attrValue : null;

  const targetSelect = div.querySelector('select[name="target_point_select"]').value;
  if (targetSelect === 'true') obj.target_point = true;
  else if (targetSelect === 'false') obj.target_point = null;
  else if (targetSelect === 'object') {
    const nestedDiv = div.querySelector('div.nested');
    obj.target_point = parseTargetPointDiv(nestedDiv.firstElementChild);
  } else {
    obj.target_point = null;
  }

  return obj;
}

function buildDictFromForm() {
  const form = document.getElementById('settingsForm');
  const dict = {};
  dict.name = form.querySelector('input[name="name"]').value;
  dict.type = form.querySelector('select[name="type"]').value;
  dict.is_expected = form.querySelector('select[name="is_expected"]').value === 'true';

  const rulesFieldset = form.querySelector('fieldset');
  dict.rules = parseTargetPointDiv(rulesFieldset.querySelector('div.nested'));

  return dict;
};
