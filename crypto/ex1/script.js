function modInverse(a, m) {
    for (let x = 1; x < m; x++) {
        if ((a * x) % m === 1) return x;
    }
    return null;
}

function affineEncrypt(text, a, b) {
    return text.toUpperCase().replace(/[A-Z]/g, char => {
        let x = char.charCodeAt(0) - 65;
        return String.fromCharCode(((a * x + b) % 26) + 65);
    });
}

function affineDecrypt(text, a, b) {
    let a_inv = modInverse(a, 26);
    if (a_inv === null) {
        alert("Invalid 'a' value!");
        return "";
    }
    return text.toUpperCase().replace(/[A-Z]/g, char => {
        let y = char.charCodeAt(0) - 65;
        return String.fromCharCode((a_inv * (y - b + 26) % 26) + 65);
    });
}


function vigenereEncrypt(text, key) {
    key = key.toUpperCase();
    let j = 0;
    return text.toUpperCase().replace(/[A-Z]/g, char => {
        let p = char.charCodeAt(0) - 65;
        let k = key[j++ % key.length].charCodeAt(0) - 65;
        return String.fromCharCode((p + k) % 26 + 65);
    });
}

function vigenereDecrypt(text, key) {
    key = key.toUpperCase();
    let j = 0;
    return text.toUpperCase().replace(/[A-Z]/g, char => {
        let c = char.charCodeAt(0) - 65;
        let k = key[j++ % key.length].charCodeAt(0) - 65;
        return String.fromCharCode((c - k + 26) % 26 + 65);
    });
}


function encrypt() {
    let text = document.getElementById("text").value;
    let cipher = document.getElementById("cipher").value;

    if (cipher === "affine") {
        let a = parseInt(document.getElementById("a").value);
        let b = parseInt(document.getElementById("b").value);
        document.getElementById("result").value = affineEncrypt(text, a, b);
    } else {
        let key = document.getElementById("key").value;
        document.getElementById("result").value = vigenereEncrypt(text, key);
    }
}

function decrypt() {
    let text = document.getElementById("text").value;
    let cipher = document.getElementById("cipher").value;

    if (cipher === "affine") {
        let a = parseInt(document.getElementById("a").value);
        let b = parseInt(document.getElementById("b").value);
        document.getElementById("result").value = affineDecrypt(text, a, b);
    } else {
        let key = document.getElementById("key").value;
        document.getElementById("result").value = vigenereDecrypt(text, key);
    }
}
