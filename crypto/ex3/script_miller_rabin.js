function modPower(base, exp, mod) {
    let result = 1n;
    base = base % mod;

    while (exp > 0n) {
        if (exp % 2n === 1n)
            result = (result * base) % mod;

        exp = exp / 2n;
        base = (base * base) % mod;
    }
    return result;
}

function isPrimeWithSteps(n, k) {
    let steps = "";
    n = BigInt(n);

    if (n <= 1n) return { prime: false, steps: "n ≤ 1 → Not Prime" };
    if (n <= 3n) return { prime: true, steps: "n ≤ 3 → Prime" };
    if (n % 2n === 0n) return { prime: false, steps: "Even number → Composite" };

    // Decompose n-1
    let d = n - 1n;
    let r = 0n;

    while (d % 2n === 0n) {
        d /= 2n;
        r++;
    }

    steps += `n − 1 = ${n - 1n} = 2^${r} × ${d}\n\n`;

    for (let i = 1; i <= k; i++) {
        steps += `Iteration ${i}:\n`;

        let a = 2n + BigInt(Math.floor(Math.random() * Number(n - 4n)));
        steps += `Random base a = ${a}\n`;

        let x = modPower(a, d, n);
        steps += `x = a^d mod n = ${x}\n`;

        if (x === 1n || x === n - 1n) {
            steps += `x = 1 or n−1 → Pass\n\n`;
            continue;
        }

        let composite = true;

        for (let j = 1n; j < r; j++) {
            x = (x * x) % n;
            steps += `x² mod n = ${x}\n`;

            if (x === n - 1n) {
                steps += `x = n−1 → Pass\n\n`;
                composite = false;
                break;
            }
        }

        if (composite) {
            steps += `No condition satisfied → Composite\n`;
            return { prime: false, steps };
        }
    }

    steps += `All iterations passed → Probably Prime\n`;
    return { prime: true, steps };
}

function checkPrime() {
    let num = document.getElementById("number").value;
    let k = parseInt(document.getElementById("iterations").value);

    if (num === "") {
        alert("Enter a number");
        return;
    }

    let result = isPrimeWithSteps(num, k);
    document.getElementById("result").value = result.steps;
}
