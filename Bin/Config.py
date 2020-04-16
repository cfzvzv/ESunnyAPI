# 配置账号信息
ip = '61.163.243.173'
port = '7171'
username = 'ES'  # 用户名
password = '123456'  # 密码
auth_code = ''  # 授权码，默认为空

# 配置订阅品种
contracts = ['COMEX F GC 2008', 'COMEX F GC 2006']

# 配置发布方式

publish = 0  # 0是打印;1是redis;2是socket;3是file

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
