function generateKey(text, key) {
    key = key.toUpperCase();
    let newKey = "";
    let j = 0;

    for (let i = 0; i < text.length; i++) {
        if (text[i] >= 'A' && text[i] <= 'Z') {
            newKey += key[j % key.length];
            j++;
        } else {
            newKey += text[i];
        }
    }
    return newKey;
}

function encrypt() {
    let text = document.getElementById("text").value.toUpperCase();
    let key = document.getElementById("key").value.toUpperCase();

    let genKey = generateKey(text, key);
    let result = "";

    for (let i = 0; i < text.length; i++) {
        if (text[i] >= 'A' && text[i] <= 'Z') {
            let x = (text.charCodeAt(i) - 65 + genKey.charCodeAt(i) - 65) % 26;
            result += String.fromCharCode(x + 65);
        } else {
            result += text[i];
        }
    }
    document.getElementById("result").value = result;
}

function decrypt() {
    let text = document.getElementById("text").value.toUpperCase();
    let key = document.getElementById("key").value.toUpperCase();

    let genKey = generateKey(text, key);
    let result = "";

    for (let i = 0; i < text.length; i++) {
        if (text[i] >= 'A' && text[i] <= 'Z') {
            let x = (text.charCodeAt(i) - genKey.charCodeAt(i) + 26) % 26;
            result += String.fromCharCode(x + 65);
        } else {
            result += text[i];
        }
    }
    document.getElementById("result").value = result;
}
