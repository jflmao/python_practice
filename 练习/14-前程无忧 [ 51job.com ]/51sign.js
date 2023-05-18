function get_sign(val){
    const CryptoJS = require('crypto-js');
    let cupid_sign_key = 'abfc8f9dcf8c3f3d8aa294ac5f2cf2cc7767e5592590f39c3f503271dd68562b';
    return CryptoJS.HmacSHA256(val, cupid_sign_key).toString();
}
function get_uuid(){
    let e = (new Date).getTime().toString();
    return e + parseInt(1e7 * Math.random().toString().slice(0, 9)).toString();
}