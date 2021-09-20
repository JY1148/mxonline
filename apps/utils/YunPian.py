import requests


def send_single_sms(apikey, code, mobile):
    #发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "您的验证码是{}。如非本人操作，请忽略本短信".format(code)

    res = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        "text": text
    })
    return res

if __name__ == "__main__":
    res = send_single_sms("apikey", "123456", "")
    import json
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("发送成功")
    else:
        print("发送失败：{}".format(msg))
    print(res.text)