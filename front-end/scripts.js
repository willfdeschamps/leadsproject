function mascara(o, f) {
    v_obj = o
    v_fun = f
    setTimeout("execmascara()", 1)
}
function execmascara() {
    v_obj.value = v_fun(v_obj.value)
}
function mtel(v) {
    v = v.replace(/\D/g, "");             //Remove tudo o que não é dígito
    v = v.replace(/^(\d{2})(\d)/g, "($1) $2"); //Coloca parênteses em volta dos dois primeiros dígitos
    v = v.replace(/(\d)(\d{4})$/, "$1-$2");    //Coloca hífen entre o quarto e o quinto dígitos
    return v;
}
function id(el) {
    return document.getElementById(el);
}
window.onload = function () {
    id('telefone').onkeyup = function () {
        mascara(this, mtel);
    }
}
function validatePhone(phone) {
    if (phone == "") {
        alert("O telefone é obrigatório");
        return false;
    }

    if(phone.length != 14 && phone.length != 15) {
        alert("Telefone em formato inválido")
        return false
    }
    return true
}

function validateEmail(email) {
    if (email == "") {
        alert("O e-mail é obrigatório");
        return false;
    }

    if (!email.includes('.com') || !email.includes('@') || email.indexOf('@') + 1 >= email.indexOf('.com')) {
        alert("E-mail em formato inválido")
        return false
    }
    return true

}

function validateForm() {
    var email = document.forms[0]["email"].value;
    var phone = document.forms[0]["telefone"].value;

    return validateEmail(email) && validatePhone(phone)
}