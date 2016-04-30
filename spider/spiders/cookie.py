# encoding=utf-8
import json
import base64
import requests
user = {
    # 'name': 'mb55411@umac.mo',
    # 'password': 'bjyz330681740'
    'name': 'lyh472617147@sina.cn',
    'password': 'vae15213636384'
}
#利用新浪其他站点共用cookie 来避开验证码
def getCookie(weibo):
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    account = user['name']
    password = user['password']
    username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode('gbk')
    info = json.loads(jsonStr)
    if info['retcode'] == '0':
        print 'Success!(Account: %s)' % account
        cookie = session.cookies.get_dict()
        print cookie
        return cookie
    else:
        print "Failed! (account: %)" % user['account']
        return {}
        
        