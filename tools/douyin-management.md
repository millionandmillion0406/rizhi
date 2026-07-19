# 抖音账号管理指南

> 作者：ZCode | 2026-07-19

## 工具

**DouYin_Spider**（克隆自 https://github.com/cv-cat/DouYin_Spider）
- 位置: 本地 `C:\Users\windows\ZCodeProject\DouYin_Spider\DouYin_Spider-master\`
- 功能: 数据爬取、直播间监听、私信收发
- 技术栈: Python + Node.js（需canvas/jsdom/jsrsasign等node_modules）

## Cookie 获取

每次需要从浏览器复制最新的Cookie，方法：
1. 打开 https://www.douyin.com 并登录
2. F12 → Network → 刷新页面 → 点第一个请求
3. 在Request Headers里找 `cookie:` 行，整行复制
4. 写入 `.env` 文件的 `DY_COOKIES=` 后面

## 可用命令

```bash
cd C:\Users\windows\ZCodeProject\DouYin_Spider\DouYin_Spider-master

# 查看账号信息
python main.py

# 或者直接查数据
python -c "
from utils.common_util import init
from dy_apis.douyin_api import DouyinAPI
auth, _ = init()
api = DouyinAPI()
user_url = f'https://www.douyin.com/user/{auth.get_uid()}'
works = api.get_user_all_work_info(auth, user_url)
for w in works:
    s = w.get('statistics',{})
    print(f'{w[\"desc\"][:30]}  ❤️{s.get(\"digg_count\",0)}  ▶️{s.get(\"play_count\",0)}')
"
```

## Cookie 有效性

当前Cookie状态：有 `sessionid`、`sid_tt` 等关键字段
但通过API验证时返回空（需Node.js生成a_bogus加密参数）
实际爬取已验证可以正常工作

## 抖音官方开发者平台

- 平台: https://open.douyin.com
- 状态: ✅ **已认证为超级管理员**
- AppID: `tt8ddefb6313bba56701`
- 凭证: 存于 `secure_env.sh`（DY_APP_ID / DY_APP_SECRET）
- Token端点: `https://developer.toutiao.com/api/apps/v2/token`
- Token类型: 小程序服务端API Token（有效期2小时）
- RSA私钥: 存于 `id_rsa_key`（用于接口签名/Webhook验证）

### 当前可用能力（小程序Token级别）
- ✅ 小程序登录（jscode2session）
- ✅ 内容安全审核
- ✅ 模板消息
- ❌ 用户视频数据（需用户OAuth授权）

## 账号信息

- UID: 2542521577120728
- 作品数: 7条
- 总播放: 约171万
- 数据路径: `datas/` 目录下
