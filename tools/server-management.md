# 服务器登录与管理指南

> 更新: 2026-07-19

---

## 旧服务器（腾讯云）

| 项目 | 值 |
|:-----|:-----|
| IP | 118.89.111.224 |
| 系统 | Ubuntu 24.04 |
| 用户 | ubuntu |
| 密码 | 123456Ab |
| 配置 | 4核 3.6GB 59GB |
| 到期 | 2027年3月 |
| 用途 | 千安 + 桥梁 + 咏明大药房网页 |

### SSH 登录

```bash
ssh ubuntu@118.89.111.224
```

### 登录后操作

```bash
# 查看服务状态
systemctl status nginx
systemctl status qianan-bridge

# 查看端口
ss -tlnp | grep -E "80|8080"

# 查看日志
tail -f /var/log/nginx/access.log

# 网站文件目录
/var/www/html/yongming/

# 桥梁目录
/home/ubuntu/bridge/
```

### ⚠️ 注意
- **药店页面不能动**（`/var/www/html/yongming/index.html`）
- 不要装 Docker
- 不要禁用密码登录
- 不要搞安全加固

---

## 新服务器（上海）

| 项目 | 值 |
|:-----|:-----|
| IP | 124.222.63.185 |
| 系统 | Ubuntu 24.04 |
| 用户 | ubuntu |
| 密码 | 123456Ab |
| 配置 | 4核 16GB 217GB |
| 用途 | 渗透工具链 + JuiceShop靶场 |

### SSH 登录

```bash
ssh ubuntu@124.222.63.185
```

### 已安装工具

```bash
# 渗透工具
nmap          # 端口扫描
sqlmap        # SQL注入（/home/ubuntu/sqlmap）
httpx         # HTTP探测
arjun         # 参数发现
autopent.py   # 轻量扫描器（/home/ubuntu/autopent.py）

# Docker容器
sudo docker ps
# 当前运行:
#   searxng       (8080端口，搜索引擎)
#   juiceshop     (8888端口，漏洞靶场)

# Docker镜像已拉
#   projectdiscovery/nuclei (925MB，欠模板)
```

### 常用操作

```bash
# 更新工具
export PATH=$PATH:/home/ubuntu/.local/bin

# 跑扫描
cd ~ && python3 autopent.py https://目标.com

# 管理Docker
sudo docker ps
sudo docker stop 容器名
sudo docker start 容器名
```

---

## Python 工具路径问题

两台服务器都可能遇到 `pip install` 后的工具不在PATH的问题，解决方法：

```bash
export PATH=$PATH:/home/ubuntu/.local/bin
```

建议加到 `.bashrc`：

```bash
echo 'export PATH=$PATH:/home/ubuntu/.local/bin' >> ~/.bashrc
```

---

## 文件传输

```bash
# 从本地传到旧服务器
scp 本地文件 ubuntu@118.89.111.224:~/目标路径

# 从旧服务器传到本地
scp ubuntu@118.89.111.224:~/文件 本地路径

# 从本地传到新服务器
scp 本地文件 ubuntu@124.222.63.185:~/目标路径
```

---

## 注意事项

1. ⚠️ 旧服务器药店页面不能动
2. 🔒 两台服务器密码相同（123456Ab）
3. 🐳 只有新服务器可以用 Docker
4. 📝 所有操作顺手记到 rizhi 知识库
