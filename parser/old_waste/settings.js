// Функция отрисовки fieldset

let json_dict = {
  schema: {
    name: {
      type: 'string',
      title: 'ИМЯ',
      required: true
    },
    }
  }


$('form').jsonForm(json_dict)

// $('form').jsonForm({
//   schema: {
//     name: {
//       type: 'string',
//       title: 'Name',
//       required: true
//     },
//     age: {
//       type: 'number',
//       title: 'Age'
//     }
//   },
//   onSubmit: function (errors, values) {
//     if (errors) {
//       $('#res').html('<p>I beg your pardon?</p>');
//     }
//     else {
//       $('#res').html('<p>Hello ' + values.name + '.' +
//         (values.age ? '<br/>You are ' + values.age + '.' : '') +
//         '</p>');
//     }
//   }
// });
