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
          let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[4]].join()
          set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id">${price_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
          <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
          <p>"${price_list[2]}"</p>
          <p id ="change_price_sett" onclick = "change_setting(1, '${tags_strint}')">&nbsp;Изменить</p>`
      }else change_setting(1, `None,None,None,None`)
      let name_list = json_obj[shop_name]['name']
      if (name_list !== undefined){
        let tags_strint = [name_list[0],name_list[1],name_list[2],name_list[4]].join()
          set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id">${name_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${name_list[0]}&nbsp</p>
          <p class = 'attr_name_sett'>${name_list[1]} =&nbsp</p>
          <p class = 'value_name_sett'>"${name_list[2]}"</p>
          <p id ="change_name_sett" onclick = "change_setting(2, '${tags_strint}')">&nbsp;Изменить</p>`
      }else change_setting(2, `None,None,None,None`)
      let chars_list = json_obj[shop_name]['chars']
      if (chars_list !== undefined){
        let tags_strint = [chars_list[0],chars_list[1],chars_list[2],chars_list[4]].join()
          set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id">${chars_list[4]}</p>&nbsp,
          <p class = 'tag_name_sett'>${chars_list[0]}&nbsp</p>
          <p class = 'attr_name_sett'>${chars_list[1]} =&nbsp</p>
          <p class = 'value_name_sett'>"${chars_list[2]}"</p>
          <p id ="change_chars_sett" onclick = "change_setting(3, '${tags_strint}')">&nbsp;Изменить</p>`
      } else change_setting(3, `None,None,None,None`)
    }
  })
}

function show_settings_ver2(shop_id) {
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'POST',
    success: function(response) {
      settings_block.innerHTML = ""
      let json_obj = $.parseJSON(response)
      let tags_types = {"price": "Цена", "name": "Название", "chars": "Характеристика"}
      let shop_header = document.createElement("h2")
      shop_header.innerHTML = `${json_obj['shop_id']}: ${json_obj['shop_name']}`
      settings_block.appendChild(shop_header)
      let update_btn = document.createElement("button")
      update_btn.innerHTML = "Обновить"
      update_btn.setAttribute("onclick", `show_settings_ver2(${json_obj['shop_id']})`)
      settings_block.appendChild(update_btn)
      for (tag_type in tags_types) {
        let row_for_sett = document.createElement("p")
        // row_for_sett.setAttribute("class", `tag_name_sett`)
        row_for_sett.innerHTML = `${tags_types[tag_type]}: `
        settings_block.appendChild(row_for_sett)
      }
    }
  })
}
function change_setting(char_num, tags_strint) {
  if (char_num === 1) {
    // alert(`Изменяем: ${char_num} ${tags_strint}`)
    let tag_list = tags_strint.split(',')
    set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_1'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_1'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_1'>
    <p onclick = "save_sett_changing(1)">Сохранить</p>`
  }
  else if (char_num === 2) {
    let tag_list = tags_strint.split(',')
    set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_2'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_2'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_2'>
    <p onclick = "save_sett_changing(2)">Сохранить</p>`
  }
  else if (char_num === 3) {
    let tag_list = tags_strint.split(',')
    set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id">${tag_list[3]}</p>&nbsp,
    <input type = "text" value = "${tag_list[0]}" id = 'inpt_tag_name_3'>
    <input type = "text" value = "${tag_list[1]}" id = 'inpt_tag_attr_3'>
    <input type = "text" value = "${tag_list[2]}" id = 'inpt_tag_val_3'>
    <p onclick = "save_sett_changing(3)">Сохранить</p>`
  }
}

function save_sett_changing(char_num) {
  if (char_num === 1) {
  let price_list = [inpt_tag_name_1.value, inpt_tag_attr_1.value, inpt_tag_val_1.value, price_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  let id_of_sett = price_sett_id.innerHTML
  alert(`Кидаем в SQL: "${price_list.slice(0,3)}" id: ${price_sett_id.innerHTML}`)
  set_row_price.innerHTML = `Цена:&nbspid:<p id = "price_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(1, '${tags_strint}')">&nbsp;Изменить</p>`
}else if (char_num === 2) {
  let price_list = [inpt_tag_name_2.value, inpt_tag_attr_2.value, inpt_tag_val_2.value, name_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  alert(`Кидаем в SQL: "${price_list}" id: ${name_sett_id.innerHTML}`)
  set_row_name.innerHTML = `Название:&nbspid:<p id = "name_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(2, '${tags_strint}')">&nbsp;Изменить</p>`
}else if (char_num === 3) {
  let price_list = [inpt_tag_name_3.value, inpt_tag_attr_3.value, inpt_tag_val_3.value, chars_sett_id.innerHTML]
  let tags_strint = [price_list[0],price_list[1],price_list[2],price_list[3]].join()
  // alert(`Кидаем в SQL: "${price_list}" id: ${chars_sett_id.innerHTML}`)
  let str_data = `{"${price_list[3]}": ["${price_list[0]}","${price_list[1]}","${price_list[2]}","True",]}`
  post_to_sql(str_data)
  set_row_chars.innerHTML = `Характеристика:&nbspid:<p id = "chars_sett_id">${price_list[3]}</p>&nbsp,
  <p class = 'tag_name_sett'>${price_list[0]}&nbsp;</p>
  <p class = 'attr_name_sett'>${price_list[1]} =&nbsp</p>
  <p>"${price_list[2]}"</p>
  <p id ="change_price_sett" onclick = "change_setting(3, '${tags_strint}')">&nbsp;Изменить</p>`
  }
}

function post_to_sql(str_data) {
  alert(`Кидаем в SQL: "${str_data}"`)

}
function draw_json_dict() {
  $.ajax({
    url: "/print_links_base",
    type: 'POST',
    success: function(json_dict) {
      let java_dict = jQuery.parseJSON(json_dict);
      for (variable in java_dict) {
        let row_for_data = document.createElement("div");
        row_for_data.setAttribute("onclick", `show_settings(${variable})`)
        row_for_data.innerHTML = `<p>${variable} ${java_dict[variable]}</p>`;
        row_list.appendChild(row_for_data);
      }

    }
  });
}
