function checkIncorrectSalary(minSalary, maxSalary) {
    if(minSalary > maxSalary) {
        return true;
    }
    return false;
}

$("#id_salary_min").focusout(function (e) {
    var min = parseInt($(this).val());
    var max = parseInt($("#id_salary_max").val());
    
    if(checkIncorrectSalary(min, max)) {
        e.preventDefault();
        $("#maxError").css('color', 'red');
        $("#minError").css('color', 'red').html("The minimum salary cannot be higher than the maximum ");
    } else {
        $("#maxError").css('color', '')
        $("#minError").css('color', '').html("");
    }
});
$("#id_salary_max").focusout(function (e) {
    var min = parseInt($("#id_salary_min").val());
    var max = parseInt($(this).val());
    
    if(checkIncorrectSalary(min, max)) {
        e.preventDefault();
        $("#maxError").css('color', 'red')
        $("#minError").css('color', 'red').html("The minimum salary cannot be higher than the maximum ");
    } else {
        $("#maxError").css('color', '')
        $("#minError").css('color', '').html("");
    }
});

$("#createJobBody").submit(function (e) {
    var min = parseInt($("#id_salary_min").val());
    var max = parseInt($("#id_salary_max").val());

    if(checkIncorrectSalary(min, max)) {
        alert('There are mistakes in the form');
        e.preventDefault();
    }
    else {
        console.log("Success!");
        e.preventDefault();
    }
});

$("#editJobBody").submit(function (e) {
    var min = parseInt($("#id_salary_min").val());
    var max = parseInt($("#id_salary_max").val());

    if(checkIncorrectSalary(min, max)) {
        alert('There are mistakes in the form');
        e.preventDefault();
    }
    else {
        console.log("Success!");
        e.preventDefault();
    }
});