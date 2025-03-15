'''
 ██████╗ ██╗   ██╗    ██╗   ██╗███████╗███████╗██████╗     ██╗███╗   ██╗███████╗ ██████╗ 
 ██╔══██╗╚██╗ ██╔╝    ██║   ██║██╔════╝██╔════╝██╔══██╗    ██║████╗  ██║██╔════╝██╔═══██╗
 ██║  ██║ ╚████╔╝     ██║   ██║███████╗█████╗  ██████╔╝    ██║██╔██╗ ██║█████╗  ██║   ██║
 ██║  ██║  ╚██╔╝      ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║██╔══╝  ██║   ██║
 ██████╔╝   ██║       ╚██████╔╝███████║███████╗██║  ██║    ██║██║ ╚████║██║     ╚██████╔╝
 ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
'''

# 作者信息: [您的名字或用户名]
# 版本: 1.0
# 日期: 2023年XX月XX日
# 描述: 抖音用户信息提取工具，支持单个ID和批量ID范围

import requests
import json
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def print_banner():
    """
    打印程序的大型颜文字标题
    """
    print('''
 ██████╗ ██╗   ██╗    ██╗   ██╗███████╗███████╗██████╗     ██╗███╗   ██╗███████╗ ██████╗ 
 ██╔══██╗╚██╗ ██╔╝    ██║   ██║██╔════╝██╔════╝██╔══██╗    ██║████╗  ██║██╔════╝██╔═══██╗
 ██║  ██║ ╚████╔╝     ██║   ██║███████╗█████╗  ██████╔╝    ██║██╔██╗ ██║█████╗  ██║   ██║
 ██║  ██║  ╚██╔╝      ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║██╔══╝  ██║   ██║
 ██████╔╝   ██║       ╚██████╔╝███████║███████╗██║  ██║    ██║██║ ╚████║██║     ╚██████╔╝
 ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
    ''')

def fetch_user_info(unique_id):
    url = f"https://www.iesdouyin.com/web/api/v2/user/info/?unique_id={unique_id}"
    
    # 添加请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.iesdouyin.com/',
    }
    
    try:
        # 发送请求时禁用 SSL 验证，添加超时设置和重试次数
        response = requests.get(
            url, 
            headers=headers, 
            verify=False,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {str(e)}")
        return None

def flatten_json(nested_json, parent_key='', sep='_'):
    """
    扁平化 JSON，展开多层嵌套结构
    :param nested_json: 输入的 JSON 数据
    :param parent_key: 用于递归时的父键
    :param sep: 连接嵌套键的分隔符
    :return: 扁平化后的字典
    """
    items = []
    
    # 如果输入是None，直接返回空字典
    if nested_json is None:
        return {}
        
    # 如果输入不是字典类型，直接返回键值对
    if not isinstance(nested_json, dict):
        return {parent_key: nested_json}
        
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # 如果列表为空，保存空列表标记
            if not v:
                items.append((new_key, []))
            else:
                # 对列表中的每个元素进行处理
                for i, item in enumerate(v):
                    if isinstance(item, (dict, list)):
                        items.extend(flatten_json(item, f"{new_key}_{i}", sep=sep).items())
                    else:
                        # 如果是基本类型，直接保存
                        items.append((f"{new_key}_{i}", item))
        else:
            items.append((new_key, v))
            
    return dict(items)

def save_to_txt(data, filename):
    """
    将数据保存到txt文件，每行一个字段
    :param data: 数据字典
    :param filename: 保存文件的名称
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    print(f"数据已保存到 {filename}")

def save_multiple_to_txt(all_data, filename):
    """
    将多个用户的数据保存到同一个txt文件
    :param all_data: 包含多个用户数据的字典 {unique_id: flattened_data}
    :param filename: 保存文件的名称
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for unique_id, data in all_data.items():
            f.write(f"\n============ 用户 ID: {unique_id} ============\n\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
            f.write("\n" + "="*50 + "\n")
    print(f"批量数据已保存到 {filename}")

def main():
    # 用户输入 id 或 ID 范围
    user_input = input("请输入用户的 unique_id（单个ID或使用'-'分隔的ID范围，如'123-456'）：")
    
    # 检测是否为范围输入
    if '-' in user_input:
        try:
            # 解析ID范围
            start_id, end_id = user_input.split('-')
            start_id = int(start_id.strip())
            end_id = int(end_id.strip())
            
            if start_id > end_id:
                print("起始ID不能大于结束ID")
                return
            
            # 打印横幅
            print_banner()
            print(f"正在批量获取ID范围 {start_id} 到 {end_id} 的用户信息...")
            
            # 存储所有用户数据的字典
            all_user_data = {}
            
            # 循环获取每个ID的用户信息
            for id_num in range(start_id, end_id + 1):
                unique_id = str(id_num)
                print(f"正在获取ID为 {unique_id} 的用户信息...")
                
                user_info = fetch_user_info(unique_id)
                if user_info:
                    flattened_data = flatten_json(user_info)
                    all_user_data[unique_id] = flattened_data
                else:
                    print(f"获取ID为 {unique_id} 的用户信息失败，跳过")
            
            # 如果获取到了用户数据，保存到一个文件中
            if all_user_data:
                # 使用范围作为文件名
                filename = f"用户_{start_id}_到_{end_id}.txt"
                save_multiple_to_txt(all_user_data, filename)
            else:
                print("未获取到任何用户数据")
                
        except ValueError:
            print("ID范围格式无效，请使用数字和'-'，例如：'123-456'")
            
    else:
        # 单个ID处理（原有功能）
        unique_id = user_input.strip()
        
        # 打印横幅
        print_banner()
        print(f"正在获取ID为 {unique_id} 的用户信息...")
        
        # 获取用户信息
        user_info = fetch_user_info(unique_id)
        
        if user_info:
            # 扁平化 JSON 数据
            flattened_data = flatten_json(user_info)
            
            # 使用输入的 unique_id 作为文件名
            filename = f"{unique_id}.txt"
            
            # 保存到文件
            save_to_txt(flattened_data, filename)
        else:
            print(f"获取ID为 {unique_id} 的用户信息失败")

if __name__ == "__main__":
    main()
