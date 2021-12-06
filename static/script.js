console.log("this is connected");

const file = document.getElementById("upload-btn");

function validation() {
  if (file.value !== "") {
    const pos_of_dot = file.value.lastIndexOf(".") + 1;
    const ext = file.value.substring(pos_of_dot);
    if (ext !== "csv") {
      alert("Selected file is not a csv file!....");
      return false;
    }
  } else {
    alert("No file selected.....");
    return false;
  }
}

const index = document.getElementById("index");

function indexValidation() {
  if (index.value === "") {
      console.log(index.value);
    alert("No index value is given....");
    return false;
  } else {
    return true;
  }
}
