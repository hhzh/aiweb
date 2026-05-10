---
title: OpenClaw 记忆系统核心详解
order: 15
---

# OpenClaw 记忆系统核心详解：从设计原则到关键模块

OpenClaw 记忆系统是一套**纯 Markdown 落地、无隐藏运行态、可观测可版本化**的智能体持久记忆体系，以工作区文件为唯一事实源，搭配检索引擎、主动召回、后台固化、自动跟进四大能力，彻底解决智能体 "失忆" 与上下文膨胀问题。本文覆盖基础记忆、三大后端、混合搜索、主动记忆、梦境固化、跟进承诺六大核心模块，完整对齐官方设计规范。

## 一、记忆系统核心设计原则

- **唯一事实源**：所有记忆持久化到磁盘 Markdown 文件，模型只 "记住" 被写入文件的内容，无内存隐状态。

- **分层存储**：长期记忆、每日短期记忆、梦境日志分离，兼顾稳定性与上下文轻量性。

- **插件化后端**：支持 Builtin / QMD / Honcho 三种引擎，按需切换，无缝降级。

- **自动保护**：会话压缩前自动执行记忆刷新，防止关键信息丢失。

- **无感召回**：主动记忆在主回复前自动检索，无需用户显式触发。

## 二、核心记忆文件体系

所有文件存放在**智能体工作区**（默认 `~/.openclaw/workspace`），分为三层结构：

### 2.1 长期记忆（ durable ）

- `MEMORY.md`：持久事实、用户偏好、重要决策、规则约定；**每次私聊会话启动自动加载**，子智能体不加载。

- `IDENTITY.md`/`USER.md`/`SOUL.md`：智能体身份、用户信息、人格边界，作为引导上下文注入。

### 2.2 短期记忆（ daily ）

- `memory/YYYY-MM-DD.md`：按天归档的会话笔记、临时上下文；**默认自动加载当日 + 昨日内容**，会话启动时注入。

### 2.3 梦境与系统记忆

- `DREAMS.md`：梦境 Consolidation 日志、候选摘要、人类可审查的固化记录。

- `memory/.dreams/`：梦境后台状态、阶段信号、索引 checkpoint（机器可读）。

### 2.4 基础记忆工具

- `memory_search`：语义检索相关记忆，支持混合搜索，无视措辞差异匹配意图。

- `memory_get`：精准读取指定记忆文件或行范围，支持截断与安全过滤。

## 三、记忆后端引擎：三大方案选型与配置

OpenClaw 提供三级记忆后端，从极简到企业级，自动兼容与降级。

### 3.1 Builtin（默认，无额外依赖）

- 存储：单智能体 SQLite 库，索引 `MEMORY.md` + `memory/*.md`，分块约 400token 重叠 80token。

- 能力：FTS5 关键词（BM25）+ 向量相似度 = **混合搜索**；支持 CJK trigram 分词；自动检测嵌入提供商。

- 适用：个人部署、轻量化场景、无额外二进制依赖。

- 配置（指定嵌入提供商）：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": { "provider": "openai" }
    }
  }
}
```

### 3.2 QMD（本地 Sidecar，增强检索）

- 定位：本地优先检索增强引擎，BM25 + 向量 + 重排序三合一。

- 增强能力：索引工作区外目录、索引会话转录、查询扩展、全自动本地 GGUF 模型。

- 降级：不可用时无缝切回 Builtin。

- 启用：

```json
{ "memory": { "backend": "qmd" } }
```

### 3.3 Honcho（插件，跨会话用户建模）

- 定位：AI 原生跨会话记忆，自动构建用户画像、多智能体感知、语义检索。

- 能力：跨会话持久、用户偏好建模、父 / 子智能体追踪、托管 / 自托管双模式。

- 启用：

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
openclaw honcho setup
```

### 3.4 三大后端对比表

| 特性 | Builtin | QMD | Honcho |
| --- | --- | --- | --- |
| 依赖 | 无 | qmd 二进制 | 插件 + 服务 |
| 检索 | 混合搜索 | 重排序 + 扩展 | 跨会话语义 |
| 外部索引 | 否 | 是 | 否 |
| 会话索引 | 否 | 是 | 是 |
| 用户建模 | 否 | 否 | 自动 |
| 降级 | — | Builtin | — |
| 适用场景 | 个人默认 | 本地增强 | 团队 / 多会话 |

## 四、记忆搜索 Hybrid Search：向量 + 关键词联合检索

### 4.1 工作原理

并行执行两路检索并合并结果：

1. **向量搜索**：匹配语义含义，适配同义转述。

2. **BM25 关键词**：匹配精确标识符、代码符号、错误串。

### 4.2 支持嵌入提供商

自动检测：OpenAI、Gemini、Voyage、Mistral、DeepInfra；手动指定：Ollama、Local（GGUF）。

### 4.3 质量优化

- **时间衰减**：旧笔记权重递减，常青文件（如 [MEMORY.md](MEMORY.md)）不衰减。

- **MMR 多样性**：减少冗余结果，提升结果覆盖面。

- **多模态**：Gemini 支持图片 / 音频索引与文本检索匹配。

### 4.4 常用命令

```bash
openclaw memory status          # 查看索引与提供商
openclaw memory search "query" # 命令行检索
openclaw memory index --force  # 强制重建索引
```

## 五、Active Memory 主动记忆：回复前自动召回

### 5.1 定位

在主智能体生成回复前，运行**阻塞式子记忆体**，自动召回相关上下文，无需用户 / 主智能体触发，让回复更连贯个性化。

### 5.2 运行条件

插件启用 → 目标智能体 → 允许的会话类型（默认私聊）→ 交互式持久会话。

### 5.3 核心配置（推荐模板）

```json
{
  "plugins": {
    "entries": {
      "active-memory": {
        "enabled": true,
        "config": {
          "agents": ["main"],
          "allowedChatTypes": ["direct"],
          "queryMode": "recent",
          "promptStyle": "balanced",
          "timeoutMs": 15000
        }
      }
    }
  }
}
```

### 5.4 查询模式（速度→质量）

- `message`：仅最新消息，最低延迟。

- `recent`：最新消息 + 短对话尾，默认平衡。

- `full`：完整对话，最高召回质量。

### 5.5 调试

```Plain Text
/verbose on        # 显示主动记忆状态
/trace on          # 显示召回摘要
/active-memory on/off  # 会话级开关
```

## 六、Dreaming 梦境 Consolidation：后台记忆固化

### 6.1 定位

`memory-core` 内置的**后台记忆巩固系统**，将短期高价值笔记提升为长期记忆，保持 `MEMORY.md` 高信噪比，默认关闭、手动启用。

### 6.2 三阶段流水线

1. **Light**：清洗、去重、暂存短期候选，不写入长期记忆。

2. **REM**：提取主题与规律，提供强化信号，不写入。

3. **Deep**：六维加权打分→达标则追加到 `MEMORY.md`，唯一可固化长期记忆的阶段。

### 6.3 启用与调度

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "frequency": "0 3 * * *"
          }
        }
      }
    }
  }
}
```

### 6.4 常用命令

```Plain Text
/dreaming status    # 查看状态
openclaw memory promote --apply  # 手动固化
openclaw memory rem-harness      # 预览 REM 摘要
```

## 七、Commitments inferred 跟进承诺

### 7.1 定位

短期上下文跟进记忆，自动识别对话中的 "未来回访点"，通过心跳投递，介于记忆与定时任务之间。

### 7.2 典型场景

- 提及 "明天面试"→ 事后回访。

- 表示 "疲惫"→ 后续询问休息情况。

- 遗留未闭环事项→ 自动提醒。

### 7.3 启用

```json
{ "commitments": { "enabled": true, "maxPerDay": 3 } }
```

### 7.4 与提醒的区别

- 精确定时提醒 → 用定时任务。

- inferred 自然回访 → 用 Commitments。

### 7.5 管理命令

```bash
openclaw commitments           # 查看待跟进
openclaw commitments dismiss cm_xxx  # 关闭
```

## 八、自动记忆刷新：压缩前的上下文保护

会话压缩开始前，OpenClaw 自动执行一轮**静默记忆刷新**，提醒智能体把未落地的关键信息写入记忆文件，从根源避免压缩导致的信息丢失，默认开启无需配置。

## 九、常用 CLI 与调试命令速查

```bash
# 记忆状态
openclaw memory status --deep
# 检索
openclaw memory search "关键词"
# 索引
openclaw memory index --force
# 梦境
openclaw memory promote --apply
# 跟进承诺
openclaw commitments --all
# 主动记忆
/active-memory status
```

## 十、最佳实践

1. **个人默认**：使用 Builtin + OpenAI 嵌入，足够轻量稳定。

2. **本地优先**：选用 QMD，索引项目文档，完全离线。

3. **团队多会话**：选用 Honcho，自动用户建模与跨会话继承。

4. **长期稳定**：开启 Dreaming 每日固化，避免 `MEMORY.md` 杂乱。

5. **私聊体验**：必开 Active Memory，实现自然无感召回。

6. **安全规范**：记忆文件放入私有 Git，绝不提交 API Key 与会话原文。

---

OpenClaw 记忆系统以**文件透明、插件扩展、自动巩固**为核心，彻底告别黑盒记忆，是构建长期可用、可解释、可维护私人 / 团队智能体的底层基石。
