# OpenClaw 消息（Messages）机制：路由、队列与流式处理全解

OpenClaw 消息机制是连接多渠道入口、智能体运行时、会话状态与投递出口的**核心中枢**，完整覆盖入站预处理、路由绑定、队列调度、运行时转向、流式分块、进度草稿、重试自愈全链路能力。它以**会话串行、全局限流、流式优先、安全投递**为设计核心，确保多渠道并发消息不乱序、不重复、不阻塞，同时提供极致流畅的交互体验。本文基于官方全套消息机制文档，完整拆解路由、队列、流式、分块、进度、重试六大核心模块。

---

## 一、消息全生命周期高层流转

所有入站消息遵循统一的标准化执行链路，是理解整个机制的基础：

```Plain Text
入站消息 → 去重 → 防抖 → 路由/绑定 → 生成会话键 → 进入命令队列 → 智能体运行（流式+工具） → 出站回复（渠道限制+分块）
```

所有行为可通过三级配置精准控制：

1. 全局：`messages.*`（前缀、队列、群聊行为）

2. 智能体默认：`agents.defaults.*`（块流式、分块默认值）

3. 渠道覆盖：`channels.<channel>.*`（上限、流式开关）

---

## 二、入站消息预处理：去重、防抖与上下文解析

入站预处理是消息不乱序、不重复、不冗余的第一道防线。

### 2.1 入站去重（Inbound Dedupe）

渠道重连后可能重复投递同一条消息，OpenClaw 基于**渠道 + 账号 + 对话 + 会话 + 消息 ID** 构建短期缓存，确保重复消息不会触发重复智能体运行，彻底避免重复回复。

### 2.2 入站防抖（Inbound Debouncing）

同一发送者快速连发的纯文本消息会被**合并为单次智能体轮次**，媒体 / 附件与控制命令立即 flush 不防抖，大幅减少 LLM 调用次数。

**配置示例**：

```json
{
  "messages": {
    "inbound": {
      "debounceMs": 2000,
      "byChannel": {
        "whatsapp": 5000,
        "slack": 1500,
        "discord": 1500
      }
    }
  }
}
```

- 生效范围：按**渠道 + 对话**隔离

- 规则：纯文本防抖；媒体 / 指令立即执行；最终使用最新消息作为回复线程依据

### 2.3 消息体三分离：保证指令与上下文隔离

OpenClaw 严格拆分三类消息体，避免指令污染模型上下文：

1. **Body**：送入智能体的提示文本，包含渠道信封与历史上下文

2. **CommandBody**：原始用户文本，用于指令解析

3. **RawBody**：CommandBody 兼容别名

### 2.4 历史上下文注入与限制

非私聊消息会自动添加**发送者前缀**，保证实时与排队消息格式一致；历史缓冲区仅包含未触发运行的消息，已入转录记录的内容不重复注入。

**历史长度限制**：

```json
// 全局默认，0=禁用
"messages.groupChat.historyLimit": 10
// 渠道覆盖
"channels.slack.historyLimit": 8
```

---

## 三、消息路由与会话绑定规则

路由决定消息归属，会话决定上下文隔离，二者共同保证多用户 / 多渠道数据安全。

### 3.1 会话所有权与存储

- 会话由 **Gateway 独占拥有**，不由客户端管理

- 私聊合并为智能体主会话键；群组 / 频道使用独立会话键

- 会话存储位置：`~/.openclaw/agents/<agentId>/sessions/`

### 3.2 会话键生成规则

- 私聊：`agent:<agentId>:<mainKey>`

- 群组 / 频道：`agent:<agentId>:<channel>-<peerId>`

- 多智能体：按 `agentId` 完全隔离，无跨智能体上下文泄露

### 3.3 多设备与跨渠道映射

多设备 / 多渠道可映射到同一会话，但历史不会全量同步回所有客户端；**推荐使用单一主设备**进行长对话，Control UI/TUI 为事实源。

---

## 四、命令队列：并发控制与会话串行

命令队列是 OpenClaw 处理并发消息的**核心调度层**，解决多消息竞争会话、触发速率超限、上下文错乱问题。

### 4.1 队列核心设计目标

- 同一会话**同一时间仅运行一个智能体轮次**，避免状态竞争

- 全局限流，保护模型提供商与渠道 API 限额

- 支持多种调度策略，适配不同交互场景

### 4.2 队列工作原理

1. 按**会话键**生成专属队列（lane），保证单会话串行

2. 全局队列（默认 `main`）控制总并发：`agents.defaults.maxConcurrent`

3. 子智能体队列：`subagents.maxConcurrent`

4. 等待超 2s 且 verbose 开启时，输出排队日志

5. 输入指示器立即触发，不影响用户体验

### 4.3 六大队列模式详解（全局 / 渠道可配）

|模式|运行中行为|后续行为|适用场景|
|---|---|---|---|
|**steer（默认）**|下一个模型边界一次性注入所有消息|不可用时回退 followup|连续指令、实时修正|
|**queue（遗留）**|模型边界逐条注入|不可用时回退 followup|兼容旧逻辑|
|**steer-backlog**|同 steer|保留消息用于后续轮次|需要即时响应 + 后续确认|
|**followup**|不注入当前运行|排队等待下一轮|严格按顺序处理全部消息|
|**collect（推荐）**|不注入当前运行|防抖窗口合并为单轮|用户分段发消息、批量处理|
|**interrupt（遗留）**|终止当前运行|无|强时效性、紧急打断|

### 4.4 队列配置与会话级覆盖

**全局配置**：

```json
{
  "messages": {
    "queue": {
      "mode": "collect",
      "debounceMs": 1000,
      "cap": 20,
      "drop": "summarize",
      "byChannel": { "discord": "collect" }
    }
  }
}
```

- `cap`：单会话最大排队消息数

- `drop`：溢出策略（old/new/summarize），summarize 会将丢弃消息合成提示

**会话级覆盖**：

```Plain Text
/queue collect debounce:2s cap:25 drop:summarize
/queue default  # 重置
```

### 4.5 全局并发与会话隔离

- 默认：`maxConcurrent:4`、`subagents.maxConcurrent:8`

- 额外 lane：`cron`/`node` 后台任务，不阻塞入站回复

- 无外部依赖，纯 TypeScript+Promise 实现

---

## 五、队列转向（Steering）：运行时消息注入

转向是**运行中注入新消息**的机制，不中断正在执行的工具调用，保证工具结果与请求配对。

### 5.1 转向运行时边界

转向**不中断正在执行的工具**，仅在以下边界触发：

1. 助手请求工具调用

2. 工具批处理完成

3. 轮次结束事件触发

4. 排空转向消息

5. 追加为用户消息，进入下一次 LLM 调用

### 5.2 转向模式与行为

- `steer`：批量注入所有排队消息（默认，效率最高）

- `queue`：逐条注入（兼容遗留）

- 不可转向时自动回退到 `followup` 队列

### 5.3 批处理与防抖

- Pi 运行时：自然批量，不使用防抖

- Codex 运行时：使用 `messages.queue.debounceMs` 作为静默窗口，批量发送

---

## 六、流式输出：块流式与预览流式双层架构

OpenClaw 提供**两套独立流式层**，分别适配渠道投递与预览体验，无真实 Token 粒度流式投递。

### 6.1 块流式（Block Streaming）：渠道消息分块发送

将模型输出按规则切分为块，**实时作为正常渠道消息发送**，非 Token 增量。

**核心配置**：

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on",
      "blockStreamingBreak": "text_end",
      "blockStreamingChunk": {
        "minChars": 500,
        "maxChars": 2000,
        "breakPreference": "paragraph"
      }
    }
  }
}
```

- `blockStreamingBreak`：

    - `text_end`：块完成立即发送（流式）

    - `message_end`：整段完成后批量发送（非流式）

- 代码围栏保护：绝不拆分 ``` 代码块，强制拆分时自动闭合重开

### 6.2 预览流式（Preview Streaming）：草稿实时更新

仅更新**临时草稿消息**，不发送多条气泡，适配 Telegram/Discord/Slack。

**四大模式**：

|模式|效果|适用场景|
|---|---|---|
|**off**|仅发送最终答案|安静频道|
|**partial**|单草稿持续替换为最新文本|看答案逐字生成|
|**block**|按大块追加更新|大段文本预览|
|**progress**|状态草稿→最终答案|工具密集、长时任务|

**渠道映射**：

- Telegram/Discord：progress 映射为 partial

- Slack：支持全部模式，可开启原生流式 API

### 6.3 分块算法：边界保护与大小控制

由 `EmbeddedBlockChunker` 实现：

1. 下限：缓冲≥minChars 才发送（强制除外）

2. 上限：优先在 maxChars 前拆分，强制则在 maxChars 分割

3. 拆分优先级：段落→换行→句子→空格→硬拆分

4. 渠道硬上限：`channels.<channel>.textChunkLimit` 优先覆盖

### 6.4 块合并（Coalescing）与拟人延迟

- **合并**：等待 idleMs 静默间隙，合并小块，减少刷屏

- **拟人延迟**：块之间添加随机停顿，更接近人类输入

```json
{
  "agents": {
    "defaults": {
      "blockStreamingCoalesce": { "idleMs": 300 },
      "humanDelay": "natural" // natural/custom/off，800-2500ms
    }
  }
}
```

---

## 七、进度草稿（Progress Drafts）：长任务状态可视化

进度草稿专为**工具密集型长时任务**设计，仅展示一条状态消息，最终替换为答案，保持聊天整洁。

### 7.1 核心价值

- 仅在任务持续≥5s 或第二条工作事件时显示

- 用一条消息展示工具进度，不刷屏

- 最终安全替换为答案，无残留草稿

### 7.2 启用配置

```json
{
  "channels": {
    "discord": {
      "streaming": { "mode": "progress" }
    }
  }
}
```

### 7.3 标签与进度行控制

- **标签**：auto 自动选取 / 固定标签 / 自定义池 / 隐藏

- **进度行**：来自真实工具事件，同 `/verbose` 格式

- **细节等级**：`explain`（简洁默认）/`raw`（原始命令，调试用）

- **行数限制**：`maxLines:4`，自动压缩避免重排

### 7.4 渠道适配与收尾

- Discord/Telegram：发送→编辑→替换为答案

- Slack：原生流式或可编辑帖子

- 含媒体 / 审批 / 多块时，走安全回退：发送新消息，停止更新草稿

---

## 八、推理可见性与消息格式

### 8.1 推理可见性

- 命令：`/reasoning on|off|stream`

- 流式模式：Telegram 可将推理写入草稿气泡

- 推理内容**计入 Token**，仅控制展示与否

### 8.2 回复前缀级联

优先级：渠道账号 > 渠道 > 全局

```json
"messages.responsePrefix": "[AI] "
```

### 8.3 回复线程与引用

- `replyToMode` 控制回复引用行为

- 群聊自动绑定线程，保证上下文关联

---

## 九、消息重试策略：瞬态故障自愈

### 9.1 核心目标

- 按**单次 HTTP 请求**重试，不重试多步骤流程

- 保证顺序，不重复非幂等操作

- 指数退避 + 抖动，避免惊群效应

### 9.2 默认参数

- 尝试次数：3

- 最大延迟：30000ms

- 抖动：10%

- Telegram 最小延迟：400ms；Discord：500ms

### 9.3 差异化重试规则

- **模型提供商**：408/409/429/5xx 可重试，超长等待自动触发故障转移

- **Discord**：仅 429 限流重试，使用 `retry_after`

- **Telegram**：429 / 超时 / 连接错误重试，解析错误降级为纯文本

### 9.4 配置示例

```json
{
  "channels": {
    "telegram": {
      "retry": {
        "attempts": 3,
        "minDelayMs": 400,
        "maxDelayMs": 30000,
        "jitter": 0.1
      }
    },
    "discord": {
      "retry": {
        "attempts": 3,
        "minDelayMs": 500,
        "maxDelayMs": 30000,
        "jitter": 0.1
      }
    }
  }
}
```

---

## 十、全链路配置速查

|模块|配置路径|核心键|
|---|---|---|
|入站防抖|messages.inbound|debounceMs、byChannel|
|队列模式|messages.queue|mode、debounceMs、cap、drop|
|块流式|agents.defaults|blockStreaming*|
|预览流式|channels.*.streaming|mode、progress、toolProgress|
|拟人延迟|agents.defaults|humanDelay|
|重试|channels.*.retry|attempts、delay、jitter|

---

## 十一、最佳实践

1. **默认队列用 collect**：合并连发消息，降低 LLM 成本

2. **工具密集任务用 progress 模式**：保持聊天整洁，提升体验

3. **私聊开启 blockStreaming**：实时回复，群组关闭避免刷屏

4. **队列 cap 设 15–20**：防止消息堆积，drop 使用 summarize

5. **拟人延迟设 natural**：多气泡回复更自然

6. **渠道单独配置重试**：适配不同平台限流规则

7. **长对话开启历史限制**：避免上下文膨胀

---

## 十二、总结

OpenClaw 消息机制以**会话串行、队列调度、双层流式、安全重试**为核心，构建了多渠道并发场景下**稳定、高效、体验流畅**的消息处理体系。从入站去重到出站分块，从运行时转向到进度可视化，每一环都经过精细化设计，既保证上下文安全隔离，又最大化交互流畅度，是 OpenClaw 支撑多渠道 AI 助理的底层基石。
