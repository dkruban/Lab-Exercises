// Extended Euclidean Algorithm with steps
function extendedEuclid(a, b) {
    let steps = "";
    let old_r = a, r = b;
    let old_s = 1, s = 0;
    let old_t = 0, t = 1;

    steps += `Initial values:\n`;
    steps += `r = ${r}, old_r = ${old_r}\n`;
    steps += `s = ${s}, old_s = ${old_s}\n`;
    steps += `t = ${t}, old_t = ${old_t}\n\n`;

    while (r !== 0) {
        let q = Math.floor(old_r / r);
        steps += `q = Math.floor(${old_r} / ${r}) = ${q}\n`;

        let temp_r = r;
        r = old_r - q * r;
        old_r = temp_r;

        let temp_s = s;
        s = old_s - q * s;
        old_s = temp_s;

        let temp_t = t;
        t = old_t - q * t;
        old_t = temp_t;

        steps += `After this step:\n`;
        steps += `r = ${r}, old_r = ${old_r}\n`;
        steps += `s = ${s}, old_s = ${old_s}\n`;
        steps += `t = ${t}, old_t = ${old_t}\n\n`;
    }

    return { gcd: old_r, x: old_s, y: old_t, steps: steps };
}

// UI function
function computeEEA() {
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);

    if (isNaN(a) || isNaN(b)) {
        alert("Enter valid numbers");
        return;
    }

    let result = extendedEuclid(a, b);

    document.getElementById("steps").value = result.steps;
    document.getElementById("result").value =
        `GCD = ${result.gcd}, x = ${result.x}, y = ${result.y}\nCheck: ${a}*${result.x} + ${b}*${result.y} = ${result.gcd}`;
}
