function isNumber(input) {
      var intRegex = /^\d+$/;
      var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
      return intRegex.test(input) || floatRegex.test(input);
}

function containsNumber(input) {
    return /\d/.test(input);
}

function testEmailValidity(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return !emailReg.test(email);
}

function verifyGradDate(gradDate, todayDate) {
    return (gradDate < todayDate);
}

$(document).ready(function () {
      $('#id_first_name').change(function () {
        var firstName = $(this).val();
        if(isNumber(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('You cannot enter a number').css('color', 'red');
        }
        else if(containsNumber(firstName)) {
            $('#id_first_name').css('border', '1px solid red');
            $('#firstNameError').html('Your string contains numbers').css('color', 'red');
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
        else if(containsNumber(lastName)) {
            $('#id_last_name').css('border', '1px solid red');
            $('#lastNameError').html('Your string contains numbers').css('color', 'red');
        }
        else {
            $('#id_last_name').css('border', '');
            $('#lastNameError').html('').css('color', '');
        }
    });

    $('#id_personal_email').focusout(function () {
        var email = $(this).val();
        if(testEmailValidity(email)) {
            $(this).css('border', '1px solid red');
            $('#personalEmailError').html('Please enter a valid email address').css('color', 'red');
        }
        else {
            $(this).css('border', '');
            $('#personalEmailError').html('').css('color', '');
        }
    });

    $('#id_expected_graduation_date').focusout(function () {
        var expDate = $(this).val();
        var today = new Date();
        var convDate = new Date(expDate);
        if(verifyGradDate(convDate, today)) {
            $(this).css('border', '1px solid red');
            $('#gradError').html('Expected graduation date cannot be in the past').css('color', 'red');
        }
        else {
            console.log("Success");
            $(this).css('border', '');
            $('#gradError').html('').css('color', '');
        }
    });
});


$("#editAlumniForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();

    if(isNumber(firstname) || isNumber(lastname) || containsNumber(firstname) || containsNumber(lastname) || testEmailValidity(email)) {
        e.preventDefault();
        alert("There are errors in the form");
    }
    else {
        console.log("Success!");
    }
});

$("#editStudentForm").submit(function (e) {
    var firstname = $("#id_first_name").val();
    var lastname = $("#id_last_name").val();
    var email = $("#id_personal_email").val();
    var expDate = $('#id_expected_graduation_date').val();
    var today = new Date();
    var convDate = new Date(expDate);

    if(isNumber(firstname) || isNumber(lastname) || containsNumber(firstname) || containsNumber(lastname) || testEmailValidity(email) || verifyGradDate(convDate, today)) {
        e.preventDefault();
        alert("There are errors in the form");
    }
    else {
        console.log("Success!");
    }
});