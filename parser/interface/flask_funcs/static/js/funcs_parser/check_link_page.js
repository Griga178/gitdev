let parsed_links_counter = 0;

function parse_link() {
  // alert($('form').serialize());
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

function show_settings(tag_id) {
  set_main_page.innerHTML = tag_id.innerHTML

}

function show_settings(shop_id) {
  $.ajax({
    url: `/links_sett/${shop_id}`,
    type: 'POST',
    success: function(response) {
      let row_counter = 0
      let json_obj = $.parseJSON(response)
      alert(`${response}`)
      set_main_page.innerHTML = Object.keys(json_obj);
      // alert(`${Object.keys(json_obj)}`)

      for (set in json_obj) {
        row_counter += 1
        let set_row = document.createElement('p')
        set_row.setAttribute("id", `set_row_${row_counter}`)
        set_row.innerHTML = Object.keys(json_obj[set])
        settings_block.appendChild(set_row)
      }
    }
  })
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
