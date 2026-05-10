---
title: OpenClaw Skills 技能系统详解
order: 14
---

# OpenClaw Skills 技能系统：模块化扩展、生态管理与安全规范

OpenClaw Skills 技能系统是智能体能力**模块化扩展**的核心标准层，基于 AgentSkills 兼容规范，以 `SKILL.md` 为统一载体，实现 "工具调用标准化、能力复用可插拔、生态分发可治理"。它既是智能体的**操作手册**，也是能力扩展的**最小单元**，联动工具系统、插件体系、ClawHub 生态与斜杠命令，构成完整的可扩展、可管控、可审计的能力扩展架构。本文覆盖技能格式、加载优先级、配置管控、命令联动、生态分发、自定义开发、OpenProse 集成与全链路安全规范，完整对齐官方文档并补充实践最佳实践。

## 一、技能系统核心定位与设计理念

### 1.1 什么是技能（Skill）

技能是 OpenClaw 中**教智能体如何使用工具**的标准化单元，由一个目录 + 一份 `SKILL.md` 构成：

- YAML 前置元数据：声明身份、依赖、兼容性、命令行为

- Markdown 正文：用自然语言编写工具使用步骤、约束、触发条件、最佳实践

- 无代码门槛：纯文本编写，无需开发能力即可自定义

### 1.2 核心设计原则

1. **声明式规范**：全部信息在 `SKILL.md` 中声明，运行时自动解析

2. **优先级覆盖**：同名技能按路径优先级自动覆盖，支持灵活定制

3. **依赖门控**：自动检测系统、环境、配置依赖，不满足则不加载

4. **生态化分发**：通过 ClawHub 实现技能的搜索、安装、更新、发布

5. **安全隔离**：支持沙箱运行、密钥注入、权限最小化，防范注入风险

6. **无侵入扩展**：不修改核心代码，通过文件与配置完成能力扩展

### 1.3 技能与工具 / 插件的关系

- **工具**：执行原子操作（`read`/`exec`/`browser`）

- **技能**：告诉智能体**何时、如何、按什么规则**调用工具

- **插件**：封装技能 + 工具 + 渠道 + 服务的完整扩展包

## 二、技能加载路径与优先级规则

OpenClaw 从多路径加载技能，**高优先级路径自动覆盖低优先级同名技能**，支持全局共享、智能体专属、插件内置三种粒度。

### 2.1 标准加载路径（优先级从高到低）

1. **工作区技能（最高）**：`<workspace>/skills/` → 仅当前智能体可用，个性化定制

2. **托管 / 共享技能**：`~/.openclaw/skills/` → 本机所有智能体共享

3. **插件内置技能**：启用的插件中声明的技能目录 → 插件启用后加载

4. **核心捆绑技能（最低）**：随 OpenClaw 安装包内置 → 基础能力

### 2.2 额外技能目录

可通过配置追加自定义共享目录，优先级低于捆绑技能：

```json
{
  "skills": {
    "load": {
      "extraDirs": ["~/common-skills", "~/team-skills"]
    }
  }
}
```

### 2.3 多智能体技能隔离

- **专属技能**：放在智能体工作区 `skills` 目录，仅该智能体可见

- **共享技能**：放在 `~/.openclaw/skills`，所有智能体可见

- 同名冲突仍遵循：**工作区 > 托管 > 插件 > 捆绑**

### 2.4 插件技能加载

插件在 `openclaw.plugin.json` 中声明 `skills` 目录，启用插件时自动加载，参与优先级规则：

```json
{
  "skills": ["./skills"]
}
```

## 三、SKILL.md 标准格式与元数据详解

`SKILL.md` 是技能的唯一入口文件，采用 **YAML frontmatter + Markdown 正文** 结构，严格遵循 AgentSkills 规范。

### 3.1 必填字段（最小可用结构）

```markdown
---
name: image-generator
description: 基于 Gemini 生成与编辑图片
---
# 图片生成技能
当用户需要生成图片、修改图片时，调用 image_generate 工具...
```

- `name`：唯一标识（snake_case/kebab-case），用于配置与命令调用

- `description`：一句话描述，智能体判断是否触发的核心依据

### 3.2 可选高级字段

| 字段 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `homepage` | string | - | 技能官网，展示在技能面板 |
| `user-invocable` | bool | true | 是否暴露为用户斜杠命令 |
| `disable-model-invocation` | bool | false | 是否排除在模型提示词外（仅命令调用） |
| `command-dispatch` | string | - | 设为 `tool` 可直接路由到工具，跳过模型 |
| `command-tool` | string | - | 配合 `command-dispatch:tool`，指定目标工具 |
| `command-arg-mode` | string | raw | 参数传递模式，默认透传原始参数 |

### 3.3 加载门控元数据（metadata.openclaw）

用于运行时自动判断是否加载，支持系统、依赖、环境、配置过滤：

```markdown
---
name: gemini-cli
description: Gemini CLI 编码与搜索助手
metadata:
  {
    "openclaw": {
      "emoji": "♊️",
      "os": ["darwin", "linux"],
      "requires": {
        "bins": ["gemini"],
        "env": ["GEMINI_API_KEY"],
        "config": ["browser.enabled"]
      },
      "primaryEnv": "GEMINI_API_KEY",
      "install": [{"id": "brew", "kind": "brew", "formula": "gemini-cli"}]
    }
  }
---
```

- `os`：限定支持系统（darwin/linux/win32）

- `requires.bins`：必须存在的系统命令

- `requires.env`：必须存在的环境变量

- `requires.config`：必须开启的配置项

- `install`：自动安装指引（brew/node/go/download）

- `always: true`：跳过所有门控，强制加载

### 3.4 命令直连工具配置（无模型转发）

```markdown
---
name: prose-run
user-invocable: true
command-dispatch: tool
command-tool: open_prose
---
# OpenProse 运行技能
直接运行 .prose 工作流文件
```

发送 `/prose-run file.prose` 直接调用工具，不经过 LLM 推理。

## 四、技能加载管控与全局配置

所有技能相关配置集中在 `~/.openclaw/openclaw.json` 的 `skills` 节点，支持全局开关、单技能覆盖、热重载、环境注入。

### 4.1 全局配置项

```json
{
  "skills": {
    "allowBundled": ["gemini", "peekaboo"],
    "load": {
      "watch": true,
      "watchDebounceMs": 250,
      "extraDirs": ["~/shared-skills"]
    },
    "install": {
      "preferBrew": true,
      "nodeManager": "pnpm"
    },
    "entries": {}
  }
}
```

- `allowBundled`：仅允许指定的捆绑技能，其余禁用

- `load.watch`：开启文件监听，修改 `SKILL.md` 自动热重载

- `install.nodeManager`：技能依赖安装使用的包管理器

### 4.2 单技能覆盖配置

通过 `skills.entries.<skillKey>` 对单个技能做启用、密钥、环境注入：

```json
{
  "skills": {
    "entries": {
      "image-generator": {
        "enabled": true,
        "apiKey": "sk-xxx",
        "env": {
          "GEMINI_API_KEY": "sk-xxx"
        },
        "config": {
          "model": "gemini-2.0-flash"
        }
      },
      "deprecated-skill": { "enabled": false }
    }
  }
}
```

- `enabled: false`：强制禁用技能

- `apiKey`：便捷注入 `primaryEnv` 声明的密钥

- `env`：会话内临时注入环境变量，运行后恢复

- `config`：自定义技能参数

### 4.3 会话快照与热重载

- 会话启动时快照可用技能列表，同一会话复用

- 开启 `watch` 后，修改 `SKILL.md` 自动刷新快照，下一轮生效

- 远程节点（macOS 节点）适配：Linux 网关可加载 macOS 专属技能

### 4.4 沙箱环境技能适配

沙箱内不继承主机环境与依赖：

1. 主机检测 `requires.bins`，沙箱内需单独安装

2. 通过 `sandbox.docker.setupCommand` 安装依赖：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "apt update && apt install -y gemini-cli"
        }
      }
    }
  }
}
```

3. 沙箱环境变量使用 `agents.defaults.sandbox.docker.env` 注入

## 五、技能与斜杠命令联动机制

技能可直接映射为聊天斜杠命令，实现**一键触发、快捷操作**，分为通用命令与原生命令。

### 5.1 技能命令生成规则

- `user-invocable: true`（默认）自动生成命令

- 通用命令：`/skill <name> [input]`，全渠道可用

- 原生命令：Discord/Telegram 注册为平台原生命令，自动补全

### 5.2 核心命令体系

1. **技能通用命令**

    - `/skill <name> 参数`：手动触发指定技能

    - `/skills list`：列出当前加载的所有技能

    - `/skills reload`：手动刷新技能列表（关闭 watch 时）

2. **动态技能命令**
技能可注册专属命令，如 OpenProse 技能注册 `/prose`：

    ```Plain Text
    /prose run workflow.prose
    /prose examples
    ```

3. **命令权限控制**
技能命令遵循全局命令授权：

    - `commands.allowFrom`：限定可调用的用户 / 渠道

    - `commands.useAccessGroups`：启用渠道白名单

### 5.3 指令（Directives）与技能区分

- 指令（`/think`/`/verbose`/`/model`）：系统控制，剥离后不进入模型

- 技能命令：业务能力，进入模型或直连工具

## 六、ClawHub 技能生态：分发与生命周期管理

ClawHub 是 OpenClaw **官方公共技能 registry**，提供搜索、安装、更新、发布、同步全链路生态能力，官网：[clawhub.ai](https://clawhub.ai)。

### 6.1 ClawHub 核心定位

- 技能发现：关键词 + 向量双搜索，精准匹配需求

- 版本管理：语义化版本，支持回滚

- 社区共享：公开技能库，安全审核

- 备份同步：一键上传本地技能，跨设备同步

### 6.2 ClawHub CLI 安装与初始化

```bash
# 全局安装 CLI
npm i -g clawhub
# 登录（浏览器/令牌）
clawhub login
clawhub login --token YOUR_TOKEN
```

### 6.3 常用操作命令

1. **搜索技能**

```bash
clawhub search "图片生成"
clawhub search "code-review" --limit 10
```

2. **安装技能**（默认安装到当前目录 `./skills`，适配工作区）

```bash
clawhub install ai-ppt-generator
clawhub install ai-ppt-generator --version 1.0.0
clawhub install ./local-skill-folder
```

3. **更新技能**

```bash
clawhub update ai-ppt-generator
clawhub update --all
```

4. **发布 / 同步技能**

```bash
# 发布单个技能
clawhub publish ./my-skill --slug my-skill --version 1.0.0 --tags "image,ai"
# 批量同步本地技能
clawhub sync --all --changelog "更新依赖版本"
```

5. **查看已安装技能**

```bash
clawhub list
```

### 6.4 技能存储与锁定

- 安装记录：`./.clawhub/lock.json`，追踪版本与哈希

- 内容校验：更新时对比本地与仓库哈希，防止意外覆盖

- 离线使用：安装后完全本地运行，不依赖网络

## 七、自定义技能开发：从零到发布

### 7.1 开发最小步骤

1. **创建技能目录**

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-greeting
cd ~/.openclaw/workspace/skills/hello-greeting
```

2. **编写 SKILL.md**

```markdown
---
name: hello-greeting
description: 发送个性化问候，支持称呼与场景
user-invocable: true
---
# 问候技能
当用户需要问候、打招呼时，根据参数生成友好回复。
支持参数：姓名、场景（日常/工作/节日）
示例：
用户：帮我问候小明
回复：小明你好呀！
```

3. **生效与验证**

```bash
# 新会话生效
/new
# 或重启网关
openclaw gateway restart
# 查看技能是否加载
openclaw skills list
```

4. **测试调用**

```bash
# 聊天触发
你好，生成问候语
# 命令触发
/skill hello-greeting 你好
```

### 7.2 技能开发最佳实践

1. **描述精准**：`description` 写明触发条件，提升调用准确率

2. **步骤清晰**：正文用步骤化指令，降低模型理解成本

3. **依赖声明**：所有系统 / 环境 / 配置依赖写入 `metadata`

4. **安全约束**：高危工具（`exec`）增加权限校验与输入过滤

5. **兼容性标注**：写明支持系统、模型、插件依赖

6. **示例丰富**：提供输入输出示例，减少歧义

## 八、OpenProse 工作流与技能系统集成

OpenProse 是**Markdown 优先的跨平台 AI 工作流格式**，以插件形式集成到技能系统，支持多智能体编排、并行执行、可复用工作流。

### 8.1 启用 OpenProse

```bash
openclaw plugins enable open-prose
openclaw gateway restart
```

### 8.2 OpenProse 技能命令

```bash
# 查看帮助
/prose help
# 运行工作流
/prose run research.prose
/prose run https://url/workflow.prose
# 查看示例
/prose examples
```

### 8.3 .prose 文件格式（技能联动）

```markdown
# 多智能体研究总结
input topic: "AI 技能系统"
agent researcher:
  model: sonnet
  prompt: 专业研究，标注来源
agent writer:
  model: opus
  prompt: 精简总结，输出 markdown
parallel:
  研究结果 = session:researcher 研究 {topic}
  初稿 = session:writer 总结 {topic}
session 合并结果生成最终报告
context: {研究结果, 初稿}
```

### 8.4 OpenProse 与技能映射

| OpenProse 能力 | OpenClaw 技能 / 工具 |
|---|---|
| 创建子会话 | `sessions_spawn` |
| 文件读写 | `read`/`write` |
| 网页获取 | `web_fetch` |
| 工作流运行 | OpenProse 技能 |

## 九、技能系统安全规范与风险防控

技能系统支持全链路安全管控，防范第三方技能恶意代码、命令注入、密钥泄露、越权操作。

### 9.1 第三方技能安全原则

1. **先审查后启用**：阅读 `SKILL.md` 与相关文件，确认无恶意逻辑

2. **最小权限**：禁用不必要工具，限制 `exec`/`browser` 等高风险能力

3. **沙箱强制**：公共 / 多用户场景，技能强制运行在沙箱

4. **禁止硬编码密钥**：密钥通过配置 `env`/`apiKey` 注入，不写入文件

### 9.2 密钥与环境安全

1. **配置注入**：使用 `skills.entries.<skill>.env`/`apiKey`，不暴露到日志 / 提示词

2. **会话级注入**：环境变量仅在当前智能体运行周期生效，运行后自动恢复

3. **沙箱隔离**：沙箱内不继承主机密钥，单独配置 `sandbox.docker.env`

### 9.3 高危技能防控

1. **命令过滤**：`exec` 技能校验输入，禁止 `rm -rf`/`mkfs` 等高危命令

2. **白名单机制**：`tools.allow` 仅开放必要工具，`deny` 阻断高危

3. **提权管控**：`tools.elevated` 限定可执行高危命令的用户

### 9.4 审计与排查

1. **技能加载审计**：`openclaw skills list` 查看已加载技能

2. **配置校验**：`openclaw config validate` 检查技能配置合法性

3. **日志排查**：开启 `verbose` 查看技能加载、门控判断、命令调用日志

## 十、Token 开销与性能优化

技能会注入系统提示词，需控制体积与数量，优化上下文占用。

### 10.1 Token 消耗计算

- 基础开销：195 字符（技能列表启用即存在）

- 单技能开销：97 字符 + 名称 / 描述 / 路径长度

- 估算：约 4 字符 = 1 Token，单技能约 25 Token

### 10.2 性能优化方法

1. **精简技能数量**：禁用不使用的技能，减少注入体积

2. **压缩描述**：`description` 简洁明了，避免冗余

3. **按需加载**：通过 `metadata` 门控，非必要不加载

4. **热重载替代重启**：开启 `watch`，避免重启网关

## 十一、常见问题与排查方案

1. **技能不加载**

    - 检查 `enabled: false`

    - 验证 `requires` 依赖（命令 / 环境 / 配置）

    - 查看优先级，是否被高优先级覆盖

    - 重启网关或 `/new` 新会话

2. **斜杠命令不生效**

    - 确认 `user-invocable: true`

    - 检查命令授权 `commands.allowFrom`

    - 原生命令需重启网关注册

3. **沙箱内技能运行失败**

    - 沙箱内缺少依赖，补充 `setupCommand`

    - 环境变量未注入沙箱，配置 `sandbox.docker.env`

    - 权限不足，开启沙箱完整权限

4. **ClawHub 安装失败**

    - 检查网络与登录状态

    - 目录权限，确保可写入 `./skills`

    - 使用 `--force` 强制覆盖冲突文件

5. **热重载不生效**

    - 确认 `skills.load.watch: true`

    - 检查文件路径是否在监听列表

    - 修改后等待 `watchDebounceMs`（默认 250ms）

## 十二、总结

OpenClaw Skills 技能系统是**低门槛、高扩展、强管控**的智能体能力扩展标准，以 `SKILL.md` 统一格式、优先级加载、配置化管控、ClawHub 生态分发、安全隔离为核心，实现：

- **平民化扩展**：无需代码，纯文本编写自定义能力

- **生态化复用**：ClawHub 共享优质技能，降低重复开发

- **企业级管控**：权限、沙箱、密钥、审计全链路安全

- **无缝联动**：与工具、插件、命令、工作流深度整合

无论是个人助理的个性化能力，还是团队 / 企业的标准化技能包，均可通过技能系统快速落地，是 OpenClaw 从 "聊天模型" 升级为 "执行引擎" 的关键基础设施。
