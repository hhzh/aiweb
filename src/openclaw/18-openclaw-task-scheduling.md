---
title: OpenClaw 任务调度详解
order: 18
---

# OpenClaw 自动化：任务调度详解

OpenClaw 自动化体系是支撑智能体**脱离人工交互、实现自主运行**的核心引擎，以**精确定时调度、周期性批量巡检、后台任务追踪、多步骤工作流、常设自治权限、事件驱动钩子、对话跟进承诺**七大能力为骨架，覆盖定时报告、定时巡检、事件响应、流程编排、长期自治全场景。本文基于官方全套自动化文档，完整拆解调度规则、执行模型、状态管理、配置范式、CLI 操作与最佳实践，做到无死角覆盖、可直接落地。

---

## 一、自动化体系总览与核心选型指南

OpenClaw 自动化由**7 大核心组件**协同工作，所有脱离即时对话的后台执行均由这套体系承载：

1. **Cron（定时任务）**：精确时间调度，支持一次性提醒与周期性任务

2. **Heartbeat（心跳）**：固定周期批处理，复用主会话上下文

3. **Background Tasks（后台任务）**：所有分离执行的任务台账与状态记录

4. **Task Flow（工作流）**：多步骤持久化编排，支持分支与重试

5. **Standing Orders（常设指令）**：赋予智能体长期自治权限与执行规则

6. **Hooks（钩子）**：事件触发脚本，响应会话 / 网关 / 命令生命周期

7. **Inferred Commitments（跟进承诺）**：从对话中提取的自然回访提醒

### 1.1 快速选型决策表（官方标准）

| 业务场景 | 推荐方案 | 核心原因 |
| --- | --- | --- |
| 每日 9 点准时发送日报 | Cron | 精确时间、隔离执行 |
| 20 分钟后一次性提醒 | Cron（--at） | 精确单点定时 |
| 每周深度分析任务 | Cron | 独立会话、可指定专用模型 |
| 每 30 分钟查收收件箱 | Heartbeat | 批处理、复用主上下文 |
| 监控日历即将到来的事件 | Heartbeat | 周期性感知、无任务记录 |
| 面试后主动回访 | Inferred Commitments | 对话派生、同智能体同渠道 |
| 查看子智能体 / ACP 运行状态 | Background Tasks | 全量分离任务台账 |
| 多步骤研究→总结流水线 | Task Flow | 持久化、可追踪、支持重试 |
| 会话重置时执行脚本 | Hooks | 生命周期事件触发 |
| 每次工具调用前校验 | Plugin Hooks | 进程内拦截、无侵入 |
| 回复前自动合规检查 | Standing Orders | 全局注入、永久生效 |

### 1.2 Cron 与 Heartbeat 核心差异

| 维度 | Cron 定时任务 | Heartbeat 心跳 |
| --- | --- | --- |
| 时间精度 | 精确（cron 表达式 / 一次性时间） | 近似（默认 30 分钟） |
| 会话上下文 | 全新隔离 / 共享主会话 | 完整主会话上下文 |
| 任务记录 | 必创建 | 不创建 |
| 结果投递 | 渠道 / Webhook / 静默 | 内联到主会话 |
| 适用场景 | 日报、提醒、后台作业 | 收件箱、日历、通知批巡检 |

---

## 二、Cron 定时任务：精确调度引擎

Cron 是 Gateway 内置**精确调度器**，持久化存储任务，支持一次性提醒、周期性表达式、Webhook 触发，是 OpenClaw 定时执行的标准方案。

### 2.1 核心特性

- 运行于 Gateway 进程内，非模型侧调度

- 任务持久化存储：`~/.openclaw/cron/jobs.json`

- 支持两种执行模式、三种调度类型、三种投递方式

- 支持按智能体绑定、模型覆盖、时区指定

### 2.2 两种执行模式

#### （1）主会话模式（systemEvent）

- 入队系统事件，在下一次心跳执行

- 复用主会话完整上下文

- payload 固定为 `systemEvent`

- wakeMode：`now`（立即唤醒）/`next-heartbeat`（等待下一次心跳）

#### （2）隔离模式（isolated，推荐）

- 独立会话：`cron:<jobId>`，不污染主会话

- 每次运行全新会话，无历史上下文残留

- 前缀标识：`[cron:<jobId> 任务名]`，可追踪

- 支持独立模型、思考等级、超时配置

- 默认自动投递结果

### 2.3 三种调度类型

1. **at（一次性）**：ISO8601 时间戳，默认执行后自动删除

2. **every（固定间隔）**：毫秒级周期执行

3. **cron（5 位表达式）**：`分 时 日 月 周`，支持 IANA 时区

### 2.4 三种投递模式

1. **announce**：直接投递到目标渠道，主会话同步摘要（隔离模式默认）

2. **webhook**：POST 结果到指定 URL，支持 Bearer Token 鉴权

3. **none**：静默执行，无任何投递

### 2.5 完整配置

```json
{
  "cron": {
    "enabled": true,
    "store": "~/.openclaw/cron/jobs.json",
    "maxConcurrentRuns": 1,
    "webhookToken": "your-webhook-token"
  }
}
```

### 2.6 常用 CLI 示例

```bash
# 一次性提醒（20分钟后，主会话立即唤醒）
openclaw cron add \
  --name "提交报销" \
  --at "20m" \
  --session main \
  --system-event "提醒：提交报销单" \
  --wake now

# 每日早7点日报（隔离模式，投递到Slack）
openclaw cron add \
  --name "早报" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "汇总昨夜更新" \
  --announce \
  --channel slack \
  --to "channel:C1234567890"

# 绑定指定智能体
openclaw cron add --name "运维巡检" --cron "0 6 * * *" --session isolated --message "检查队列" --agent ops

# 查看任务列表/运行记录
openclaw cron list
openclaw cron runs --id <jobId>

# 手动运行/编辑/删除
openclaw cron run <jobId>
openclaw cron edit <jobId> --model opus
openclaw cron remove <jobId>
```

### 2.7 重试与异常规则

- 一次性任务：执行后自动删除，失败不重试

- 周期性任务：失败指数退避重试（30s→1m→5m→15m→60m）

- 成功后重置退避计数

- Telegram 话题投递：使用 `-100xxx:topic:123` 格式

---

## 三、Heartbeat 心跳：周期性批量巡检

Heartbeat 是**默认每 30 分钟执行一次的主会话轮次**，用于批量执行轻量巡检，不创建任务记录，不延长会话过期时间。

### 3.1 核心机制

- 执行时机：默认每 30 分钟，可配置

- 执行环境：主会话，完整上下文

- 不产生任务记录，不刷新会话存活时间

- Cron 运行时自动跳过心跳，避免冲突

### 3.2 配置与 Checklist

心跳逻辑写在工作区 `HEARTBEAT.md`，作为巡检清单：

```markdown
# 心跳检查清单
1. 检查未读邮件
2. 检查日历即将开始的事件
3. 检查待跟进承诺
4. 检查系统服务状态
```

空文件直接跳过，无任务时标记为 `empty-heartbeat-file`

### 3.3 与 Cron 配合

Cron 负责**精确时间**，Heartbeat 负责**批量感知**，二者互补：

- Cron：9 点发送日报

- Heartbeat：每 30 分钟查收邮件、日历

---

## 四、Background Tasks 后台任务：执行台账与状态追踪

Background Tasks 是**所有分离执行操作的统一台账**，只记录、不调度，用于审计、监控、异常排查。

### 4.1 哪些操作会生成任务

| 来源 | 运行时类型 | 触发时机 | 默认通知策略 |
| --- | --- | --- | --- |
| ACP 后台运行 | acp | 创建子 ACP 会话 | done_only |
| 子智能体编排 | subagent | sessions_spawn 创建 | done_only |
| Cron 执行（所有） | cron | 每次 Cron 运行 | silent |
| CLI 命令 | cli | openclaw agent 命令 | silent |
| 媒体生成 | cli | music_generate/video_generate | silent |

### 4.2 任务生命周期

```Plain Text
queued（排队）→ running（运行中）→ terminal（终止态）
```

终止态包括：

- succeeded（成功）、failed（失败）、timed_out（超时）

- cancelled（取消）、lost（丢失，5 分钟无状态）

### 4.3 通知策略

- `done_only`（默认）：仅终止态通知

- `state_changes`：所有状态变更通知

- `silent`：完全静默

### 4.4 存储与自动清理

- 存储：`$OPENCLAW_STATE_DIR/tasks/runs.sqlite`（SQLite）

- 自动清理：终止态保留 7 天，扫描器每 60 秒运行一次

- 自动 reconcile：5 分钟无状态标记为 lost

### 4.5 常用 CLI

```bash
openclaw tasks list # 全量任务
openclaw tasks list --runtime cron --status running # 过滤
openclaw tasks show <taskId> # 详情
openclaw tasks cancel <taskId> # 取消
openclaw tasks notify <taskId> state_changes # 修改通知
openclaw tasks audit # 健康检查
openclaw tasks maintenance --apply # 清理
```

### 4.6 聊天内看板

任意会话发送 `/tasks`，查看当前会话关联的后台任务。

---

## 五、Task Flow 工作流：多步骤持久化编排

Task Flow 是**构建在后台任务之上的流程编排层**，用于多步骤、可恢复、可追踪的复杂自动化流程。

### 5.1 适用场景

- 单步骤后台任务 → 用普通 Task

- 多步骤顺序 / 分支流程 → 用 Task Flow

- 外部任务统一视图 → 用 Mirrored 模式

### 5.2 两种同步模式

#### （1）Managed 托管模式（推荐）

Flow 全权管理生命周期：创建步骤任务→等待完成→自动推进，支持重启恢复。
示例：每周报告流程：采集数据→生成报告→投递。

#### （2）Mirrored 镜像模式

仅观测外部任务（Cron/CLI/ 子智能体），同步状态不控制执行，用于统一视图。

### 5.3 核心特性

- 持久化状态，重启不丢失进度

- 修订追踪，并发冲突检测

- 取消粘性：取消后跨重启仍保持取消状态

### 5.4 常用 CLI

```bash
openclaw tasks flow list # 流程列表
openclaw tasks flow show <flowId> # 详情
openclaw tasks flow cancel <flowId> # 取消流程（含所有子任务）
```

---

## 六、Standing Orders 常设指令：智能体自主权限底座

Standing Orders 是**赋予智能体长期自治权限的规则集**，注入到每一次会话，结合 Cron 实现完全自主运行。

### 6.1 核心价值

告别逐次指令：从 "每次让发报告" 变为 "你负责每周报告，异常才找我"。

### 6.2 存放位置

固定写入工作区 `AGENTS.md`（每次会话自动注入），也可单独写 `standing-orders.md` 引用。

### 6.3 标准结构

```markdown
## Program: 每周状态报告
**Authority（权限）**：采集数据、生成报告、投递干系人
**Trigger（触发）**：每周五 16 点（Cron 强制执行）
**Approval Gate（审批）**：标准报告无需审批，异常标注人工复核
**Escalation（升级）**：数据源不可用、指标异常（>2σ）立即上报

### 执行步骤
1. 从数据源拉取指标
2. 对比上周与目标
3. 生成报告到 Reports/weekly
4. 投递到指定渠道
5. 记录完成日志

### 禁止行为
- 不向外部发送报告
- 不修改源数据
- 不隐瞒异常指标
```

### 6.4 与 Cron 协同

Standing Orders 定义**能做什么**，Cron 定义**何时做**：

```bash
openclaw cron add \
  --name daily-inbox-triage \
  --cron "0 8 * * 1-5" \
  --tz Asia/Shanghai \
  --session isolated \
  --message "按常设指令执行每日收件箱分类，未知项升级给所有者" \
  --announce --channel whatsapp --to "+15551234567"
```

### 6.5 执行范式：Execute-Verify-Report

所有任务必须遵循：

1. **Execute**：实际执行

2. **Verify**：验证结果（文件存在 / 消息发送成功）

3. **Report**：告知执行结果
禁止只确认不执行、只执行不验证。

---

## 七、Hooks 钩子：事件驱动扩展机制

Hooks 是**响应生命周期事件的轻量脚本**，无侵入扩展 OpenClaw 行为，分为内部钩子与插件钩子。

### 7.1 事件类型

1. **Command 命令事件**：`/new`、`/reset`、`/stop`

2. **Agent 事件**：`agent:bootstrap`（引导注入前）

3. **Gateway 事件**：`gateway:startup`（网关启动）

4. **Plugin 钩子**：`tool_result_persist`（工具结果拦截）

### 7.2 发现路径（优先级从高到低）

1. 工作区钩子：`<workspace>/hooks/`

2. 托管钩子：`~/.openclaw/hooks/`

3. 捆绑钩子：`<openclaw>/dist/hooks/bundled/`

### 7.3 标准结构

每个钩子是目录，包含：

- `HOOK.md`：YAML 元数据 + 说明

- `handler.ts`：执行逻辑

示例 `HOOK.md`：

```markdown
---
name: session-memory
description: 新建会话时保存上下文快照
metadata:
  {
    "openclaw": {
      "emoji": "💾",
      "events": ["command:new"],
      "requires": { "config": ["workspace.dir"] }
    }
  }
---
```

### 7.4 官方内置钩子

1. **session-memory**：`/new` 时保存会话快照到工作区记忆

2. **bootstrap-extra-files**：引导阶段注入额外配置文件

3. **command-logger**：全局命令审计日志，输出到 `~/.openclaw/logs/commands.log`

4. **boot-md**：网关启动时执行 `BOOT.md`

### 7.5 配置与 CLI

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": true }
      }
    }
  }
}
```

```bash
openclaw hooks list # 列出所有钩子
openclaw hooks enable session-memory # 启用
openclaw hooks check # 检查可用性
openclaw hooks info <hookId> # 详情
```

### 7.6 自定义钩子开发

1. 创建目录：`~/openclaw/hooks/my-hook`

2. 编写 `HOOK.md` + `handler.ts`

3. 启用并重启网关

4. 触发对应事件测试

---

## 八、Inferred Commitments 对话跟进承诺

Inferred Commitments 是**从对话中自动提取的短期回访记忆**，通过心跳投递，介于提醒与记忆之间。

### 8.1 典型场景

- 用户提到 "明天面试"→ 事后回访

- 用户表示疲惫→ 后续问候

- 未闭环事项→ 自动提醒

### 8.2 与 Cron 提醒区别

- 精确定时提醒 → Cron

- 自然语境派生回访 → Commitments

### 8.3 启用配置

```json
{
  "commitments": {
    "enabled": true,
    "maxPerDay": 3
  }
}
```

### 8.4 管理 CLI

```bash
openclaw commitments # 查看待跟进
openclaw commitments dismiss cm_xxx # 关闭
```

---

## 九、全链路协同与配置实战

### 9.1 标准自动化协同流程

1. Standing Orders 注入权限边界

2. Cron 触发定时执行

3. 隔离会话运行，生成 Background Task

4. 多步骤走 Task Flow 编排

5. 事件触发 Hooks 扩展

6. Heartbeat 批量巡检

7. Commitments 对话回访

### 9.2 生产级完整配置

```json
{
  "cron": {
    "enabled": true,
    "maxConcurrentRuns": 2,
    "webhookToken": "sk-xxx"
  },
  "commitments": {
    "enabled": true,
    "maxPerDay": 3
  },
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": true },
        "boot-md": { "enabled": true }
      }
    }
  },
  "heartbeat": {
    "intervalMinutes": 30,
    "skipWhenBusy": true
  }
}
```

---

## 十、CLI 命令速查表

| 模块 | 常用命令 |
| --- | --- |
| Cron | openclaw cron add/list/run/edit/remove/runs |
| Tasks | openclaw tasks list/show/cancel/notify/audit |
| Task Flow | openclaw tasks flow list/show/cancel |
| Hooks | openclaw hooks list/enable/check/info |
| Commitments | openclaw commitments/dismiss |
| 系统 | openclaw status /tasks /new /reset |

---

## 十一、最佳实践与安全规范

1. **定时任务优先隔离模式**：避免污染主会话历史

2. **常设指令最小权限**：从窄权限开始，逐步放开

3. **钩子轻量化**：禁止阻塞事件，异步后台执行

4. **任务通知分级**：核心任务 state_changes，常规任务 done_only

5. **多智能体绑定**：运维 / 业务分开，隔离权限与数据

6. **审计必开**：command-logger 记录所有命令操作

7. **媒体与重型任务**：用隔离 Cron，不影响交互响应

---

## 十二、故障排查指南

1. **Cron 不执行**

    - 检查 cron.enabled=true，Gateway 持续运行

    - 校验时区、表达式、会话模式

    - 查看 `openclaw cron runs` 运行日志

2. **任务标记为 lost**

    - 运行时状态丢失（网关重启）

    - 5 分钟无状态更新，自动标记

    - 用 `tasks maintenance` 修复

3. **Hooks 不触发**

    - 确认钩子启用、事件匹配

    - 检查依赖

    - 重启网关加载新钩子

4. **投递失败**

    - 校验渠道 ID、话题格式、权限

    - 开启 `delivery.bestEffort=true` 避免任务失败

    - Webhook 检查 Token 与 URL 可达

---

## 总结

OpenClaw 自动化体系以**Cron 精确定时、Heartbeat 周期巡检、Tasks 状态台账、Task Flow 流程编排、Standing Orders 自治权限、Hooks 事件响应、Commitments 对话回访**为闭环，实现从简单提醒到复杂自主运营的全覆盖。它让智能体从 "被动应答" 升级为 "自主运行"，是个人助理、团队助理、企业数字员工的核心基础设施。
