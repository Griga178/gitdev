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

function draw_settings(shop_id){
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'GET',
    beforeSend: function() {
      set_main_page.innerHTML = "Загрузка..."
    },
    success: function(response) {

      // let json_obj = $.parseJSON(response)
      draw_settings_form(response)

      // set_main_page.innerHTML = `<span id = "${json_obj.shop_id}">${json_obj.shop_name}</span>`
      // alert(json_obj.tag_setting)

      // for (tag_type in json_obj.tag_setting) {



        // let json_string_out = JSON.stringify(json_obj.tag_setting[tag_type])

        // div_for_tags.innerHTML = `<p>${tags_types[tag_type]['rus_tag']}:</p>`
        // if (typeof json_obj.tag_setting[tag_type] === "undefined") {
        //   alert('input')
        //   // draw_input_tags(json_obj.tag_setting[tag_type])
        // } else {
        //   // draw_div_tags(json_string_out, div_for_tags)
        // }

    //   use_selenium_message.innerHTML = `Selenium: <b>${json_obj['use_selenium']}</b>`
    //   btn_show_few_links.innerHTML = `<p onclick = "show_few_links(${shop_id})">Показать пару ссылок <p>`
    }
  })
}

function draw_settings_form(response){
  let json_obj = $.parseJSON(response)

  block_for_sett_tags.innerHTML = ''
  set_main_page.innerHTML = `<span id = "${json_obj.shop_id}">${json_obj.shop_name}</span>`
  // set_main_page.innerHTML = 'Company name'
  let shop_settings_tags = {
    "price": {"rus_tag": "Теги цены"},
    "sold_out": {"rus_tag": 'Теги "Нет в наличии"'},
    "name": {"rus_tag": "Теги названия"},
    "chars": {"rus_tag": "Теги характеристик"}
  }
  let shop_settings_checkboxes = {
    'need_selenium': {"rus_tag": "Есть JavaScript"},
    'headless_mode': {"rus_tag": "Отключить headless_mode"},
    'sett_active': {"rus_tag": "Не парсить магазин"},
  }

  for (tag_type in shop_settings_tags) {
    let form_for_tags = document.createElement('form');
    form_for_tags.setAttribute("class", "form_for_tags");
    form_for_tags.setAttribute("id", `${tag_type}`);
    block_for_sett_tags.appendChild(form_for_tags)

    form_for_tags.innerHTML = `<label>${shop_settings_tags[tag_type]['rus_tag']}:</label>`

    input_rows = draw_input_tag(json_obj.tag_setting[tag_type])
    form_for_tags.appendChild(input_rows)
  }
  for (tag_type in shop_settings_checkboxes) {
    let form_for_tags = document.createElement('form');
    form_for_tags.setAttribute("class", "form_for_checkbox");
    form_for_tags.setAttribute("id", `${tag_type}`);
    block_for_sett_tags.appendChild(form_for_tags)

    form_for_tags.innerHTML = `<p>${shop_settings_checkboxes[tag_type]['rus_tag']}:</p>`

    input_rows = draw_input_checkbox(json_obj.tag_setting[tag_type])
    form_for_tags.appendChild(input_rows)
  }
}
function draw_input_tag(obj_set) {
  let final_row = document.createElement("div")

  let input_tag = document.createElement("input")
  input_tag.setAttribute("name", "tag");
  input_tag.setAttribute("title", "Название тега (прим.: div / span / h1)");
  input_tag.setAttribute("type", "text");
  input_tag.setAttribute("value", `${obj_set?obj_set['tag_name']:''}`);

  let input_attr = document.createElement("input")
  input_attr.setAttribute("name", "attr");
  input_attr.setAttribute("title", "Атрибут внутри тега (прим.: class / id / itemprop)");
  input_attr.setAttribute("type", "text");
  input_attr.setAttribute("value", `${obj_set?obj_set['attr_name']:''}`);

  let input_attr_val = document.createElement("input")
  input_attr_val.setAttribute("name", "attr_val");
  input_attr_val.setAttribute("title", "Значение атрибута (прим.: price / name)");
  input_attr_val.setAttribute("type", "text");
  input_attr_val.setAttribute("value", `${obj_set?obj_set['attr_value']:''}`);
  input_attr_val.setAttribute("onchange", "alert(this.value)");

  let delete_btn = document.createElement("span")
  delete_btn.setAttribute("class", "delete_btn pct_btn");
  delete_btn.setAttribute("title", "Удалить");
  delete_btn.innerHTML = "&#128473;"
  let save_btn = document.createElement("span")
  save_btn.setAttribute("class", "confirm_btn pct_btn");
  save_btn.setAttribute("title", "Сохранить");
  save_btn.innerHTML = "&#10004;"
  let cancel_btn = document.createElement("span")
  cancel_btn.setAttribute("class", "cancel_btn pct_btn");
  cancel_btn.setAttribute("title", "Отмена");
  cancel_btn.innerHTML = "&#10008;"
  // let all_func_btn = document.createElement("span")
  // all_func_btn.setAttribute("class", "all_func_btn pct_btn");
  // all_func_btn.innerHTML = "&#8942;"

  final_row.appendChild(input_tag)
  final_row.appendChild(input_attr)
  final_row.appendChild(input_attr_val)

  final_row.appendChild(delete_btn)
  final_row.appendChild(cancel_btn)
  final_row.appendChild(save_btn)

  // final_row.appendChild(all_func_btn)

  return final_row;
}

function draw_input_checkbox(obj_set) {
  let final_row = document.createElement("div")

  let input_checkbox = document.createElement("input")
  input_checkbox.setAttribute("id", "checkbox");
  input_checkbox.setAttribute("type", "checkbox");
  input_checkbox.setAttribute("checked", '');
  input_checkbox.setAttribute("onchange", "alert(this.value)");

  let save_btn = document.createElement("span")
  save_btn.setAttribute("class", "confirm_btn pct_btn");
  save_btn.setAttribute("title", "Сохранить");
  save_btn.innerHTML = "&#10004;"
  let cancel_btn = document.createElement("span")
  cancel_btn.setAttribute("class", "cancel_btn pct_btn");
  cancel_btn.setAttribute("title", "Отмена");
  cancel_btn.innerHTML = "&#10008;"

  final_row.appendChild(input_checkbox)
  final_row.appendChild(cancel_btn)
  final_row.appendChild(save_btn)
  return final_row;
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
function draw_check_box(input_data){

}

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

function post_to_sql(str_data) {
  $.ajax({
    url: `/save_sett/${str_data}`,
    type: 'POST',
    success: function(response) {
      draw_div_tags(response)
    }
  })
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


// СТАРОЕ. НЕ НУЖНОЕ?
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
  <p onclick = 'del_set_from_sql(${json_string_in})'>Удалить</p>`
}
