function disable_fields(status) {
    if (status) {
        document.getElementById('id_expected_graduation_date').disabled = true
        document.getElementById('id_personal_email').disabled = true
        document.getElementById('id_student_id').disabled = true
        document.getElementById('id_student_id').required = false
        document.getElementById('id_personal_email').required = true
        document.getElementById('id_expected_graduation_date').required = false
    } else {
        document.getElementById('id_expected_graduation_date').disabled = false
        document.getElementById('id_personal_email').disabled = false
        document.getElementById('id_student_id').disabled = false
        document.getElementById('id_student_id').required = true
        document.getElementById('id_personal_email').required = true
        document.getElementById('id_expected_graduation_date').required = true
    }
}

function isNumber(input) {
    var intRegex = /^\d+$/;
    var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
    if(intRegex.test(input) || floatRegex.test(input)) {
        return true;
    }
    else {
        return false;
    }
}

$(document).ready(function () {
    $('.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
    $('#id_first_name').focusout(function () {
        var firstName = $(this).val()
        if(isNumber(firstName)) {
            $('#id_first_name').css({'border' : '1px solid red'});
            $('#firstNameError').css('color', 'red');
            $('#firstNameError').html('You cannot enter a number');
        }
        else {
            $('#id_first_name').css({'border': ''});
            $('#firstNameError').css('color', '');
            $('#firstNameError').html('');
        }
    });
    $('#id_last_name').focusout(function () {
        var lastName = $(this).val()
        if(isNumber(lastName)) {
            $('#id_last_name').css({'border' : '1px solid red'});
            $('#lastNameError').css('color', 'red');
            $('#lastNameError').html('You cannot enter a number');
        }
        else {
            $('#id_first_name').css({'border': ''});
            $('#lastNameError').css('color', '');
            $('#lastNameError').html('');
        }
    });
    $('#id_password1').focusout(function () {
        if($(this).val().length < 6) {
            $('#password1Error').css({'border': ''});
            $('#password1Error').css('color', 'red');
            $('#password1Error').html('Your password cannot be fewer than 6 characters');
        }
        else {
            $('#password1Error').css({'border': ''});
            $('#password1Error').css('color', '');
            $('#password1Error').html('');
        }
    });
    $('#id_password2').focusout(function () {
        if($(this).val() != $('#id_password1').val()) {
            $('#password2Error').css({'border': ''});
            $('#password2Error').css('color', 'red');
            $('#password2Error').html('Both passwords should match');
        }
        else {
            $('#password2Error').css({'border': ''});
            $('#password2Error').css('color', '');
            $('#password2Error').html('');
        }
    });
});