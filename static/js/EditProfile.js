$(document).ready(function() {
    $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd'});
});

function disable_fields(status) {
    if (status) {
        document.getElementById('id_expected_graduation_date').disabled = true;
        document.getElementById('id_personal_email').disabled = true;
        document.getElementById('id_personal_email').required = false;
        document.getElementById('id_expected_graduation_date').required = false;
    } else {
        document.getElementById('id_expected_graduation_date').disabled = false;
        document.getElementById('id_personal_email').disabled = false;
        document.getElementById('id_personal_email').required = true;
        document.getElementById('id_expected_graduation_date').required = true;
    }
}

function validatePhone() {
            const field = document.getElementById("num");
            if(field.value.length === 0)
            {
                return true
            }
            else
            {
                if (!(/^\+?[0-9 -]+$/.test(field.value))) {
                    alert("Invalid phone number.");
                    field.focus();
                    field.select();
                    return false
                }
            }
            return true
        }