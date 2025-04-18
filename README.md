# 刷时间不加时长，是因为最近微信读书又缩紧限制了，需要更新或重新fork配置 ！！！

## 项目介绍 📚

这个脚本主要是为了在微信读书的阅读**挑战赛中刷时长**和**保持天数**。由于本人偶尔看书时未能及时签到，导致入场费打了水漂。网上找了一些，发现高赞的自动阅读需要挂阅读器模拟或者用ADB模拟，实现一点也不优雅。因此，我决定编写一个自动化脚本。通过对官网接口的抓包和JS逆向分析实现。

该脚本具备以下功能：

- **阅读时长调节**：默认计入排行榜和挑战赛，时长可调节，默认为60分钟。
- **定时运行推送**：可部署在GitHub Action/服务器上，支持每天定时运行并推送结果到微信。
- **Cookie自动更新**：脚本能自动获取并更新Cookie，一次部署后面无需其它操作。
- **轻量化设计**：本脚本实现了轻量化的编写，部署服务器/GIthub action后到点运行，无需额外硬件。

***
## 操作步骤（v5.0） 🛠️

### 抓包准备

脚本逻辑还是比较简单的，`main.py`与`push.py`代码不需要改动。在微信阅读官网 [微信读书](https://weread.qq.com/) 搜索【三体】点开阅读点击下一页进行抓包，抓到`read`接口 `https://weread.qq.com/web/book/read`，如果返回格式正常（如：

```json
{
  "succ": 1,
  "synckey": 564589834
}
```
右键复制为Bash格式。

### 方法一： GitHub Action部署运行（GitHub运行）


- Fork这个仓库，在仓库 **Settings** -> 左侧列表中的 **Secrets and variables** -> **Actions**，然后在右侧的 **Repository secrets** 中添加如下值：
  - `WXREAD_CURL_BASH`：上面抓read接口后转换为curl_bash的数据。
  - `PUSH_METHOD`：推送方法，3选1推送方式（pushplus、wxpusher、telegram）。
  - `PUSHPLUS_TOKEN` or `WXPUSHER_SPT` or `TELEGRAM_BOT_TOKEN`&`TELEGRAM_CHAT_ID`: 选择推送后填写对应token。
  
- 在 **Variables** 部分，最下方添加变量：
  - `READ_NUM`：设定每次阅读的目标次数。


- 基本释义：

| key                        | Value                               | 说明                                                         | 属性      |
| ------------------------- | ---------------------------------- | ------------------------------------------------------------ | --------- |
| `WXREAD_CURL_BASH`         | `read` 接口 `curl_bash`数据 | **必填**，必须提供有效指令                                   | secrets   |
| `READ_NUM`                 | 阅读次数（每次 30 秒）              | **可选**，阅读时长，默认 20 分钟                           | variables |
| `PUSH_METHOD`              | `pushplus`/`wxpusher`/`telegram`    | **可选**，推送方式，3选1，默认不推送                                       |    secrets     |
| `PUSHPLUS_TOKEN`           | PushPlus 的 token                   | 当 `PUSH_METHOD=pushplus` 时必填，[获取地址](https://www.pushplus.plus/uc.html) | secrets   |
| `WXPUSHER_SPT`             | WxPusher 的token                    | 当 `PUSH_METHOD=wxpusher` 时必填，[获取地址](https://wxpusher.zjiecode.com/docs/#/?id=获取spt) | secrets   |
| `TELEGRAM_BOT_TOKEN`  <br>`TELEGRAM_CHAT_ID`   <br>`http_proxy`/`https_proxy`（可选）| 群组id以及机器人token                 | 当 `PUSH_METHOD=telegram` 时必填，[配置文档](https://www.nodeseek.com/post-22475-1) | secrets   |

**重要：除了READ_NUM配置在varables，其它的都配置在secrets里面的；需要推送`PUSH_METHOD`是必填的。**

### 视频教程

[![视频教程](https://github.com/user-attachments/assets/ec144869-3dbb-40fe-9bc5-f8bf1b5fce3c)](https://www.bilibili.com/video/BV1kJ6gY3En3/ "点击查看视频")


### 方法二： 服务器运行（docker部署）

- 在你的服务器上有Python运行环境即可，使用`cron`定义自动运行。
- 或者通过docker运行，将抓到的bash命令在 [Convert](https://curlconverter.com/python/) 转化为Python字典格式，复制需要的headers与cookies即可（data不需要）。

steps1：克隆这个项目：`git clone https://github.com/findmover/wxread.git`<br>
steps2：配置config.py里的headers、cookies、READ_NUM、PUSH_METHOD以及对应推送方式token<br>
steps3：进入目录使用镜像构建容器：
`docker rm -f wxread && docker build -t wxread . && docker run -d --name wxread -v $(pwd)/logs:/app/logs --restart always wxread`<br>
steps4：测试：`docker exec -it wxread python /app/main.py`

***
## Attention 📢

1. **签到次数调整**：只需签到完成挑战赛可以将`num`次数从120调整为2，每次`num`为30秒，200即100分钟。
   
2. **解决阅读时间问题**：对于issue中提出的“阅读时间没有增加”，“增加时间与刷的时间不对等”建议保留`config.py`中的【data】字段，默认阅读三体，其它书籍自行测试。

3. **GitHub Action部署/本地部署**：主要配置config.py即可，Action部署使用环境变量，本地部署修改config.py里的阅读次数、headers、cookies即可。

4. **推送**：pushplus推送偶尔出问题，猜测是GitHub action环境问题，增加重试机制。并增加wxpusher的极简推送方式。


***
## 字段解释 🔍

| 字段 | 示例值 | 解释 |
| --- | --- | --- |
| `appId` | `"wbxxxxxxxxxxxxxxxxxxxxxxxx"` | 应用的唯一标识符。 |
| `b` | `"ce032b305a9bc1ce0b0dd2a"` | 书籍或章节的唯一标识符。 |
| `c` | `"0723244023c072b030ba601"` | 内容的唯一标识符，可能是页面或具体段落。 |
| `ci` | `60` | 章节或部分的索引。 |
| `co` | `336` | 内容的具体位置或页码。 |
| `sm` | `"[插图]威慑纪元61年，执剑人在一棵巨树"` | 当前阅读的内容描述或摘要。 |
| `pr` | `65` | 页码或段落索引。 |
| `rt` | `88` | 阅读时长或阅读进度。 |
| `ts` | `1727580815581` | 时间戳，表示请求发送的具体时间（毫秒级）。 |
| `rn` | `114` | 随机数或请求编号，用于标识唯一的请求。 |
| `sg` | `"bfdf7de2fe1673546ca079e2f02b79b937901ef789ed5ae16e7b43fb9e22e724"` | 安全签名，用于验证请求的合法性和完整性。 |
| `ct` | `1727580815` | 时间戳，表示请求发送的具体时间（秒级）。 |
| `ps` | `"xxxxxxxxxxxxxxxxxxxxxxxx"` | 用户标识符或会话标识符，用于追踪用户或会话。 |
| `pc` | `"xxxxxxxxxxxxxxxxxxxxxxxx"` | 设备标识符或客户端标识符，用于标识用户的设备或客户端。 |
| `s` | `"fadcb9de"` | 校验和或哈希值，用于验证请求数据的完整性。 |


