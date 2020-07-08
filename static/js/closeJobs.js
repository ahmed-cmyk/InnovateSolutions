function validate(form) {
    var rb = document.querySelector('input[name="isMurdochStd"]:checked').value;
    if (rb === 'no') {
        alert("Jobs can only be closed if filled by murdoch students. Please delete the job instead.");
        return false
    } else {
        return true
    }
}