# Codex MCP 全流程使用教程：打通模型与工具

Model Context Protocol（MCP，模型上下文协议）是连接 AI 模型与外部工具、数据源、服务的标准化协议，也是 Codex 扩展能力的核心通道。通过 MCP，Codex 可直接对接开发文档、Figma、浏览器、GitHub 等工具，实现从 “代码生成” 到 “全流程开发协作” 的升级。本文基于官方 MCP 文档，从零讲解 Codex MCP 的核心能力、两种配置方式、实战示例、服务端部署与调试方法，覆盖 CLI 与 IDE 全端通用配置。

## 一、MCP 核心概述与 Codex 支持能力

MCP 是一套开放、通用的模型外部连接标准，作用是为 AI 提供统一的工具调用接口，让模型安全访问本地程序、第三方服务与自定义数据。Codex 原生支持 MCP，且 CLI 与 IDE 扩展共用一套配置，切换终端 / 编辑器无需重复配置。

### Codex 支持的 MCP 核心特性

- 本地 STDIO 服务器：通过本地命令启动的 MCP 服务（如文档查询、浏览器控制）

- 可流式访问的 HTTP 服务器：通过 URL 远程调用的 MCP 服务（如 Figma 远程服务）

- 环境变量注入：为 MCP 服务配置专属环境参数

- 认证方式：Bearer Token 认证、OAuth 认证（需开启实验性客户端）

- 全端共享：配置一次，CLI、桌面端、IDE 扩展全部生效

## 二、快速配置 MCP 服务器（两种方式任选）

Codex MCP 配置统一存储在 `~/.codex/config.toml`，支持**CLI 一键添加**与**手动编辑配置文件**两种方式，新手优先用 CLI，进阶用户用手动配置实现精细控制。

### 方式一：CLI 命令快速添加（推荐新手）

CLI 提供 `codex mcp` 命令集，无需手动改文件，一行命令完成 MCP 服务接入。

#### 1. 添加 MCP 服务器

```bash
codex mcp add <服务名称> --env <变量1=值1> -- <启动命令>
```

示例：添加开发者文档服务 Context7

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

#### 2. 常用 MCP 管理命令

```bash
# 查看所有已配置的 MCP 服务
codex mcp list
# 删除指定 MCP 服务
codex mcp remove <服务名称>
# 查看帮助
codex mcp --help
```

#### 3. TUI 内查看连接状态

启动 Codex 后，在交互终端输入 `/mcp`，即可实时查看已连接的 MCP 服务列表。

### 方式二：config.toml 手动精细配置

需要自定义超时、请求头、环境变量等高级参数时，直接编辑配置文件，支持 STDIO 与 HTTP 两种服务类型。

配置文件路径：

- macOS/Linux：`~/.codex/config.toml`

- Windows：`%USERPROFILE%.codex\\config.toml`

#### 1. 本地 STDIO 类型 MCP（必选：command）

```toml
# 开启 OAuth 支持（如需第三方登录）
experimental_use_rmcp_client = true

# 配置 Context7 文档服务
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
# 自定义环境变量
[mcp_servers.context7.env]
LOG_LEVEL = "info"
# 启动超时（秒）
startup_timeout_sec = 20
# 工具执行超时（秒）
tool_timeout_sec = 30
```

#### 2. 远程 HTTP 类型 MCP（必选：url）

```toml
# 配置 Figma 远程 MCP 服务
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
# 认证 Token
bearer_token = "your-figma-token"
startup_timeout_sec = 15
```

## 三、高频实用 MCP 服务器实战示例

以下是开发场景中最常用的 MCP 服务，直接复制配置即可使用，快速扩展 Codex 能力。

### 示例 1：开发者文档查询（Context7）

让 Codex 实时查询最新官方文档，告别过时知识。

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

使用场景：“帮我查看 React 18 最新 Hooks 文档并实现 useCallback 示例”

### 示例 2：Figma 设计稿读取（远程）

直接读取 Figma 设计规范，自动生成匹配的 UI 代码。

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token = "your-figma-access-token"
```

使用场景：“读取我 Figma 中的登录页设计，生成对应的 React 组件”

### 示例 3：浏览器自动化控制（Playwright）

让 Codex 自动打开浏览器、操作页面、生成自动化脚本。

```toml
[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp"]
[mcp_servers.playwright.env]
PLAYWRIGHT_BROWSERS_PATH = "chromium"
```

使用场景：“用 Playwright 写一个自动打开 GitHub 并登录的脚本”

### 示例 4：Chrome 开发者工具调试

直接控制浏览器调试，定位前端页面问题。

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["-y", "chrome-devtools-mcp"]
```

使用场景：“帮我调试当前页面的控制台报错”

## 四、将 Codex 作为 MCP 服务端供其他客户端调用

除了接入外部 MCP 服务，Codex 自身也可作为 MCP 服务端，被其他 AI 客户端（如自定义 Agent、OpenAI Agents SDK）调用，实现多模型协同。

### 1. 启动 Codex MCP 服务端

```bash
# 基础启动
codex mcp-server
# 搭配 MCP 调试器启动（推荐测试）
npx @modelcontextprotocol/inspector codex mcp-server
```

### 2. 核心可用工具

Codex 作为服务端暴露两个核心工具，供外部客户端调用：

1. **codex**：创建新会话，执行开发任务

2. **codex-reply**：基于已有会话继续交互

### 3. 调用示例（生成井字棋游戏）

在 MCP Inspector 中传入以下参数，自动生成完整游戏代码：

|参数|取值|
|---|---|
|prompt|Implement a simple tic-tac-toe game with HTML, JS, CSS in one index.html|
|approval-policy|never|
|sandbox|workspace-write|

## 五、MCP 连接验证与调试

1. **TUI 内验证**：启动 Codex → 输入 `/mcp` → 查看服务状态为 `connected` 即成功

2. **配置测试**：修改配置后重启 Codex，观察日志无报错则正常

3. **日志排查**：查看日志路径 `~/.codex/log/codex-tui.log`，定位启动失败原因

4. **超时调优**：服务启动慢时，调高 `startup_timeout_sec` 至 30 秒以上

## 六、常见问题与注意事项

1. **MCP 服务启动失败**：检查命令是否正确、依赖是否安装（如 npx 环境正常）、网络是否可访问

2. **OAuth 无法使用**：必须在配置文件顶层设置 `experimental_use_rmcp_client = true`

3. **Windows 路径问题**：配置中路径使用双反斜杠 `\\\\` 或正斜杠 `/`

4. **权限不足**：确保 Codex 沙箱模式为 `workspace-write` 及以上，避免沙箱限制 MCP 调用

5. **Token 安全**：HTTP 类型 MCP 的 Token 不要硬编码在配置中，建议通过环境变量注入

6. **IDE 扩展不生效**：修改配置后重启 IDE 扩展，配置与 CLI 完全同步

7. **服务冲突**：同一端口被占用时，关闭其他服务再启动 MCP

8. **超时优化**：远程 MCP 服务因网络慢启动失败，适当延长超时时间

## 七、总结

MCP 是 Codex 突破原生能力边界的关键，通过标准化协议无缝对接各类开发工具，实现**文档查询、UI 还原、自动化测试、远程服务调用**等全场景能力。CLI 快速配置适合日常快速接入，手动配置适合企业级精细管控，而将 Codex 作为 MCP 服务端则可打通多 AI 协同工作流。无论是个人开发提效，还是团队工具链集成，MCP 都能让 Codex 从单一编程助手升级为全流程开发中枢。

