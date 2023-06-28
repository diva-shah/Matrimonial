function calcAge() {

    var date = new Date(document.getElementById("bday").value);
    var today = new Date();
    var timeDiff = Math.abs(today.getTime() - date.getTime());
    var age1 = Math.ceil(timeDiff / (1000 * 3600 * 24)) / 365.2425;

    return age1;
}

function ageCheck() {
    var minAge = 18;
    var age = calcAge();
    if (age < minAge) {
        swal("Warning!", "You must be 18 years of age to Register!", "warning");
    }
}
