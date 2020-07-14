function isNumber(input) {
      var intRegex = /^\d+$/;
      var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
      return intRegex.test(input) || floatRegex.test(input);
}

function testEmailValidity(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

// $("#id_email").focusout(function (e) {
//               e.preventDefault();
//               var username = $(this).val();
//               $.ajax({
//                     type: 'GET',
//                     url: "{% url 'check_alumni_username' %}",
//                     data: {"username": username},
//                     success: function (response) {
//                           console.log("I'm going in");
//                           if(!response["valid"]){
//                                 $("#personalEmailError").css('color', 'red');
//                                 $("#personalEmailError").html("This username is already being used");
//                                 var username = $("#id_email");
//                                 username.focus();
//                             }
//                           else {
//                                 $("#personalEmailError").css('color', '');
//                                 $("#personalEmailError").html("");
//                           }
//                     },
//                     error: function (response) {
//                           console.log(response);
//                     }
//               });
//             });

$(document).ready(function () {
      $('#id_first_name').change(function () {
        var firstName = $(this).val();
        if(isNumber(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('You cannot enter a number').css('color', 'red');
        }
        else {
            $('#id_first_name').css('border', '');
            $('#firstNameError').html('').css('color', '');
        }
    });
    $('#id_last_name').change(function () {
        var lastName = $(this).val();
        if(isNumber(lastName)) {
            $('#id_last_name').css('border', '1px solid red');
            $('#lastNameError').html('You cannot enter a number').css('color', 'red');
        }
        else {
            $('#id_last_name').css('border', '');
            $('#lastNameError').html('').css('color', '');
        }
    });
    $('#id_email').change(function () {
        if(($(this).val() === '') || (!testEmailValidity($(this).val()))) {
            $(this).css('border', '1px solid red');
            $('#personalEmailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#personalEmailError').html('').css('color', '');
        }
    });
});

$("#alumniForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();
    var email = $("#id_email").val();

    if(isNumber(firstname) || isNumber(lastname) || testEmailValidity(email)) {
        e.preventDefault();
    }
    else {
        console.log("Success!");
    }
});
