// Цвета и стили для каждого типа связи
const EDGE_STYLES = {
  "ЧАСТЬ_ОТ":     { color: "#E74C3C", style: "solid"  },
  "РАСШИРЯЕТ":    { color: "#2ECC71", style: "solid"  },
  "ИСПОЛЬЗУЕТСЯ_В": { color: "#3498DB", style: "dashed" },
  "ПРЕДШЕСТВУЕТ": { color: "#9B59B6", style: "solid"  },
  "СВЯЗАНА_С":    { color: "#95A5A6", style: "dotted" },
  "АЛЬТЕРНАТИВА": { color: "#F39C12", style: "dashed" },
  "РЕАЛИЗУЕТ":    { color: "#1ABC9C", style: "solid"  }
};

// Цвета для узлов по тегам
const TAG_COLORS = {
  "basics":      "#4A90D9",
  "sql":         "#4A90D9",
  "dml":         "#4A90D9",
  "performance": "#E67E22",
  "acid":        "#8E44AD",
  "design":      "#16A085",
  "db":          "#34495E",
  "nosql":       "#7F8C8D"
};

const DEFAULT_NODE_COLOR = "#7F8C8D";

let cy;
let graph;

// Загрузка данных
fetch("graph.json")
  .then(r => r.json())
  .then(data => {
    graph = data;
    renderGraph();
    renderLegend();
  })
  .catch(err => {
    document.body.innerHTML =
      `<pre style="padding:20px;color:#c00">Ошибка загрузки graph.json:\n${err}\n\n` +
      `Запусти локальный сервер: python -m http.server 8000</pre>`;
  });

function renderGraph() {
  const elements = {
    nodes: graph.nodes.map(n => ({
      data: { ...n, color: pickNodeColor(n.tags) }
    })),
    edges: graph.edges.map(e => ({
      data: {
        id: `${e.from}->${e.to}:${e.type}`,
        source: e.from,
        target: e.to,
        type: e.type,
        note: e.note || ""
      }
    }))
  };

  cy = cytoscape({
    container: document.getElementById("cy"),
    elements,
    style: buildStyle(),
    layout: {
      name: "cose",
      animate: true,
      animationDuration: 600,
      nodeRepulsion: 8000,
      idealEdgeLength: 120,
      edgeElasticity: 100,
      gravity: 0.3,
      padding: 40
    },
    wheelSensitivity: 0.2
  });

  cy.on("tap", "node", evt => showInfo(evt.target.data()));
  cy.on("tap", "edge", evt => showEdgeInfo(evt.target.data()));
  cy.on("tap", evt => {
    if (evt.target === cy) clearInfo();
  });
}

function buildStyle() {
  const style = [
    {
      selector: "node",
      style: {
        "label": "data(label)",
        "background-color": "data(color)",
        "color": "#222",
        "font-size": 11,
        "text-valign": "bottom",
        "text-margin-y": 4,
        "text-outline-color": "#fff",
        "text-outline-width": 2,
        "width": 28,
        "height": 28,
        "border-width": 2,
        "border-color": "#fff"
      }
    },
    {
      selector: "node:selected",
      style: {
        "border-color": "#000",
        "border-width": 3
      }
    },
    {
      selector: "edge",
      style: {
        "width": 1.8,
        "curve-style": "bezier",
        "target-arrow-shape": "triangle",
        "arrow-scale": 0.8,
        "opacity": 0.8
      }
    },
    {
      selector: "edge:selected",
      style: { "width": 3, "opacity": 1 }
    }
  ];

  for (const [type, s] of Object.entries(EDGE_STYLES)) {
    style.push({
      selector: `edge[type = "${type}"]`,
      style: {
        "line-color": s.color,
        "target-arrow-color": s.color,
        "line-style": s.style
      }
    });
  }

  return style;
}

function pickNodeColor(tags = []) {
  for (const t of tags) {
    if (TAG_COLORS[t]) return TAG_COLORS[t];
  }
  return DEFAULT_NODE_COLOR;
}

// Легенда с чекбоксами-фильтрами
function renderLegend() {
  const container = document.getElementById("legend-items");
  container.innerHTML = "";

  for (const [type, desc] of Object.entries(graph.edgeTypes)) {
    const s = EDGE_STYLES[type] || { color: "#999", style: "solid" };
    const row = document.createElement("label");
    row.className = "legend-row";
    row.title = desc;
    row.innerHTML = `
      <input type="checkbox" checked data-type="${type}">
      <span class="legend-color" style="background:${s.color}"></span>
      <span>${type}</span>
    `;
    const cb = row.querySelector("input");
    cb.addEventListener("change", () => {
      row.classList.toggle("off", !cb.checked);
      filterEdges();
    });
    container.appendChild(row);
  }
}

function filterEdges() {
  const active = new Set(
    [...document.querySelectorAll("#legend-items input:checked")]
      .map(cb => cb.dataset.type)
  );
  cy.edges().forEach(edge => {
    const t = edge.data("type");
    edge.style("display", active.has(t) ? "element" : "none");
  });
}

// Панель информации
function showInfo(d) {
  document.getElementById("info-title").textContent = d.label;
  document.getElementById("info-desc").textContent = d.description || "—";
  const tagsBox = document.getElementById("info-tags");
  tagsBox.innerHTML = "";
  (d.tags || []).forEach(t => {
    const span = document.createElement("span");
    span.className = "tag";
    span.textContent = t;
    tagsBox.appendChild(span);
  });
}

function showEdgeInfo(d) {
  document.getElementById("info-title").textContent = d.type;
  document.getElementById("info-desc").textContent = d.note || "Связь между темами.";
  document.getElementById("info-tags").innerHTML = "";
}

function clearInfo() {
  document.getElementById("info-title").textContent = "Кликни по узлу";
  document.getElementById("info-desc").textContent = "Здесь появится описание темы.";
  document.getElementById("info-tags").innerHTML = "";
}

// Переключатель подписей
document.getElementById("toggle-labels").addEventListener("change", e => {
  cy.style()
    .selector("node")
    .style("label", e.target.checked ? "data(label)" : "")
    .update();
});
