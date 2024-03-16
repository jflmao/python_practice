window = global;
window.location = {
    href : "https://fanyi.youdao.com/index.html#/"
}
navigator={};
document={};
document.createElement = function (a) {
    return {
        href:"",
        pathname:"",
        setAttribute:function (h, r) {
            this[h] = r
        }
    };
}
document.body =  {
    appendChild:function (d) {
        return {}
    }
}
const {_jflmao} = require("./webpack");
const decodeKey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl";
const decodeIv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4";

function get_decrypt(args) {
    return _jflmao("8139").a.decodeData(args, decodeKey, decodeIv);
}

console.log(get_decrypt());