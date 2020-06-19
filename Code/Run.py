import socket
from time import sleep

from path import Path

import redis
from Include.Sarge import ES
from Include.Log import log
from Include.OlConfig import Config

CONFIG = Config().config['root']


class Publish:
    def __init__(self):
        self.way = CONFIG['publish']
        self.tool = None

    def __config_tool(self):
        self.way = CONFIG['publish']
        if self.way == 1:  # redis
            tool = self.__get_redis()

            def send(msg):
                chanel = ''.join(msg[:3])
                tool.publish(chanel, ','.join(msg))

        elif self.way == 2:  # socket
            tool = self.__get_socket()

            def send(msg):
                tool.send(bytes(','.join(msg), encoding='gbk'))

        elif self.way == 3:  # file
            def send(msg):
                name = f"Bin//{''.join(msg[:3])}.txt"
                Path(name).write_text(','.join(msg))

        elif self.way == 4:  # file_json
            names = ['ExchangeNo', 'CommodityNo', 'Contract.ContractNo1', 'DateTimeStamp', 'QPreClosingPrice',
                     'QPreSettlePrice', 'QPrePositionQty', 'QOpeningPrice', 'QLastPrice', 'QHighPrice', 'QLowPrice',
                     'QHisHighPrice', 'QHisLowPrice', 'QLimitUpPrice', 'QLimitDownPrice', 'QTotalQty', 'QTotalTurnover',
                     'QPositionQty', 'QAveragePrice', 'QClosingPrice', 'QSettlePrice', 'QLastQty', 'QImpliedBidPrice',
                     'QImpliedBidQty', 'QImpliedAskPrice', 'QImpliedAskQty', 'QPreDelta', 'QCurrDelta', 'QInsideQty',
                     'QOutsideQty', 'QTurnoverRate', 'Q5DAvgQty', 'QPERatio', 'QTotalValue', 'QNegotiableValue',
                     'QPositionTrend', 'QChangeSpeed', 'QChangeRate', 'QChangeValue', 'QSwing', 'QTotalBidQty',
                     'QTotalAskQty'] + ['QBidPrice', 'QBidQty', 'QAskPrice', 'QAskQty'] * 20

            def send(msg):
                name = f"Bin\\{''.join(msg[:3])}.txt"
                content = {_name: _values for _name, _values in zip(names, msg)}
                Path(name).write_text(str(content).replace("'", '"'))

        else:
            send = print

        self.tool = send

    @staticmethod
    def __get_redis():
        redis_conf = CONFIG['redis'].dict_props
        redis_conf['socket_timeout'] = 3
        pool = redis.ConnectionPool(**redis_conf)
        r = redis.Redis(connection_pool=pool)
        log('start Redis->' + ','.join(redis_conf))
        return r

    @staticmethod
    def __get_socket():
        socket_conf = CONFIG['socket'].dict_props
        srv = socket.socket()  # 创建一个socket
        srv.bind((socket_conf['ip'], socket_conf['port']))
        srv.listen(5)

        log(f"socket等待链接")

        connect_socket, _ = srv.accept()

        log(f"socket链接成功")
        return connect_socket

    def get_tool(self):
        self.__config_tool()
        return self.tool


# 判断是否登录成功
def asset_success(es, exe_id='1'):
    for _ in range(500):
        es.reading_out()
        if es.success:
            print('for_num', _)
            log(f'{exe_id}登录成功')
            return True
        elif es.error_:
            log(f'{exe_id}登录失败->{es.error_}')
            return False
    else:
        log(f'{exe_id}登录未知')
        es.kill(f'{exe_id}Kill')
    return False


# 循环登录获取可以使用的ES2
def log_es2(r, es2_list):
    # 指定登录账号
    es2 = ES('Bin/Data/APP2/9762.exe', r, app_id='2')
    es2.config_re_login(30)  # 重连时间,s
    es2.config_account(ip=CONFIG['ip'],
                       port=CONFIG['port'],
                       username=CONFIG['username'],
                       password=CONFIG['password'],
                       auth_code=CONFIG['auth_code'])

    if asset_success(es2, '2'):  # 登录成功
        log('2开始订阅')
        for i in es2_list:
            es2.config_subscribes(i)  # 订阅
        log('2订阅完毕，等待交易所')
        return es2

    return None


# 190810优化逻辑
def get_quote():
    # 分发
    r = Publish().get_tool()

    # 所有需要订阅的品种，190702增加去重功能
    con = CONFIG['contracts']

    # 断线重连，断线重连的时候也要判断是否在有效期内
    _error = 'No log in'
    while 1:
        es2 = log_es2(r, con)
        if es2 is not None:  # 如果es2成功
            _error = loop(es2)
        else:  # 如果es2不成功
            _error = 'No log in'  # 全军覆没
        log(f'restart->{_error}')
        sleep(3)


def loop(es2):
    while es2.should_loop:
        es2.reading_out()
    if es2.error_:
        es2.kill()
        return es2.error_
    else:
        return 'NoCode'
