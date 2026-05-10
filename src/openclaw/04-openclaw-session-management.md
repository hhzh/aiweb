# OpenClaw Session 会话管理教程

会话（Session）是 OpenClaw 组织对话、管理上下文、存储交互状态的核心单元，所有消息、工具执行、记忆关联均依托会话完成。本文整合官方会话、渠道对接、会话修剪、会话工具、会话压缩五大核心文档，完整覆盖会话路由、隔离、生命周期、存储、维护、扩展与优化的全流程操作与配置。

## 一、会话管理核心概述

OpenClaw 以**会话**为维度拆分所有对话交互，消息来源决定路由规则，会话负责承载上下文历史、工具状态、模型配置与记忆关联。会话的合理管理直接影响对话连续性、上下文准确性、系统资源占用与多用户隔离安全性。

## 二、消息路由与会话隔离

### 2.1 消息路由规则

不同消息来源会被自动路由到对应会话，确保上下文隔离：

| 消息来源 | 会话行为 |
|---|---|
| 私聊（DM） | 默认共享单个会话 |
| 群组聊天 | 每个群组独立隔离会话 |
| 房间/频道 | 每个房间独立隔离会话 |
| 定时任务（Cron） | 每次运行新建临时会话 |
| Webhook | 每个钩子独立隔离会话 |

### 2.2 私聊隔离（DM Isolation）

单用户场景可默认共享私聊会话；**多用户场景必须开启私聊隔离**，避免用户间上下文泄露。

配置方式（`openclaw.json`）：

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  }
}
```

`dmScope` 可选值：

- `main`：默认，所有私聊共享一个会话
- `per-peer`：按发送者跨渠道隔离
- `per-channel-peer`：按渠道 + 发送者隔离（**推荐**）
- `per-account-channel-peer`：按账号 + 渠道 + 发送者隔离

### 2.3 跨渠道身份关联

同一用户在多渠道发送消息，可通过 `identityLinks` 关联身份，共享同一个会话：

```json
{
  "session": {
    "identityLinks": {
      "alice": ["telegram:123", "discord:456", "slack:U123"]
    }
  }
}
```

配置后可通过 `openclaw security audit` 校验隔离效果。

## 三、会话生命周期管理

会话默认复用，直至触发重置规则，重置后开启全新会话：

1. **每日重置**：网关主机本地时间每日凌晨 4 点自动新建会话
2. **空闲重置**：配置空闲时长后自动重置，`session.reset.idleMinutes` 设置分钟数
3. **手动重置**：聊天内发送 `/new` 或 `/reset`；`/new <模型名>` 可同步切换模型

优先级：每日重置与空闲重置以**先触发**的为准；活跃的 CLI 会话不会被默认每日重置中断。

## 四、会话状态存储位置

所有会话状态由 Gateway 网关统一管理，UI 客户端仅从网关查询数据：

- 会话元数据：`~/.openclaw/agents/<agentId>/sessions/sessions.json`
- 会话转录记录：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`

## 五、会话维护与自动清理

OpenClaw 自动限制会话存储总量，避免磁盘占用过大：

### 5.1 配置自动清理

```json
{
  "session": {
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "30d",
      "maxEntries": 500
    }
  }
}
```

- `mode`：`warn` 仅报告（默认），`enforce` 自动清理
- `pruneAfter`：保留时长，超过则清理
- `maxEntries`：最大会话数量

### 5.2 清理预览命令

```bash
openclaw sessions cleanup --dry-run
```

## 六、会话检查与调试

通过命令快速查看会话状态、上下文占用与历史信息：

- `openclaw status`：查看会话存储路径与最近活动
- `openclaw sessions --json`：列出所有会话，可加 `--active <分钟数>` 过滤活跃会话
- 聊天内 `/status`：查看上下文占用、模型与开关状态
- 聊天内 `/context list`：查看系统提示词注入内容

## 七、渠道对接（Channel Docking）

渠道对接是会话级**通话转接**，保留上下文不变，仅修改后续回复的投递渠道。

### 7.1 核心作用

任务在一个聊天平台发起，后续回复转接到另一平台，上下文不中断。

### 7.2 前置配置

必须配置 `identityLinks` 关联同一用户的多渠道身份：

```json
{
  "session": {
    "identityLinks": {
      "alice": ["telegram:123", "discord:456"]
    }
  }
}
```

### 7.3 对接命令

| 目标渠道 | 命令 | 别名 |
|---|---|---|
| Discord | `/dock-discord` | `/dock_discord` |
| Telegram | `/dock-telegram` | `/dock_telegram` |
| Slack | `/dock-slack` | `/dock_slack` |
| Mattermost | `/dock-mattermost` | `/dock_mattermost` |

### 7.4 关键约束

- 不创建渠道账号、不跳过白名单、不迁移转录记录
- 仅修改当前会话的 `lastChannel`/`lastTo` 投递字段

## 八、会话修剪（Session Pruning）

会话修剪是**内存级**优化，在每次 LLM 调用前清理旧工具结果，不修改磁盘转录记录。

### 8.1 核心作用

减少工具输出（执行结果、文件读取、搜索返回）导致的上下文膨胀，降低 Token 成本，延缓压缩触发。

### 8.2 工作原理

1. 等待缓存 TTL 过期（默认 5 分钟）
2. 软修剪超大结果：保留首尾，中间用 `...` 替代
3. 硬清理过期结果：替换为占位符
4. 重置 TTL，复用新缓存

### 8.3 配置启用

```json
{
  "agents": {
    "defaults": {
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "5m"
      }
    }
  }
}
```

- 关闭：`mode: "off"`
- OpenClaw 对 Anthropic 提供商自动启用修剪

### 8.4 修剪 vs 压缩

| 维度 | 会话修剪 | 会话压缩 |
|---|---|---|
| 操作对象 | 仅清理工具结果 | 总结全部对话历史 |
| 存储修改 | 仅内存，不写磁盘 | 写入会话转录记录 |
| 作用时机 | 每次 LLM 调用前 | 上下文溢出时触发 |

## 九、会话压缩（Compaction）

会话压缩是**持久化**优化，当对话接近模型上下文窗口上限时，将旧消息总结为精简条目。

### 9.1 工作原理

1. 旧对话轮次总结为紧凑条目
2. 总结结果写入会话转录
3. 保留最近消息完整内容
4. 工具调用与结果成对保留，不拆分

### 9.2 自动压缩

默认开启，触发条件：

- 会话上下文接近窗口上限
- 模型返回 `context length exceeded` 等溢出错误

压缩前自动提醒智能体将重要信息保存到记忆文件，避免丢失。

### 9.3 手动压缩

聊天内发送：

```bash
/compact 聚焦API设计决策
```

### 9.4 自定义压缩模型

使用更擅长总结的模型处理压缩：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "model": "openrouter/anthropic/claude-sonnet-4-6"
      }
    }
  }
}
```

### 9.5 压缩通知

开启压缩时提示用户：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "notifyUser": true
      }
    }
  }
}
```

## 十、会话工具（Session Tools）

OpenClaw 提供跨会话管理、子智能体编排的工具集，支持会话间交互与后台任务管理。

### 10.1 核心工具清单

| 工具名 | 功能 |
|---|---|
| `sessions_list` | 过滤列出会话（类型、活跃度） |
| `sessions_history` | 读取指定会话转录记录 |
| `sessions_send` | 跨会话发送消息，可等待回复 |
| `sessions_spawn` | 创建隔离子智能体会话（后台任务） |
| `sessions_yield` | 结束当前轮次，等待子智能体结果 |
| `subagents` | 管理子智能体（列出/引导/终止） |
| `session_status` | 查看会话状态，设置会话级模型 |

### 10.2 工具可见性范围

控制智能体可访问的会话权限，默认 `tree`：

- `self`：仅当前会话
- `tree`：当前会话 + 子智能体
- `agent`：当前智能体所有会话
- `all`：全部会话（跨智能体）

沙箱会话强制限制为 `tree` 级别。

### 10.3 子智能体编排

`sessions_spawn` 创建隔离后台会话，非阻塞执行，返回 `runId` 与子会话 ID，支持沙箱强制、模型覆盖、线程绑定。

## 十一、会话管理最佳实践

1. 多用户场景必须开启 `dmScope: per-channel-peer`，防止上下文泄露
2. 长期运行网关配置 `session.maintenance.enforce`，自动清理过期会话
3. 大模型对话组合使用**会话修剪 + 压缩**，平衡上下文质量与 Token 成本
4. 跨渠道协作优先用 `identityLinks + channel docking`，保留上下文不中断
5. 子智能体任务用 `sessions_spawn` 隔离，避免主会话上下文污染
6. 定期用 `/context list` 检查上下文占用，及时手动压缩优化
