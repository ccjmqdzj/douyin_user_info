# douyin_user_info
这是一款爬虫软件 通过抖音的接口 可以批量爬取抖音用户信息
📝 功能介绍
该工具可以通过抖音用户的unique_id获取用户的详细信息，并将信息以易读的格式保存到本地文件。
✨ 主要特点
✅ 支持单个用户ID查询
✅ 支持ID范围批量查询（如"123-456"）
✅ 自动将查询结果保存为文本文件
✅ 批量查询结果整合到一个文件，便于分析
✅ 自动扁平化嵌套JSON数据，使输出更易读
✅ 直观的命令行界面，操作简单
🔧 安装说明
前提条件
Python 3.6+
pip (Python包管理器)
安装步骤
1. 安装依赖项
   ```bash
   pip3 install -r requirements.txt
   ```

2. 运行程序
   ```bash
   python3 1.py
   ```
![image](https://github.com/user-attachments/assets/82e7cea6-ae59-4bb2-b823-edbd29ccfecb)
![image](https://github.com/user-attachments/assets/f2c02435-88ab-4e5b-ad3f-eb6b688ec6bf)
```bash
extra_logid: 唯一标识请求的日志ID
extra_now: 当前时间的时间戳
is_oversea: 表示用户是否在海外，值为0表示不在海外
status_code: 状态码 0通常表示成功
user_info_short_id: 用户的短ID
user_info_nickname: 用户昵称
user_info_signature: 用户签名
user_info_avatar_thumb_uri 和 user_info_avatar_thumb_url_list: 用户头像的缩略图链接
user_info_avatar_medium_uri 和 user_info_avatar_medium_url_list: 用户头像的中等尺寸链接
user_info_follow_status: 关注状态
user_info_aweme_count: 用户发布的视频数量
user_info_following_count: 用户关注的数量
user_info_favoriting_count: 用户喜欢的数量
user_info_total_favorited: 用户被总点赞数
user_info_mplatform_followers_count: 用户在多平台上的粉丝数
user_info_sec_uid: 用户的安全UID
```
