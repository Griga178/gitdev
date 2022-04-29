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
        let json = jQuery.parseJSON(response);
        answer_div.innerHTML = `${parsed_links_counter} <a id = "res_${parsed_links_counter}" href = "${json.link}" target = "_blank">${json.main_page}<a><b> ${json.price} руб.</b>
          <button onclick="show_settings(res_${parsed_links_counter})"><i>Показать настройки</i></button>`;
        console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });

}

function show_settings (tag_id){
  set_main_page.innerHTML = tag_id.innerHTML

}
