function validatePhone() {
    const field = document.getElementById("num");
    if(field.value.length == 0)
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