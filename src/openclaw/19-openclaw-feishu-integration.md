# OpenClaw 接入飞书渠道教程详解

OpenClaw 支持接入 WhatsApp、Telegram、Discord、飞书等主流聊天渠道，本文以**飞书**为实战案例，完整讲解从开放平台应用创建、OpenClaw 配置、授权配对到安全管控与高级定制的全流程，适配国内飞书与国际版 Lark，开箱即用。

## 一、渠道概览

OpenClaw 飞书渠道为**官方内置插件**，无需额外安装，核心特性：

- 采用 **WebSocket 长连接**接收消息，**无需公网 IP、无需配置回调地址**
- 完整支持私聊、群组、@提及、消息引用、流式卡片输出、媒体收发
- 支持多账号、多智能体路由、精细化访问控制
- 国际版 Lark 只需切换域名即可兼容

---

## 二、前置准备

1. 已完成 OpenClaw 安装与网关基础部署
2. 飞书企业账号，具备开放平台开发者权限
3. 记录 OpenClaw 配置文件路径：`~/.openclaw/openclaw.json`

---

## 三、飞书开放平台：创建并配置机器人应用

### 1. 创建企业自建应用

- 国内飞书：访问 https://open.feishu.cn/app
- 国际版 Lark：访问 https://open.larksuite.com/app
- 点击**创建企业自建应用**，填写应用名称、描述、图标，完成创建

### 2. 获取应用核心凭证

进入「凭证与基础信息」，复制以下内容备用：

- App ID（格式：`cli_xxx`）
- App Secret（妥善保管，禁止泄露）

### 3. 批量导入权限（一键配置）

进入「权限管理」→ 点击**批量导入**，粘贴以下 JSON 并导入：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "im:chat",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

### 4. 启用机器人能力

进入「应用能力 → 机器人」，开启机器人并设置机器人名称。

### 5. 配置事件订阅（关键）

前提：先在 OpenClaw 执行 `openclaw channels add` 并启动网关

- 进入「事件与回调 → 事件配置」
- 选择**使用长连接接收事件（WebSocket）**
- 添加事件：
    - `im.message.receive_v1`（接收消息）
    - `im.message.reaction.created_v1`（表情添加）
    - `im.message.reaction.deleted_v1`（表情移除）
    - `application.bot.menu_v6`（菜单事件）

### 6. 发布应用

进入「版本管理与发布」→ 创建版本 → 提交上线，等待企业管理员审批（测试企业可自动通过）。

---

## 四、OpenClaw 配置飞书渠道

### 方式 1：交互式向导（推荐新手）

```bash
openclaw channels add
```

按提示选择 **Feishu**，依次输入 App ID、App Secret，完成配置。

### 方式 2：手动编辑配置文件

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "domain": "feishu",
      "dmPolicy": "pairing",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "AI助手"
        }
      }
    }
  }
}
```

> 注：国际版 Lark 将 `domain` 改为 `"lark"`

### 方式 3：环境变量配置

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

---

## 五、启动网关与配对授权

### 1. 启动/重启网关

```bash
openclaw gateway restart
# 查看状态
openclaw gateway status
# 实时日志
openclaw logs --follow
```

### 2. 用户授权配对（默认安全策略）

1. 飞书私聊发送消息给机器人，机器人返回**配对码**
2. 终端执行批准命令：

```bash
# 查看待审批配对
openclaw pairing list feishu
# 批准指定码
openclaw pairing approve feishu &lt;配对码&gt;
```

批准后即可正常对话。

---

## 六、访问控制与安全配置

### 1. 私聊策略（dmPolicy）

| 策略 | 说明 |
|---|---|
| pairing | 默认，需批准配对 |
| allowlist | 仅白名单用户可聊 |
| open | 所有人可聊（谨慎） |
| disabled | 禁用私聊 |

白名单配置示例：

```json
{
  "channels": {
    "feishu": {
      "allowFrom": ["ou_xxx", "ou_yyy"]
    }
  }
}
```

### 2. 群组策略（groupPolicy）

- `open`：所有群组可用，默认需 @机器人
- `allowlist`：仅指定群组可用
- `disabled`：禁用群组

群组白名单 + 强制 @提及示例：

```json
{
  "channels": {
    "feishu": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["oc_xxx"],
      "groups": {
        "oc_xxx": { "requireMention": true }
      }
    }
  }
}
```

### 3. 获取用户/群组 ID

- 用户 ID（ou_xxx）：`openclaw pairing list feishu`
- 群组 ID（oc_xxx）：`openclaw logs --follow` 查看日志

---

## 七、高级功能配置

### 1. 多机器人账号

```json
{
  "channels": {
    "feishu": {
      "defaultAccount": "main",
      "accounts": {
        "main": { "appId": "cli_xxx", "appSecret": "xxx" },
        "backup": { "appId": "cli_yyy", "appSecret": "yyy", "enabled": false }
      }
    }
  }
}
```

### 2. 流式卡片输出（默认开启）

```json
{
  "channels": {
    "feishu": {
      "streaming": true,
      "blockStreamingCoalesce": { "enabled": true, "minDelayMs": 50 }
    }
  }
}
```

### 3. 消息引用

```json
{
  "channels": {
    "feishu": {
      "replyToMode": "all",
      "groups": { "oc_xxx": { "replyToMode": "first" } }
    }
  }
}
```

> `replyToMode` 可选值：`all` / `first` / `off`

### 4. 多智能体路由

按用户/群组绑定不同智能体：

```json
{
  "agents": { "list": [{ "id": "main" }, { "id": "work" }] },
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "peer": { "kind": "dm", "id": "ou_xxx" } } },
    { "agentId": "work", "match": { "channel": "feishu", "peer": { "kind": "group", "id": "oc_xxx" } } }
  ]
}
```

---

## 八、常用命令速查

| 命令 | 作用 |
|---|---|
| openclaw channels add | 添加渠道 |
| openclaw gateway restart | 重启网关 |
| openclaw gateway status | 网关状态 |
| openclaw logs --follow | 实时日志 |
| openclaw pairing list feishu | 查看配对 |
| openclaw pairing approve feishu &lt;code&gt; | 批准用户 |

---

## 九、故障排除

### 1. 机器人收不到任何消息

- 确认应用已**发布上线**
- 确认事件订阅为 **WebSocket 长连接**
- 确认网关运行：`openclaw gateway status`
- 检查权限是否完整导入
- 查看日志：`openclaw logs --follow`

### 2. 群组中不响应

- 机器人已加入群组
- 默认需 **@机器人** 才响应
- 检查 `groupPolicy` 非 `disabled`
- 检查群组白名单配置

### 3. 发送消息失败

- 检查 `im:message:send_as_bot` 权限已开通
- 重启网关：`openclaw gateway restart`

### 4. 找不到 openclaw 命令

```bash
node -v
npm prefix -g
echo "$PATH"
# 修复 PATH
export PATH="$(npm prefix -g)/bin:$PATH"
# 写入 shell 配置
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 5. WebSocket 连接失败

- 确认网关已启动再保存事件订阅
- 关闭代理/VPN 重试
- 检查 App ID/App Secret 正确

---

## 十、完成验证

1. 飞书私聊/群组 @机器人发送测试消息
2. 机器人正常回复，流式输出流畅
3. 日志无报错，网关状态正常

至此，OpenClaw 飞书渠道接入完成。
