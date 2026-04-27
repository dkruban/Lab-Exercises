let globalIV;
let globalCipher;

async function getKey(password) {
    const enc = new TextEncoder();

    const keyMaterial = await crypto.subtle.importKey(
        "raw",
        enc.encode(password),
        "PBKDF2",
        false,
        ["deriveKey"]
    );

    return crypto.subtle.deriveKey(
        {
            name: "PBKDF2",
            salt: enc.encode("salt"),
            iterations: 100000,
            hash: "SHA-256",
        },
        keyMaterial,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
    );
}

async function encryptAES() {
    const text = document.getElementById("text").value;
    const password = document.getElementById("password").value;

    const enc = new TextEncoder();
    const key = await getKey(password);

    globalIV = crypto.getRandomValues(new Uint8Array(12));

    const encrypted = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv: globalIV },
        key,
        enc.encode(text)
    );

    globalCipher = new Uint8Array(encrypted);

    const result = btoa(String.fromCharCode(...globalCipher));

    document.getElementById("aesOutput").innerText =
        "Encrypted (Base64): " + result;
}

async function decryptAES() {
    const password = document.getElementById("password").value;

    if (!globalCipher || !globalIV) {
        document.getElementById("aesOutput").innerText =
            "No encrypted data available!";
        return;
    }

    const key = await getKey(password);

    try {
        const decrypted = await crypto.subtle.decrypt(
            { name: "AES-GCM", iv: globalIV },
            key,
            globalCipher
        );

        const dec = new TextDecoder();
        const result = dec.decode(decrypted);

        document.getElementById("aesOutput").innerText =
            "Decrypted Text: " + result;
    } catch (err) {
        document.getElementById("aesOutput").innerText =
            "Decryption failed! Wrong password?";
    }
}