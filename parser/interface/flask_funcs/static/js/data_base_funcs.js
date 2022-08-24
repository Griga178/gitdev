function get_links_info(){
  $.ajax({
    url: "/links",
    type: "GET",
    // success: draw_links_table(links_table)
    success: function(links_table) {
      draw_links_table(links_table)
    }
  })
}

function draw_links_table(links__info) {

  let links_table

  links_table = document.getElementById("links_table")

  if (links_table) {
    alert('finded')
  }
  else{

    alert(links_table)
    links_table = document.createElement("table")
    links_table. setAttribute('id', 'links_table')
    links_block.appendChild(links_table)
    alert(links_table)
  }

  alert(links__info)
}
