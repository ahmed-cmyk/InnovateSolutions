function isNumber(input) {
      var intRegex = /^\d+$/;
      var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
      return intRegex.test(input) || floatRegex.test(input);
}

function checkFalseStudentEmail(student_email) {
    var studentEmailRegex = /[a-zA-Z0-9]+@student.murdoch.edu.au/;
    return !studentEmailRegex.test(student_email);
}

function checkFalseEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

$(document).ready(function () {
    $('#id_first_name').focusout(function () {
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
    $('#id_last_name').focusout(function () {
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
    $('#id_password1').focusout(function () {
        if($(this).val().length < 6) {
            $('#id_password1').css('border', '1px solid red');
            $('#password1Error').html('Your password cannot be fewer than 6 characters').css('color', 'red');
        }
        else {
            $('#id_password1').css('border', '');
            $('#password1Error').html('').css('color', '');
        }
    });
    $('#id_password2').focusout(function () {
        if($(this).val() !== $('#id_password1').val()) {
            $('#id_password2').css('border', '1px solid red');
            $('#password2Error').html('Both passwords should match').css('color', 'red');
        }
        else {
            $('#id_password2').css('border', '');
            $('#password2Error').html('').css('color', '');
        }
    });
    $('#id_personal_email').focusout(function () {
        if(($(this).val() === '') || (checkFalseEmail($(this).val()))) {
            $(this).css('border', '1px solid red');
            $('#personalEmailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#personalEmailError').html('').css('color', '');
        }
    });
    $('#id_email').focusout(function () {
        if(($(this).val() === '') || (checkFalseEmail($(this).val()))) {
            $(this).css('border', '1px solid red');
            $('#studentEmailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#studentEmailError').html('').css('color', '');
        }
    });
    $('#id_email').focusout(function () {
        console.log(checkFalseStudentEmail($(this).val()));
        if(checkFalseStudentEmail($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#studentEmailError').html('Please enter a valid student email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#studentEmailError').html('').css('color', '');
        }
    });
});

$("#studentForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();
    var student_email = $("#id_email").val();
    var personal_email = $("#id_personal_email").val();

    if(isNumber(firstname) || isNumber(lastname) || checkFalseEmail(student_email) || checkFalseStudentEmail(student_email) || checkFalseEmail(personal_email)) {
        e.preventDefault();
    }
    else {
        console.log("Success!");
    }
});
