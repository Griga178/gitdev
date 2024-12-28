function draw_settings(shop_id){
  $.ajax({
    url: `/get_shop_setting/${shop_id}`,
    type: 'GET',
    beforeSend: function() {
      set_main_page.innerHTML = "Загрузка..."
    },
    success: function(response) {
      draw_settings_form(response)

      btn_show_links.setAttribute('onclick', `show_few_links(${shop_id})`)
      btn_show_links.removeAttribute("hidden")

    }
  })
}

function draw_settings_form(response){
  let json_obj = $.parseJSON(response)

  block_for_sett_tags.innerHTML = ''
  set_main_page.innerHTML = `<span id = "${json_obj.shop_id}">${json_obj.shop_name}</span>`
  set_domain_name.innerHTML = json_obj.shop_name

  // при расширении - закинуть типы в бд - выводить из бд по типам
  let shop_settings_tags = {
    "price": {"rus_tag": "Теги цены", "form_class": "form_for_tags"},
    "sold_out": {"rus_tag": 'Теги "Нет в наличии"', 'form_class': "form_for_tags"},
    "name": {"rus_tag": "Теги названия", 'form_class': "form_for_tags"},
    "chars": {"rus_tag": "Теги характеристик", 'form_class': "form_for_tags"},
    "need_selenium": {"rus_tag": "Есть JavaScript", 'form_class': "form_for_checkbox"},
    "headless_mode": {"rus_tag": "Отключить headless_mode", 'form_class': "form_for_checkbox"},
    "sett_active": {"rus_tag": "Не парсить магазин", 'form_class': "form_for_checkbox"},
  }

  for (tag_type in shop_settings_tags) {
    let form_block = document.createElement('form');
    form_block.setAttribute("id", `${tag_type}`);
    form_block.setAttribute("class", `${shop_settings_tags[tag_type]['form_class']}`);
    // form_block.innerHTML = `<label>${shop_settings_tags[tag_type]['rus_tag']}:</label>`
    let label_block = document.createElement('label');
    label_block.innerHTML = `${shop_settings_tags[tag_type]['rus_tag']}:`
    form_block.appendChild(label_block)
    block_for_sett_tags.appendChild(form_block)

    if (shop_settings_tags[tag_type]['form_class'] === "form_for_tags") {
      draw_input_tag(json_obj.tag_setting[tag_type], form_block)
      draw_save_buttons(json_obj.tag_setting[tag_type], tag_type, form_block)

    } else {
      draw_input_checkbox(json_obj[tag_type], form_block)
      draw_save_checkbox(json_obj[tag_type], tag_type, form_block)
    }
    // label_block.appendChild(input_rows)
    // form_block.appendChild(input_rows)
  }
}

function draw_input_tag(obj_set, form_block) {

  var element = form_block.getElementsByTagName("div")
  // alert(element)
  // document.removeChild(element)
  let input_types = {
    "tag_name":{"name":"tag", "title": "Название тега (прим.: div / span / h1)"},
    "attr_name":{"name":"attr", "title": "Атрибут внутри тега (прим.: class / id / itemprop)"},
    "attr_value":{"name":"attr_val", "title": "Значение атрибута (прим.: price / name)"},
  }
  let final_row = document.createElement("div")
  // let expriment_obj = {"input":{"name":"tag", "title": "Подсказка 1", "type": "text", "value": ""}}
  for (type in input_types) {
    let input_obj = document.createElement("input")
    input_obj.setAttribute("name", `${input_types[type]["name"]}`);
    input_obj.setAttribute("title", `${input_types[type]["title"]}`);
    input_obj.setAttribute("type", "text");
    input_obj.setAttribute("value", `${obj_set?obj_set[type]:''}`);
    // input_obj.setAttribute("onchange", "alert(this.value)");
    final_row.appendChild(input_obj)
  }

  let cancel_btn = document.createElement("span")
  cancel_btn.setAttribute("class", "cancel_btn pct_btn");
  cancel_btn.setAttribute("title", "Отмена");
  cancel_btn.innerHTML = "&#10008;"
  final_row.appendChild(cancel_btn)

  if (obj_set) draw_delete_buttons(tag_type, final_row, obj_set['tag_id']);

  form_block.appendChild(final_row)
}

function draw_input_checkbox(obj_type, form_block) {
  let input_checkbox = document.createElement("input")
  input_checkbox.setAttribute("type", "checkbox");
  if (obj_type) input_checkbox.setAttribute("checked", "");
  // input_checkbox.setAttribute("onchange", "alert(this.value)");
  form_block.appendChild(input_checkbox)
}
// СОХРАНЕНИЕ
function draw_save_checkbox (obj_set, tag_id, final_row) {
  let save_btn = document.createElement("span")
  save_btn.setAttribute("class", "confirm_btn pct_btn");
  save_btn.setAttribute("title", "Сохранить");
  save_btn.setAttribute("onclick", `save_checkbox_setting("${tag_id}")`);
  save_btn.innerHTML = "&#10004;"
  final_row.appendChild(save_btn)
}

function save_checkbox_setting(setting_name) {
  let shop_id_value = set_main_page.firstChild.id
  let checkbox = document.getElementById(setting_name)[0]
  let dict_out = {"id": shop_id_value}
  dict_out[setting_name] = checkbox.checked

  json_dict_out = JSON.stringify(dict_out)
  // alert(json_dict_out)
  send_checkbox_value_to_db(json_dict_out)
}

function send_checkbox_value_to_db(js_dict){
  $.ajax({
    url: '/save_shop_setting',
    contentType: 'application/json',
    type: 'POST',
    dataType : 'json',
    data: js_dict,
    success: function(response) {
      alert(response)
    }
  })
}

function draw_save_buttons (obj_set, tag_id, final_row) {
  let save_btn = document.createElement("span")
  save_btn.setAttribute("class", "confirm_btn pct_btn");
  save_btn.setAttribute("title", "Сохранить");
  save_btn.setAttribute("onclick", `save_sett_changing('${obj_set?obj_set['tag_id']:''}', "${tag_id}")`);
  save_btn.innerHTML = "&#10004;"
  final_row.appendChild(save_btn)
}

function save_sett_changing (data, form_id) {
  let shop_id_value = set_main_page.firstChild.id
  let changing_form = document.getElementById(form_id);

  let in_tag = changing_form.elements.tag.value;
  let in_attr = changing_form.elements.attr.value;
  let in_value = changing_form.elements.attr_val.value;
  let dict_out = {
    "id_main_page": shop_id_value,
    "tag_type": form_id,
    "tag_name": in_tag,
    "attr_name": in_attr,
    "attr_value": in_value,
    "id": data?data:false
  }
  let json_string_out = JSON.stringify(dict_out);
  post_to_sql(json_string_out);
}

function draw_delete_buttons (tag_id, final_row, tag_id) {
  let delete_btn = document.createElement("span")
  delete_btn.setAttribute("class", "delete_btn pct_btn");
  delete_btn.setAttribute("title", "Удалить");
  delete_btn.setAttribute("onclick", `del_set_from_sql(${tag_id})`);
  delete_btn.innerHTML = "&#128473;"
  final_row.appendChild(delete_btn)
}

function post_to_sql(str_data) {
  $.ajax({
    url: `/save_tag_setting`,
    contentType: 'application/json',
    type: 'POST',
    dataType : 'json',
    data: str_data,
    success: function(response) {
      form_block = document.getElementById(response.tag_type)
      // alert(form_block)
      draw_input_tag(response, form_block)
    }
  })
}

function del_set_from_sql(tag_id) {
  let shure = confirm("Вы уверены?")
  if (shure) {
    $.ajax({
      url: `/del_sett/${tag_id}`,
      type: 'POST',
      success: function(response) {
        alert(response)
      }
    })
  }
}
