// funcs.js

/* ===================== ПОДГОТОВКА ===================== */
const categories = rawData.filter(d => !d.category);
const entities   = rawData.filter(d =>  d.category);
const byId       = Object.fromEntries(entities.map(e => [e.id, e]));
const sortedEntities = [...entities].sort((a,b) => (a.year||0) - (b.year||0));

const activeCategories = new Set(categories.map(c => c.id));

let hoveredId = null;
let lockedId  = null;
let lastActiveId = null;

let cachedRelated    = null;
let cachedRelatedFor = null;

/* ===================== DOM ===================== */
const filtersEl    = document.getElementById('filters');
const categoriesEl = document.getElementById('filter-categories');
const entitiesEl   = document.getElementById('entities');
const graphEl      = document.getElementById('graph');

/* ===================== ФИЛЬТРЫ ===================== */
categories.forEach(cat => {
  const btn = document.createElement('button');
  btn.className = 'filter-btn active';
  btn.dataset.cat = cat.id;
  btn.textContent = cat.title;
  btn.title = cat.title;
  btn.addEventListener('click', () => toggleCategory(cat.id));
  categoriesEl.appendChild(btn);
});

document.getElementById('enable-all').addEventListener('click', () => {
  categories.forEach(c => activeCategories.add(c.id));
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.add('active'));
  refresh();
});

document.getElementById('disable-all').addEventListener('click', () => {
  activeCategories.clear();
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  refresh();
});

/* ===================== СУЩНОСТИ ===================== */
sortedEntities.forEach(e => {
  const div = document.createElement('div');
  div.className = 'entity';
  div.dataset.id = e.id;
  const catTitle = (categories.find(c => c.id === e.category) || {}).title || '';
  div.innerHTML = `
    <div class="entity-id">${e.id}</div>
    <div class="entity-title">${e.title}</div>
    <div class="entity-year">${e.year || ''}</div>
    <div class="entity-cat">${catTitle}</div>
    <div class="tooltip">${e.description || 'Нет описания'}</div>
  `;

  div.addEventListener('mouseenter', () => { hoveredId = e.id; onHighlightChange(); });
  div.addEventListener('mouseleave', () => { hoveredId = null;  onHighlightChange(); });
  div.addEventListener('click', (ev) => {
    ev.stopPropagation();
    lockedId = (lockedId === e.id) ? null : e.id;
    onHighlightChange();
  });
  div.addEventListener('mousemove', (ev) => {
    const tip = div.querySelector('.tooltip');
    tip.style.left = (ev.clientX + 16) + 'px';
    tip.style.top  = (ev.clientY + 16) + 'px';
  });

  entitiesEl.appendChild(div);
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.entity')) {
    lockedId = null;
    onHighlightChange();
  }
});

/* ===================== ВИДИМОСТЬ ===================== */
function getActiveId() { return lockedId || hoveredId; }

function getRelatedIds(activeId) {
  if (!activeId) return null;
  if (cachedRelatedFor === activeId && cachedRelated) return cachedRelated;

  const related = new Set([activeId]);
  const stack = [activeId];

  while (stack.length) {
    const id = stack.pop();
    const e = byId[id];
    if (!e) continue;
    (e.parent || []).forEach(pid => {
      if (!related.has(pid)) { related.add(pid); stack.push(pid); }
    });
  }
  stack.length = 0; stack.push(activeId);
  while (stack.length) {
    const id = stack.pop();
    const e = byId[id];
    if (!e) continue;
    (e.child || []).forEach(cid => {
      if (!related.has(cid)) { related.add(cid); stack.push(cid); }
    });
  }

  cachedRelated    = related;
  cachedRelatedFor = activeId;
  return related;
}

function isVisible(entity) {
  if (!entity || !entity.category) return false;
  if (activeCategories.has(entity.category)) return true;

  const activeId = getActiveId();
  if (activeId) {
    const related = getRelatedIds(activeId);
    return related && related.has(entity.id);
  }
  return false;
}

function toggleCategory(catId) {
  if (activeCategories.has(catId)) activeCategories.delete(catId);
  else                              activeCategories.add(catId);

  document.querySelector(`.filter-btn[data-cat="${catId}"]`).classList.toggle('active');
  refresh();
}

function updateVisibility() {
  sortedEntities.forEach(e => {
    const el = document.querySelector(`.entity[data-id="${e.id}"]`);
    const visible = isVisible(e);
    const filterVisible = activeCategories.has(e.category);

    el.classList.toggle('hidden',   !visible);
    el.classList.toggle('revealed', visible && !filterVisible);
  });
}

/* ===================== СВЯЗИ ===================== */
function getNearestVisibleDescendants(id) {
  const result = [];
  const e = byId[id];
  if (!e) return result;
  (e.child || []).forEach(cid => {
    const child = byId[cid];
    if (!child) return;
    if (isVisible(child)) result.push(cid);
    else result.push(...getNearestVisibleDescendants(cid));
  });
  return result;
}

/* ===================== ВЫРАВНИВАНИЕ ПОД КАТЕГОРИИ ===================== */
function applyOffsets() {
  const containerRect = entitiesEl.getBoundingClientRect();

  sortedEntities.forEach(e => {
    const el  = document.querySelector(`.entity[data-id="${e.id}"]`);
    const btn = document.querySelector(`.filter-btn[data-cat="${e.category}"]`);
    if (!el || !btn) return;

    const btnRect = btn.getBoundingClientRect();
    const leftOffset = Math.max(0, btnRect.left - containerRect.left);

    el.style.marginLeft = leftOffset + 'px';
    el.style.width      = btnRect.width + 'px';
  });
}

/* ===================== ОТРИСОВКА ЛИНИЙ (КРИВЫЕ) ===================== */
function redraw() {
  const svg = document.getElementById('lines');
  svg.innerHTML = '';
  const graphRect = graphEl.getBoundingClientRect();
  let lineIdx = 0;

  sortedEntities.forEach(e => {
    if (!isVisible(e)) return;
    const fromEl = document.querySelector(`.entity[data-id="${e.id}"]`);
    if (!fromEl) return;
    const fromRect = fromEl.getBoundingClientRect();

    const descendants = getNearestVisibleDescendants(e.id);

    descendants.forEach((did) => {
      const toEl = document.querySelector(`.entity[data-id="${did}"]`);
      if (!toEl) return;
      const toRect = toEl.getBoundingClientRect();

      const x1 = fromRect.right - graphRect.left;
      const y1 = fromRect.top   - graphRect.top + fromRect.height / 2;
      const x2 = toRect.right   - graphRect.left;
      const y2 = toRect.top     - graphRect.top + toRect.height / 2;

      // Кривая с ограничением по ширине графа — не выходит за экран
      const maxX = Math.max(x1, x2);
      const available = Math.max(0, graphRect.width - maxX - 16);
      const baseW = 30 + (lineIdx % 4) * 12;
      const w = Math.min(baseW, available);
      lineIdx++;

      const d = `M ${x1} ${y1} C ${x1 + w} ${y1}, ${x2 + w} ${y2}, ${x2} ${y2}`;

      const path = document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d', d);
      path.setAttribute('stroke', '#4a90e2');
      path.setAttribute('stroke-width', '2');
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke-linejoin', 'round');
      path.setAttribute('opacity', '0.7');
      path.dataset.from = e.id;
      path.dataset.to   = did;
      svg.appendChild(path);

      [[x1,y1],[x2,y2]].forEach(([cx,cy]) => {
        const c = document.createElementNS('http://www.w3.org/2000/svg','circle');
        c.setAttribute('cx', cx);
        c.setAttribute('cy', cy);
        c.setAttribute('r', 3);
        c.setAttribute('fill', '#4a90e2');
        c.dataset.from = e.id;
        c.dataset.to   = did;
        svg.appendChild(c);
      });
    });
  });

  applyHighlight();
}

/* ===================== ПОДСВЕТКА ===================== */
function applyHighlight() {
  const activeId = getActiveId();

  document.querySelectorAll('.entity').forEach(el => {
    el.classList.toggle('highlighted', el.dataset.id === activeId);
  });

  document.querySelectorAll('#lines path').forEach(p => {
    p.classList.toggle('highlighted', p.dataset.from === activeId);
  });
  document.querySelectorAll('#lines circle').forEach(c => {
    c.classList.toggle('highlighted', c.dataset.from === activeId);
  });
}

/* ===================== ОБНОВЛЕНИЕ ===================== */
let refreshScheduled = false;

function refresh() {
  if (refreshScheduled) return;
  refreshScheduled = true;
  requestAnimationFrame(() => {
    updateVisibility();
    applyOffsets();
    redraw();
    refreshScheduled = false;
  });
}

function onHighlightChange() {
  const activeId = getActiveId();
  if (activeId === lastActiveId) {
    applyHighlight();
    return;
  }
  lastActiveId = activeId;
  cachedRelated    = null;
  cachedRelatedFor = null;
  refresh();
}

/* ===================== ИНИЦИАЛИЗАЦИЯ ===================== */
function init() {
  updateVisibility();
  applyOffsets();
  redraw();
}

window.addEventListener('load',   () => requestAnimationFrame(init));
window.addEventListener('resize', () => {
  requestAnimationFrame(() => {
    applyOffsets();
    redraw();
  });
});
