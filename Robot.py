import requests
import yaml
import base64
import json
import datetime
import sys


def log(msg):
    time = datetime.datetime.now()
    print('[' + time.strftime('%Y.%m.%d-%H:%M:%S') + ']:' + msg)


# 保存到文件
def save_to_file(file_name, content):
    with open(file_name, 'wb') as f:
        f.write(content)


# 获取订阅地址数据:
def get_proxies(url):
    headers = {
        'User-Agent': 'V2rayToClash'
    }
    # 请求订阅地址
    raw = requests.get(url, headers=headers, timeout=5000).content.decode('utf-8')
    v2ray_raw = base64.b64decode(raw)
    v2ray_list = v2ray_raw.splitlines()
    log('已获取{}个节点'.format(len(v2ray_list)))
    # 解析vmess链接为json
    proxy_list = []
    for item in v2ray_list:
        b64_proxy = item.decode('utf-8')[8:]
        proxy_str = base64.b64decode(b64_proxy).decode('utf-8')
        proxy_dict = json.loads(proxy_str)
        proxy_list.append(proxy_dict)
    return proxy_list


# 转换成Clash节点
def convert2clash(arr):
    log('节点转换中...')
    proxies = {
        'proxy_list': [],
        'proxy_names': []
    }
    for item in arr:
        obj = {
            'name': item.get('ps'),
            'type': 'vmess',
            'server': item.get('add'),
            'port': item.get('port'),
            'uuid': item.get('id'),
            'alterId': item.get('aid') if type(item.get('aid')) is int else item.get('alterId'),
            'cipher': item.get('type') if item.get('type') and item.get('type') != 'none' else 'auto',
            'udp': True,
            'network': item.get('net') if item.get('net') else None,
            'tls': True if item.get('tls') == 'tls' else None,
            'ws-path': item.get('path'),
            'ws-headers': {'Host': item.get('host')} if item.get('host') else None
        }
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        proxies['proxy_list'].append(obj)
        proxies['proxy_names'].append(obj['name'])
    return proxies


# 获取本地规则策略的配置文件
def load_local_config(path):
    try:
        f = open(path, 'r', encoding="utf-8")
        local_config = yaml.load(f.read(), Loader=yaml.FullLoader)
        f.close()
        return local_config
    except FileNotFoundError:
        log('配置文件加载失败')
        sys.exit()


# 获取规则策略的配置文件
def get_default_config(url, path):
    try:
        raw = requests.get(url, timeout=5000).content.decode('utf-8')
        template_config = yaml.load(raw, Loader=yaml.FullLoader)
    except requests.exceptions.RequestException:
        log('网络获取规则配置失败,加载本地配置文件')
        template_config = load_local_config(path)
    log('已获取规则配置文件')
    return template_config


# 将代理添加到配置文件
def add_proxies_to_model(data, model):
    model['proxies'] = data['proxy_list']
    # 规则策略的占位符
    placeholder = ['气抖冷']
    for group in model['proxy-groups']:
        if group['proxies'] is None:
            group['proxies'] = data['proxy_names']
        replace = [False for proxy in group['proxies'] if proxy in placeholder]
        if replace:
            group['proxies'] = [proxy for proxy in group['proxies'] if proxy not in placeholder]
            group['proxies'].extend(data['proxy_names'])
    return model


# 保存配置文件
def save_config(path, data):
    config = yaml.dump(data, sort_keys=False, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    save_to_file(path, config)
    log('成功更新:{}个节点'.format(len(data['proxies'])))


# 程序入口
if __name__ == '__main__':
    # 订阅地址
    v2ray_url = ''
    # 输出路径
    output_path = './output.yaml'
    # 规则策略
    config_url = 'https://raw.githubusercontent.com/Celeter/v2toclash/master/config.yaml'
    config_path = './config.yaml'

    v2ray_proxy = get_proxies(v2ray_url)
    node_list = convert2clash(v2ray_proxy)
    default_config = get_default_config(config_url, config_path)
    final_config = add_proxies_to_model(node_list, default_config)
    save_config(output_path, final_config)
