function checkFalseEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

function isNumber(input) {
    var intRegex = /^\d+$/;
    var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
    return intRegex.test(input) || floatRegex.test(input);
}

function checkUnmatchedPasswords(password1, password2) {
    if (password1 !== password2) {
        return true;
    }
    return false;
}

$(function () {
    $('#id_email').focusout(function () {
        if(($(this).val() === '') || (checkFalseEmail($(this).val()))) {
            $(this).css('border', '1px solid red');
            $('#emailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#emailError').html('').css('color', '');
        }
    });
    $('#id_company_name').focusout(function () {
        if(($(this).val() === '') || (isNumber($(this).val()))) {
            $(this).css('border', '1px solid red');
            $('#companyNameError').html('Please enter a valid company name').css('color', 'red')
        }
        else {
            $(this).css('border', '');
            $('#companyNameError').html('').css('color', '')
        }
    });
    $('#id_password1').focusout(function () {
        if($(this).val().length < 8) {
            $('#id_password1').css('border', '1px solid red');
            $('#password1Error').html('Your password cannot be fewer than 8 characters').css('color', 'red');
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
});

$("#companyForm").submit(function (e) {
    var company_email = $("#id_email").val();
    var password1 = $('#id_password1').val();
    var password2 = $('#id_password2').val();

    if(checkFalseEmail(company_email)  || checkUnmatchedPasswords(password1, password2)) {
        e.preventDefault();
    }
    else {
        console.log("Success!");
    }
});