// textarea maxlength
$('textarea#destination_description').maxlength({
  alwaysShow: true,
  warningClass: "badge badge-success",
  limitReachedClass: "badge badge-danger"
});

// File Upload
$('.dropify').dropify({
    allowedFileExtensions: ['jpg', 'jpeg', 'png', 'gif'],
    messages: {
        'default': 'Drag and drop a file here or click',
        'replace': 'Drag and drop or click to replace',
        'remove': 'Remove',
        'error': 'Ooops, something wrong appended.'
    },
    error: {
        'fileSize': 'The file size is too big (1M max).'
    }
});

// Autonumeric
jQuery(function($) {
  $('.autonumber').autoNumeric('init');
});


// Empty input validation
$('#submit_destination').click(function() {
  console.log("start validation")

  var haveEmptyField = false;

  var name = $('#destination_name')
  var description = $('#destination_description')
  var location = $('#destination_location')
  var longitude = $('#destination_longitude')
  var latitude = $('#destination_latitude')
  var country = $('#destination_country')
  var avatar = $('#destination_avatar')


  // Check if all required fields are filled
  if (name.val() === '') {
    $(name).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(name).removeClass('is-invalid');
  }
  if (description.val() === '') {
    $(description).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(description).removeClass('is-invalid');
  }
  if (location.val() === '') {
    $(location).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(location).removeClass('is-invalid');
  }
  if (longitude.val() === '') {
    $(longitude).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(longitude).removeClass('is-invalid');
  }
  if (latitude.val() === '') {
    $(latitude).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(latitude).removeClass('is-invalid');
  }
  if (country.val() === '') {
    $(country).addClass('is-invalid');
    console.log("Empty")
    haveEmptyField = true // Prevent form submission
  } else {
    $(country).removeClass('is-invalid');
  }


  if (avatar[0].files.length === 0) {
    avatar.addClass('is-invalid');
    console.log("Empty Avatar")
    haveEmptyField = true // Prevent form submission
  } else {
    avatar.removeClass('is-invalid');
  }

//   function encodeFileToBase64Sync(file) {
//   var reader = new FileReader();
//   reader.readAsDataURL(file);
//
//   while (!reader.result) {
//     // 等待文件读取完成
//   }
//
//   var base64String = reader.result.split(',')[1];
//   return base64String;
// }

  if (haveEmptyField === false) {
      console.log("submit successfully")
              // 创建一个新的 FormData 对象
          var formData = new FormData();
          // 将文件添加到 FormData 中
          var fileInput = $( "#destination_avatar" )[0]; // 获取文件输入框元素
          var file = fileInput.files[0]; // 获取第一个文件
          formData.append( "file", file ); // 将文件添加到 FormData 中，使用 "file" 作为文件参数的名称

    $('#destination_form').submit(function( event ) {
          event.preventDefault(); // 阻止默认的表单提交行为

          $.ajax({
            url: "/admin/upload_destination",
            method: "POST",
            data: 1,
            success: function( response ) {
                alert("Submit Successfully.")
              console.log( "Form submitted successfully." );
            },
            error: function( error ) {
              console.error( "Error submitting form: " + error );
            }
          });
        })
  }

});





    // if (name.val() === ''){
    //   $(name).addClass('is-invalid');
    //   console.log("Empty name")
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_description').val().trim() === ''){
    //   $(this).addClass('is-invalid');
    //   console.log("Empty description")
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_location').val() === ''){
    //   $(this).addClass('is-invalid');
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_longitude').val() === ''){
    //   $(this).addClass('is-invalid');
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_latitude').val() === ''){
    //   $(this).addClass('is-invalid');
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_country').val() === ''){
    //   $(this).addClass('is-invalid');
    //   return false; // Prevent form submission
    // }
    // if ($('#destination_avatar')[0].files.length === 0){
    //   $(this).addClass('is-invalid');
    //   return false; // Prevent form submission
    // }

    // If all fields are filled, allow form submission



// $(function() {
//   // Validate form before submitting
//   $('#submit_destination').click(function() {
//     // Check if all required fields are filled
//     var error = false;
//     $('input[type="text"], textarea').each(function() {
//       if ($(this).val() == '') {
//         $(this).addClass('is-invalid');
//         error = true;
//       } else {
//         $(this).removeClass('is-invalid');
//       }
//     });
//
//
//     // If there are no errors, submit the form
//     if (!error) {
//       console.log("submit successfully")
//       $('#destination_form').submit();
//
//     }
//   });
// });
