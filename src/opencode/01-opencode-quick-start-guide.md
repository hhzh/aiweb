---
title: OpenCode 快速入门教程
order: 1
---

# OpenCode 快速入门教程：开源 AI 编码代理从零上手

## 一、认识 OpenCode

你是否正在寻找一款不受厂商锁定的 AI 编码助手？传统 AI 编码工具普遍存在模型绑定、终端适配差、数据隐私风险等问题。**OpenCode** 是一款开源 AI 编码代理（AI Coding Agent），主打终端优先的交互模式，同时提供桌面应用、IDE 扩展等多端使用方案，可无缝融入开发者现有工作流。

它支持对接市面上主流大模型（Claude、GPT、Gemini 等）及本地离线模型，无厂商锁定，且遵循隐私优先设计，默认不存储代码与会话数据，适配个人开发、团队协作、企业私有化部署等多种场景。其内置 **Plan（计划）** 和 **Build（构建）** 两大核心代理模式，搭配会话分享、代码回退、多会话并行等实用能力，能够独立完成代码解读、功能开发、代码重构、Bug 修复等全流程开发工作，是终端开发者的高效结对编程助手。

## 二、多平台安装指南

OpenCode 全平台兼容，支持 macOS、Linux、Windows 等系统，提供脚本、包管理器、Docker 等多种安装方式，你可根据自身操作系统选择对应方案。

### 2.1 通用一键安装脚本（全平台推荐）

这是官方最简洁的安装方式，适用于绝大多数类 Unix 终端（macOS、Linux、WSL）：

```bash
curl -fsSL https://opencode.ai/install | bash
```

### 2.2 基于 Node.js 生态安装

若本地已安装 Node.js、Bun、pnpm、Yarn 等工具，可使用包管理器全局安装：

```bash
# NPM
npm install -g opencode-ai

# Bun
bun install -g opencode-ai

# pnpm
pnpm install -g opencode-ai

# Yarn
yarn global add opencode-ai
```

### 2.3 macOS & Linux（Homebrew）

官方推荐使用 OpenCode 专属 Tap 源，可第一时间获取最新版本；系统默认 `brew install opencode` 由 Homebrew 团队维护，版本更新较慢：

```bash
# 推荐方式（官方 Tap 源）
brew install anomalyco/tap/opencode
```

### 2.4 Arch Linux

分为稳定版和 AUR 最新版两种安装渠道：

```bash
# 安装稳定版
sudo pacman -S opencode

# 安装 AUR 最新版（需提前安装 paru）
paru -S opencode-bin
```

### 2.5 Windows 系统安装

官方**强烈推荐 Windows 用户使用 WSL（Windows 子系统 for Linux）**，WSL 具备更优的文件系统性能、完整终端支持，可兼容 OpenCode 全部功能。原生 Windows 仅作为备选方案。

1. **WSL 方案（优先选择）**
先参照微软官方指南安装 WSL，打开 WSL 终端后，执行通用安装脚本即可，后续使用方式与 Linux 完全一致。

2. **原生 Windows 备选方案**

```powershell
# Chocolatey
choco install opencode

# Scoop
scoop install opencode

# NPM
npm install -g opencode-ai
```

> 补充：Windows 原生环境下，Bun 安装方式目前仍在开发中，暂不建议使用。
> 
> 

### 2.6 Docker 临时运行

无需本地安装，通过 Docker 容器快速体验：

```bash
docker run -it --rm ghcr.io/anomalyco/opencode
```

### 2.7 二进制包

你也可以前往 OpenCode 官方 Releases 页面，直接下载对应系统的二进制文件手动部署。

## 三、基础配置：对接大模型提供商

安装完成后，首要步骤是配置 LLM 模型 API 密钥，OpenCode 支持市面上绝大多数大模型服务商，新手优先选择官方精选的 **OpenCode Zen** 模型集（经过官方测试适配，开箱即用）。

1. 任意终端执行 OpenCode 启动程序，进入 TUI（终端交互界面）；

2. 在界面中输入命令连接模型：

    ```bash
    /connect
    ```

3. 选择 `opencode` 作为提供商，根据提示跳转至 `opencode.ai/auth` 页面；

4. 登录账号并补充账单信息，复制页面生成的 API 密钥；

5. 返回终端，粘贴 API 密钥完成配置。

若需使用 OpenAI、Anthropic 等第三方模型，可在 `/connect` 命令的提供商列表中选择对应服务商，按指引填入专属 API 密钥即可。

## 四、项目初始化

配置完模型后，即可针对本地项目初始化 OpenCode，让工具识别项目结构与编码规范：

1. 通过 `cd` 命令进入目标项目根目录：

    ```bash
    cd /path/to/your/project
    ```

2. 启动 OpenCode：

    ```bash
    opencode
    ```

3. 执行初始化命令，工具会自动分析项目，并在根目录生成 `AGENTS.md` 文件：

    ```bash
    /init
    ```

> 重要提示：请将 `AGENTS.md` 文件提交至 Git 仓库。该文件记录了项目结构、编码规则等信息，能帮助 OpenCode 长期适配项目风格，保证代码修改的一致性。
> 
> 

## 五、核心功能实战

初始化完成后，即可通过自然语言与 OpenCode 协作开发，下文覆盖日常开发高频场景。

### 5.1 代码解读与查询

面对陌生代码库时，可直接让 OpenCode 解析代码逻辑。使用 `@` 符号可**模糊检索项目文件**，精准定位目标代码：

```text
# 示例：查询指定文件中的身份验证逻辑
How is authentication handled in @packages/functions/src/api/index.ts
```

### 5.2 功能开发（Plan + Build 双模式）

这是正式开发的核心流程，分为「方案规划」和「代码构建」两个阶段，通过 `Tab` 键快速切换模式。

1. **Plan 计划模式（默认进入）**
该模式下 OpenCode 仅输出实现方案、不修改代码，适合复杂功能提前评审。按下 `Tab` 切换至计划模式（右下角会显示模式标识），输入详细需求：

```text
# 示例需求：实现笔记删除与恢复功能
When a user deletes a note, we'd like to flag it as deleted in the database. Then create a screen that shows all the recently deleted notes. From this screen, the user can undelete a note or permanently delete it.
```

2. **迭代优化方案**
若对生成的计划不满意，可补充细节、参考设计图优化方案。支持直接将图片拖拽至终端，OpenCode 会自动识别图片内容并纳入需求：

```text
We'd like to design this new screen using a design I've used before.
# 拖拽设计图到终端
```

3. **Build 构建模式**
方案确认后，再次按下 `Tab` 切换至构建模式，指令工具执行代码修改：

```text
Sounds good! Go ahead and make the changes.
```

### 5.3 简易代码直接修改

对于单行修改、接口补充、规则复用等简单场景，无需进入计划模式，直接描述需求即可完成修改：

```text
# 示例：复用已有路由的鉴权逻辑
We need to add authentication to the /settings route. Take a look at how this is handled in the /notes route in @packages/functions/src/notes.ts and implement the same logic in @packages/functions/src/settings.ts
```

### 5.4 代码撤销与重做

若修改结果不符合预期，使用内置命令快速回退或恢复操作，支持多次连续撤销 / 重做：

```bash
# 撤销上一次代码修改（可多次执行，逐层回退）
/undo

# 重做已撤销的修改
/redo
```

### 5.5 会话分享（团队协作）

开发过程中如需和同事同步对话、排查问题，使用分享命令生成会话链接并自动复制到剪贴板：

```bash
/share
```

> 说明：会话默认不会自动分享，必须手动执行 `/share` 才会生成公开链接。
> 
> 

## 六、Windows WSL 深度配置（专属优化）

Windows 用户使用 WSL 运行 OpenCode 可获得最佳体验，本节补充文件访问、桌面应用联动、Web 客户端部署等进阶配置。

### 6.1 访问 Windows 本地文件

WSL 通过 `/mnt/` 目录映射 Windows 磁盘，盘符规则如下：

- Windows C 盘 → WSL 路径 `/mnt/c/`

- Windows D 盘 → WSL 路径 `/mnt/d/`

示例（进入 Windows 桌面项目目录）：

```bash
cd /mnt/c/Users/你的用户名/Documents/project
opencode
```

> 优化建议：长期使用建议将项目克隆至 WSL 本地文件系统（如 `~/code/`），文件读写性能会大幅提升。
> 
> 

### 6.2 桌面应用 + WSL 服务器联动

若习惯使用 OpenCode 桌面应用，可在 WSL 中启动服务端，桌面端远程连接：

1. WSL 终端启动服务，开放外部访问权限：

    ```bash
    # 基础启动（开放局域网连接）
    opencode serve --hostname 0.0.0.0 --port 4096
    ```

2. 安全加固：开启外网访问时，必须设置服务密码防止恶意访问：

    ```bash
    OPENCODE_SERVER_PASSWORD=自定义密码 opencode serve --hostname 0.0.0.0
    ```

3. 连接方式：

    - 局域网正常：桌面应用连接 `http://localhost:4096`；

    - `localhost` 异常：在 WSL 执行 `hostname -I` 获取 WSL 内网 IP，使用 `http://WSL-IP:4096` 连接。

### 6.3 Web 客户端 + WSL

如需通过浏览器使用 OpenCode，在 WSL 终端启动 Web 服务（请勿在 PowerShell 中执行）：

```bash
opencode web --hostname 0.0.0.0
```

启动后终端会输出访问地址，直接在 Windows 浏览器打开即可。

### 6.4 配套工作流

可搭配 VS Code WSL 扩展，实现「WSL 运行 OpenCode + VS Code 编辑代码」的一体化开发流程；OpenCode 所有配置、会话数据均存储在 WSL 的 `~/.local/share/opencode/` 目录下。

## 七、高阶配置：opencode.json 配置文件详解

OpenCode 支持通过 **JSON / JSONC（带注释 JSON）** 配置文件自定义全局、项目规则，配置文件采用「合并生效」机制（而非覆盖），多配置项冲突时，优先级高的配置会覆盖低优先级配置。

### 7.1 配置文件加载优先级（由低到高）

优先级越靠后，配置权限越高，可覆盖前面的设置：

1. 远程配置（组织默认配置，`.well-known/opencode`）；

2. 全局配置（用户个人偏好，路径 `~/.config/opencode/opencode.json`）；

3. 自定义配置（`OPENCODE_CONFIG` 环境变量指定的文件）；

4. 项目配置（项目根目录 `opencode.json`，推荐提交 Git）；

5. 项目 `.opencode` 目录（存放代理、插件、自定义命令）；

6. 内联配置（`OPENCODE_CONFIG_CONTENT` 环境变量，运行时临时覆盖）。

### 7.2 通用配置示例

新建 `opencode.jsonc`（支持注释），放置在对应目录即可生效，以下为高频配置模板：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // 配置默认使用的大模型
  "model": "anthropic/claude-sonnet-4-5",
  // 轻量任务专用小模型
  "small_model": "anthropic/claude-haiku-4-5",
  // 开启/关闭自动更新（可选："notify" 仅提醒更新）
  "autoupdate": true,
  // 服务器端口、跨域配置（serve/web 命令生效）
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "cors": ["http://localhost:5173"]
  },
  // TUI 终端界面配置
  "tui": {
    "scroll_speed": 3,
    "diff_style": "auto"
  },
  // 工具权限：编辑、执行命令需手动确认
  "permission": {
    "edit": "ask",
    "bash": "ask"
  },
  // 文件监视器忽略目录，减少资源占用
  "watcher": {
    "ignore": ["node_modules/**", "dist/**", ".git/**"]
  },
  // 禁用指定模型提供商
  "disabled_providers": ["openai"],
  // 仅允许指定模型提供商（黑白名单同时存在时，禁用优先级更高）
  "enabled_providers": ["anthropic"]
}
```

### 7.3 进阶用法

1. **自定义配置路径**
通过环境变量指定配置文件位置，适配多环境切换：

```bash
export OPENCODE_CONFIG=/自定义路径/custom-config.json
opencode
```

2. **变量替换（保护敏感信息）**
支持读取环境变量、本地文件填充 API 密钥等敏感数据，避免明文泄露：

```jsonc
{
  "provider": {
    "anthropic": {
      "options": {
        // 读取系统环境变量
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

3. **自定义命令与代理**
针对重复工作封装自定义命令，或创建专用代码审查、测试代理，提升团队效率。

## 八、个性化与拓展

1. **主题与快捷键**：通过配置文件 `theme`、`keybinds` 字段自定义终端主题和操作快捷键，适配个人使用习惯；

2. **代码格式化**：对接 Prettier 等格式化工具，统一项目代码风格；

3. **插件拓展**：将插件放入 `.opencode/plugins/` 目录，或在配置中通过 `plugin` 字段引入 NPM 插件，扩展工具能力；

4. **自定义代理**：在 `.opencode/agents/` 目录创建 Markdown 文件，定制代码审查、UI 开发等专用代理。

## 九、总结

OpenCode 凭借**开源免费、多模型兼容、全平台适配、隐私安全**四大核心优势，成为终端开发者首选的 AI 编码代理。新手可按照「安装 → 配置模型 → 项目初始化 → 协作开发」的流程快速上手：

1. Windows 用户优先使用 WSL 环境，规避原生系统兼容性问题；

2. 团队项目务必提交 `AGENTS.md` 和项目级 `opencode.json`，统一团队开发规范；

3. 复杂功能使用 Plan + Build 双模式，先评审方案再落地代码，降低修改风险；

4. 涉密项目可对接本地离线模型，全程不联网，保障代码安全。

无论是个人小型项目、大型商业项目，还是企业私有化部署，OpenCode 都能灵活适配，结合自定义配置、插件、代理等拓展能力，可打造完全贴合自身工作流的 AI 开发环境。
