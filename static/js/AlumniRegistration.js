function isNumber(input) {
      var intRegex = /^\d+$/;
      var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
      return intRegex.test(input) || floatRegex.test(input);
}

function testEmailValidity(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

function checkFalseDob(date) {
    var dateString = date.toString();
    var parts = dateString.split("-");
    var year = parseInt(parts[0], 10);
    if (year > 2005) {
        return true;
    }
    return false;
}

function checkUnmatchedPasswords(password1, password2) {
    if (password1 !== password2) {
        return true;
    }
    return false;
}

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
            $('#id_password1').css('border', '1px solid red');
            $('#password1Error').html('Both passwords should match').css('color', 'red');
            $('#id_password2').css('border', '1px solid red');
            $('#password2Error').html('Both passwords should match').css('color', 'red');
        }
        else {
            $('#id_password1').css('border', '');
            $('#password1Error').html('').css('color', '');
            $('#id_password2').css('border', '');
            $('#password2Error').html('').css('color', '');
        }
    });
    $('#id_email').change(function () {
        if(testEmailValidity($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#personalEmailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#personalEmailError').html('').css('color', '');
        }
    });
    $('#id_date_of_birth').focusout(function () {
        if(checkFalseDob($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#dobError').html('Please enter a valid date of birth').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#dobError').html('').css('color', '');
        }
    });
});

$("#alumniForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();
    var email = $("#id_email").val();
    var dob = $('#id_date_of_birth').val();
    var password1 = $('#id_password1').val();
    var password2 = $('#id_password2').val();

    if(isNumber(firstname) || isNumber(lastname) || testEmailValidity(email) || checkUnmatchedPasswords(password1, password2)) {
        alert('There are errors present in the form');
        e.preventDefault();
    }
    else {
        console.log("Success!");
    }
});
