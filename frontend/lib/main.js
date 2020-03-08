'use strict';

document.addEventListener('DOMContentLoaded', function () {
  var imageUpload = document.querySelector('#image-upload-container input[type=file]');
  imageUpload.onchange = function () {
    return imageUploadSelected(imageUpload);
  };
});

function imageUploadSelected(imageUpload) {
  var files = imageUpload.files;
  if (files.length > 0) {
    var file = files[0];
    var fileName = document.querySelector('#image-upload-container .file-name');
    fileName.textContent = file.name;

    if (file.type.match(/image.*/)) {
      var thumbnail = document.querySelector("#image-upload-container #thumbnail");
      var reader = new FileReader();
      reader.onload = function (e) {
        return thumbnail.src = e.target.result;
      };
      reader.readAsDataURL(file);
      thumbnail.classList.add("show-upload-thumbnail");
    }
  }
}