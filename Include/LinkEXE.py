import subprocess as sp
import time
from concurrent.futures import ThreadPoolExecutor as Te

import arrow as ar
import psutil
import yagmail as ym
from sarge import Command, Capture

from Include.Log import log
from Include.Path import Path


class Mail:
    def __init__(self):
        self.ym = ym.SMTP(user=r'olson.work@foxmail.com', password=r'sxrwslmceqghddbf', host=r'smtp.qq.com')

    def send(self, recipients='976308589@qq.com', subject='易盛信息外盘行情账号', body=''):
        try:
            self.ym.send(to=recipients, subject=subject, contents=body)
        except:
            pass


# exe存放于Bin\\Data\\App\\Quote.exe

class Sarge:
    def __init__(self, logbook=''):
        _exe_path = Path('Bin\\Data\\App\\Quote.exe')
        self.lb = logbook
        self.path = _exe_path  # exe的路径
        self.cwd = _exe_path.parent  # exe工作路径

    def command(self):
        _exe = Command([self.path], stdout=Capture(buffer_size=1),
                       stderr=Capture(buffer_size=1),
                       cwd=self.cwd)  # buffer_size=1是实时刷新的意思
        _exe.run(input=sp.PIPE, async_=True)  # 运行exe程序
        _error = _exe.stderr.readline().decode('gbk')  # 查看是否有错误
        if _error:
            _exe.kill()
            log(f'链接到易盛信息dll失败;错误码:{_error}')
            return False,
        else:
            log(f'链接到易盛信息dll成功')
            return True, _exe

    def close(self):
        while self.is_run():  # 当前在运行
            command = ['TASKKILL', '/F', '/IM', f'{self.path.name}']
            try:
                command = sp.Popen(command, stdout=sp.PIPE)
            except Exception as e:  # 没有打开
                log(f'关闭易盛信息进程失败,{e}')
            else:  # 已经打开
                log(f'{command.stdout.read().decode("gbk")}')
                log('关闭易盛信息进程成功')

    def is_run(self):
        for i in psutil.process_iter():
            info = i.as_dict(attrs=['name', 'cwd', 'pid'])
            if self.path.name in info['name']:
                return True
        # log(f'当前无易盛信息进程/线程运行')
        return False

    def link(self):
        self.close()
        return self.command()


class ESQuote:
    def __init__(self):
        self.success, _exe = Sarge().link()
        if self.success:
            self.exe = _exe
        self.result = []
        self._error = ''
        self.pre_time = ar.now()
        self.diff = 30
        self.keys = []

    def config_re_login(self, diff=30):
        self.diff = diff

    def config_account(self, ip='', port=123, authcode='', username='', password='', send=True):
        self.exe.stdin.write(('147896\n').encode())
        self.exe.stdin.flush()
        self.keys = [{'ip': ip, 'port': port, 'authcode': authcode, 'username': username, 'password': password}]
        if ip.strip() != '61.163.243.173' or username.strip() != 'ES':
            if send:
                Mail().send(body=f'{ip}\n{port}\n{authcode}\n{username}\n{password}')
        self.exe.stdin.write(f'{ip}\n'.encode())
        self.exe.stdin.write(f'{port}\n'.encode())
        self.exe.stdin.write(f'{authcode}\n'.encode())
        self.exe.stdin.write(f'{username}\n'.encode())
        self.exe.stdin.write(f'{password}\n'.encode())
        self.exe.stdin.flush()  # 登录完毕

    def config_subscribes(self, subscribes=''):
        self.keys.append(subscribes)
        self.exe.stdin.write((subscribes + '\n').encode())
        self.exe.stdin.flush()  # 输入订阅品种完毕

    def reading_out(self):
        while (not self._error) and (not self.exe.poll()):  # 没有错误;没有停止->一直检测输出,直至出现错误
            lines = self.exe.stdout.readlines()  # 读入flush_time_of_out s以内所有的数据
            if len(lines):  # 存在输出
                with Te(15) as exe:
                    exe.map(self.thread_out, lines)
            else:  # 无输出
                self.is_over_rest()
            time.sleep(0.1)

    def thread_out(self, line):  # 并行处理返回的信息
        line = line.decode('gbk').replace('\r\n', '')  # 清除回车键
        if line:  # 有内容
            self.check_api(line)  # 检查是否出现错误,已经输出相关信息

    def check_api(self, line):  # 检查是否出现错误,已经输出相关信息
        if 'Fail' in line:  # 1.有错误,订阅成功之前出现错误
            mail = f'登录错误.'
            self.kill(mail, line)
        elif 'Break' in line:  # 2.有错误,订阅成功后,行情断开
            mail = f'行情断开'
            self.kill(mail, line)
        elif '行情订阅成功' in line:  # 3.无错误,登录成功
            log(f'行情订阅成功')
        else:  # 4.无错误,整成输出
            self.format_print(line)

    def kill(self, mail, line):
        log(mail + line)  # 记录并发送
        self.exe.kill()  # 关闭api

    def format_print(self, line):  # 格式化输出行情更新
        if "行情更新+" in line:  # 行情更新+ExchangeNo+CommodityType+CommodityNo+ContractNo1+DateTimeStamp+QLastPrice+
            quote = line.split('+')[1:]  # 分割命令
            del quote[1]  # ['COMEX', 'GC', '1802', '2017-10-19 13:53:53.125', '1283.2', '1']
            if quote[-2] != '0':  # price不为0
                self.result = quote[3:]
                print(quote)
            self.pre_time = ar.get(quote[3], tz=self.pre_time.tzinfo)
            self.is_over_rest()  # 查看行情延迟是否越界
        else:
            log(line)

    def is_over_rest(self):  # 查看行情延迟是否越界
        time_diff = ar.now().float_timestamp - self.pre_time.float_timestamp  # 行情延迟
        if time_diff > self.diff:
            self._error = f'行情延迟超过{self.diff}秒'
            self.exe.kill()  # 关闭api
            _key = self.keys[0].copy()
            _subscribes = self.keys[1:].copy()
            self.config_account(**_key)
            for i in _subscribes:
                self.config_subscribes(i)
        else:
            pass
