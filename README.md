# xiecheng

### 功能
爬取携程机票信息，设置一个心理阈值，如果机票价格最低价低于这个阈值，则发送邮件通知。  
例如：
```python
start_station = '成都'
arrive_station = '上海'
wish_date_list = ['2018-03-12', '2018-03-13']
```
我希望监听2018-03-12，2018-03-13从成都到上海的机票价格，我期望的机票最低价为
```python
wish_down_threshold = 1000
```
则当机票最低价低于1000，`qq_email_address`发送邮件给`inform_email_address`。    
每一小时刷新一次，机票信息变化频率很低，不需要过快，可以自己手动设置，但是不建议太快。
### Requirements
```
PyExecJS
requests
```
### 注意事项
携程爬取机票时，如果直接get这样的url:
```
http://flights.ctrip.com/booking/CTU-SHA-day-1.html?DDate1=2018-03-13
```
并不会得到机票信息，但是如果你get这个url:
```
http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=CTU&ACity1=SHA&SearchType=S&DDate1=2018-03-13&IsNearAirportRecommond=0&LogToken=980342546776496ebab5631bf4a30f85&rk=7.201366593865179225816&CK=E2CB39252256436934ECE11B8F9951F9&r=0.53186630183055359500419
```
在浏览器中抓包，可以获得返回的数据，在`return_data.json`中。 
但是当你直接get第二个url，返回的数据并不完全甚至为空。
因此需要执行一段js代码。   
最简单的方式是使用`phantomjs`，这里使用pyexecjs执行js代码。
### 如何使用
需要配置config.py，具体如何修改请看注释
* 发送邮件  
发送邮件使用了qq邮箱，请打开qq邮箱->设置->账户->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务->开启服务->温馨提示，生成授权码     
如果你要使用自定义邮箱，请重写`sendEmail`函数。
