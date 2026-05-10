# OpenClaw 工具系统：内置能力、安全管控与自定义扩展详解

OpenClaw 工具系统是智能体从**文本生成**走向**实际执行**的核心引擎，通过**Tools（工具）、Skills（技能）、Plugins（插件）** 三层协同架构，提供文件读写、命令执行、浏览器自动化、消息收发、媒体生成、会话编排等全栈能力，并支持精细化安全管控与第三方扩展。本文基于官方全套工具与插件文档，完整覆盖内置工具、配置策略、安全隔离、原生插件、第三方兼容包、依赖解析、技能体系全维度知识点，为部署与开发提供一站式参考。

## 一、工具系统核心三层架构

OpenClaw 工具能力由**三层模块化体系**支撑，每层职责清晰、解耦可扩展，是系统的核心设计原则：

### 1.1 工具（Tools）：执行原子能力

工具是智能体可调用的**类型化函数**，对应具体操作（如 `exec` 执行命令、`read` 读取文件、`browser` 控制浏览器），以结构化函数定义形式提供给模型 API，是所有操作的最小执行单元。

### 1.2 技能（Skills）：工具使用指南

技能是存储于工作区的 `SKILL.md` 文档，在系统提示词中注入，告知智能体**何时、如何、按什么规则使用工具**，包含约束条件、步骤指引、边界限制，让工具调用更规范、更安全。

### 1.3 插件（Plugins）：能力封装包

插件是完整的扩展单元，可注册**工具、技能、渠道、模型提供商、语音、媒体、后台服务**等任意组合能力，分为核心内置插件与第三方社区插件，是系统扩展的标准载体。

### 1.4 三层协同流程

```Plain Text
用户请求 → 技能（指导调用逻辑）→ 工具（执行具体操作）→ 插件（提供能力底座）
```

## 二、内置工具全量清单与功能分类

OpenClaw 提供开箱即用的**内置工具集**，无需安装插件即可使用，覆盖文件、执行、网络、会话、媒体、网关等全场景：

| 工具分组 | 包含工具 | 核心功能 |
|---|---|---|
| **文件系统（group:fs）** | `read`/`write`/`edit`/`apply_patch` | 工作区文件读写、编辑、多区块补丁应用 |
| **运行时执行（group:runtime）** | `exec`/`process`/`code_execution` | Shell 命令执行、后台进程管理、沙箱 Python 分析 |
| **网络工具（group:web）** | `web_search`/`x_search`/`web_fetch` | 网页搜索、平台检索、页面内容抓取 |
| **会话管理（group:sessions）** | `sessions_list`/`sessions_history`/`sessions_send`/`sessions_spawn`/`session_status` | 会话查询、历史读取、跨会话消息、子智能体创建、状态查看 |
| **记忆工具（group:memory）** | `memory_search`/`memory_get` | 记忆检索、精准读取记忆文件 |
| **UI 交互（group:ui）** | `browser`/`canvas` | Chromium 浏览器自动化、节点 UI 驱动 |
| **自动化（group:automation）** | `cron`/`gateway` | 定时任务管理、网关配置更新与重启 |
| **消息通信（group:messaging）** | `message` | 全渠道消息发送 |
| **节点设备（group:nodes）** | `nodes` | 配对设备发现与控制 |
| **多媒体（group:media）** | `image`/`image_generate`/`music_generate`/`video_generate`/`tts` | 图像分析/生成、音乐/视频生成、文本转语音 |
| **智能体管理（group:agents）** | `agents_list` | 智能体列表查询 |
| **网关管控** | `config.*`/`update.run` | 配置查询/补丁、系统自更新 |

> 说明：`bash` 是 `exec` 的兼容别名，工具调用不区分大小写。

## 三、工具配置与安全管控体系

工具系统支持**全局、智能体、提供商**三级管控，遵循**拒绝优先（Deny > Allow）** 原则，实现最小权限安全隔离。

### 3.1 基础允许/拒绝列表

通过 `tools.allow`/`tools.deny` 配置工具权限，支持工具名与分组通配：

```json
{
  "tools": {
    "allow": ["group:fs", "web_search", "session_status"],
    "deny": ["exec", "browser", "canvas"]
  }
}
```

- 优先级：`deny` 强制覆盖 `allow`，即使工具在允许列表中也会被禁用。
- 支持通配符：如 `deny: ["*"]` 禁用所有工具，`allow: ["group:*"]` 允许全部分组。

### 3.2 工具配置文件（Tool Profiles）

工具配置文件是预定义的权限模板，快速批量配置工具权限，支持全局与单智能体覆盖：

| 配置文件 | 包含工具范围 |
|---|---|
| `full` | 无限制（默认） |
| `coding` | 文件、运行时、网络、会话、记忆、定时任务、多媒体全量工具 |
| `messaging` | 消息、会话基础工具 |
| `minimal` | 仅 `session_status` |

配置示例：

```json
{
  "tools": {
    "profile": "coding"
  },
  "agents": {
    "list": [
      {
        "id": "family",
        "tools": {
          "profile": "minimal"
        }
      }
    ]
  }
}
```

### 3.3 提供商专属限制

针对不同模型提供商，设置差异化工具权限，不影响全局配置：

```json
{
  "tools": {
    "profile": "coding",
    "byProvider": {
      "google-antigravity": { "profile": "minimal" },
      "openai/gpt-4o": { "allow": ["group:fs", "sessions_list"] }
    }
  }
}
```

### 3.4 提权安全管控

控制沙箱外高危 `exec` 执行权限，仅允许指定用户/渠道触发：

```json
{
  "tools": {
    "elevated": {
      "enabled": true,
      "allowFrom": {
        "whatsapp": ["+15551234567"],
        "discord": ["123456789"]
      }
    }
  }
}
```

### 3.5 工具分组快捷配置

使用 `group:*` 分组批量管理工具，无需单独配置单个工具：

- `group:fs`：文件操作全套工具
- `group:runtime`：命令执行相关工具
- `group:web`：网络检索工具
- `group:sessions`：会话管理工具
- `group:memory`：记忆检索工具
- `group:openclaw`：所有内置原生工具（排除插件工具）

## 四、原生插件体系：扩展与管理

插件是 OpenClaw 扩展能力的标准形式，与网关进程内运行，支持渠道、模型、工具、技能、服务全维度扩展。

### 4.1 插件核心能力

插件可注册以下能力：

1. 网关 RPC 方法与 HTTP 处理器
2. 智能体工具与自定义技能
3. CLI 命令与自动回复斜杠命令
4. 后台服务与生命周期钩子
5. 消息渠道与模型提供商认证流程

### 4.2 插件管理 CLI 命令

```bash
# 查看插件列表
openclaw plugins list
openclaw plugins list --enabled --verbose

# 安装插件（npm/本地/ClawHub）
openclaw plugins install @openclaw/voice-call
openclaw plugins install ./local-plugin
openclaw plugins install clawhub:official-plugin

# 更新/卸载插件
openclaw plugins update --all
openclaw plugins uninstall <plugin-id> --keep-files

# 插件调试
openclaw plugins inspect <id> --runtime
openclaw plugins doctor
```

### 4.3 插件配置结构

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["voice-call", "memory-core"],
    "deny": ["untrusted-plugin"],
    "load": {
      "paths": ["~/custom-extensions"]
    },
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "accountSid": "",
          "authToken": ""
        }
      }
    },
    "slots": {
      "memory": "memory-core"
    }
  }
}
```

### 4.4 插件插槽（Exclusive Slots）

插槽是互斥能力分类，同一插槽仅允许一个插件生效：

- `memory`：记忆引擎插件（`memory-core`/`memory-lancedb`）
- `contextEngine`：上下文引擎插件

配置方式：`plugins.slots.<slot> = <plugin-id>`，设为 `none` 禁用该类别插件。

### 4.5 插件依赖解析规则

1. 安装时处理依赖：运行时不执行包管理，避免安全风险
2. 依赖归属：插件包自行管理 `dependencies`，OpenClaw 仅负责加载
3. 安装路径：
    - npm 包：`~/.openclaw/npm/`
    - Git 仓库：`~/.openclaw/git/`
    - 本地插件：直接引用，不自动安装依赖
4. 修复命令：`openclaw doctor --fix` 清理旧依赖、补全缺失插件。

### 4.6 官方核心插件清单

内置插件随核心包分发，无需单独安装：

- 模型提供商：`openai`/`anthropic`/`google`/`ollama` 等全平台支持
- 渠道插件：`whatsapp`/`telegram`/`discord`/`slack`/`msteams`
- 功能插件：`memory-core`/`browser`/`web-readability`/`file-transfer`
- 语音媒体：`elevenlabs`/`azure-speech`/`tts-local-cli`

## 五、第三方兼容包（Bundles）：跨生态兼容

OpenClaw 支持直接兼容 **Codex、Claude、Cursor** 三大生态插件包，无需重写即可使用现有能力，称为 Bundles。

### 5.1 兼容包核心价值

无需改造第三方插件，自动映射为 OpenClaw 原生能力，降低扩展成本。

### 5.2 支持映射的能力

| 源生态 | 映射能力 | 支持状态 |
|---|---|---|
| 全生态 | 技能内容、MCP 工具 | 完全支持 |
| Claude/Cursor | 命令集、配置文件 | 完全支持 |
| Codex | 钩子包（HOOK 格式） | 完全支持 |
| Claude | LSP 服务器、嵌入式配置 | 完全支持 |
| 全生态 | 自动化规则、UI 样式 | 仅检测不执行 |

### 5.3 MCP 工具集成

兼容包的 MCP（Model Context Protocol）工具自动合并到嵌入式运行时，支持两种传输方式：

1. **Stdio**：子进程启动 MCP 服务

```json
{
  "mcp": {
    "servers": {
      "my-server": {
        "command": "node",
        "args": ["server.js"]
      }
    }
  }
}
```

2. **HTTP**：连接远程 MCP 服务

```json
{
  "mcp": {
    "servers": {
      "remote-server": {
        "url": "http://localhost:3000/mcp",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer ${TOKEN}"
        }
      }
    }
  }
}
```

### 5.4 兼容包安装与检测

```bash
# 安装本地/归档兼容包
openclaw plugins install ./claude-bundle
openclaw plugins install ./codex-bundle.tgz

# 检测兼容包格式
openclaw plugins list # 显示 Format: bundle + 子类型
```

### 5.5 安全隔离特性

兼容包比原生插件更安全：

- 不加载任意运行时代码，仅解析技能与配置
- 路径强制限制在插件根目录，禁止越权访问
- MCP 工具以子进程运行，不侵入网关进程。

## 六、技能系统：工具的使用规范

技能是连接智能体与工具的**行为指南**，模块化管理工具使用规则，避免无节制调用。

### 6.1 技能加载优先级

冲突时按以下优先级覆盖（从高到低）：

1. 工作区技能：`<workspace>/skills/`（最高）
2. 全局托管技能：`~/.openclaw/skills/`
3. 插件内置技能
4. 核心内置技能（最低）

### 6.2 技能文件结构

每个技能是独立目录，包含 `SKILL.md`，支持 YAML 前置元数据与使用说明，智能体启动时自动注入提示词。

### 6.3 技能与工具的关系

- 工具：**能做什么**
- 技能：**该怎么做、不能做什么**
- 插件：**提供工具与技能的载体**

## 七、安全最佳实践

1. **最小权限原则**：公共/群组智能体使用 `minimal` 配置文件，禁用 `exec`/`browser` 高危工具
2. **拒绝优先配置**：先用 `deny` 禁用高危能力，再用 `allow` 开放必要工具
3. **插件白名单**：仅安装官方/可信插件，启用 `plugins.allow` 列表
4. **兼容包优先**：第三方扩展优先使用 Bundles，降低代码注入风险
5. **提权严格限制**：`tools.elevated` 仅允许指定用户触发高危命令
6. **定期审计**：用 `openclaw plugins inspect` 校验插件权限，清理无用扩展
7. **沙箱强制**：多用户/公共场景启用智能体沙箱，隔离文件与网络访问

## 八、常见问题排查

1. **工具调用失败**
    - 检查 `tools.deny` 是否包含目标工具
    - 确认配置文件未覆盖权限
    - 查看提供商专属限制是否禁用工具

2. **插件加载失败**
    - 执行 `openclaw plugins doctor` 检测依赖
    - 确认插件 ID 与配置一致
    - 重启网关生效配置

3. **兼容包不生效**
    - 用 `openclaw plugins inspect` 查看是否识别为 bundle
    - 确认技能文件在 `skills/` 或 `commands/` 目录
    - 重启网关加载映射能力

4. **MCP 工具不可用**
    - 检查传输配置（stdio/http）是否正确
    - 确认端口/命令无冲突
    - 查看工具名是否为 `serverName__toolName` 格式

## 九、总结

OpenClaw 工具系统以**三层架构**为核心，内置全场景原子能力，配合**精细化权限管控**实现安全隔离，通过**原生插件 + 第三方兼容包**打造开放生态，兼顾开箱即用与自定义扩展。无论是个人助理的轻量工具调用，还是企业级智能体的权限严控、多能力扩展，均可通过标准化配置实现，是 OpenClaw 成为可落地、可管控、可扩展的企业级 AI 智能体平台的核心基石。
