from Include.LinkEXE import ESQuote

from Include.Path import Path

pre = []


def log():
    global pre
    print('如有任何问题，请联系976308589@qq.com')
    _path = Path('Config.txt')
    if not _path.exists():
        print('Config.txt不存在,请构建Config.txt，格式如下\n'
              '第1行:IP;'
              '第2行:port;'
              '第3行:账号;'
              '第4行:密码;'
              '第5行:authcode;'
              '第6行:订阅品种，譬如COMEX F GC 1902;'
              '如果有多个品种，累加即可，格式同第6行'
              )
    else:
        _config = _path.lines()
        _send = False if pre == _config else True
        pre = _config
        es = ESQuote()
        es.config_re_login(60)  # 重连时间,s
        es.config_account(ip=_config[0],
                          port=_config[1],
                          username=_config[2],
                          password=_config[3],
                          authcode=_config[4],
                          send=_send)
        for i in _config[5:]:
            es.config_subscribes(i)
        es.reading_out()


if __name__ == '__main__':
    while 1:
        try:
            log()
        except:
            pass
    input('按任意键退出\n如有任何问题，请联系976308589@qq.com')
