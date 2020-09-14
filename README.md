ESunnyAPI是一款基于C++/Python的易盛信息官方封装开源库，用于易盛信息的行情获取以及交易。
如果你在开发易盛信息程序的时候遇到了奇奇怪怪的问题，请使用Quote.exe，其中打包了详尽的错误处理，可以快速定位问题。


祝贺 ESunnyAPI 入选 GITEE 最有价值开源项目 GVP
-----------------------------------------------


30s内上手EsunnyAPI？

配置文件位于Bin/Cinfig.py中
--------------------
- **配置账号信息**
  - ip = '61.163.243.173'
  - port = '7171'
  - username = 'ES'  # 用户名
  - password = '123456'  # 密码
  - auth_code = ''  # 授权码，默认为空
--------------------
- **配置订阅品种**
  - contracts = ['COMEX F GC 2006', 'COMEX F GC 2008']
--------------------
- **配置发布方式**
  - publish = 0  # 0是打印;1是redis;2是socket;3是file;4可以生成json文件
--------------------
- **配置发布信息**
- **如果publish==1,需要配置redis**
  - redis = {'host': 'localhost',
         'port': 6379,
         'db': 0,
         'password': None
         }
- **如果publish==2,需要配置socket**
  - socket = {'ip': '127.0.0.1',
          'port': 8080}

--------------------
    # 运行
  - 慵懒版:直接运行Quote.exe
  - 勤劳版:运行Quote.py
    
有任何问题请联系QQ:976308589;
--------------------
  - 行情字段如下
  - ExchangeNo
  - CommodityNo
  - Contract.ContractNo1
  - DateTimeStamp
  - QPreClosingPrice
  - QPreSettlePrice
  - QPrePositionQty
  - QOpeningPrice
  - QLastPrice
  - QHighPrice
  - QLowPrice
  - QHisHighPrice
  - QHisLowPrice
  - QLimitUpPrice
  - QLimitDownPrice
  - QTotalQty
  - QTotalTurnover
  - QPositionQty
  - QAveragePrice
  - QClosingPrice
  - QSettlePrice
  - QLastQty
  - QImpliedBidPrice
  - QImpliedBidQty
  - QImpliedAskPrice
  - QImpliedAskQty
  - QPreDelta
  - QCurrDelta
  - QInsideQty
  - QOutsideQty
  - QTurnoverRate
  - Q5DAvgQty
  - QPERatio
  - QTotalValue
  - QNegotiableValue
  - QPositionTrend
  - QChangeSpeed
  - QChangeRate
  - QChangeValue
  - QSwing
  - QTotalBidQty
  - QTotalAskQty
  - QBidPrice、QBidQty、QAskPrice、 QAskQty共计20档

字段释义如下
  -  //! 行情全文
  - struct TapAPIQuoteWhole
  - {
  -  	TapAPIContract				Contract;						///< 合约
  -  	TAPISTR_10					CurrencyNo;						///< 币种编号
  -  	TAPICHAR					TradingState;					///< 交易状态。1,集合竞价;2,集合竞价撮合;3,连续交易;4,交易暂停;5,闭市
  -  	TAPIDTSTAMP					DateTimeStamp;					///< 时间戳
  -  	TAPIQPRICE					QPreClosingPrice;				///< 昨收盘价
  -  	TAPIQPRICE					QPreSettlePrice;				///< 昨结算价
  -  	TAPIQVOLUME					QPrePositionQty;				///< 昨持仓量
  -  	TAPIQPRICE					QOpeningPrice;					///< 开盘价
  -  	TAPIQPRICE					QLastPrice;						///< 最新价
  -  	TAPIQPRICE					QHighPrice;						///< 最高价
  -  	TAPIQPRICE					QLowPrice;						///< 最低价
  -  	TAPIQPRICE					QHisHighPrice;					///< 历史最高价
  -  	TAPIQPRICE					QHisLowPrice;					///< 历史最低价
  -  	TAPIQPRICE					QLimitUpPrice;					///< 涨停价
  -  	TAPIQPRICE					QLimitDownPrice;				///< 跌停价
  -  	TAPIQVOLUME					QTotalQty;						///< 当日总成交量
  -  	TAPIQPRICE					QTotalTurnover;					///< 当日成交金额
  -  	TAPIQVOLUME					QPositionQty;					///< 持仓量
  -  	TAPIQPRICE					QAveragePrice;					///< 均价
  -  	TAPIQPRICE					QClosingPrice;					///< 收盘价
  -  	TAPIQPRICE					QSettlePrice;					///< 结算价
  -  	TAPIQVOLUME					QLastQty;						///< 最新成交量
  -  	TAPIQPRICE					QBidPrice[20];					///< 买价1-20档
  -  	TAPIQVOLUME					QBidQty[20];					///< 买量1-20档
  -  	TAPIQPRICE					QAskPrice[20];					///< 卖价1-20档
  -  	TAPIQVOLUME					QAskQty[20];					///< 卖量1-20档
  -  	TAPIQPRICE					QImpliedBidPrice;				///< 隐含买价
  -  	TAPIQVOLUME					QImpliedBidQty;					///< 隐含买量
  -  	TAPIQPRICE					QImpliedAskPrice;				///< 隐含卖价
  -  	TAPIQVOLUME					QImpliedAskQty;					///< 隐含卖量
  -  	TAPIQPRICE					QPreDelta;						///< 昨虚实度
  -  	TAPIQPRICE					QCurrDelta;						///< 今虚实度
  -  	TAPIQVOLUME					QInsideQty;						///< 内盘量
  -  	TAPIQVOLUME					QOutsideQty;					///< 外盘量
  -  	TAPIQPRICE					QTurnoverRate;					///< 换手率
  -  	TAPIQVOLUME					Q5DAvgQty;						///< 五日均量
  -  	TAPIQPRICE					QPERatio;						///< 市盈率
  -  	TAPIQPRICE					QTotalValue;					///< 总市值
  -  	TAPIQPRICE					QNegotiableValue;				///< 流通市值
  -  	TAPIQDIFF					QPositionTrend;					///< 持仓走势
  -  	TAPIQPRICE					QChangeSpeed;					///< 涨速
  -  	TAPIQPRICE					QChangeRate;					///< 涨幅
  -  	TAPIQPRICE					QChangeValue;					///< 涨跌值
  -  	TAPIQPRICE					QSwing;							///< 振幅
  -  	TAPIQVOLUME					QTotalBidQty;					///< 委买总量
  -  	TAPIQVOLUME					QTotalAskQty;					///< 委卖总量
  -  	TapAPIContract				UnderlyContract;				///< 虚拟合约对应的真实合约
  -  };
