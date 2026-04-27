class PlayfairCipher {
    constructor(key) {
        this.matrix = [];
        this.generateKeyMatrix(key);
    }

    generateKeyMatrix(key) {
        key = key.toUpperCase().replace(/J/g, 'I');
        let used = new Array(26).fill(false);
        let letters = [];

        for (let c of key) {
            if (c >= 'A' && c <= 'Z' && !used[c.charCodeAt(0)-65]) {
                used[c.charCodeAt(0)-65] = true;
                letters.push(c);
            }
        }

        for (let c = 65; c <= 90; c++) {
            let ch = String.fromCharCode(c);
            if (ch === 'J') continue;
            if (!used[c-65]) {
                used[c-65] = true;
                letters.push(ch);
            }
        }

        for (let i = 0; i < 5; i++)
            this.matrix[i] = letters.slice(i*5, i*5+5);
    }

    prepareText(text) {
        text = text.toUpperCase().replace(/J/g, 'I').replace(/[^A-Z]/g, '');
        let out = '';
        for (let i = 0; i < text.length; i++) {
            out += text[i];
            if (i+1 < text.length && text[i] == text[i+1])
                out += 'X';
        }
        if (out.length % 2 != 0) out += 'X';
        return out;
    }

    findPos(c) {
        for (let i = 0; i < 5; i++)
            for (let j = 0; j < 5; j++)
                if (this.matrix[i][j] == c)
                    return [i,j];
    }

    encrypt(text) {
        text = this.prepareText(text);
        let res = '';
        for (let i = 0; i < text.length; i += 2) {
            let [r1,c1] = this.findPos(text[i]);
            let [r2,c2] = this.findPos(text[i+1]);

            if (r1 == r2) {
                res += this.matrix[r1][(c1+1)%5];
                res += this.matrix[r2][(c2+1)%5];
            } else if (c1 == c2) {
                res += this.matrix[(r1+1)%5][c1];
                res += this.matrix[(r2+1)%5][c2];
            } else {
                res += this.matrix[r1][c2];
                res += this.matrix[r2][c1];
            }
        }
        return res;
    }

    decrypt(text) {
        let res = '';
        for (let i = 0; i < text.length; i += 2) {
            let [r1,c1] = this.findPos(text[i]);
            let [r2,c2] = this.findPos(text[i+1]);

            if (r1 == r2) {
                res += this.matrix[r1][(c1+4)%5];
                res += this.matrix[r2][(c2+4)%5];
            } else if (c1 == c2) {
                res += this.matrix[(r1+4)%5][c1];
                res += this.matrix[(r2+4)%5][c2];
            } else {
                res += this.matrix[r1][c2];
                res += this.matrix[r2][c1];
            }
        }
        return res;
    }
}

function showMatrix(matrix) {
    let html = "<table>";
    for (let row of matrix) {
        html += "<tr>";
        for (let cell of row)
            html += `<td>${cell}</td>`;
        html += "</tr>";
    }
    html += "</table>";
    document.getElementById("matrix").innerHTML = html;
}

function encryptText() {
    let key = document.getElementById("key").value;
    let text = document.getElementById("text").value;
    let pf = new PlayfairCipher(key);
    document.getElementById("result").value = pf.encrypt(text);
    showMatrix(pf.matrix);
}

function decryptText() {
    let key = document.getElementById("key").value;
    let text = document.getElementById("text").value;
    let pf = new PlayfairCipher(key);
    document.getElementById("result").value = pf.decrypt(text);
    showMatrix(pf.matrix);
}
