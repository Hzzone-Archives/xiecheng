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

### 如何使用
需要配置config.py，具体如何修改请看注释
* 发送邮件
发送邮件使用了qq邮箱，请打开qq邮箱->设置->账户->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务->开启服务->温馨提示，生成授权码     
如果你要使用自定义邮箱，请重写`sendEmail`函数。
