"""
目标网址：https://image.baidu.com/

获取到动态接口里面的图片数据进行下载；下载页数3页图图
"""
import requests
import time

req = requests.session()
req.headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Pragma": "no-cache",
    "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1674020336709_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=python",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "^\\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\\^Windows^^"
}

req.cookies.update({
    "BDqhfp": "python^%^26^%^260-10-1undefined^%^26^%^260^%^26^%^261",
    "BAIDUID": "F788A3B9F6477D014A3C8C7724540312:FG=1",
    "BIDUPSID": "F788A3B9F6477D014A3C8C7724540312",
    "PSTM": "1473996812",
    "__yjs_duid": "1_27fe9d7e5c0dac497b9c9fbe1b75edab1624628739864",
    "BDSFRCVID": "G6POJeC62656sO7HRmREuloQ9L5mM4nTH6bHwtHdiGoiijJi8J0WEG0Phf8g0KuMsB3LogKKL2OTHmAF_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
    "H_BDCLCKID_SF": "tbPO_KIatKD3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDk9qfQcy4LdjG5N-xoIKmO7bDQdJ-5SDUDwDRrDeMDB3-Aq5fvy-grQLJTV2f8KMII40bKaQfbQ0-cPqP-jW5Tubhbxbn7JOpvsDxnxy-uFQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ht6IetbKD_D0yJKvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbp0C0MnkbfJBDGDttJJ9J2bNWxoNbRRoVDTsjtcYj-C7yajaBnbJWIn0Kb7V2RckjDn_DhJpQT8rMMDOK5Oibmje5DO1ab3vOp44XpO1hf_zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDe_K8hJUK",
    "BDSFRCVID_BFESS": "G6POJeC62656sO7HRmREuloQ9L5mM4nTH6bHwtHdiGoiijJi8J0WEG0Phf8g0KuMsB3LogKKL2OTHmAF_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
    "H_BDCLCKID_SF_BFESS": "tbPO_KIatKD3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDk9qfQcy4LdjG5N-xoIKmO7bDQdJ-5SDUDwDRrDeMDB3-Aq5fvy-grQLJTV2f8KMII40bKaQfbQ0-cPqP-jW5Tubhbxbn7JOpvsDxnxy-uFQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ht6IetbKD_D0yJKvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbp0C0MnkbfJBDGDttJJ9J2bNWxoNbRRoVDTsjtcYj-C7yajaBnbJWIn0Kb7V2RckjDn_DhJpQT8rMMDOK5Oibmje5DO1ab3vOp44XpO1hf_zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDe_K8hJUK",
    "BAIDUID_BFESS": "F788A3B9F6477D014A3C8C7724540312:FG=1",
    "BAIDU_WISE_UID": "wapp_1672822934332_447",
    "RT": "^\\^z=1&dm=baidu.com&si=cxyzjzzwje&ss=lcrrlfqe&sl=2&tt=3b8&bcn=https^%^3A^%^2F^%^2Ffclog.baidu.com^%^2Flog^%^2Fweirwood^%^3Ftype^%^3Dperf&ld=3sg&ul=9iq&hd=9ji^^",
    "ZFY": "ylVpkdkqU:BmDvYJzrvIbqXnyfgWKc4qAIzurj68svj8:C",
    "MCITY": "-316^%^3A",
    "BDRCVFR^[X_XKQks0S63^]": "mk3SLVN4HKm",
    "image_bff_sam": "1",
    "firstShowTip": "1",
    "H_PS_PSSID": "36547_37551_37517_38053_36920_37990_37932_38041_26350_37881",
    "BA_HECTOR": "2g248k208g848h01a425almu1hsesse1l",
    "BDRCVFR^[feWj1Vr5u3D^]": "I67x6TjHwwYf0",
    "delPer": "0",
    "PSINO": "5",
    "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    "indexPageSugList": "^%^5B^%^22python^%^22^%^5D",
    "cleanHistoryStatus": "0",
    "BDRCVFR^[dG2JNJb_ajR^]": "mk3SLVN4HKm",
    "BDUSS": "nMxbWl4NW1UbXFDOUFaNjc3dTRmc1JKcTBrNU5rZnNCWlBWNGRTYnJGSXlELTlqSVFBQUFBJCQAAAAAAAAAAAEAAADJLM2dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADKCx2MygsdjZ",
    "BDUSS_BFESS": "nMxbWl4NW1UbXFDOUFaNjc3dTRmc1JKcTBrNU5rZnNCWlBWNGRTYnJGSXlELTlqSVFBQUFBJCQAAAAAAAAAAAEAAADJLM2dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADKCx2MygsdjZ",
    "BDRCVFR^[-pGxjrCMryR^]": "mk3SLVN4HKm",
    "userFrom": "null",
    "ab_sr": "1.0.1_YjJjZDY1MDBkYTlmYmIzMjdiM2ZjZjUxNTgzYWE2OTZkNjgzOGVlODcwMGNhZTZkYTU1ODU5MjQ3YzE2MWQ0YTk0Y2FkNTI5MDAzNDQ5NDI2YzUxMjk5YzE3OWQxNzI3YjI1MzE4OTMwYTY3ODA2MDBjNjc0MzNiZTdlZmVjNzFlYzZhZTExYWRjMDU4NjdiYzU3NGMwZTlmMDQ4YzgwYQ=="
})


def get_baidu_image_list(_word: str, _page: int) -> tuple:
    """
        在百度图片中获取指定搜索关键字的图片列表，每页默认获取30个

    :param _word: 搜索关键词
    :param _page: 获取第几页
    :return: 返回获取的图片列表，类型为元组
    """
    _image_url_list = []
    pn = _page * 30  # 每次请求的起始数
    url = "https://image.baidu.com/search/acjson"
    # 请求参数
    params = {
        "tn": "resultjson_com",
        "logid": "7189006849677576979",
        "ipn": "rj",
        "ct": "201326592",
        "is": "",
        "fp": "result",
        "fr": "",
        "word": _word,
        "queryWord": _word,
        "cl": "2",
        "lm": "-1",
        "ie": "utf-8",
        "oe": "utf-8",
        "adpicid": "",
        "st": "-1",
        "z": "",
        "ic": "0",
        "hd": "",
        "latest": "",
        "copyright": "",
        "s": "",
        "se": "",
        "tab": "",
        "width": "",
        "height": "",
        "face": "0",
        "istype": "2",
        "qc": "",
        "nc": "1",
        "expermode": "",
        "nojc": "",
        "isAsync": "",
        "pn": str(pn),
        "rn": "30",
        "gsm": "{:x}".format(pn),  # 请求起始数的十六进制
        f"{round(time.time() * 1000)}": ""  # 时间戳
    }
    response = req.get(url, params=params).json()['data']
    for _item in response:
        if _item:
            _image_url_list.append(_item['thumbURL'])

    return tuple(_image_url_list)


def download_and_save_image(_image_url_list: list) -> None:
    """
        下载并保存图片

    :param _image_url_list: 图片地址列表
    :return: 返回 None
    """
    for _url in _image_url_list:
        res = req.get(_url)
        with open(f'{round(time.time() * 1000)}.jpg', 'wb') as f:
            f.write(res.content)


def main():
    word = 'python'  # 搜索关键词
    page = 3  # 获取的页数
    image_ulr_list = []
    # 获取图片列表
    for item in range(page):
        image_tuple = get_baidu_image_list(word, item)
        image_ulr_list += list(image_tuple)
    # 下载并保存图片
    download_and_save_image(image_ulr_list)


if __name__ == '__main__':
    main()
