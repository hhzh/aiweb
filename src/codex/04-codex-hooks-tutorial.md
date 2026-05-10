# codex hooks 使用教程｜生命周期钩子实战，解锁Codex定制化能力

在使用 OpenAI Codex 进行 AI 编程时，默认的运行流程往往难以满足个性化或企业级的定制需求——比如会话日志自定义、敏感信息拦截、命令执行校验等。而 Codex Hooks（钩子）作为官方提供的可扩展框架，能够让开发者在 Codex 生命周期的关键节点注入自定义脚本，实现流程管控、功能增强与安全加固。本文基于官方文档，从零讲解 Hooks 的启用、配置、核心事件与实战示例，所有代码可直接复制落地，帮助开发者快速解锁 Codex 的定制化潜力。
## 一、核心认知：Codex Hooks 是什么？

Codex Hooks 是一套用于扩展 Codex 运行逻辑的框架，本质是「生命周期事件拦截器」——它允许你在 Codex 会话的不同阶段（如会话启动、工具调用、用户提交提示等），自动执行自定义脚本，实现各类个性化需求。

### 核心价值

- 日志与分析：将会话数据同步至自定义日志/分析引擎，实现操作可追溯；

- 安全管控：扫描用户提示中的敏感信息（如 API Key），避免泄露；

- 自动化操作：自动总结会话内容生成持久化记忆，或执行自定义校验；

- 场景定制：在特定目录下自定义提示词，适配不同项目的开发规范；

- 权限增强：配合 Codex Rules 与沙箱，构建更精细的权限管控体系。

### 关键特性

- 多配置形式：支持 `hooks.json` 文件与 `config.toml` 内联配置两种方式；

- 并发执行：同一事件的多个匹配钩子会并发运行，互不干扰、无法相互阻止；

- 分层加载：支持全局、项目级、企业级多层配置，加载时自动合并；

- 版本兼容：目前已支持 6 类核心生命周期事件，部分增强版 Codex 已扩展至 18 种事件，对齐 Claude Code 的钩子能力。

## 二、前置准备：启用 Codex Hooks

Hooks 功能默认处于关闭状态，需先在 `config.toml` 中启用功能开关，这是所有 Hooks 配置的前提。

```toml
# 打开 config.toml（全局路径：~/.codex/config.toml）
[features]
codex_hooks = true  # 启用 Hooks 功能，必须设置为 true

```

启用后，Codex 启动时会自动扫描所有激活配置层中的 Hooks 配置，无需额外重启操作（修改 Hooks 配置后需重启 Codex 生效）。

## 三、Hooks 配置基础：存放位置与格式

Codex 会在「激活的配置层」中寻找 Hooks 配置，支持两种格式（`hooks.json` 和 `config.toml` 内联），推荐按使用场景选择对应存放位置。

### 3.1 常用存放路径（优先级无高低，自动合并）

- 全局配置（所有项目生效）：`~/.codex/hooks.json` 或 `~/.codex/config.toml`（内联配置）；

- 项目配置（仅当前项目生效）：`项目根目录/.codex/hooks.json` 或 `项目根目录/.codex/config.toml`（内联配置）；

- 企业配置（强制生效）：通过 `requirements.toml` 配置托管 Hooks，用于团队统一管控。

⚠️ 注意：项目级 Hooks 仅在项目的 `.codex/` 目录被标记为「信任」时才会加载，未信任项目会自动跳过项目级 Hooks，仅加载全局 Hooks，保障安全。

### 3.2 两种配置格式（二选一，推荐 hooks.json）

Hooks 配置分为三个层级：「钩子事件 → 匹配器组 → 钩子处理器」，以下是两种格式的完整示例，可直接复制修改使用。

#### 格式1：hooks.json（推荐，结构清晰）

```json
{
  "hooks": {
    "SessionStart": [  // 钩子事件（会话启动）
      {
        "matcher": "startup|resume",  // 匹配器（筛选事件触发条件）
        "hooks": [  // 钩子处理器（事件触发时执行的操作）
          {
            "type": "command",  // 处理器类型（目前仅支持 command）
            "command": "python3 ~/.codex/hooks/session_start.py",  // 要执行的脚本
            "statusMessage": "Loading session notes"  // 可选：UI 显示的状态提示
          }
        ]
      }
    ],
    "PreToolUse": [  // 钩子事件（工具调用前）
      {
        "matcher": "Bash",  // 仅匹配 Bash 工具调用
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ]
  }
}

```

#### 格式2：config.toml 内联配置（适合简单场景）

```toml
[features]
codex_hooks = true  # 必须启用

# 内联 PreToolUse 钩子
[[hooks.PreToolUse]]
matcher = "^Bash$"  # 正则匹配，仅匹配 Bash 工具

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30  # 可选：超时时间（秒），默认 600 秒
statusMessage = "Checking Bash command"

# 内联 PostToolUse 钩子
[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py"'
timeout = 30
statusMessage = "Reviewing Bash output"

```

### 3.3 核心配置字段说明

- `matcher`：正则字符串，用于筛选事件触发条件，部分事件不支持（下文详细说明）；可省略或设为 `"*"`，表示匹配所有场景；

- `type`：钩子处理器类型，目前官方仅支持 `command`（执行 Shell 命令/脚本），增强版 Codex 已支持 Prompt、Agent 两种额外类型；

- `command`：要执行的命令/脚本路径，推荐使用绝对路径或 Git 根目录路径（避免 Codex 从子目录启动时路径失效）；

- `timeout`：可选，超时时间（秒），默认 600 秒，超过时间钩子会被强制终止；

- `statusMessage`：可选，Codex UI 中显示的钩子运行状态提示，提升用户体验。

## 四、核心钩子事件详解（6类必掌握）

Codex 目前支持 6 类核心生命周期事件，覆盖会话从启动到结束的全流程，不同事件的触发时机、匹配规则、输入输出均有差异，以下是重点解析（含实战用法）。

### 4.1 事件概览与匹配规则

并非所有事件都支持 `matcher` 筛选，以下表格明确各事件的匹配规则（必记）：

|钩子事件|触发时机|matcher 筛选内容|核心用途|
|---|---|---|---|
|SessionStart|会话启动/恢复时|会话启动来源（startup/resume/clear）|初始化会话、加载项目规范、初始化日志|
|PreToolUse|工具（Bash/apply_patch 等）调用前|工具名称（Bash/apply_patch 等）|拦截危险命令、校验工具输入|
|PermissionRequest|Codex 发起权限审批前|工具名称（Bash/apply_patch 等）|自动审批/拒绝权限请求，简化流程|
|PostToolUse|工具调用后（含执行失败）|工具名称（Bash/apply_patch 等）|校验工具输出、记录操作结果、反馈异常|
|UserPromptSubmit|用户提交提示词后|不支持（忽略 matcher 配置）|扫描敏感信息、优化提示词、补充上下文|
|Stop|会话结束/暂停时|不支持（忽略 matcher 配置）|总结会话、清理资源、触发后续通知|

补充说明：apply_patch 事件（文件编辑）的 matcher 可使用 `Edit` 或 `Write` 替代，简化配置。

### 4.2 通用输入/输出字段

所有钩子执行时，都会通过 `stdin` 接收一个 JSON 格式的输入（包含当前会话、事件等信息），并通过 `stdout` 输出结果影响 Codex 行为。

#### 通用输入字段（所有事件都包含）

|字段|类型|说明|
|---|---|---|
|session_id|string|当前会话 ID，用于关联日志、记忆等数据|
|transcript_path|string \| null|会话记录文件路径（若有）|
|cwd|string|当前会话的工作目录|
|hook_event_name|string|当前触发的钩子事件名称（如 SessionStart）|
|model|string|当前使用的 Codex 模型名称|

#### 通用输出字段（部分事件支持，详见下文）

|字段|作用|
|---|---|
|continue|布尔值，false 表示终止当前钩子运行|
|stopReason|字符串，记录终止钩子的原因（可选）|
|systemMessage|字符串，在 Codex UI 中显示警告/提示信息|

### 4.3 重点事件实战解析（附示例）

以下是 4 个最常用的钩子事件，结合实际场景提供完整配置与脚本示例，可直接复制使用。

#### 示例1：SessionStart（会话启动时加载项目规范）

触发时机：会话启动（startup）或恢复（resume）时，用于初始化会话环境、加载项目规范等。

```json
// hooks.json 中配置
"SessionStart": [
  {
    "matcher": "startup|resume",  // 匹配启动和恢复场景
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.codex/hooks/session_start.py",
        "statusMessage": "Loading project conventions"
      }
    ]
  }
]

```

配套脚本（session_start.py）：加载项目规范并添加到会话上下文

```python
import sys
import json

# 读取钩子输入（stdin 中的 JSON）
input_data = json.loads(sys.stdin.read())
# 读取项目规范文件
with open(f"{input_data['cwd']}/.codex/project_conventions.md", "r") as f:
    conventions = f.read()

# 输出结果，添加额外上下文
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": f"Project conventions loaded:\n{conventions}"
    }
}
# 输出到 stdout，供 Codex 读取
print(json.dumps(output))

```

#### 示例2：PreToolUse（拦截危险 Bash 命令）

触发时机：Bash 工具调用前，用于拦截`rm -rf` 等危险命令，保障系统安全。

```json
// hooks.json 中配置
"PreToolUse": [
  {
    "matcher": "Bash",  // 仅匹配 Bash 工具
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.codex/hooks/pre_tool_use.py",
        "statusMessage": "Checking Bash command safety"
      }
    ]
  }
]

```

配套脚本（pre_tool_use.py）：拦截危险命令并提示

```python
import sys
import json

input_data = json.loads(sys.stdin.read())
# 获取 Bash 命令
bash_command = input_data["tool_input"]["command"]

# 定义危险命令列表
dangerous_commands = ["rm -rf", "sudo", "mv /"]
if any(cmd in bash_command for cmd in dangerous_commands):
    # 拦截命令，返回拒绝信息
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Dangerous command blocked: {bash_command}\nPlease run manually if necessary."
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# 允许命令执行（无输出即可）
sys.exit(0)

```

#### 示例3：UserPromptSubmit（拦截敏感信息）

触发时机：用户提交提示词后，用于扫描 API Key、密码等敏感信息，避免泄露。

```json
// hooks.json 中配置
"UserPromptSubmit": [
  {
    "hooks": [  // 不支持 matcher，省略即可
      {
        "type": "command",
        "command": "python3 ~/.codex/hooks/check_sensitive.py"
      }
    ]
  }
]

```

配套脚本（check_sensitive.py）：扫描 API Key 并拦截

```python
import sys
import json
import re

input_data = json.loads(sys.stdin.read())
user_prompt = input_data["prompt"]

# 匹配 API Key 正则（以 sk- 开头的字符串）
api_key_pattern = r"sk-[a-zA-Z0-9]{24,}"
if re.search(api_key_pattern, user_prompt):
    # 拦截提示词，返回错误信息
    output = {
        "decision": "block",
        "reason": "Sensitive information (API Key) detected! Please remove it before submitting."
    }
    print(json.dumps(output))
    sys.exit(2)  #  exit code 2 也可表示拦截

# 允许提示词提交
sys.exit(0)

```

#### 示例4：PostToolUse（校验 Bash 命令输出）

触发时机：Bash 命令执行后，用于校验输出结果，若出现错误则提示用户。

```json
// hooks.json 中配置
"PostToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.codex/hooks/post_tool_use.py",
        "statusMessage": "Reviewing Bash output"
      }
    ]
  }
]

```

配套脚本（post_tool_use.py）：校验命令执行状态并反馈

```python
import sys
import json

input_data = json.loads(sys.stdin.read())
# 获取命令输出和执行状态
tool_output = input_data["tool_response"]
exit_code = tool_output.get("exit_code", 1)

if exit_code != 0:
    # 命令执行失败，返回反馈
    output = {
        "decision": "block",
        "reason": f"Bash command failed (exit code {exit_code}):\n{tool_output.get('stderr', 'No error message')}",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "Please check the command and try again."
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# 命令执行成功，无输出
sys.exit(0)

```

## 五、企业级托管 Hooks（团队统一管控）

企业场景中，管理员可通过 `requirements.toml` 配置「托管 Hooks」，强制所有团队成员使用统一的钩子规则，无法被用户覆盖，实现标准化管控。

```toml
[features]
codex_hooks = true  # 必须启用

[hooks]
managed_dir = "/enterprise/hooks"  # macOS/Linux 托管脚本目录
windows_managed_dir = "C:\\enterprise\\hooks"  # Windows 托管脚本目录

# 强制配置 PreToolUse 钩子（拦截危险命令）
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
timeout = 30
statusMessage = "Checking managed Bash command"
```

### 托管 Hooks 注意事项

- 托管脚本需通过 MDM 等企业设备管理工具单独安装、更新，Codex 不负责分发；

- 脚本路径必须使用 `managed_dir` 下的绝对路径，确保所有成员可访问；

- 托管 Hooks 会与用户 Hooks 合并执行，若存在冲突，以托管 Hooks 为准。

## 六、Hooks 进阶技巧与最佳实践

### 6.1 进阶技巧

- 路径稳定性：项目级 Hooks 推荐使用 `$(git rev-parse --show-toplevel)` 获取 Git 根目录，避免 Codex 从子目录启动时路径失效；

- 多钩子协同：同一事件可配置多个钩子，并发执行，例如「日志记录 + 敏感信息扫描」同时进行；

- 错误处理：钩子脚本中使用 exit code 区分状态（0=成功，2=拦截），配合 stderr 输出错误信息；

- 功能扩展：增强版 Codex 可通过 Prompt、Agent 类型的钩子，实现更复杂的校验逻辑（如让模型判断提示词合理性）。

### 6.2 最佳实践

- 最小权限原则：钩子脚本仅授予必要权限，避免使用 root 权限执行，防止脚本被篡改后造成风险；

- 分层管理：全局 Hooks 负责通用需求（如敏感信息拦截），项目级 Hooks 负责项目专属需求（如项目规范加载）；

- 日志记录：所有钩子的执行日志建议同步至统一日志系统，便于问题排查；

- 避免过度拦截：仅拦截高风险操作，避免频繁拦截影响开发效率；

- 版本兼容：Hooks 目前仍在迭代，升级 Codex 后需检查钩子脚本是否兼容，尤其是输入输出格式；

- 协同使用：与 Codex Rules、沙箱模式配合，构建「钩子拦截 + 规则管控 + 沙箱隔离」的三层安全防护体系。

## 七、常见问题排查

- Hooks 不生效：检查 `config.toml` 中 `codex_hooks = true` 是否启用；确认 Hooks 配置路径正确；项目级 Hooks 需确认项目已信任；

- 钩子脚本执行失败：检查脚本路径是否正确、脚本是否有执行权限；查看 Codex 日志（默认路径：~/.codex/logs）排查错误；

- matcher 不生效：确认事件是否支持 matcher（如 UserPromptSubmit 不支持）；检查正则表达式是否正确；

- 多个钩子冲突：同一事件的多个钩子并发执行，无法相互阻止，若需优先级控制，可在脚本中添加逻辑判断；

- 托管 Hooks 不生效：检查`managed_dir` 路径是否正确；确认脚本已通过企业工具安装到位。

## 八、总结

Codex Hooks 是解锁 Codex 定制化能力的核心工具，通过在生命周期关键节点注入自定义脚本，能够实现安全管控、流程自动化、场景适配等多种需求，尤其适合企业级团队的标准化管理。本文从启用配置、核心事件、实战示例到最佳实践，覆盖了 Hooks 使用的全流程，新手可直接复制示例快速上手，进阶用户可结合自身需求扩展钩子功能。

需要注意的是，Hooks 目前仍处于迭代阶段，部分功能（如输入输出字段）可能会更新，建议结合 OpenAI 官方文档定期更新配置。同时，合理搭配 Codex Rules 与沙箱模式，能够构建更安全、更高效的 AI 编程工作流，让 Codex 真正适配你的开发场景。

