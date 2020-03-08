
document.addEventListener('DOMContentLoaded', () => {
  const imageUpload = document.querySelector('#image-upload-container input[type=file]')
  imageUpload.onchange = () => imageUploadSelected(imageUpload);
});


function imageUploadSelected(imageUpload) {
  var files = imageUpload.files;
  if (files.length > 0) {
    var file = files[0];
    const fileName = document.querySelector('#image-upload-container .file-name');
    fileName.textContent = file.name;

    if (file.type.match(/image.*/)) {
      var thumbnail = document.querySelector("#image-upload-container #thumbnail");
      var reader = new FileReader();
      reader.onload = (e) => thumbnail.src = e.target.result;
      reader.readAsDataURL(file);
      thumbnail.classList.add("show-upload-thumbnail");
    }
  }
}
