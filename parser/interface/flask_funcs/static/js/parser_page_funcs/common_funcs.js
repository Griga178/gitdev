// стартовые функции
function draw_shops_list() {
  $.ajax({
    url: "/select_shops",
    type: 'GET',
    beforeSend: function() {
      let before_message = document.createElement('h3')
      before_message.setAttribute("id", "temp_message")
      before_message.innerHTML = 'Загрузка списка ...'
      row_list.appendChild(before_message);
    },
    success: function(json_dict) {
      $('#temp_message').hide()
      let java_dict = jQuery.parseJSON(json_dict);

      draw_shop_rows(java_dict)
    }
  });
}

function draw_shop_rows(shops_list) {

  for (index in shops_list) {
    let shop_obj = shops_list[index]

    let row_for_data = document.createElement("section");
    row_for_data.setAttribute("onclick", `draw_settings(${shop_obj.shop_id})`)

    if (shop_obj.tag_setting['price']) {
      let indicator = document.createElement("div");
      indicator.setAttribute("class", 'shop_price row_indicat')
      row_for_data.appendChild(indicator)
    }
    if (shop_obj.tag_setting['name']) {
      let indicator = document.createElement("div");
      indicator.setAttribute("class", 'shop_name row_indicat')
      row_for_data.appendChild(indicator)
    }
    if (shop_obj.tag_setting['chars']) {
      let indicator = document.createElement("div");
      indicator.setAttribute("class", 'shop_chars row_indicat')
      row_for_data.appendChild(indicator)
    }

    row_for_data.setAttribute("class", 'shop_row')

    let text_content = document.createElement('p');
    text_content.setAttribute('class', 'shop_name_text')
    text_content.innerHTML = `${shop_obj.shop_id} ${shop_obj.shop_name}`;

    row_for_data.appendChild(text_content);
    row_list.appendChild(row_for_data);
  }
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
