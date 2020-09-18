# v2ray-to-clash

#### 说明 : 本脚本提供解析v2ray订阅链接为Clash配置文件的自动化,供学习交流使用.
#### Robot.py中的参数 :
     1. v2ray_url=v2ray订阅地址
     2. output_path=转换成功后文件输出路径 默认输出至当前文件夹的output.yaml中
     3. config_url=来自互联网的规则策略 默认值为https://raw.githubusercontent.com/Celeter/v2toclash/master/config.yaml
	 4. config_path=来自本地的规则策略 默认选择当前文件的config.yaml文件
##### 当config_url获取失败，使用config_path的策略。正常情况下只需修改v2ray_url。
#### 使用说明:
     1. 先执行pip install -r requirements.txt
     2. 再运行Robot.py 
