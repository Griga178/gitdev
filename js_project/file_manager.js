let my_path = "new_file.txt";

function save_file(file_name) {
  let my_row = "json_dict";
  let blob = new Blob([my_row], {
    type: "text/plain"
  });
  let link = document.createElement("a");
  link.setAttribute("href", URL.createObjectURL(blob));
  link.setAttribute("download", my_path);
  link.click();
}