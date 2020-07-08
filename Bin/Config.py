# 配置账号信息
ip = '61.163.243.173'
port = '7171'
username = 'ES'  # 用户名
password = '123456'  # 密码
auth_code = ''  # 授权码，默认为空

# 配置订阅品种
contracts = ['SGX Z CN MAIN', 'COMEX F GC 2010']

# 配置发布方式

publish = 1  # 0是打印;1是redis;2是socket;3是file

# 配置发布信息
# 如果publish==1,需要配置redis
redis = {'host': 'localhost',
         'port': 6379,
         'db': 0,
         'password': None
         }
# 如果publish==2,需要配置socket
socket = {'ip': '127.0.0.1',
          'port': 8080}

# 每日休息的时间(北京时间)，每日的凌晨5点到6点
everyday = [['05:00', '06:00']]
# 每周休息的时间(北京时间)，每周的周六5点到下周一6点
everyweek = [[[6, '05:00'], [1, '06:00']]]
# 特定时间(北京时间)，元旦的凌晨5点到次日6点
holiday = [['2021-01-01 05:00', '2021-01-02 06:00']]  # 元旦假期
