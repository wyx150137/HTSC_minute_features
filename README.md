# 华泰高频特征

### Description

暂时还没拿到分笔数据，所以只能考虑用分钟数据来合成一部分特征，然后用特征再来做遗传规划，拟合出一部分因子出来。

整个因子计算分为 *RAW* 部分和 *PROCEED* 部分, *RAW* 部分主要是由一天的信息来进行计算的， *PROCEED* 的部分是基于
*RAW* 数据进行 计算的。

### Using

*RAW* 特征只能描述对象在特定的时间区间内做了什么，但是如果想要放到 model 中，还是建议在进行可理解的处理后，在放到
model 里面，所以 *PROCEED* 部分的特征，可以在 *RAW* 特征的基础上进行计算，然后再放到 model 中。具体的计算方式，
可以自行发挥。

### Some Details

0. 本文的所有 feature 来自于华泰金工研报，因此请在使用前，先阅读相关的研报，以便于理解。
由于本人比较贫穷，确实没钱买显卡，所以计算全量数据时均使用多进程进行计算。如果有显卡的话，可以考虑使用 GPU 进行计算，

1. 本文的数据基于 '1min' 的数据，数据来源为 [jointquant](https://www.joinquant.com/data)，已经下载并存储到本地
由于一些地方可能会用到如 'trade_calender' 等数据，所以请在目录下放入 'config.py', 里面包括了绝大多数的配置信息，包括
需要的账号密码，以及分钟文件的存储路径，多进程的进程数等，具体可以参考 'samplee_config.py' 文件内部的内容

2. 后续的*PROCEED* 因子分析数据，基于 '1d' 进行测试，测试周期一般为 1d, 5d, 20d, 所使用的框架为 [rqfactor](https://www.ricequant.com/doc/rqfactor/manual.html#%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E7%9A%84%E5%9B%A0%E5%AD%90)
具体的使用方法可以参考官方文档，这里不再赘述。

