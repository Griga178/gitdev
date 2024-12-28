function parse_one_link(net_link_id) {
  let answer_div = document.createElement("div")
  answer_div.innerHTML = "Думаем..."
  $.ajax({
    url: `/parse_one_links/${net_link_id}`,
    type: 'GET',
    beforeSend: function() {
      parse_result_block.appendChild(answer_div)
    },
    success: function(response) {
      draw_parse_result(response, answer_div)
    }
  })
}
// вставка ссылок через форму - POST
function parse_link() {
  let answer_div = document.createElement("div")
  answer_div.innerHTML = "Думаем..."
  $.ajax({
    url: "/parser_link_check",
    data: $('form').serialize(),
    type: 'POST',
    beforeSend: function() {
      parse_result_block.appendChild(answer_div)
      link_input.value = ''
    },
    success: function(response) {
      draw_parse_result(response, answer_div)
    },
    error: function(error) {
      console.log(error);
    }
  });
}

let parsed_links_counter = 0;
function draw_parse_result(js_respone, html_tag) {
  let send_to_db = js_respone
  let parse_info = $.parseJSON(js_respone);
  parsed_links_counter += 1;
  html_tag.innerHTML = `
    ${parsed_links_counter}
    <a href = "${parse_info.http_link}" target = "_blank">${parse_info.main_page}</a>
    <b> ${parse_info.current_price} руб.</b>
    <p>${parse_info.current_name}</p>
    <p>${parse_info.current_date}</p>`;
    // <div id = 'send_to_db_${parse_info.link_id}'> <button onclick = 'send_parse_result_to_db(${send_to_db})'>Сохранить</button></div>
    if (parse_info.new_parse) {
      let save_div = document.createElement("div")
      save_div.setAttribute("id", `"send_to_db_${parse_info.link_id}"`)
      let parse_btn = document.createElement("button")
      parse_btn.setAttribute("onclick", `send_parse_result_to_db('${send_to_db}')`)
      parse_btn.innerHTML = "Сохранить"
      save_div.appendChild(parse_btn)
      html_tag.appendChild(save_div)
    }
}
function show_few_links(shop_id) {
  $.ajax({
    url: `show_few_links/${shop_id}`,
    type: 'GET',
    beforeSend: function() {
      btn_show_few_links.innerHTML
      btn_show_few_links.innerHTML = 'Загружаем ... (это вы не должны увспеть увидеть)'
    },
    success: function(response) {
      btn_show_few_links.innerHTML = ''

      let json_dict = $.parseJSON(response);
      for (net_link_id in json_dict) {

        let links_p = document.createElement("a")
        links_p.setAttribute("href", `${json_dict[net_link_id]}`)
        links_p.setAttribute("target", `_blank`)
        links_p.innerHTML = `${json_dict[net_link_id].slice(0, 30)} ...`
        btn_show_few_links.appendChild(links_p)
        let parse_btn = document.createElement("p")
        parse_btn.textContent = "Отпарсить"
        parse_btn.setAttribute("onclick", `parse_one_link('${net_link_id}')`)
        btn_show_few_links.appendChild(parse_btn)
      }
    },
  })
}
