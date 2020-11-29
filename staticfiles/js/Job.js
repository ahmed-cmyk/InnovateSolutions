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