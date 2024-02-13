let mDateFormat = function(date_string){
  let arr = date_string.split('-')
  return arr[2]+'.'+arr[1]+'.'+arr[0]
}

let fill_common_info = function(responce_objest) {
  inp_end_date.value = responce_objest.today_date
  inp_start_date.value = responce_objest.last_contract_date
  common_info_last_update_date.innerHTML = mDateFormat(responce_objest.last_update_date)
  common_info_last_update_date_2.innerHTML = mDateFormat(responce_objest.last_update_date)
  common_info_first_contract_date.innerHTML = mDateFormat(responce_objest.first_contract_date)
  common_info_last_contract_date.innerHTML = mDateFormat(responce_objest.last_contract_date)
  common_info_contract_amount.innerHTML = responce_objest.contract_amount + ' шт'
  common_info_empty_contract_amount.innerHTML = responce_objest.empty_contract_amount + ' шт'
  common_info_empty_contract_amount_2.innerHTML = responce_objest.empty_contract_amount
  common_info_product_amount.innerHTML = responce_objest.product_amount + ' шт'
}

let get_sum_info = function() {
  $.ajax({
    url: '/get_sum_info',
    type: 'get',
    success: function (response){
      console.log(response)
      fill_common_info(response)
    }
  })
}

get_sum_info()

let start_parse_number = function() {
    $.ajax({
      url: '/start_parse_numbers',
      data: {
        "date_from": inp_start_date.value,
        "date_to": inp_end_date.value,
      },
      type: 'post',
      success: function (response){
        console.log(response)
        app_active = response.app_status
        change_number_parse_menu_start()
      }
    })

}
let stop_parse_number = function() {
  change_number_parse_menu_stop()
}
let refresh_parse_number = function() {
  change_number_parse_menu_refresh()
}

let change_number_parse_menu_start = function () {
  fldst_contract_dates.disabled = true
  btn_parse_number_start.hidden = true
  div_number_progres.hidden = false
  btn_parse_number_stop.hidden = false
}

let change_number_parse_menu_stop = function () {
  btn_parse_number_stop.hidden = true
  btn_parse_number_refresh.hidden = false
}

let change_number_parse_menu_refresh = function () {
  fldst_contract_dates.removeAttribute('disabled')
  btn_parse_number_start.hidden = false
  div_number_progres.hidden = true
  btn_parse_number_stop.hidden = true
  btn_parse_number_refresh.hidden = true
}

if (app_active === 1){
  console.log('parse_numbers')
  change_number_parse_menu_start()
}
else if (app_active === 2)
console.log('parse_products')
else if (app_active === 3)
console.log('update_contracts')
else
console.log('have not start - zero')

setInterval(
  function(){
    if (app_active === 1){
      console.log('parse_numbers')

      $.ajax({
        url: '/check_info',
        type: 'get',
        success: function (response){
          // progress_bar_parse_number.setAttribute('aria-valuenow', response.parse_progress)
          progress_bar_parse_number.value = response.parse_progress
          // console.log('1')
          }
      })}
    else if (app_active === 2)
    console.log('parse_products')
    else if (app_active === 3)
    console.log('update_contracts')
    else
    console.log('have not start - zero')

},
   update_interval);
btn_parse_number_start.onclick = function () {
  start_parse_number()
}
btn_parse_number_stop.onclick = function () {
  stop_parse_number()
}
btn_parse_number_refresh.onclick = function () {
  refresh_parse_number()
}
