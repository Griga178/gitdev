function parse_link() {
  alert($('form').serialize());
  let answer_div = document.createElement("div")
  answer_div.innerHTML = "Думаем..."

  $.ajax({
      url: "/parser_link_check",
      data: $('form').serialize(),
      type: 'POST',
      beforeSend: function() {
        parse_result_block.appendChild(answer_div)
      },
      success: function(response) {
          var json = jQuery.parseJSON(response)
          answer_div.innerHTML = `<a href = "${json.link}" target = "_blank">${json.main_page}<a> ${json.price} руб.`
          console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });

}

function show_settings (){
  alert('Смотри')
}
