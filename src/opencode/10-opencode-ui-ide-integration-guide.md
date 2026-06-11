---
title: OpenCode UI 界面与 IDE 集成教程
order: 10
---

# OpenCode UI 界面与 IDE 集成教程

OpenCode 除了强大的命令行能力外，还提供 **TUI 终端交互界面**、**Web 网页界面**两类可视化 UI，并深度适配 VS Code、Cursor 等主流代码编辑器，形成终端、浏览器、IDE 全场景使用体系。TUI 适配纯终端、服务器等无图形环境；Web 界面支持多设备远程访问与可视化会话管理；IDE 集成则打通编码与 AI 辅助的链路，无需切换窗口即可完成代码解读、调试、优化等操作。

本文结合官方文档，系统讲解 OpenCode TUI、Web 界面的启动方式、交互语法、指令用法、个性化配置，同时详细介绍主流 IDE 的集成步骤、专属快捷键、环境配置与故障排查，帮助开发者根据业务场景灵活选用界面，最大化发挥 OpenCode 的辅助能力。

## 一、OpenCode TUI 终端交互界面

TUI（终端用户界面）是 OpenCode 原生交互式界面，也是使用最广泛的界面形态，依托终端运行，支持对话交互、文件调用、Shell 命令执行、快捷指令等功能，轻量化且兼容性极强。

### 1.1 TUI 基础启动

仅需一行命令即可启动 TUI，支持在当前目录或指定项目目录运行，启动后直接进入对话输入状态：

```bash
# 在当前工作目录启动 TUI
opencode

# 指定项目路径启动 TUI，自动绑定目标项目
opencode /path/to/project
```

### 1.2 三大核心交互语法

TUI 内置专属语法，可快速关联项目文件、执行终端命令，实现对话上下文联动，无需手动复制粘贴内容。

1. **常规文本提问**
直接输入自然语言、代码问题或开发需求，适用于代码解读、方案咨询、问题排查等基础场景。

```Plain Text
Give me a quick summary of the codebase.
```

2. **文件引用（@ 语法）**
使用 `@` 拼接文件路径可引用项目文件，支持路径模糊搜索，文件内容会自动加载至对话上下文，常用于代码评审、接口逻辑分析。

```Plain Text
# 解读指定接口文件的鉴权逻辑
How is auth handled in @packages/functions/src/api/index.ts?
```

3. **Shell 命令执行（! 语法）**
以 `!` 开头的内容会被识别为终端命令并执行，命令输出结果自动作为对话上下文传递给 AI，可快速查看目录、日志、提交记录等项目信息。

```Plain Text
# 查看当前目录文件详情
!ls -la
```

### 1.3 内置斜杠快捷命令

TUI 支持 `/` 开头的内置命令，覆盖会话管理、编辑器调用、会话导出、模型切换等高频操作，多数命令搭配默认前导键 `ctrl+x` 设有专属快捷键。完整命令、别名、快捷键及功能如下表：

|斜杠命令|别名|默认快捷键|功能说明|
|---|---|---|---|
|`/connect`|-|-|选择 AI 服务提供商，配置并添加 API 密钥|
|`/compact`|`/summarize`|`ctrl+x c`|压缩当前会话，精简对话上下文|
|`/details`|-|`ctrl+x d`|切换工具执行详情的显示 / 隐藏状态|
|`/editor`|-|`ctrl+x e`|调用系统预设编辑器编写长文本消息|
|`/exit`|`/quit`、`/q`|`ctrl+x q`|退出 TUI 界面|
|`/export`|-|`ctrl+x x`|将当前会话导出为 Markdown 并通过默认编辑器打开|
|`/help`|-|`ctrl+x h`|打开帮助弹窗，查看功能说明|
|`/init`|-|`ctrl+x i`|创建或更新项目内 `AGENTS.md` 配置文件|
|`/models`|-|`ctrl+x m`|列出当前已配置的所有可用 AI 模型|
|`/new`|`/clear`|`ctrl+x n`|清空会话，新建空白对话|
|`/redo`|-|`ctrl+x r`|恢复上一步撤销的消息与文件变更（依赖 Git 仓库）|
|`/sessions`|`/resume`、`/continue`|`ctrl+x l`|查看并切换历史会话|
|`/share`|-|`ctrl+x s`|生成分享链接，公开当前会话|
|`/themes`|-|`ctrl+x t`|查看并切换 TUI 主题|
|`/thinking`|-|-|切换模型推理块的显示 / 隐藏（仅控制展示，不修改模型能力）|
|`/undo`|-|`ctrl+x u`|撤销最后一条消息、AI 响应及对应文件修改（依赖 Git 仓库）|
|`/unshare`|-|-|取消当前会话的公开分享|

> 重要提示：`/undo` 和 `/redo` 依托 Git 版本控制管理文件变更，使用前需将项目初始化为 Git 仓库，否则文件回滚功能失效。
> 
> 

### 1.4 编辑器环境变量配置

`/editor` 与 `/export` 命令依赖 `EDITOR` 环境变量调用外部编辑器，不同操作系统配置方式存在差异，图形化编辑器需追加 `--wait` 参数，保证编辑器阻塞至手动关闭。

#### 1.4.1 Linux /macOS 系统

临时配置（仅当前终端生效）：

```bash
# 终端编辑器 nano
export EDITOR=nano
# 终端编辑器 vim
export EDITOR=vim
# VS Code（必须添加 --wait 参数）
export EDITOR="code --wait"
```

永久配置：将上述命令写入 `~/.bashrc`、`~/.zshrc` 等 Shell 配置文件，执行 `source 配置文件` 完成生效。

#### 1.4.2 Windows 系统

1. CMD 终端（临时生效）

```cmd
:: 系统记事本
set EDITOR=notepad
:: VS Code
set EDITOR=code --wait
```

2. PowerShell 终端（临时生效）

```powershell
# 系统记事本
$env:EDITOR = "notepad"
# VS Code
$env:EDITOR = "code --wait"
```

永久配置：Windows 可在「系统属性 - 环境变量」中添加全局变量；PowerShell 用户可将配置写入 PowerShell 专属配置文件。

**常用编辑器标识参考**：`code`（VS Code）、`cursor`（Cursor）、`nvim/vim`（Neovim/Vim）、`nano`（轻量终端编辑器）、`subl`（Sublime Text）。

### 1.5 TUI 个性化配置

通过项目根目录的 `opencode.json` 文件可自定义 TUI 滚动行为，优化终端操作体验，配置模板如下：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "tui": {
    "scroll_speed": 3,
    "scroll_acceleration": {
      "enabled": true
    }
  }
}
```

配置说明：

1. `scroll_speed`：控制滚动速度，最小值为 1，默认值 3；

2. `scroll_acceleration`：开启 macOS 风格滚动加速，快速滚动自动提速、慢速滚动保持精准；该功能优先级高于 `scroll_speed`，启用后滚动速度配置会失效。

## 二、OpenCode Web 网页界面

OpenCode 支持启动独立 Web 服务，可在浏览器中使用完整功能，无需依赖终端。Web 界面适配远程办公、多人局域网共享、图形化会话管理等场景，支持端口、跨域、身份认证等多项自定义配置。

### 2.1 Web 服务快速启动

执行基础命令即可启动 Web 服务，默认绑定本地地址 `127.0.0.1`、随机可用端口，启动后自动唤起默认浏览器：

```bash
# 基础启动，仅本地访问
opencode web
```

### 2.2 核心服务配置

支持通过**命令行标志**或**配置文件**自定义服务参数，命令行标志优先级高于配置文件。

#### 2.2.1 端口与主机名配置

1. 指定固定监听端口

```bash
# 监听 4096 端口，仅限本机访问
opencode web --port 4096
```

2. 开启局域网访问
设置 `--hostname 0.0.0.0` 后，同一局域网内的其他设备可通过本机 IP 访问服务：

```bash
opencode web --port 4096 --hostname 0.0.0.0
```

启动后终端会输出两类访问地址：本地地址 `http://localhost:4096`、局域网地址 `http://设备IP:4096`。

#### 2.2.2 mDNS 局域网自动发现

启用 mDNS 可让服务器在局域网内被自动识别，默认域名为 `opencode.local`，支持自定义域名，适用于同一网络部署多个 OpenCode Web 实例的场景：

```bash
# 启用 mDNS，默认域名 opencode.local
opencode web --mdns --port 4096

# 自定义 mDNS 域名，区分多实例
opencode web --mdns --mdns-domain myproject.local --port 4096
```

启用 mDNS 会自动将主机名设置为 `0.0.0.0`，无需额外配置。

#### 2.2.3 CORS 跨域配置

对接自定义前端页面时，可通过 `--cors` 添加允许跨域的域名：

```bash
# 允许 https://example.com 跨域访问
opencode web --port 4096 --cors https://example.com
```

#### 2.2.4 身份认证（安全加固）

未配置密码的 Web 服务无访问限制，**禁止直接暴露在公网中**。通过环境变量可设置访问密码与自定义用户名，提升安全性：

```bash
# 设置访问密码，默认用户名 opencode
OPENCODE_SERVER_PASSWORD=secret opencode web --port 4096

# 自定义用户名 + 访问密码
OPENCODE_SERVER_PASSWORD=123456 OPENCODE_SERVER_USERNAME=dev opencode web --port 4096
```

#### 2.2.5 持久化配置文件

将服务参数写入 `opencode.json`，无需每次启动重复输入命令：

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": true,
    "cors": ["https://example.com"]
  }
}
```

### 2.3 Web 界面核心功能

1. **会话管理**：首页集中展示所有历史会话，支持新建会话、切换会话、查看会话详情，操作逻辑与 TUI 完全一致；

2. **服务器管理**：点击「See Servers」可查看已连接的服务节点，支持新增、切换服务器；

3. **多端联动**：Web 服务启动后，可通过 `attach` 命令让终端 TUI 连接该服务，实现 Web 与终端共享会话、同步状态：

```bash
# 终端1：启动 Web 服务
opencode web --port 4096

# 终端2：TUI 连接 Web 服务
opencode attach http://localhost:4096
```

### 2.4 Windows 平台使用建议

Windows 系统运行 `opencode web` 时，优先使用 **WSL（Windows 子系统）**，而非原生 PowerShell，可规避文件系统访问、终端集成等兼容性问题。

## 三、OpenCode IDE 集成

OpenCode 深度适配主流代码编辑器，目前支持 VS Code、Cursor、Windsurf、VSCodium 等基于 Electron 的 IDE。集成后可在编码过程中直接调用 OpenCode，实现代码选中、文件引用、AI 问答一体化，大幅提升开发效率。

### 3.1 IDE 专属快捷键

集成完成后，IDE 提供全局快捷键，区分 Mac 与 Windows/Linux 平台，同时具备上下文感知能力，自动同步选中代码、当前标签页内容至 OpenCode。

|操作功能|Mac 快捷键|Windows / Linux 快捷键|
|---|---|---|
|打开 / 聚焦已有 OpenCode 会话|`Cmd+Esc`|`Ctrl+Esc`|
|强制新建 OpenCode 会话|`Cmd+Shift+Esc`|`Ctrl+Shift+Esc`|
|快速插入文件引用（@文件路径）|`Cmd+Option+K`|`Alt+Ctrl+K`|

### 3.2 两种安装方式

#### 3.2.1 自动安装（推荐）

1. 打开 VS Code、Cursor 等目标 IDE；

2. 打开 IDE 内置集成终端；

3. 在终端执行 `opencode` 命令；

4. 程序自动检测环境并完成扩展安装，全程无需手动操作。

#### 3.2.2 手动安装

1. 进入 IDE 扩展商店；

2. 搜索关键词 `OpenCode`；

3. 点击「Install」安装扩展，重启 IDE 后生效。

### 3.3 配套环境配置

若需在 IDE 联动的 TUI 中使用 `/editor`、`/export` 命令，需配置 `EDITOR` 环境变量指向当前 IDE，以 VS Code 为例：

```bash
# Linux / macOS 终端
export EDITOR="code --wait"

# Windows PowerShell
$env:EDITOR = "code --wait"
```

### 3.4 故障排查

若扩展安装失败、快捷键失效，按以下步骤逐一排查：

1. **检查运行终端**：必须使用 IDE 内置集成终端执行 `opencode`，外部终端无法触发自动安装；

2. **校验 IDE 命令环境变量**
主流 IDE 需将命令行工具加入系统 PATH：VS Code 对应 `code`、Cursor 对应 `cursor`、VSCodium 对应 `codium`。
修复方式：在 IDE 中按下 `Cmd+Shift+P`（Mac）/`Ctrl+Shift+P`（Windows/Linux），搜索 `Shell Command: Install 'xxx' command in PATH`（xxx 为 IDE 对应命令）并执行；

3. **权限校验**：Windows 系统可尝试以管理员身份启动 IDE，解决扩展安装权限不足问题。

## 四、全场景使用最佳实践

1. **按场景选择界面**
纯服务器、无图形环境优先使用 TUI 终端界面；多人局域网共享、远程浏览器访问选择 Web 界面并开启密码认证；日常编码、代码调试、实时评审搭配 IDE 集成。

2. **安全规范**
Web 服务暴露至公网时，务必配置 `OPENCODE_SERVER_PASSWORD` 开启身份认证；局域网共享服务按需配置 CORS 域名，避免权限过度开放。

3. **多端协同方案**
团队统一部署一台 OpenCode Web 服务，成员通过 `opencode attach` 连接服务，共享模型、会话与配置，统一团队工作规范。

4. **Git 环境适配**
频繁使用 `undo`、`redo` 功能的项目，建议初始化为 Git 仓库，保障文件变更回滚功能正常使用。

5. **统一编辑器配置**
全设备统一 `EDITOR` 环境变量，确保 `/editor`、`/export` 命令在 TUI、Web、IDE 中行为一致。

## 总结

OpenCode 三大使用界面各有侧重、互联互通：TUI 轻量化、兼容性强，主打终端快速交互；Web 界面可视化程度高，适配多设备远程访问；IDE 集成深度绑定编码流程，实现编码与 AI 辅助无缝衔接。

熟练掌握 TUI 交互语法、斜杠命令、Web 服务配置、IDE 快捷键与排障方法，可根据设备环境、工作场景灵活切换界面，充分发挥 OpenCode 在代码开发、评审、自动化运维中的价值。同时遵循安全配置规范与最佳实践，能进一步提升使用稳定性与协作效率。
