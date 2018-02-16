'''
时间间隔，默认一小时
'''
interval = 3600

'''
期望的最便宜机票
'''
wish_down_threshold = 700

'''
通知邮箱
'''
inform_email_address = 'None'
inform_phonenumber = 'XXX'



'''
机票设置
'''
# start_station = '成都'
# arrive_station = '上海'
planes = [["成都", "上海"], ["重庆", "上海"]]
wish_date_list = ['2018-02-25', '2018-02-26', '2018-02-27']

'''
配置qq邮箱，地址和授权码
打开qq邮箱->设置->账户->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务->开启服务->温馨提示，生成授权码
'''
qq_email_address = 'None'
qq_email_code = '*****'