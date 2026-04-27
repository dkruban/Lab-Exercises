function feistel(left, right, key) {
    let newLeft = right;
    let newRight = left ^ (right ^ key);
    return [newLeft, newRight];
}

function encrypt() {
    let data = parseInt(document.getElementById("inputData").value);
    let key = parseInt(document.getElementById("key").value);

    if (isNaN(data) || isNaN(key)) {
        document.getElementById("output").innerText = "Invalid input";
        return;
    }

    let left = (data >> 8) & 0xFF;
    let right = data & 0xFF;

    // Round 1
    [left, right] = feistel(left, right, key);

    // Round 2
    [left, right] = feistel(left, right, key);

    let cipher = (left << 8) | right;

    document.getElementById("output").innerText =
        "Encrypted Cipher: " + cipher;
}

function decrypt() {
    let data = parseInt(document.getElementById("inputData").value);
    let key = parseInt(document.getElementById("key").value);

    if (isNaN(data) || isNaN(key)) {
        document.getElementById("output").innerText = "Invalid input";
        return;
    }

    let left = (data >> 8) & 0xFF;
    let right = data & 0xFF;

    // Reverse order of rounds
    [left, right] = feistel(left, right, key);
    [left, right] = feistel(left, right, key);

    let plain = (left << 8) | right;

    document.getElementById("output").innerText =
        "Decrypted Plaintext: " + plain;
}