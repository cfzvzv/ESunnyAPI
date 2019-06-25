import redis
from path import Path

from Code.Sarge import ESRedis as ESQuote
from Include.Log import log


def log_es(r=None):
    # 获取账户信息
    acc = Path('Account.txt')
    if not acc.exists():
        input('当前目录下不存在Account.txt，请创建并配置账号')
        return
    acc = [i.strip() for i in acc.lines() if i.strip()]

    # 登录账户
    es = ESQuote(r=r)
    es.config_account(*acc)
    # 是否登录成功
    while es.can_log_in == -1:
        es.reading_out()
    # 订阅行情
    es_list = Path('Config.txt')
    if not es_list.exists():
        input('当前目录下不存在Account.txt，请创建并配置账号')
        return
    es_list = [i.strip() for i in es_list.lines() if i.strip()]
    if es.can_log_in:
        for i in es_list:
            es.config_subscribes(i)  # 订阅

        # 获取订阅成功
        while es.should_loop:
            es.reading_out()


def get_redis():
    redis_conf = Path('Redis.txt')
    if not redis_conf.exists():
        return None
    redis_conf = [i.strip() for i in Path('Redis.txt').lines() if i.strip()]
    log('启动Redis' + ','.join(redis_conf))
    return redis.Redis(host=redis_conf[0],
                       port=int(redis_conf[1]),
                       db=redis_conf[2],
                       password=redis_conf[3])


def quote():
    my_redis = get_redis()
    log_es(my_redis)
    input('按任意键退出，有问题请联系QQ:976308589')
