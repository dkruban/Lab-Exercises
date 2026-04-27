// Fast Modular Exponentiation
function modExp(base, exp, mod) {
    base = parseInt(base);
    exp = parseInt(exp);
    mod = parseInt(mod);

    let result = 1;
    base = base % mod;

    while (exp > 0n) {
        if (exp % 2 === 1) {
            result = (result * base) % mod;
        }
        exp = exp / 2;
        base = (base * base) % mod;
    }
    return result;
}

// Fermat Theorem Checker
function fermatTheorem(a, p) {
    if (p <= 1) return "p must be prime and > 1";

    const result = modExp(a, p - 1, p);

    if (result === 1n) {
        return `Verified: ${a}^(p-1) ≡ 1 (mod ${p})`;
    } else {
        return `Not verified. Result = ${result}`;
    }
}

f = fermatTheorem(3,7)
console.log(f)