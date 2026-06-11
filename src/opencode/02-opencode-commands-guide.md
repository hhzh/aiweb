---
title: OpenCode 命令使用教程
order: 2
---

# OpenCode 命令使用教程

熟练使用 CLI 命令是高效驾驭 OpenCode 的基础。OpenCode 提供了丰富的命令行工具集——从启动交互界面（TUI）、执行非交互任务，到管理模型与代理、部署远程服务、集成 GitHub 等工作流——覆盖了本地开发到自动化运维的全场景。本文将系统讲解 OpenCode CLI 基础命令、核心功能、TUI 自定义命令、快捷键配置以及环境变量，同时补充实战场景与最佳实践，帮助开发者全面掌握 OpenCode 的使用方法。

## 一、快速入门：基础启动与全局标志

### 1.1 基础启动命令

OpenCode CLI 无参数运行时，默认启动**终端交互界面（TUI）**，这是最常用的使用方式：

```bash
# 启动默认 TUI 交互界面
opencode

# 指定项目目录，启动 TUI 并绑定对应项目
opencode [项目路径]
```

### 1.2 全局通用标志

所有 OpenCode 命令均支持以下全局标志，用于基础功能控制：

|标志|简写|功能说明|
|---|---|---|
|`--help`|`-h`|查看当前命令的帮助文档|
|`--version`|`-v`|查看 OpenCode 安装版本|
|`--print-logs`|-|将运行日志输出到标准错误流（stderr）|
|`--log-level`|-|设置日志级别，可选：`DEBUG`/`INFO`/`WARN`/`ERROR`|

示例：

```bash
# 查看 OpenCode 版本
opencode -v

# 查看 run 命令帮助
opencode run -h
```

## 二、核心 CLI 命令详解

OpenCode 提供十余类细分命令，覆盖**交互运行、服务部署、代理管理、认证授权、会话运维、第三方集成**等场景，下面按功能分类逐一讲解。

### 2.1 交互运行类命令

#### 2.1.1 run（非交互执行指令）

`run` 是高频命令，用于**非交互模式**直接传入提示词执行任务，适配脚本编写、自动化批量处理、快速问答等场景，无需启动完整 TUI。
**语法**：

```bash
opencode run [提示词内容]
```

**常用标志**：

|标志|简写|功能说明|
|---|---|---|
|`--continue`|`-c`|继续上一次会话|
|`--session`|`-s`|指定会话 ID，接续对应会话|
|`--fork`|-|接续会话时创建会话分支（搭配 `--continue`/`--session` 使用）|
|`--model`|`-m`|指定模型，格式为 `提供商/模型名`|
|`--file`|`-f`|附加本地文件到对话上下文|
|`--attach`|-|连接已启动的 OpenCode 远程服务，规避 MCP 服务器冷启动|
|`--format`|-|输出格式：`default`（格式化文本）/`json`（原始事件流）|

**实战示例**：

```bash
# 快速提问：解释 JavaScript 闭包
opencode run "Explain how closures work in JavaScript"

# 指定模型并附加代码文件提问
opencode run -m anthropic/claude-3.5-sonnet -f main.go "优化这段 Go 代码"

# 连接本地 serve 服务执行指令（双终端配合）
# 终端1：启动无界面服务
opencode serve
# 终端2：连接服务并执行指令
opencode run --attach http://localhost:4096 "讲解 JS async/await 原理"
```

#### 2.1.2 attach（连接远程后端服务）

用于将本地 TUI 连接到通过 `serve` 或 `web` 启动的远程 OpenCode 后端，实现**多终端共享远程服务**。
**语法**：

```bash
opencode attach [远程服务URL]
```

**附加标志**：

- `--dir`：指定 TUI 启动的工作目录

- `--session`/`-s`：接续指定会话 ID

**实战示例**：

```bash
# 终端1：启动带 Web 界面的远程服务，监听 4096 端口
opencode web --port 4096 --hostname 0.0.0.0

# 终端2：本地 TUI 连接远程服务
opencode attach http://10.20.30.40:4096
```

### 2.2 代理管理命令（agent）

用于管理 OpenCode 自定义代理，支持创建、查看代理列表。
**基础语法**：

```bash
opencode agent [子命令]
```

1. **create**：交互式引导创建自定义代理，可配置专属系统提示词、工具权限。

    ```bash
    opencode agent create
    ```

2. **list**：列出当前环境中所有可用代理。

    ```bash
    opencode agent list
    ```

### 2.3 认证凭据命令（auth）

管理 AI 提供商的 API 密钥与登录状态，密钥默认存储路径：`~/.local/share/opencode/auth.json`。OpenCode 同时兼容环境变量、项目 `.env` 文件中的密钥配置。
**基础语法**：

```bash
opencode auth [子命令]
```

1. **login**：配置 AI 提供商 API 密钥（对接 Models.dev 提供商列表）。

    ```bash
    opencode auth login
    ```

2. **list/ls**：查看已完成认证的提供商列表。

    ```bash
    opencode auth list
    # 简写形式
    opencode auth ls
    ```

3. **logout**：清除指定提供商的凭据，完成登出。

    ```bash
    opencode auth logout
    ```

### 2.4 GitHub 仓库集成命令（github）

专为 GitHub 仓库自动化设计，用于配置和运行 GitHub 代理，对接 GitHub Actions 工作流。
**基础语法**：

```bash
opencode github [子命令]
```

1. **install**：在当前仓库安装 GitHub 代理，自动配置 GitHub Actions 工作流并引导完成配置。

    ```bash
    opencode github install
    ```

2. **run**：运行 GitHub 代理（多用于 GitHub Actions 流水线中）。
**附加标志**：

    - `--event`：指定模拟 GitHub 事件

    - `--token`：传入 GitHub 个人访问令牌

    ```bash
    opencode github run --token "你的GitHub令牌"
    ```

### 2.5 MCP 服务器管理命令（mcp）

管理 Model Context Protocol（MCP）服务器，支持添加、查看、认证、排障等操作。
**基础语法**：

```bash
opencode mcp [子命令]
```

1. **add**：交互式添加本地 / 远程 MCP 服务器。

    ```bash
    opencode mcp add
    ```

2. **list/ls**：列出所有已配置 MCP 服务器及连接状态。

    ```bash
    opencode mcp ls
    ```

3. **auth**：对支持 OAuth 的 MCP 服务器进行认证；`auth list` 可查看 OAuth 服务器认证状态。

4. **logout**：移除指定 MCP 服务器的 OAuth 凭据。

5. **debug**：排查指定 MCP 服务器的 OAuth 连接故障。

### 2.6 模型管理命令（models）

查看已配置提供商的所有可用模型，可刷新模型缓存、查看模型费用等元数据。
**基础语法**：

```bash
opencode models [提供商ID]
```

**附加标志**：

- `--refresh`：从 models.dev 刷新本地模型缓存（提供商新增模型时使用）

- `--verbose`：展示模型详细元数据（包含调用费用、参数等）

**示例**：

```bash
# 查看 Anthropic 提供商下的所有模型
opencode models anthropic

# 全局刷新模型缓存
opencode models --refresh

# 查看全量模型及费用信息
opencode models --verbose
```

### 2.7 服务部署命令

#### 2.7.1 serve（无界面 API 服务）

启动纯后台 HTTP 服务，对外提供 OpenCode API 接口，无前端界面。可通过环境变量 `OPENCODE_SERVER_PASSWORD` 开启 HTTP 基础认证（默认用户名：`opencode`）。
**语法**：

```bash
opencode serve
```

**附加标志**：

- `--port`：指定监听端口

- `--hostname`：指定监听主机名

- `--mdns`：启用 mDNS 服务发现

- `--cors`：配置允许跨域的浏览器源

#### 2.7.2 web（带 Web 界面服务）

启动 HTTP 服务并自动打开浏览器，通过 Web 界面访问 OpenCode，参数与 `serve` 完全一致。

```bash
# 启动 Web 服务，监听 8080 端口
opencode web --port 8080
```

#### 2.7.3 acp（ACP 协议服务器）

启动 Agent Client Protocol（ACP）服务器，基于 `stdin/stdout` 通过 nd-JSON 格式通信。
**附加标志**：`--cwd`（指定工作目录）、`--port`、`--hostname`。

```bash
opencode acp --cwd ./project
```

### 2.8 会话管理与统计命令

#### 2.8.1 session（会话管理）

管理所有历史对话会话，核心子命令为 `list`。
**语法**：

```bash
opencode session list
```

**附加标志**：

- `-n`/`--max-count`：限制展示最近 N 条会话

- `--format`：输出格式，支持 `table`（默认表格）/`json`

#### 2.8.2 export /import（会话导入导出）

用于会话备份、分享与迁移。

```bash
# 导出指定会话为 JSON 文件（不传 ID 则交互式选择）
opencode export [会话ID]

# 从本地 JSON 文件或在线分享链接导入会话
opencode import session.json
opencode import https://opncd.ai/s/abc123
```

#### 2.8.3 stats（用量统计）

统计会话的 Token 消耗、调用费用、模型用量等数据。
**附加标志**：

- `--days`：统计最近 N 天数据

- `--models`：展示模型用量明细

- `--project`：按项目筛选统计数据

```bash
# 统计最近 7 天全项目用量及模型明细
opencode stats --days 7 --models
```

### 2.9 运维命令（卸载 / 升级）

#### 2.9.1 uninstall（卸载 OpenCode）

卸载程序并清理相关文件，支持保留配置、模拟删除等操作。
**常用标志**：

- `-c`/`--keep-config`：保留配置文件

- `-d`/`--keep-data`：保留会话数据与快照

- `--dry-run`：模拟删除，仅展示待删除文件（不实际执行）

- `-f`/`--force`：跳过确认，强制卸载

```bash
# 模拟卸载，保留配置文件
opencode uninstall --dry-run -c
```

#### 2.9.2 upgrade（版本升级）

升级 OpenCode 至最新版本或指定历史版本。

```bash
# 升级到最新版本
opencode upgrade

# 升级到指定版本
opencode upgrade v0.1.48

# 指定安装方式升级（curl/npm/pnpm/brew 等）
opencode upgrade --method npm
```

## 三、TUI 自定义命令

OpenCode TUI 内置 `/init`、`/undo`、`/redo`、`/share`、`/help` 等基础斜杠命令，同时支持**自定义命令**，用于固化重复提示词、简化高频操作，自定义命令可覆盖同名内置命令。

### 3.1 命令存放目录

自定义命令分为**全局命令**和**项目级命令**，优先级：项目级 > 全局：

1. 全局命令（全系统生效）：`~/.config/opencode/commands/`

2. 项目级命令（仅当前项目生效）：`.opencode/commands/`

### 3.2 两种创建方式

#### 3.2.1 Markdown 文件（推荐）

在上述目录中创建 `.md` 文件，**文件名即为命令名**，文件分为两部分：顶部 `frontmatter` 配置元数据，正文为提示词模板。

示例：`.opencode/commands/test.md`（项目级测试命令）

```markdown
---
description: 运行测试并生成覆盖率报告
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---
运行完整测试套件并输出覆盖率报告，定位失败用例并给出修复方案。
```

**使用方式**：进入 TUI 后输入以下指令执行：

```Plain Text
/test
```

#### 3.2.2 JSON 配置（opencode.jsonc）

在项目根目录 `opencode.jsonc` 中通过 `command` 节点配置命令，适合集中管理多条自定义命令。

```json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "运行完整测试套件并输出覆盖率报告，定位失败用例并给出修复方案。",
      "description": "运行测试并生成覆盖率报告",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

### 3.3 高级占位符语法

自定义命令支持三类占位符，实现动态传参、注入系统信息，大幅提升灵活性。

#### 3.3.1 参数传递

用于向命令传递自定义参数：

1. `$ARGUMENTS`：接收所有传入参数

2. `$1`、`$2`、`$3`...：按位置单独获取参数

示例 1：创建组件命令 `.opencode/commands/component.md`

```markdown
---
description: 创建 TypeScript React 组件
---
创建名为 $ARGUMENTS 的 React + TypeScript 组件，补充基础类型定义。
```

使用：`/component Button`，`$ARGUMENTS` 会被替换为 `Button`。

示例 2：多参数文件创建命令

```markdown
---
description: 新建文件
---
在 $2 目录下创建文件 $1，文件内容：$3
```

使用：`/create-file config.json src "{"key":"value"}"`。

#### 3.3.2 Shell 输出注入

使用 `!`+``shell命令`` 将终端命令输出注入提示词，自动读取系统 / 项目实时状态。

> 注意：Shell 命令以当前项目根目录为执行路径，请勿执行包含敏感信息或高危操作的指令。
> 
> 

示例（查看 Git 最近提交）：

```markdown
---
description: 评审近期代码提交
---
以下是最近 10 条 Git 提交记录：
!`git log --oneline -10`
基于提交记录给出代码优化建议。
```

#### 3.3.3 文件引用

使用 `@文件路径` 引用项目文件，文件内容会自动加载到对话上下文。

```markdown
---
description: 代码评审
---
评审 @src/components/Button.tsx 组件，检查性能问题并优化。
```

### 3.4 核心配置字段说明

|字段|必填|说明|
|---|---|---|
|`template`|是|发送给 AI 的提示词模板，命令核心内容|
|`description`|否|命令描述，在 TUI 命令列表中展示|
|`agent`|否|指定执行该命令的代理|
|`model`|否|单独指定该命令使用的模型，覆盖全局配置|
|`subtask`|否|布尔值，强制以子代理模式运行（隔离上下文）|

## 四、TUI 快捷键配置与使用

OpenCode TUI 提供全套快捷键，支持自定义修改，默认采用 **前导键（Leader Key）** 机制，避免与终端原生快捷键冲突。

### 4.1 前导键机制

- 默认前导键：`ctrl+x`，绝大多数组合快捷键需要**先按前导键，再按功能键**。

- 示例：新建会话快捷键 `<leader>n`，实际操作：按下 `ctrl+x` → 松开 → 按下 `n`。

### 4.2 常用默认快捷键

#### 4.2.1 全局功能快捷键

|快捷键组合|功能|
|---|---|
|`ctrl+x q`|退出 OpenCode|
|`ctrl+x e`|打开外部编辑器|
|`ctrl+x b`|切换侧边栏显示 / 隐藏|
|`ctrl+x n`|新建会话|
|`ctrl+x l`|查看会话列表|
|`escape`|中断当前会话响应|

#### 4.2.2 输入框专属快捷键（Emacs 风格）

输入框内置文本编辑快捷键，无需配置，通用所有终端：

|快捷键|功能|
|---|---|
|`ctrl+a`|光标移动到行首|
|`ctrl+e`|光标移动到行尾|
|`ctrl+b`/`ctrl+f`|光标左 / 右移动单个字符|
|`alt+b`/`alt+f`|光标左 / 右移动单个单词|
|`ctrl+u`|删除光标到行首内容|
|`ctrl+k`|删除光标到行尾内容|
|`ctrl+w`|删除前一个单词|

### 4.3 自定义快捷键

快捷键配置文件为 `tui.json`，仅需修改需要自定义的项，未配置项沿用默认值；将快捷键设为 `none` 可禁用该功能。

**基础配置示例**：

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "keybinds": {
    // 修改前导键为 ctrl+z
    "leader": "ctrl+z",
    // 禁用会话压缩快捷键
    "session_compact": "none",
    // 绑定多快捷键到消息复制功能
    "messages_copy": "<leader>y, ctrl+shift+c"
  }
}
```

### 4.4 Windows Terminal 适配（Shift+Enter）

部分 Windows 终端默认不识别 `Shift+Enter`，需手动修改配置：

1. 打开终端配置文件：`%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json`

2. 在 `actions` 数组中添加转义配置：

    ```json
    "actions": [
      {
        "command": { "action": "sendInput", "input": "\u001b[13;2u" },
        "id": "User.sendInput.ShiftEnterCustom"
      }
    ]
    ```

3. 在 `keybindings` 数组中绑定按键：

    ```json
    "keybindings": [
      { "keys": "shift+enter", "id": "User.sendInput.ShiftEnterCustom" }
    ]
    ```

4. 保存文件并重启终端即可生效。

## 五、环境变量配置

OpenCode 支持通过环境变量实现全局配置，分为基础配置、服务安全、功能开关、实验性功能四大类，可临时在终端设置，或写入系统环境变量永久生效。

### 5.1 常用基础环境变量

|环境变量|类型|功能说明|
|---|---|---|
|`OPENCODE_CONFIG`|字符串|自定义配置文件路径|
|`OPENCODE_CONFIG_DIR`|字符串|自定义配置目录|
|`OPENCODE_AUTO_SHARE`|布尔|开启会话自动分享|
|`OPENCODE_DISABLE_AUTOUPDATE`|布尔|禁用自动版本检查|

### 5.2 服务认证环境变量

用于 `serve`/`web` 服务开启密码认证：

- `OPENCODE_SERVER_PASSWORD`：设置服务访问密码（必填）

- `OPENCODE_SERVER_USERNAME`：自定义登录用户名（默认：`opencode`）

### 5.3 功能开关环境变量

|环境变量|类型|功能说明|
|---|---|---|
|`OPENCODE_DISABLE_DEFAULT_PLUGINS`|布尔|禁用默认插件|
|`OPENCODE_ENABLE_EXA`|布尔|启用 Exa 网络搜索工具|
|`OPENCODE_DISABLE_AUTOCOMPACT`|布尔|禁用自动上下文压缩|

### 5.4 实验性功能变量

以 `OPENCODE_EXPERIMENTAL_` 为前缀，用于启用内测功能，例如：

- `OPENCODE_EXPERIMENTAL`：一次性启用所有实验功能

- `OPENCODE_EXPERIMENTAL_PLAN_MODE`：启用计划模式

- `OPENCODE_EXPERIMENTAL_FILEWATCHER`：启用全局文件监听

## 六、实战最佳实践

1. **自动化脚本搭配**
结合 `opencode run` 编写 Shell 脚本，实现批量代码检查、文档生成等任务，示例：

    ```bash
    # 批量检查当前目录所有 JS 文件语法
    opencode run "检查当前目录所有 JS 文件语法错误并给出修复建议"
    ```

2. **远程服务协同**
团队多人协作时，服务端执行 `opencode web` 部署共享服务，成员通过 `opencode attach` 连接，统一使用一套模型与配置。

3. **密钥安全管理**
优先使用项目 `.env` 文件存储 API 密钥，避免将密钥硬编码在命令或脚本中；定期通过 `opencode auth logout` 清理闲置凭据。

4. **自定义命令团队共享**
将项目级 `.opencode/commands` 目录提交至 Git，团队成员同步后即可共用自定义命令，统一工作流程。

5. **高危操作防护**
使用 Shell 注入语法（`!`命令）时，禁止执行删除文件、读取隐私数据等高危指令，避免敏感信息泄露。

## 七、总结

OpenCode CLI 是连接开发者与 AI 能力的核心入口，整体能力可分为三大板块：

1. **基础命令**：覆盖 TUI 启动、会话管理、模型 / 代理运维、服务部署，兼顾交互式操作与后台服务化；

2. **自定义命令**：通过占位符、Shell 注入、文件引用实现提示词复用，大幅提升重复工作效率；

3. **快捷键与配置**：前导键机制解决终端快捷键冲突，环境变量与配置文件支持个性化定制。

日常交互式开发优先使用 TUI + 自定义命令；自动化、CI/CD 场景使用 `opencode run` + GitHub 代理；多人远程协作推荐 `serve/web + attach` 组合。熟练掌握以上命令与配置，可充分发挥 OpenCode 在代码开发、审查、自动化运维中的价值。
