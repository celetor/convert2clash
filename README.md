# convert2clash

#### 说明 : 本项目提供解析ss/ssr/v2ray/clashR/clash订阅链接为Clash配置文件的自动化脚本,供学习交流使用.
#### Robot.py中的参数 :
     1. sub_url=订阅地址（多个地址;隔开）
     2. output_path=转换成功后文件输出路径 默认输出至当前文件夹的output.yaml中
     3. config_url=来自互联网的规则策略 默认值为https://cdn.jsdelivr.net/gh/Celeter/convert2clash/config.yaml
     4. config_path=来自本地的规则策略 默认选择当前文件的config.yaml文件
##### 当config_url获取失败，使用config_path的策略。正常情况下只需修改sub_url即可食用。
#### 使用说明:
     1. 先执行pip install -r requirements.txt
     2. 再运行Robot.py 
