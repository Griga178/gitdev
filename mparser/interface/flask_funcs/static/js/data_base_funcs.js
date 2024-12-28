// ПОЛУЧАЕМ ТАБЛИЦУ С СЕРВЕРА
function get_links_info(){
  $.ajax({
    url: "/links",
    type: "GET",
    // success: draw_links_table(links_table)
    success: function(links_table) {
      p_btn_draw_links.remove()
      find_tag_for_table(links_table)
    }
  })
}

// НАХОДИМ/СОЗДАЕМ ТЕГ ДЛЯ ВСТАВКИ ТАБЛИЦЫ
function find_tag_for_table(links__info) {

  let links_table

  links_table = document.getElementById("links_table")

  if (links_table) {  }

  else{

    links_table = document.createElement("table")
    links_table.setAttribute('id', 'links_table')
    links_block.appendChild(links_table)

  }


  let json_obj = $.parseJSON(links__info)

  let table_header = document.createElement('tr')
  links_table.appendChild(table_header)

  for (t_caption in json_obj.table_header) {
    let table_head = document.createElement('th')
    table_head.innerHTML = json_obj.table_header[t_caption]
    table_header.appendChild(table_head)
  }
  delete json_obj.table_header

  for (links in json_obj) {
    let row = document.createElement('tr')
    row.setAttribute('id', links)

    let data_num = document.createElement('td')
    data_num.innerHTML = links
    row.appendChild(data_num)

    let data_domain = document.createElement('td')
    data_domain.innerHTML = json_obj[links][0].slice(0, 20)
    row.appendChild(data_domain)

    let data_link = document.createElement('td')
    data_link.innerHTML = `<a href = "${json_obj[links][1]}" target="_blank"> ${json_obj[links][1].slice(-20)}<a>`

    row.appendChild(data_link)

    let data_name = document.createElement('td')
    data_name.setAttribute('title', `${json_obj[links][2]}`)
    data_name.innerHTML = json_obj[links][2].slice(0, 20)
    row.appendChild(data_name)

    let data_price = document.createElement('td')
    data_price.innerHTML = json_obj[links][3]
    row.appendChild(data_price)
    let data_parse_date = document.createElement('td')
    data_parse_date.innerHTML = json_obj[links][4]
    row.appendChild(data_parse_date)



    links_table.appendChild(row)
  }
}
