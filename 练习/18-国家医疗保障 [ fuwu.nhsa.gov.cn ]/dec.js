window = global;
const _jf = require('./webout');

function t(t) {
    return 0 > t ? NaN : 30 >= t ? 0 | Math.random() * (1 << t) : 53 >= t ? (0 | Math.random() * (1 << 30)) + (0 | Math.random() * (1 << t - 30)) * (1 << 30) : NaN
}

function e(t, e) {
    for (let n = t.toString(16), r = e - n.length, a = "0"; r > 0; r >>>= 1, a += a) 1 & r && (n = a + n);
    return n
}

n = ""
Zi = e(t(32), 8) + n + e(t(16), 4) + n + e(16384 | t(12), 4) + n + e(32768 | t(14), 4) + n + e(t(48), 12)
a = Zi.substring(0, 16)
i = "c=B|4Nl_NnGbjwY"
Tingyun = i += ";x=" + a
function getReqData(pageNum = 1, pageSize = 10) {
    t = {
        "headers": {
            "Contenttype": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "channel": "web"
        }, "data": {
            "addr": "",
            "regnCode": "110000",
            "medinsName": "",
            "medinsLvCode": "",
            "medinsTypeCode": "",
            "openElec": "",
            "pageNum": pageNum,
            "pageSize": pageSize,
            "queryDataSource": "es"
        }
    }
    let data = _jf('7d92').a(t)
    data.headers["x-tingyun"] = Tingyun
    data.headers['x-tif-paasid'] = ''
    return data
}

function getDecDate(pageNum=1,pageSize=10) {
    let reqData = getReqData(pageNum,pageSize);
    let request = require('sync-request');
    let res = request('POST', 'https://fuwu.nhsa.gov.cn/ebus/fuwu/api/nthl/api/CommQuery/queryFixedHospital', {
        body: reqData['data'],
        headers: reqData['headers']
    });
    let user = JSON.parse(res.getBody('utf8'));
    return _jf('7d92').b('SM4', user)
}

console.log(getDecDate(2,10));