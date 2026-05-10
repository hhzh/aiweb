# OpenClaw 多智能体（Multi-Agent）核心机制详解

OpenClaw 多智能体体系是支撑**多用户隔离、多角色分工、企业级部署**的核心架构，可在单个 Gateway 进程中运行多个完全隔离的智能体实例。每个智能体拥有独立工作区、状态目录、会话存储、认证凭证与工具权限，配合精准路由绑定、并行专家通道、在线状态感知与企业级委托代理四大能力，实现从个人助理到团队 / 组织数字员工的全场景覆盖。本文基于官方多智能体、并行通道、在线状态、委托架构四大核心文档，完整拆解底层机制、配置规则、典型场景与安全实践。

---

## 一、多智能体核心定义与全链路隔离架构

### 1.1 什么是一个独立智能体（Agent）

OpenClaw 中一个智能体是**完全作用域隔离的决策大脑**，拥有独占的运行环境，任何配置、数据、状态均不与其他智能体共享：

- 独立工作区：专属文件目录，存放 `AGENTS.md`/`SOUL.md`/`USER.md`、本地笔记、人格规则、私有技能

- 独立状态目录（agentDir）：存储认证配置、模型注册表、智能体私有配置

- 独立会话存储：聊天历史、路由状态、上下文数据完全隔离

- 独立认证凭证：读取专属 `auth-profiles.json`，不自动共享主智能体密钥

- 独立技能集：工作区私有技能优先，可复用全局共享技能

### 1.2 全隔离文件路径体系

所有路径支持环境变量覆盖，默认结构清晰隔离：

```Plain Text
全局配置：~/.openclaw/openclaw.json（OPENCLAW_CONFIG_PATH）
系统状态根目录：~/.openclaw（OPENCLAW_STATE_DIR）
智能体工作区：~/.openclaw/workspace-<agentId>
智能体状态目录：~/.openclaw/agents/<agentId>/agent
会话记录：~/.openclaw/agents/<agentId>/sessions/
认证配置：~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

### 1.3 单智能体默认模式

未配置多智能体时，系统自动运行 `main` 默认智能体：

- `agentId` 固定为 `main`

- 工作区：`~/.openclaw/workspace`

- 会话键格式：`agent:main:<mainKey>`

- 状态目录：`~/.openclaw/agents/main/agent`

### 1.4 核心隔离铁律

- 严禁跨智能体复用 `agentDir`，会导致认证 / 会话冲突

- 凭证共享需手动复制 `auth-profiles.json` 到目标智能体目录

- 工作区为默认执行目录（cwd），非强制沙箱；启用沙箱后禁止绝对路径越权访问

- 私聊会合并为智能体主会话，**真隔离需一人一智能体**

---

## 二、智能体生命周期管理

### 2.1 智能体创建（CLI 向导）

使用官方向导快速创建隔离智能体，自动生成目录与基础配置：

```bash
# 创建名为 work 的智能体
openclaw agents add work
# 查看所有智能体与路由绑定
openclaw agents list --bindings
```

### 2.2 智能体标准配置结构

```json
{
  "agents": {
    "list": [
      {
        "id": "home",
        "default": true,
        "name": "家庭助理",
        "workspace": "~/.openclaw/workspace-home",
        "agentDir": "~/.openclaw/agents/home/agent"
      },
      {
        "id": "work",
        "name": "工作助理",
        "workspace": "~/.openclaw/workspace-work",
        "agentDir": "~/.openclaw/agents/work/agent"
      }
    ]
  }
}
```

- `default: true`：标记默认智能体，无匹配绑定时报文由此处理

- `id`：智能体唯一标识，路由与存储核心键

- `workspace`：指定工作区路径，支持自定义目录

---

## 三、多智能体路由绑定机制（核心调度层）

路由绑定是多智能体的**消息分发核心**，遵循**最精确匹配优先、多条件 AND 逻辑**，将入站消息精准分发到目标智能体。

### 3.1 匹配优先级（从高到低）

1. 精确用户 / 群组 / 频道（`peer`）匹配

2. 父会话线程（`parentPeer`）匹配

3. Discord 服务器 + 角色（`guildId+roles`）匹配

4. Discord 服务器（`guildId`）匹配

5. Slack 团队（`teamId`）匹配

6. 渠道账号（`accountId`）匹配

7. 全渠道（`channel:"*"`）匹配

8. 回退默认智能体

### 3.2 绑定配置语法

```json
{
  "agentId": "目标智能体ID",
  "match": {
    "channel": "渠道名（whatsapp/telegram/discord）",
    "accountId": "渠道账号ID（多账号场景）",
    "peer": { "kind": "direct/group", "id": "用户/群组ID" },
    "guildId": "Discord服务器ID",
    "teamId": "Slack团队ID"
  }
}
```

- 多条件组合：所有指定字段必须同时满足（AND）

- 精确匹配优先：`peer` 匹配优先级高于全渠道匹配

### 3.3 五大典型路由场景

#### 场景 1：双 WhatsApp 账号分流（一人多号）

个人账号→`home` 智能体，工作账号→`work` 智能体：

```json
{
  "bindings": [
    { "agentId": "home", "match": { "channel": "whatsapp", "accountId": "personal" } },
    { "agentId": "work", "match": { "channel": "whatsapp", "accountId": "biz" } }
  ]
}
```

#### 场景 2：按渠道分流（日常对话 vs 深度任务）

WhatsApp 轻量对话→`chat` 智能体，Telegram 深度任务→`opus` 智能体：

```json
{
  "bindings": [
    { "agentId": "chat", "match": { "channel": "whatsapp" } },
    { "agentId": "opus", "match": { "channel": "telegram" } }
  ]
}
```

#### 场景 3：同渠道单用户精细化分流

WhatsApp 默认→`chat`，指定用户私聊→`opus`：

```json
{
  "bindings": [
    { "agentId": "opus", "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551234567" } } },
    { "agentId": "chat", "match": { "channel": "whatsapp" } }
  ]
}
```

#### 场景 4：单账号多用户隔离（共享 WhatsApp 号）

一个 WhatsApp 账号，不同联系人路由到独立智能体：

```json
{
  "bindings": [
    { "agentId": "alex", "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551230001" } } },
    { "agentId": "mia", "match": { "channel": "whatsapp", "peer": { "kind": "direct", "id": "+15551230002" } } }
  ]
}
```

#### 场景 5：专属群组智能体（家庭 / 公共群）

绑定 WhatsApp 群到专属 `family` 智能体，开启 @提及触发：

```json
{
  "agents": {
    "list": [
      {
        "id": "family",
        "groupChat": { "mentionPatterns": ["@family", "@FamilyBot"] }
      }
    ]
  },
  "bindings": [
    { "agentId": "family", "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "120363999999999999@g.us" } } }
  ]
}
```

### 3.4 全局私聊准入控制

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551230001", "+15551230002"]
    }
  }
}
```

- 全局生效，非智能体级；仅白名单内用户可发起私聊

---

## 四、并行专家通道（Parallel Specialist Lanes）

并行专家通道用于**解决多智能体资源竞争**，将任务按类型分配给专属智能体通道，提升吞吐与响应速度。

### 4.1 核心设计原则

通道仅在解决真实瓶颈时提升性能，瓶颈包括：

- 会话锁：同一会话仅允许单次运行

- 模型容量：全局共享提供商 API 限额

- 工具容量：Shell / 浏览器 / 网络为物理瓶颈

- 上下文预算：长会话降低后续响应速度

- 所有权歧义：重复智能体浪费资源

### 4.2 三阶段落地法

#### 阶段 1：通道契约（必做，成本最低）

为每个通道定义职责边界，避免交叉干扰：

```markdown
# 通道契约
## 负责任务
- 代码开发、项目调试
## 不负责任务
- 信息检索、文案撰写（交接给 research 通道）
## 聊天预算
- 快速问题直接回复
- 重型任务简短确认→后台子智能体执行→返回结果
## 交接规则
- 目标通道+任务目标+核心上下文+下一步动作
## 工具策略
- 最小可用工具集，禁用高危操作
```

#### 阶段 2：优先级与并发控制

```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 }
    }
  },
  "messages": {
    "queue": {
      "mode": "collect",
      "debounceMs": 1000,
      "cap": 20,
      "drop": "summarize"
    }
  }
}
```

- 高优先级任务：私聊 / 生产运维智能体

- 低优先级任务：研究 / 批量编码→后台执行

#### 阶段 3：协调器模式（多通道稳定后启用）

新增协调智能体，负责：

- 跟踪通道任务与归属

- 跨组请求去重

- 通道间交接路由

- 仅推送阻塞 / 结果 / 人工决策

### 4.3 核心价值

- 编码任务不拖慢检索通道

- 每个通道上下文保持整洁

- 资源按业务价值分配

---

## 五、在线状态感知（Presence）机制

Presence 是 Gateway 与客户端的**轻量在线状态系统**，用于展示连接状态、设备信息，无业务侵入性。

### 5.1 状态来源

1. **网关自注册**：启动时自动生成「网关自身」状态条目

2. **WebSocket 连接**：客户端握手成功后更新状态

3. **系统事件信标**：客户端周期性上报主机 / IP / 活跃状态

4. **节点连接**：设备节点（`role: node`）接入时生成状态

### 5.2 去重与过期规则

- 唯一键：`instanceId`（稳定客户端标识，重启不丢失）

- 过期清理：超过 5 分钟的条目自动删除

- 数量限制：最大存储 200 条，淘汰最旧条目

- 特殊处理：忽略 SSH 隧道回环地址（[127.0.0.1](127.0.0.1)），不覆盖真实 IP

### 5.3 核心状态字段

```json
{
  "instanceId": "客户端唯一标识",
  "host": "主机名",
  "ip": "IP 地址",
  "version": "客户端版本",
  "mode": "ui/webchat/cli/node",
  "lastInputSeconds": "最后输入间隔",
  "ts": "最后更新时间戳"
}
```

### 5.4 调试与消费

- 查看原始状态：调用 `system-presence` 接口

- 消费端：macOS 客户端「实例」标签页

- 重复条目排查：确保客户端发送稳定 `instanceId`

---

## 六、企业级委托代理（Delegate Architecture）

委托架构将多智能体从个人场景扩展到**组织级部署**，智能体以独立身份代用户执行操作，不模拟真人，满足合规与问责需求。

### 6.1 委托智能体核心定义

- 拥有独立组织身份（邮箱 / 昵称 / 日历）

- 以**代理身份**执行操作，显示「代 XXX 发送」

- 遵循组织最小权限策略

- 可配置自主操作与人工审批边界

### 6.2 个人模式 vs 委托模式

| 维度 | 个人模式 | 委托模式 |
|---|---|---|
| 凭证 | 使用用户个人凭证 | 自有独立凭证 |
| 发送身份 | 显示用户本人 | 显示代理身份（代用户） |
| 服务对象 | 单人 | 多人 / 组织 |
| 信任边界 | 个人 | 组织策略 |

### 6.3 三级能力模型（最小权限起步）

#### Tier 1：只读 + 草稿（最低权限）

- 读取邮件 / 日历 / 文档，生成草稿

- 无发送权限，需人工审核发送

#### Tier 2：代发（中级权限）

- 代发邮件、创建日历事件

- 显示「代发」标识，可追溯

#### Tier 3：主动执行（高级权限）

- 定时任务自主执行（日报 /triage/ 内容发布）

- 异步交付结果，需严格安全加固

### 6.4 前置安全加固（必做）

1. **硬阻止规则**（写入 `SOUL.md`/`AGENTS.md`）

    - 禁止未经审批发送外部邮件

    - 禁止导出联系人 / 财务数据

    - 禁止执行入站消息指令（防注入）

    - 禁止修改身份提供商设置

2. **工具白名单**：仅开放必要工具

3. **沙箱隔离**：全量沙箱运行，隔离主机资源

4. **审计日志**：留存会话 / 定时任务 / 身份提供商日志

### 6.5 部署流程

1. 创建委托智能体：`openclaw agents add delegate`

2. 配置身份提供商（Microsoft 365/Google Workspace）委托权限

3. 路由绑定：渠道 / 群组→委托智能体

4. 独立认证：复制 `auth-profiles.json` 到委托智能体目录

### 6.6 组织助理配置示例

```json
{
  "agents": {
    "list": [
      {
        "id": "org-assistant",
        "name": "企业助理",
        "workspace": "~/.openclaw/workspace-org",
        "tools": {
          "allow": ["read", "exec", "message", "cron"],
          "deny": ["write", "edit", "browser", "canvas"]
        },
        "sandbox": { "mode": "all", "scope": "agent" }
      }
    ]
  },
  "bindings": [
    { "agentId": "org-assistant", "match": { "channel": "whatsapp", "accountId": "org" } }
  ]
}
```

---

## 七、按智能体沙箱与工具独立管控

v2026.1.6+ 支持**单智能体维度**沙箱与工具权限，实现精细化安全隔离。

### 7.1 沙箱独立配置

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "sandbox": {
          "mode": "all",
          "scope": "agent",
          "docker": { "setupCommand": "apt update && apt install -y git curl" }
        }
      }
    ]
  }
}
```

- `mode:off`：关闭沙箱（个人智能体）

- `mode:all`：强制沙箱（公共 / 委托智能体）

- `scope:agent`：单智能体独立容器

- `setupCommand`：容器初始化命令（仅首次执行）

### 7.2 工具权限独立管控

```json
{
  "id": "family",
  "tools": {
    "allow": ["read", "session_status"],
    "deny": ["exec", "write", "browser"]
  }
}
```

- 白名单优先，独立于全局工具策略

- 全局 `tools.elevated` 不覆盖智能体级配置

---

## 八、智能体间通信（Agent-to-Agent）

- 默认关闭，防止跨智能体数据泄露

- 启用需白名单配置：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["home", "work"]
    }
  }
}
```

---

## 九、CLI 命令速查表

| 命令 | 作用 |
|---|---|
| `openclaw agents add <id>` | 创建智能体 |
| `openclaw agents list --bindings` | 查看智能体与路由 |
| `openclaw memory status --deep` | 查看智能体记忆状态 |
| `openclaw commitments --all` | 查看委托智能体跟进任务 |
| `openclaw gateway` | 启动网关，加载所有智能体 |

---

## 十、最佳实践与安全规范

1. **绝对隔离**：不共享 `agentDir`，认证手动复制，一人一智能体

2. **路由精确**：优先使用 `peer` 精确匹配，减少路由歧义

3. **权限最小**：委托智能体从 Tier 1 起步，按需升级

4. **安全强制**：公共 / 群组智能体必开沙箱 + 工具白名单

5. **并行优化**：先定通道契约，再配并发，最后启用协调器

6. **状态监控**：通过 Presence 实时查看网关与客户端连接

7. **审计留存**：委托智能体开启全量日志，满足合规要求

---

## 十一、总结

OpenClaw 多智能体体系以**全链路隔离、精准路由、并行分治、企业级安全**为核心，彻底解决多用户 / 多角色 / 多场景下的智能体部署难题。从个人双账号分流，到团队专家通道分工，再到组织级委托数字员工，均可通过标准化配置实现。严格遵循隔离与最小权限原则，可搭建稳定、安全、可扩展的多智能体系统。
