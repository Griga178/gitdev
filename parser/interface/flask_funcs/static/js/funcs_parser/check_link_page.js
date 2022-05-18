let parsed_links_counter = 0;


function draw_shops_list() {
  $.ajax({
    url: "/print_links_base",
    type: 'GET',
    beforeSend: function() {
      let before_message = document.createElement('h3')
      before_message.setAttribute("id", "temp_message")
      before_message.innerHTML = 'Загрузка списка ...'
      row_list.appendChild(before_message);
    },
    success: function(json_dict) {
      // alert(json_dict)
      $('#temp_message').hide()
      let java_dict = jQuery.parseJSON(json_dict);
      for (variable in java_dict) {
        let row_for_data = document.createElement("section");
        row_for_data.setAttribute("onclick", `show_settings(${variable})`)

        if (java_dict[variable]['price'] === true) {
          let indicator = document.createElement("div");
          indicator.setAttribute("class", 'shop_price row_indicat')
          row_for_data.appendChild(indicator)
        }
        if (java_dict[variable]['name'] === true) {
          let indicator = document.createElement("div");
          indicator.setAttribute("class", 'shop_name row_indicat')
          row_for_data.appendChild(indicator)
        }
        if (java_dict[variable]['chars'] === true) {
          let indicator = document.createElement("div");
          indicator.setAttribute("class", 'shop_chars row_indicat')
          row_for_data.appendChild(indicator)
        }
        row_for_data.setAttribute("class", 'shop_row')
        let text_content = document.createElement('p');
        text_content.setAttribute('class', 'shop_name_text')
        text_content.innerHTML = `${variable} ${java_dict[variable]['shop_name']}`;

        row_for_data.appendChild(text_content);
        row_list.appendChild(row_for_data);
      }
    }
  });
}

function shop_filter() {
  let filter = search_shop.value.toUpperCase();
  let shop_list = row_list.getElementsByTagName('section')
  for (i = 0; i < shop_list.length; i++) {
    txtValue = shop_list[i].textContent || shop_list[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      shop_list[i].style.display = "";
    } else {
      shop_list[i].style.display = "none";
    }
  }
}

function show_settings(shop_id) {
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'GET',
    beforeSend: function() {
      set_main_page.innerHTML = "Загрузка..."
    },
    success: function(response) {
      block_for_sett_tags.innerHTML = ''
      let json_obj = $.parseJSON(response)
      let tags_types = ["price", "name", "chars"]
      set_main_page.innerHTML = `${json_obj['shop_name']}`

      for (tag_type in tags_types) {

        let div_for_tags = document.createElement('div');
        div_for_tags.setAttribute("class", "div_for_tags");
        div_for_tags.setAttribute("title", "Изменить - Двойной щелчек");
        div_for_tags.setAttribute("id", `${[tags_types[tag_type]]}`);
        block_for_sett_tags.appendChild(div_for_tags)

        let json_string_out = JSON.stringify(json_obj[tags_types[tag_type]])

        if (json_obj[tags_types[tag_type]]['tag_id'] === false) {
          draw_input_tags(json_obj[tags_types[tag_type]])
        } else {
          draw_div_tags(json_string_out)
        }
      }
      use_selenium_message.innerHTML = `Selenium: <b>${json_obj['use_selenium']}</b>`
      btn_show_few_links.innerHTML = `<p onclick = "show_few_links(${shop_id})">Показать пару ссылок <p>`
    }
  })
}

function draw_div_tags(json_string_in) {
  let sett_dict = $.parseJSON(json_string_in)
  let div_for_tags = document.getElementById(sett_dict['tag_type'])
  div_for_tags.setAttribute("ondblclick", `draw_input_tags(${json_string_in})`);
  div_for_tags.setAttribute("onmousedown", "return false");

  div_for_tags.innerHTML =
    `<p>${sett_dict['rus_tag']}:</p>
  &lt;<p class = 'tag_name_sett'>${sett_dict['tag_name']}&nbsp;</p>
  <p class = 'attr_name_sett'>${sett_dict['attr_name']} =&nbsp</p>
  <p class = 'value_name_sett'>"${sett_dict['attr_val']}"</p>&gt&nbsp
  <p onclick = 'del_set_from_sql(${json_string_in})'>Удалить</p>
  `
}

function draw_input_tags(json_string_in) {
  let json_string_out = JSON.stringify(json_string_in)
  let div_tag_for_change = document.getElementById(json_string_in['tag_type'])
  div_tag_for_change.removeAttribute("ondblclick")
  div_tag_for_change.removeAttribute("onmousedown")

  div_tag_for_change.innerHTML =
    `<form id = "${json_string_in['tag_type']}_form" name = "${json_string_in['tag_type']}_form">
  ${json_string_in['rus_tag']}:
  <input type = "text" value = "${json_string_in['tag_name']}" name = "tag">
  <input type = "text" value = "${json_string_in['attr_name']}" name = "attr">
  <input type = "text" value = "${json_string_in['attr_val']}" name = "attr_val">
  <p onclick = 'save_sett_changing_ver2(${json_string_out})'>Сохранить</p> </form>`
}

// ФОРМЫ НАСТРОЕК
// Поиск ЦЕНЫ
// function draw_price_setting_form(json_string_in){
//
// }

let examp_json = `{'tag_type':'price',
'tag_name':'div',
'attr_name':'class',
'attr_val':'attr_value_price',
}`
function save_sett_changing_ver2(json_string_in) {
  let dict_out;
  let changing_form = document.getElementById(`${json_string_in['tag_type']}_form`);
  let in_tag = changing_form.elements.tag.value;
  let in_attr = changing_form.elements.attr.value;
  let in_value = changing_form.elements.attr_val.value;
  dict_out = {
    "shop_id": json_string_in['shop_id'],
    "tag_type": json_string_in['tag_type'],
    "tag_name": in_tag,
    "attr_name": in_attr,
    "attr_val": in_value,
    "tag_status": true,
    "tag_id": false
  };

  if (json_string_in['tag_id'] !== false) {
    dict_out['tag_id'] = json_string_in['tag_id'];
  }
  let json_string_out = JSON.stringify(dict_out);
  post_to_sql(json_string_out);
}

function delete_settings(json_string_in) {
  let json_string_out = JSON.stringify(json_string_in)

}

function del_set_from_sql(str_data) {
  let json_string_out = JSON.stringify(str_data)
  let shure = confirm("Вы уверены?")
  if (shure) {
    $.ajax({
      url: `/del_sett/${json_string_out}`,
      type: 'POST',
      success: function(response) {
        obj_data = $.parseJSON(response)
        draw_input_tags(obj_data)
      }
    })
  }
}

function post_to_sql(str_data) {
  $.ajax({
    url: `/save_sett/${str_data}`,
    type: 'POST',
    success: function(response) {
      draw_div_tags(response)
    }
  })
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

function send_parse_result_to_db(js_parse_result) {
  let parse_result = $.parseJSON(js_parse_result)
  let send_btn = document.getElementById(`"send_to_db_${parse_result.link_id}"`)
  alert(send_btn)
  alert(`send_to_db_${parse_result.link_id}`)
  $.ajax({
    url: 'send_parse_result',
    type: "POST",
    data: parse_result,
    beforeSend: function(){
      // send_btn.innerHTML = "ОТПРАВЛЯЕМ..."
    },
    success: function(response) {
      alert(response)
      // send_btn.innerHTML = response
    }
  })
}
