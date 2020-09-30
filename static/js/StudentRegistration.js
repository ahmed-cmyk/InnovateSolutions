function isNumber(input) {
      var intRegex = /^\d+$/;
      var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
      return intRegex.test(input) || floatRegex.test(input);
}

function containsNumber(input) {
    return /\d/.test(input);
}

function checkString(input) {
    var stringRegex = /^[a-z]+$/i;
    return !stringRegex.test(input);
}

function checkFalseStudentEmail(student_email) {
    var studentEmailRegex = /[a-zA-Z0-9]+@student.murdoch.edu.au/;
    return !studentEmailRegex.test(student_email);
}

function checkFalseEmail(email) {
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

function  getTodayDate() {
    let today = new Date();
    var month = ''+(today.getMonth()+1);
    var day = '' + today.getFullYear();
    var year = today.getDate();
    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [day, month, year].join('-');
}

function checkFalseGradDate(date) {
    var dateString = date.toString();
    var parts = dateString.split("-");
    var day = parseInt(parts[2], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[0], 10);
    var dateToday = getTodayDate();
    console.log(date);
    console.log(dateToday);
    if (year < 2020 || year > 2030) {
        return true;
    }
    else if(date <= dateToday) {
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
    $('#id_first_name').focusout(function () {
        var firstName = $(this).val();
        if(isNumber(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('You cannot enter a number').css('color', 'red');
        }
        else if(containsNumber(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('Your string contains numbers').css('color', 'red');
        }
        else if(checkString(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('You can only enter characters').css('color', 'red');
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
        else if(containsNumber(lastName)) {
            $('#id_last_name').css('border', '1px solid red');
            $('#lastNameError').html('Your string contains numbers').css('color', 'red');
        }
        else if(checkString(lastName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('You can only enter characters').css('color', 'red');
        }
        else {
            $('#id_last_name').css('border', '');
            $('#lastNameError').html('').css('color', '');
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
        if(checkFalseStudentEmail($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#studentEmailError').html('Please enter a valid student email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#studentEmailError').html('').css('color', '');
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
    $('#id_expected_graduation_date').focusout(function () {
        if(checkFalseGradDate($(this).val())) {
            $(this).css('border', '1px solid red');
            $('#expGradDateError').html('Please enter a valid graduation date').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#expGradDateError').html('').css('color', '');
        }
    });
});

$("#studentForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();
    var student_email = $("#id_email").val();
    var personal_email = $("#id_personal_email").val();
    var dob = $('#id_date_of_birth').val();
    var gradDate = $('#id_expected_graduation_date').val();
    var password1 = $('#id_password1').val();
    var password2 = $('#id_password2').val();

    if(isNumber(firstname) || isNumber(lastname) || containsNumber(firstname) || containsNumber(lastname) || checkString(firstname) || checkString(lastname) || checkFalseEmail(student_email) || checkFalseStudentEmail(student_email) || checkFalseEmail(personal_email) || checkFalseDob(dob) || checkFalseGradDate(gradDate) || checkUnmatchedPasswords(password1, password2)) {
        alert('There are mistakes in the form');
        e.preventDefault();
    }
    else {
        console.log("Success!");
    }
});
