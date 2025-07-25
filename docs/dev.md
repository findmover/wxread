# 开发者文档
## 项目结构

### 文件结构

```
├── api
│   ├── notifier.py     # 推送通知模块，支持 PushPlus、Telegram 和 WxPusher
│   └── reader.py       # 核心阅读功能模块，模拟微信读书行为
├── README.md           # 项目说明文档
├── app.py              # 主程序入口（未使用）
├── build.py            # 构建脚本（未使用）
├── main.py             # 程序启动文件，控制阅读时长和推送方式
├── multi_main.py       # 多账户支持的启动文件
└── pyproject.toml      # Python项目配置文件
```

### 模块说明

#### api/notifier.py
- **PushPlusNotifier**：PushPlus消息推送类，实现消息推送功能
- **TelegramNotifier**：Telegram消息推送类，支持代理和直连两种方式
- **WxPusherNotifier**：WxPusher消息推送类，支持简单的消息推送
- **Notifier**：统一推送接口类，根据配置选择不同的推送方式

#### api/reader.py
- **WXReader**：微信读书SDK核心类，包含以下功能：
  - `read`：执行阅读操作
  - `refresh_cookie`：刷新cookie密钥
  - `_fix_no_synckey`：修复无 synckey 的情况
  - `cal_hash`：计算哈希值，用于请求签名
  - `parse_curl_bash`：解析 curl 命令，提取 headers、cookies 和 payload
  - `sync_run`：同步运行方法，循环执行阅读任务

#### main.py
- 控制程序的主要逻辑，包括：
  - 从环境变量读取配置
  - 解析 curl 命令获取请求配置
  - 创建 WXReader 实例
  - 根据配置创建 Notifier 实例
  - 运行阅读任务，支持推送通知

#### multi_main.py
- 支持多账号的主程序，可以同时为多个微信读书账号执行阅读任务