// - - - - - - -получение настроек из БД- - - - - - -
function get_domain_setting(domain_id){
  $.ajax({
    url: `/get_domain_setting/${domain_id}`,
    type: 'GET',
    success: function(response) {

      write_domain_setting(response)
    }
  })
}

function write_domain_setting(response){
  alert(`select domain by id: ${response}`)
}
