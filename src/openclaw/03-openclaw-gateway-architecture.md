---
title: OpenClaw Gateway 网关架构设计
order: 3
---

# OpenClaw Gateway 网关架构设计

OpenClaw Gateway 是整个系统的**核心常驻守护进程**与统一控制平面，承担多聊天渠道接入、会话路由、设备管理、事件分发与安全管控的中枢职能，是系统内会话、路由与渠道连接的唯一事实源。本文基于官方架构文档，完整拆解 Gateway 的设计原则、组件构成、通信协议、连接生命周期与运维规范。

## 一、架构总览

### 1.1 核心定位

- 单主机单网关：**每台主机仅运行一个 Gateway 进程**，统一管理所有聊天渠道长连接（WhatsApp/Telegram/Discord/Signal/iMessage 等），是唯一维护 WhatsApp 会话的节点。

- 统一控制平面：macOS 应用、CLI、Web 界面、自动化脚本、移动 / 无头节点均通过 WebSocket 连接到 Gateway，实现集中管控。

- 双端口默认配置：

    - 控制平面：`127.0.0.1:18789`（WebSocket，客户端 / 节点接入）

    - Canvas 主机：`18793`（提供智能体可编辑 HTML 与 A2UI）

### 1.2 整体拓扑

```Plain Text
WhatsApp/Telegram/Discord/Slack/iMessage/WebChat
          ↓
┌─────────────────────────────────┐
│        Gateway 网关(守护进程)       │ ←→ Pi 智能体运行时
└─────────────┬─────────────┬──────┘
              │             │
┌─────────────▼─────┐ ┌─────▼─────────────┐
│  客户端(CLI/Web/桌面) │ │ 节点(iOS/Android/无头) │
└───────────────────┘ └───────────────────┘
```

## 二、核心组件与职责

### 2.1 Gateway 网关（守护进程）

- 维护所有聊天渠道的提供商长连接，管理渠道状态。

- 暴露强类型 WebSocket API，支持请求 / 响应与服务器主动推送事件。

- 基于 JSON Schema 校验入站消息帧，保障通信合法性。

- 主动下发系统事件：`agent`/`chat`/`presence`/`health`/`heartbeat`/`cron` 等。

- 统一管理会话生命周期、设备配对与安全策略。

### 2.2 控制平面客户端

覆盖 macOS 应用、CLI、Web 管理界面、自动化脚本四类角色：

- 单客户端单 WebSocket 连接，与网关保持长连通。

- 主动发送操作请求：`health`/`status`/`send`/`agent`/`system-presence`。

- 订阅系统事件：`tick`/`agent`/`presence`/`shutdown`，实时感知状态变化。

### 2.3 设备节点（macOS/iOS/Android/无头设备）

- 以 `role: node` 身份接入同一 WebSocket 服务器，与客户端逻辑隔离。

- 连接时携带设备身份信息，基于设备维度完成配对与信任存储。

- 向外暴露硬件能力命令：`canvas.*`/`camera.*`/`screen.record`/`location.get` 等。

### 2.4 WebChat

- 基于 WebSocket 调用网关 API，实现聊天历史拉取与消息发送。

- 远程场景下，通过 SSH/Tailscale 隧道与其他客户端共用同一条安全链路接入。

## 三、客户端连接生命周期

单个客户端从接入到交互的完整时序流程：

```Plain Text
Client                          Gateway
  |                               |
  |--------- req:connect -------->|  # 首帧必须为connect，完成握手
  |<-------- res(ok) -------------|  # 携带hello-ok快照（在线状态+健康信息）
  |                               |
  |<------ event:presence --------|  # 推送在线状态
  |<-------- event:tick ----------|  # 系统心跳事件
  |                               |
  |--------- req:agent --------->|  # 发起智能体调用
  |<-------- res:agent -----------|  # 回执：runId+accepted状态
  |<------ event:agent -----------|  # 流式响应推送
  |<-------- res:agent -----------|  # 最终结果：runId+status+summary
  |                               |
```

- 强制握手规则：**首帧必须为 connect**，非 JSON 或非 connect 帧会被直接关闭连接。

- 事件机制：服务器主动推送，客户端不重放历史事件，出现间隙需主动刷新状态。

## 四、网关线路协议

### 4.1 基础传输规范

- 传输层：WebSocket，文本帧承载 JSON 格式载荷。

- 认证方式：支持 `OPENCLAW_GATEWAY_TOKEN` 或 `--token` 参数，`connect.params.auth.token` 必须匹配，否则断开套接字。

- 幂等保障：有副作用的方法（`send`/`agent`）必须携带幂等键，服务端维护短期去重缓存，支持安全重试。

### 4.2 消息格式定义

1. 请求帧

```json
{"type":"req","id":"xxx","method":"health","params":{}}
```

2. 响应帧

```json
{"type":"res","id":"xxx","ok":true,"payload":{}}
```

3. 事件帧

```json
{"type":"event","event":"agent","payload":{},"seq":1,"stateVersion":"1.0"}
```

4. 节点标识：节点必须在 connect 帧中声明 `role: "node"`，并附带能力、命令与权限声明。

## 五、设备配对与本地信任机制

### 5.1 身份与配对规则

- 所有 WebSocket 客户端（操作员 + 节点）均在 connect 阶段携带**设备唯一身份**。

- 新设备 ID 必须经过配对批准，网关为可信设备颁发设备令牌，后续连接免审批。

- 本地连接（回环地址或网关主机的 tailnet 地址）可自动批准，保障同主机流畅体验。

- 非本地连接必须签名 `connect.challenge` 随机数，且需**显式人工批准**方可接入。

- 网关级认证（`gateway.auth.*`）对本地 / 远程连接统一生效，无例外豁免。

## 六、远程访问方案

### 6.1 推荐方案

- 优先使用 **Tailscale 或企业 VPN**，实现安全内网穿透。

- 备选方案：SSH 本地端口转发

```bash
ssh -N -L 18789:127.0.0.1:18789 user@网关主机IP
```

- 远程场景可启用 WebSocket TLS 与证书固定，提升传输安全性。

- 握手流程、认证令牌规则与本地连接完全一致，无差异化配置。

## 七、运维与健康管理

### 7.1 启动方式

- 前台启动：`openclaw gateway`，日志直接输出到标准输出。

- 服务化部署：macOS 使用 launchd，Linux 使用 systemd，实现进程守护与自动重启。

### 7.2 健康检查

- 通过 WebSocket 调用 `health` 方法获取健康状态，该信息也包含在 `hello-ok` 握手响应中。

- 配合系统服务管理器，实现异常自动恢复与告警。

## 八、架构不变量

Gateway 架构严格遵循以下不可变约束，保障系统稳定性：

1. 每台主机**恰好一个** Gateway 进程，控制单个 WhatsApp Baileys 会话。

2. 所有客户端 / 节点接入**强制握手**，非法首帧直接关闭连接。

3. 服务器不重放历史事件，客户端间隙需主动拉取最新状态。

4. 网关是会话、路由、渠道连接的**唯一事实源**，所有状态统一收敛于此。

## 九、与 Pi 智能体的集成

Gateway 作为编排层，通过嵌入式 SDK 方式对接 Pi 智能体运行时，不使用子进程或 RPC 模式：

- 由 Gateway 统一管理会话生命周期、工具注入、系统提示词与上下文压缩。

- 智能体执行结果通过网关的 WebSocket 事件流式推送给对应客户端与渠道，实现端到端交互闭环。
