let parsed_links_counter = 0;

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
      parsed_links_counter += 1;
      let json = $.parseJSON(response);
      answer_div.innerHTML = `${parsed_links_counter} <a id = "res_${parsed_links_counter}" href = "${json.link}" target = "_blank">${json.main_page}<a><b> ${json.price} руб.</b>
          <button onclick="show_settings(res_${parsed_links_counter})"><i>Показать настройки</i></button>`;
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });

}

function draw_main_page_list() {
  $.ajax({
    url: "/print_links_base",
    type: 'POST',
    beforeSend: function() {
      let before_message = document.createElement('h3')
      before_message.setAttribute("id", "temp_message")
      before_message.innerHTML = 'Загрузка списка ...'
      row_list.appendChild(before_message);
    },
    success: function(json_dict) {
      $('#temp_message').hide()
      let java_dict = jQuery.parseJSON(json_dict);
      for (variable in java_dict) {
        let row_for_data = document.createElement("div");
        row_for_data.setAttribute("onclick", `show_settings_ver2(${variable})`)
        row_for_data.innerHTML = `<p>${variable} ${java_dict[variable]}</p>`;
        row_list.appendChild(row_for_data);
      }
    }
  });
}

function show_settings_ver2(shop_id) {
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'POST',
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
          let json_string = $.parseJSON(json_string_out)
          draw_input_tags(json_string)
        } else {
          draw_div_tags(json_string_out)
        }
      }
    }
  })
}

function draw_div_tags(json_string_in) {
  // let json_string_out = json_string_in
  let sett_dict = $.parseJSON(json_string_in)
  let div_for_tags = document.getElementById(sett_dict['tag_type'])
  div_for_tags.setAttribute("ondblclick", `draw_input_tags(${json_string_in})`);
  div_for_tags.setAttribute("onmousedown", "return false");
  // alert(json_string_in)
  div_for_tags.innerHTML =
  `<p>${sett_dict['rus_tag']}:&nbspid:</p>
  &lt;<p class = 'tag_name_sett'>${sett_dict['tag_name']}&nbsp;</p>
  <p class = 'attr_name_sett'>${sett_dict['attr_name']} =&nbsp</p>
  <p class = 'value_name_sett'>"${sett_dict['attr_val']}"</p>&gt
  <p onclick = 'delete_settings(${json_string_in})'>Удалить</p>`
}

function draw_input_tags(json_string_in) {
  let json_string_out = JSON.stringify(json_string_in)
  let div_tag_for_change = document.getElementById(json_string_in['tag_type'])
  div_tag_for_change.removeAttribute("ondblclick")
  div_tag_for_change.removeAttribute("onmousedown")

  div_tag_for_change.innerHTML =
  `${json_string_in['rus_tag']}:&nbspid:
  <input type = "text" value = "${json_string_in['tag_name']}">
  <input type = "text" value = "${json_string_in['attr_name']}">
  <input type = "text" value = "${json_string_in['attr_val']}">
  <p onclick = 'save_sett_changing_ver2(${json_string_out})'>Сохранить</p>`
}

function save_sett_changing_ver2(json_string_in) {
  let dict_out;
  let div_tag_for_change = document.getElementById(json_string_in['tag_type'])
  let a = div_tag_for_change.children
  // json_string_in меняем в нем tag_name, attr, val на значения из формы
  if (json_string_in['tag_id'] === false) {
    dict_out = {"shop_id": json_string_in['shop_id'], "tag_type": json_string_in['tag_type'], "tag_name": a[0].value, "attr_name": a[1].value, "attr_val": a[2].value, "tag_status": true, "tag_id": false}
  }else {
    dict_out = {"shop_id": json_string_in['shop_id'], "tag_type": json_string_in['tag_type'], "tag_name": a[0].value, "attr_name": a[1].value, "attr_val": a[2].value, "tag_status": true, "tag_id": json_string_in['tag_id']}
  }
  let json_string_out = JSON.stringify(dict_out)
  post_to_sql(json_string_out)
}

function delete_settings(json_string_in) {
  let json_string_out = JSON.stringify(json_string_in)
  let shure = confirm("Вы уверены?")
  if (shure) {
    del_set_from_sql(json_string_out)
  }
}

function del_set_from_sql(str_data) {
  $.ajax({
    url: `/del_sett/${str_data}`,
    type: 'POST',
    success: function(response){
      obj_data = $.parseJSON(response)
      draw_input_tags(obj_data)
    }
  })
}
function post_to_sql(str_data) {
  $.ajax({
    url: `/save_sett/${str_data}`,
    type: 'POST',
    success: function(response){
      draw_div_tags(response)
    }
  })
}
