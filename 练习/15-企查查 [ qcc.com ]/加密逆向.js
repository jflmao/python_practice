const CryptoJS = require('crypto-js');

const dict_str = {
    "n": 20, "codes": {
        "0": "W",
        "1": "l",
        "2": "k",
        "3": "B",
        "4": "Q",
        "5": "g",
        "6": "f",
        "7": "i",
        "8": "i",
        "9": "r",
        "10": "v",
        "11": "6",
        "12": "A",
        "13": "K",
        "14": "N",
        "15": "k",
        "16": "4",
        "17": "L",
        "18": "1",
        "19": "8"
    }
}

function r() {
    for (var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase(), t = e + e, n = "", i = 0; i < t.length; ++i) {
        var a = t[i].charCodeAt() % dict_str.n;
        n += dict_str.codes[a]
    }
    return n
}

function key(t = "/", e) {
    e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
    t = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase();
    let n = JSON.stringify(e).toLowerCase();
    return CryptoJS.HmacSHA512(t + n, r(t)).toString().toLowerCase().substr(8, 20)
}

function value(n = "/", e , t = "") {
    e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
    t = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "";
    n = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase();
    let i = JSON.stringify(e).toLowerCase();
    return CryptoJS.HmacSHA512(n + "pathString" + i + t, r(n)).toString()
}
