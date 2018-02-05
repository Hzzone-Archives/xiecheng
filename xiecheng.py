# -*- coding:utf-8 -*-
import requests
import re
import execjs
import json
import config
import smtplib
from email.mime.text import MIMEText
import time

import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("xiecheng.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

logger.info('''
    start station: %s
    arrive station: %s
    wish date: %s
    qq email address: %s
    inform email address: %s
    refreshing interval: %ss
    ''' % (config.start_station, config.arrive_station, " ".join(config.wish_date_list), 
        config.qq_email_address, config.inform_email_address, config.interval))

'''
subject: 主题
msg: 内容
_to: 发送邮件地址
'''
def sendEmail(subject, msg, _to):

    msg = MIMEText(msg)
    msg["Subject"] = subject
    msg["From"]    = config.qq_email_address
    msg["To"]      = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(config.qq_email_address, config.qq_email_code)
        s.sendmail(config.qq_email_address, _to, msg.as_string())
        s.quit()
    except smtplib.SMTPException as e:
        logger.error("Falied,%s"%e)

headers1={
    "Host":"flights.ctrip.com",
    "Origin":"http://www.ctrip.com",
    "Upgrade-Insecure-Requests":"1",
    "Proxy-Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}

headers2={
  "Accept":"*/*",
  "Accept-Encoding":"gzip, deflate, sdch",
  "Accept-Language":"zh-CN,zh;q=0.8",
  "Cache-Control":"no-cache",
  "Connection":"keep-alive",
  "Host":"flights.ctrip.com",
  "Referer":"",
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
  "Pragma":"no-cache",
  "Connection":"keep-alive"
}

#封装函数
def getData(city1,city2,date):
    #获取加密js
    session=requests.Session()
    indexUrl="http://flights.ctrip.com/booking/"+city1+"-"+city2+"-day-1.html?DDate1="+date
    req1=session.get(indexUrl,headers=headers1,verify=False)
    try:
        cookie=req1.headers["Set-Cookie"]
    except:
        # print(str(count1)+" "+city1+"-"+city2+":"+"获取cookie失败\n")
        logger.error(str(count1)+" "+city1+"-"+city2+":"+"获取cookie失败\n")
    return_data=req1.text
    js_match=re.findall('var fn=(.*?)var jsonCallback',return_data)
    js=''
    indexUrl=''
    para=''
    if(js_match):
        indexJs=js_match[0]
        js += '''r = n.replace(/^[\s\xA0]+|[\s\xA0]+$/g, "");
        c = t.split(".")[1];t = "0." + c.substring(1, c.length - 1);u = r.split("&");
        h = r.indexOf("rk=") >= 0 || r.indexOf("rt=") >= 0 ? u.splice(u.length - 2, 1)[0] : u.pop();
        u.push("CK=");h = h.split("=")[1];var fn='''+indexJs
        js=js.replace('if(!window.location.href){return;}','')
        js=js.replace('t.open(\'GET\', ','lastUrl= (')
        js=js.replace(', !0);',');')
        js=js.replace('t.send(null);','')
        js="function ajaxRequest(n,t){"+js
        url_match=re.findall('var url = "(.*?)";', return_data)
        # print(url_match)
        if(url_match):
            indexUrl="http:"+url_match[0]
        else:
            logger.error("未匹配到对应url信息")
        para_match=re.findall('ajaxRequest\(url(.*?)\'\);',return_data)
        if(para_match):
            para=para_match[0]
        else:
            logger.error("未匹配到对应url信息")
        js="function getUrl(){var i='';var lastUrl='';var url='"+indexUrl+"';"+js+"ajaxRequest(url"+para+"');return lastUrl;}"
        
        #执行加密js得到加密后的url
        ctx=execjs.compile(js)
        dataUrl=(ctx.call("getUrl"))

        headers2["Referer"] = indexUrl
        cookie={
            "Cookie":cookie
        }
        req2=session.get(dataUrl,headers=headers2,verify=False,cookies=cookie)
        req2.encoding="gb2312"

        #从获取的数据中提取有用数据
        try:
            info=json.loads(req2.text)
            fis = info['fis']
            #print(info)
            info_list = []
            for i in fis:
                slist = []
                slist.append(i['fn'])
                slist.append(str(i['dcn']))
                slist.append(str(i['dpbn']))
                slist.append(str(i['acn']))
                slist.append(str(i['apbn']))
                slist.append(str(i['dt']))
                slist.append(str(i['at']))
                slist.append(int(i['lp']))
                info_list.append(slist)
            return sorted(info_list, key=lambda x:x[-1])
        except:
            logger.error("获取数据失败")
    else:
        logger.error("未匹配到对应js代码")

def main():
	#获取所有城市
    with open("city_info.json","r") as f:
        all_city=json.loads(f.read())

    try:
        city1_code = all_city[config.start_station]
        city2_code = all_city[config.arrive_station]
    except:
        logger.error("没有该城市编码")
    while True:
        for wish_date in config.wish_date_list:
            info_list = getData(city1_code, city2_code, wish_date)
            # print(info_list)
            try:
                loweset_plane = info_list[0]
            except:
                logger.error('爬取到的数据为空')
                exit(1)
            logger.info('<%s->%s %s> current loweset price: %s' % (config.start_station, config.arrive_station, wish_date, loweset_plane[-1]))
            if loweset_plane[-1] <= config.wish_down_threshold:
                send_content = "航班 %s\n<%s %s> 到 <%s %s>\n出发时间: %s\n到达时间: %s\n现价: %s\n" % (
                        loweset_plane[0], loweset_plane[1], loweset_plane[2], loweset_plane[3], loweset_plane[4],
                        loweset_plane[5], loweset_plane[6], loweset_plane[7])
                sendEmail('携程机票心愿最低价达成', send_content, config.inform_email_address)
                logger.info(send_content)
            time.sleep(10)
        time.sleep(config.interval)

if __name__ == '__main__':
    main()
