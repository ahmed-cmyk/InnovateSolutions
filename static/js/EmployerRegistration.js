function checkFalseEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

function isNumber(input) {
    var intRegex = /^\d+$/;
    var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
    return intRegex.test(input) || floatRegex.test(input);
}

function checkFalseUAENumber(number) {
    var phoneReg = /^(?:\+971|00971|0)?(?:50|51|52|55|56|2|3|4|6|7|9)\d{7}$/;
    return !phoneReg.test(number);
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
    $('#id_phone_number').focusout(function () {
        $('#id_phone_number').css('border', '1px solid red');
        if(checkFalseUAENumber($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#phoneNumberError').html('Please enter a valid UAE phone number').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#phoneNumberError').html('').css('color', '');
        }
    });
});

$("#companyForm").submit(function (e) {
    var companyname = $("#id_company_name").val();
    var phonenumber = $("#id_phone_number").val();
    var company_email = $("#id_email").val();

    if(checkFalseEmail(company_email)) {
        e.preventDefault();
    }
    else {
        alert("Success!");
    }
});