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

function show_settings(shop_id) {
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'POST',
    success: function(response) {
      let row_counter = 0
      let json_obj = $.parseJSON(response)
      let shop_name = Object.keys(json_obj)
      set_main_page.innerHTML = shop_name;
      let price_list = json_obj[shop_name]['price']
      if (price_list !== undefined){
          let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[4],shop_id].join()
          set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id" class = 'value_name_sett'>${price_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
          <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
          <p class = 'value_name_sett'>"${price_list[2]}"</p>
          <p id ="change_price_sett" onclick = "change_setting(1, '${tags_strint}')">&nbsp;Изменить</p>`
      }else change_setting(1, `None,None,None,None,${shop_id}`)
      let name_list = json_obj[shop_name]['name']
      if (name_list !== undefined){
        let tags_strint = [name_list[0],name_list[1],name_list[2],name_list[4],shop_id].join()
          set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id" class = 'value_name_sett'>${name_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${name_list[0]}&nbsp</p>
          <p class = 'attr_name_sett'>${name_list[1]} =&nbsp</p>
          <p class = 'value_name_sett'>"${name_list[2]}"</p>
          <p id ="change_name_sett" onclick = "change_setting(2, '${tags_strint}')">&nbsp;Изменить</p>`
      }else change_setting(2, `None,None,None,None,${shop_id}`)
      let chars_list = json_obj[shop_name]['chars']
      if (chars_list !== undefined){
        let tags_strint = [chars_list[0],chars_list[1],chars_list[2],chars_list[4],shop_id].join()
          set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id" class = 'value_name_sett'>${chars_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${chars_list[0]}&nbsp</p>
          <p class = 'attr_name_sett'>${chars_list[1]} =&nbsp</p>
          <p class = 'value_name_sett'>"${chars_list[2]}"</p>
          <p id ="change_chars_sett" onclick = "change_setting(3, '${tags_strint}')">&nbsp;Изменить</p>`
      } else change_setting(3, `None,None,None,None,${shop_id}`)
    }
  })
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
      let tags_types_dict = {"price": "Цена", "name": "Название", "chars": "Характеристика"}
      set_main_page.innerHTML = `${json_obj['shop_name']}`

      for (tag_type in tags_types_dict) {

        json_obj[tag_type]['rus_tag'] = tags_types_dict[tag_type]
        json_obj[tag_type]['shop_id'] = shop_id
        json_obj['new_sett'] = false
        let json_string_out = JSON.stringify(json_obj[tag_type])

        if (json_obj[tag_type].length === 0) {
          json_obj['new_sett'] = true
          empty_json_string_out = JSON.stringify(json_obj)
          draw_input_tags(empty_json_string_out)
        }
        else {
          draw_div_tags(json_string_out)
        }
      }
    }
  })
}

function draw_div_tags(json_string_in) {
  let json_string_out = json_string_in
  let sett_dict = $.parseJSON(json_string_in)
  let div_for_tags = document.createElement('div');
  div_for_tags.setAttribute("class", "div_for_tags");
  div_for_tags.setAttribute("ondblclick", `draw_input_tags(${json_string_out})`);
  div_for_tags.setAttribute("title", "Изменить - Двойной щелчек");
  div_for_tags.setAttribute("id", `${sett_dict['tag_id']}`);
  block_for_sett_tags.appendChild(div_for_tags)

  div_for_tags.innerHTML =
  `${sett_dict['rus_tag']}:&nbspid:
  <p class = 'tag_name_sett'>${sett_dict['tag_name']}&nbsp;</p>
  <p class = 'attr_name_sett'>${sett_dict['attr_name']} =&nbsp</p>
  <p class = 'value_name_sett'>"${sett_dict['attr_val']}"</p>`
}

function draw_input_tags(json_string_in) {
  let json_string_out = JSON.stringify(json_string_in)
  alert("vS PLTCM")
  // НА ВХОД ТОЛЬКО ТИП ТЕГОВ (ДЛЯ ПОИСКА ЦЕНЫ/ИМЕНИ/ХАРАКТЕРИСТИК)
  if (json_string_out['new_sett'] === true){
    alert('true')
    // let json_string_in_out = {'shop_id': 'shop_id', 'tag_type': json_string_in}
    let div_for_tags = document.createElement('div');
    div_for_tags.setAttribute("class", "div_for_tags");
    div_for_tags.setAttribute("id", `${json_string_in}`);
    block_for_sett_tags.appendChild(div_for_tags)
    div_for_tags.innerHTML =
    `${json_string_in}:&nbspid:
    <input type = "text" value = "">
    <input type = "text" value = "">
    <input type = "text" value = "">
    <p onclick = 'save_sett_changing_ver2(${json_string_in})'>Сохранить</p>
    <p onclick = "">Удалить</p>`
  }
  // НА ВХОД СЛОВАРЬ С ЗАПОЛНЕННЫМИ ТЕГАМИ И ДРУГИМИ ДАННЫМИ
  else {

    let div_tag_for_change = document.getElementById(json_string_in['tag_id'])
    div_tag_for_change.innerHTML =
    `${json_string_in['rus_tag']}:&nbspid:
    <input type = "text" value = "${json_string_in['tag_name']}">
    <input type = "text" value = "${json_string_in['attr_name']}">
    <input type = "text" value = "${json_string_in['attr_val']}">
    <p onclick = 'save_sett_changing_ver2(${json_string_out})'>Сохранить</p>
    <p onclick = "">Удалить</p>`

  }
}
function save_sett_changing_ver2(json_string_in) {
  if (json_string_in['new_sett'] === true){
    alert(" я тут")
    let div_tag_for_change = document.getElementById(json_string_in)
    let a = div_tag_for_change.children
    // получаем id магазина
  }else {
    let div_tag_for_change = document.getElementById(json_string_in['tag_id'])
    let a = div_tag_for_change.children
    let dict_out = {"shop_id": json_string_in['shop_id'], "tag_type": json_string_in['tag_type'], "tag_name": a[0].value, "attr_name": a[1].value, "attr_val": a[2].value, "tag_status": true, "tag_id": json_string_in['tag_id']}
    json_string_out = JSON.stringify(dict_out)
    alert(json_string_out)
    // json_answer = post_to_sql(json_string_out)
    // draw_div_tags(json_answer)
  }
}
function change_setting(char_num, tags_strint) {
  if (char_num === 1) {
    // alert(`Изменяем: ${char_num} ${tags_strint}`)
    let tag_list = tags_strint.split(',')
    set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_1'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_1'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_1'>
    <p onclick = "save_sett_changing(1, ${tag_list[4]})">Сохранить</p>`
  }
  else if (char_num === 2) {
    let tag_list = tags_strint.split(',')
    set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_2'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_2'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_2'>
    <p onclick = "save_sett_changing(2,${tag_list[4]})">Сохранить</p>`
  }
  else if (char_num === 3) {
    let tag_list = tags_strint.split(',')
    set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_3'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_3'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_3'>
    <p onclick = "save_sett_changing(3,${tag_list[4]})">Сохранить</p>`
  }
}

function save_sett_changing(char_num, shop_id) {
  if (char_num === 1) {
  let price_list = [inpt_tag_name_1.value, inpt_tag_attr_1.value, inpt_tag_val_1.value, price_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  let id_of_sett = price_sett_id.innerHTML
  // alert(`Кидаем в SQL: "${price_list.slice(0,3)}" id: ${price_sett_id.innerHTML} shop_id:${shop_id}`)
  let str_data = `{"${price_list[3]}": ["${price_list[0]}","${price_list[1]}","${price_list[2]}","True", "${shop_id}", "price"]}`
  post_to_sql(str_data)
  set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(1, '${tags_strint}')">&nbsp;Изменить</p>`
}else if (char_num === 2) {
  let price_list = [inpt_tag_name_2.value, inpt_tag_attr_2.value, inpt_tag_val_2.value, name_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  // alert(`Кидаем в SQL: "${price_list}" id: ${name_sett_id.innerHTML} shop_id:${shop_id}`)
  let str_data = `{"${price_list[3]}": ["${price_list[0]}","${price_list[1]}","${price_list[2]}","True", "${shop_id}", "name"]}`
  post_to_sql(str_data)
  set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(2, '${tags_strint}')">&nbsp;Изменить</p>`
}else if (char_num === 3) {
  let price_list = [inpt_tag_name_3.value, inpt_tag_attr_3.value, inpt_tag_val_3.value, chars_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  // alert(`Кидаем в SQL: "${price_list}" id: ${chars_sett_id.innerHTML} shop_id:${shop_id}`)
  let str_data = `{"${price_list[3]}": ["${price_list[0]}","${price_list[1]}","${price_list[2]}","True", "${shop_id}", "chars"]}`
  post_to_sql(str_data)
  set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(3, '${tags_strint}')">&nbsp;Изменить</p>`
  }
}

function post_to_sql(str_data) {
  // alert(`Кидаем в SQL: "${str_data}"`)
  $.ajax({
    url: `/save_sett/${str_data}`,
    type: 'POST',
    success: function(response){
      alert(response)
    }
  })
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
        // row_for_data.setAttribute("onclick", `show_settings(${variable})`)
        row_for_data.setAttribute("onclick", `show_settings_ver2(${variable})`)
        row_for_data.innerHTML = `<p>${variable} ${java_dict[variable]}</p>`;
        row_list.appendChild(row_for_data);
      }
    }
  });
}
