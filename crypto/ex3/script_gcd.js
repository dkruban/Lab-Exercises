function gcd(a, b, out){
    out += `a = ${a}  b = ${b}`;
    document.getElementById("result").value += out;
    return b === 0 ? a : gcd(b, a % b);
}

function euclidean(){
    let a = parseInt(document.getElementById("a").value);
    let b = parseInt(document.getElementById("b").value);
    let out = "";
    let res = gcd(a,b,out);
    document.getElementById("result").value = res;
    //window.alert("GCD of " + a + " + " + b + ": " + res);
}
