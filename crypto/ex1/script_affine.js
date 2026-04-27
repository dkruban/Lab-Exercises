function gcd(a, b) {
    return b === 0 ? a : gcd(b, a % b);
}

function modInverse(a, m) {
    a = a % m;
    for (let x = 1; x < m; x++) {
        if ((a * x) % m === 1) return x;
    }
    return null;
}

function encrypt() {
    let text = document.getElementById("plainText").value.toUpperCase();
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);

    if (gcd(a, 26) !== 1) {
        alert("Key 'a' must be coprime with 26");
        return;
    }

    let result = "";
    for (let ch of text) {
        if (ch >= 'A' && ch <= 'Z') {
            let x = ch.charCodeAt(0) - 65;
            let enc = (a * x + b) % 26;
            result += String.fromCharCode(enc + 65);
        } else {
            result += ch;
        }
    }
    document.getElementById("result").value = result;
}

function decrypt() {
    let text = document.getElementById("plainText").value.toUpperCase();
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);

    let aInv = modInverse(a, 26);
    if (aInv === null) {
        alert("Inverse does not exist for given 'a'");
        return;
    }

    let result = "";
    for (let ch of text) {
        if (ch >= 'A' && ch <= 'Z') {
            let y = ch.charCodeAt(0) - 65;
            let dec = (aInv * (y - b + 26)) % 26;
            result += String.fromCharCode(dec + 65);
        } else {
            result += ch;
        }
    }
    document.getElementById("result").value = result;
}
