ESunnyAPI是一款基于C++/Python的易盛信息官方封装开源库，用于易盛信息的行情获取以及交易。
如果你在开发易盛信息程序的时候遇到了奇奇怪怪的问题，请使用Run.exe，其中打包了详尽的错误处理，可以快速定位问题。


祝贺 HIKYUU 入选 GITEE 最有价值开源项目 GVP
-----------------------------------------------


如何在一分钟内使用 EsunnyAPI？
--------------------

- **1.配置账号信息:Account.txt**
    - 第一行:IP
    - 第二行:Port
    - 第三行:账号
    - 第四行:密码
    - 第五行:授权码
    - 例如:
    - 61.163.243.173
    - 7171
    - ES
    - 123456
    - B112F916FE7D27BCE7B97EB620206457946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC946CED32E26C1EAC5211AF9FEE541DDE9D6F622F72E25D5DEF7F47AA93A738EF5A51B81D8526AB6A9D19E65B41F59D6A946CED32E26C1EACCAF8D4C61E28E2B1ABD9B8F170E14F8847D3EA0BF4E191F5DCB1B791E63DC196D1576DEAF5EC563CA3E560313C0C3411B45076795F550EB050A62C4F74D5892D2D14892E812723FAC858DEBD8D4AF9410729FB849D5D8D6EA48A1B8DC67E037381A279CE9426070929D5DA085659772E24A6F5EA52CF92A4D403F9E46083F27B19A88AD99812DADA44100324759F9FD1964EBD4F2F0FB50B51CD31C0B02BB437

- **2.配置需要订阅的合约:Config.txt**
    - 合约的形式为:交易所 类别 商品 合约
    - 例如(测试的时候自动修改为最新合约):
    - HKEX F HSI 1906
    - NYMEX F NG 1907
    - HKEX F MHI 1906
    - SGX F CN 1906

- **3.配置Redis信息:Redis.txt(可选)**
    - 第一行:IP
    - 第二行:Port
    - 第三行:数据库
    - 第四行:密码
    - 例如:
    - 127.0.0.1
    - 6379
    - 0
    - 123456

- **4.运行**
    - 慵懒版:直接运行Run.exe
    - 勤劳版:运行Run.py
    
有任何问题请联系QQ:976308589;
--------------------