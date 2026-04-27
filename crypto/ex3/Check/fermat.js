function modPow(base, exp, mod) {
    let result = 1;
    base = base % mod;

    while (exp > 0) {
        if (exp % 2 === 1)
            result = (result * base) % mod;

        base = (base * base) % mod;
        exp = Math.floor(exp / 2);
    }
    return result;
}

function calculateFermat() {
    let a = parseInt(document.getElementById("a").value);
    let p = parseInt(document.getElementById("p").value);

    if (isNaN(a) || isNaN(p)) {
        document.getElementById("result").innerText = "Please enter valid numbers";
        return;
    }

    let result = modPow(a, p - 1, p);

    document.getElementById("result").innerText =
        `Result: ${a}^(${p-1}) mod ${p} = ${result}`;
}