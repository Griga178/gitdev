
function findElements(rule, context) {
  if (!rule) return [];
  const tag = rule.tag_name || '*';
  let elements = [];

  if (rule.attr_name && rule.attr_value) {
    elements = Array.from(context.querySelectorAll(`${tag}[${rule.attr_name}="${rule.attr_value}"]`));
  } else if (rule.attr_name) {
    elements = Array.from(context.querySelectorAll(`${tag}[${rule.attr_name}]`));
  } else {
    elements = Array.from(context.getElementsByTagName(tag));
  }

  if (rule.search_index >= 0)
    elements = elements[rule.search_index] ? [elements[rule.search_index]] : [];
  else if (rule.search_index === -1 && rule.recursive) {
    // оставляем все
  } else if (rule.search_index === -1 && !rule.recursive) {
    elements = elements.length > 0 ? [elements[0]] : [];
  }

  return elements;
}

function recursiveParse(rule, context) {
  if (rule === true) return ['[target_point=true]'];
  if (!rule) return [];

  const els = findElements(rule, context);
  if (els.length === 0) return [];

  let results = [];

  if (rule.target_point === true) {
    results = els.map(el => el.textContent.trim());
  } else if (rule.target_point === null) {
    results = els.map(el => el.outerHTML);
  } else {
    for (const el of els) {
      results.push(...recursiveParse(rule.target_point, el));
    }
  }
  return results;
}

function runParsing(d, doc) {
  const res = recursiveParse(d.rules, doc);
  const block = document.getElementById('parseResult');
  if (res.length === 0) {
    block.textContent = 'Ничего не найдено.';
  } else {
    block.innerHTML = '<ul>' + res.map(i => `<li>${i}</li>`).join('') + '</ul>';
  }
}
