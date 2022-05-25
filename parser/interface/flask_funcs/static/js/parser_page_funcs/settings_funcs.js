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

      block_for_sett_tags.innerHTML = ''
      let json_obj = $.parseJSON(response)
      let tags_types = {
        "price": {"rus_tag": "Теги цены"},
        "name": {"rus_tag": "Теги названия"},
        "chars": {"rus_tag": "Теги характеристик"},
        "sold_out": {"rus_tag": 'Теги "Нет в наличии"'}
      }
      let shop_settings_type = {
        'need_selenium': {"rus_tag": "Есть JavaScript"},
        'headless_mode': {"rus_tag": "Отключить headless_mode"},
        'sett_active': {"rus_tag": "Не парсить магазин"},
      }
      set_main_page.innerHTML = `<span id = "${json_obj.shop_id}">${json_obj.shop_name}</span>`
      // alert(json_obj.tag_setting)
      for (tag_type in tags_types) {
      // for (tag_type in json_obj.tag_setting) {

        let div_for_tags = document.createElement('div');
        div_for_tags.setAttribute("class", "div_for_tags");
        div_for_tags.setAttribute("title", "Изменить - Двойной щелчек");
        div_for_tags.setAttribute("id", `${tag_type}`);
        block_for_sett_tags.appendChild(div_for_tags)

        let json_string_out = JSON.stringify(json_obj.tag_setting[tag_type])

        div_for_tags.innerHTML = `<p>${tags_types[tag_type]['rus_tag']}:</p>`
        if (typeof json_obj.tag_setting[tag_type] === "undefined") {
          alert('input')
          // draw_input_tags(json_obj.tag_setting[tag_type])
        } else {
          // draw_div_tags(json_string_out, div_for_tags)
        }
      }
    //   use_selenium_message.innerHTML = `Selenium: <b>${json_obj['use_selenium']}</b>`
    //   btn_show_few_links.innerHTML = `<p onclick = "show_few_links(${shop_id})">Показать пару ссылок <p>`
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
