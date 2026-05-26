# Hermes Agent 快速入门教程：从环境准备到基础配置


## 一、Hermes Agent 概述

Hermes Agent 是由 Nous Research 开发的**开源自进化 AI 智能体框架**，采用 MIT 许可证，核心定位是 “会随使用不断成长的数字同事”，而非单纯的聊天机器人。它打破传统 AI 无状态对话的局限，内置持久记忆、技能自动沉淀、闭环学习引擎，支持 200+ 大模型一键切换，可接入 15+ 主流消息平台，兼顾个人助手、团队自动化、开发辅助等多场景需求。

### 核心差异化特性

1. **自进化学习闭环**：基于 GEPA 引擎，通过 “任务执行 - 效果评估 - 策略优化 - 技能沉淀” 闭环，仅需 100-500 次迭代即可优化能力，越用越智能。

2. **三层持久记忆**：采用 “上下文压缩 + SQLite 会话检索 + 持久化 \[MEMORY.md\](MEMORY.md)” 架构，跨会话记住用户偏好、项目背景，避免重复沟通。

3. **技能自动沉淀**：完成复杂任务后，自动将流程提炼为可复用技能（遵循 \[agentskills.io\](agentskills.io) 标准），支持手动编写与社区安装。

4. **全模型兼容**：零锁定设计，支持 OpenAI、Anthropic、智谱、Kimi、MiniMax 等国内外模型，也兼容 Ollama 本地部署。

5. **多平台统一网关**：一键接入飞书、钉钉、企业微信、Telegram、Discord 等，跨平台保持统一记忆与会话。

6. **安全沙箱执行**：支持本地、Docker、SSH 等 7 种终端后端，容器隔离避免权限风险，保障执行安全。

### 与同类工具核心对比

目前主流 AI 智能体 / 工具包括 **Claude Code、OpenAI Codex、OpenClaw**，与 Hermes Agent 定位、能力差异显著：

|对比维度|Hermes Agent|Claude Code（Anthropic）|OpenAI Codex|OpenClaw（龙虾）|
|---|---|---|---|---|
|核心定位|**通用自进化 Agent**（全场景）|**专用编码 Agent**（仅代码）|**轻量编码 Agent**（仅代码）|**多平台网关 Agent**（连接优先）|
|模型兼容性|支持 200+ 模型（国产 / 海外 / 本地）|**仅 Claude 系列**（模型锁定）|**仅 OpenAI 系列**（模型锁定）|支持多模型，但生态较弱|
|记忆能力<br>|**三层持久记忆**（跨会话长期保存）|会话记忆（无长期持久化）|会话记忆（无长期持久化）|文件记忆（仅基础存储，无检索）|
|技能机制|**自动生成 + 优化技能**（自进化）|手动配置插件|手动配置工具|静态技能（无自动沉淀）|
|平台接入|15+ 平台（含飞书 / 钉钉）|仅 IDE / 终端|仅 IDE / 终端|22+ 平台（含微信 / QQ）|
|部署方式|自托管（本地 / Docker/VPS）|云端 + 本地|云端优先|自托管 + 端侧|
|核心优势|**自进化 + 全场景 + 模型自由**|代码理解深度强|轻量高效、并行任务|接入广、消费级体验好|

**一句话选型**：

- 选 Hermes Agent：需要**全场景通用、长期记忆、自动进化**，不想被单一模型锁定；

- 选 Claude Code：专注**复杂代码开发、深度工程化**，接受 Claude 模型锁定；

- 选 OpenAI Codex：追求**轻量编码、快速执行**，依赖 OpenAI 生态；

- 选 OpenClaw：优先**多平台接入、端侧联动**，不需要自进化能力。

## 二、环境准备

### 系统要求

- 支持系统：macOS、Linux、Windows（需 WSL2，原生 PowerShell 为 Beta 版）

- 基础依赖：Git（必需）、Python 3.11（自动安装）、Node.js v22（自动安装）

- 网络提示：中国大陆用户默认走国内镜像加速，精简非必要依赖，安装更稳定

### 安装前检查

打开终端（Windows 用 WSL2 或 PowerShell），执行以下命令检查依赖：

```bash
git --version  # 需输出 2.0+ 版本
```

## 三、快速安装

### 1. macOS / Linux / WSL2（推荐）

执行一键安装命令（国内镜像加速）：

```bash
curl -fsSL https://res1.hermesagent.org.cn/install.sh | bash
```

安装完成后刷新环境变量：

```bash
source ~/.bashrc  # bash 用户
```

### 2. Windows 原生 PowerShell（Beta）

以管理员身份打开 PowerShell，执行：

```powershell
irm https://res1.hermesagent.org.cn/install.ps1 | iex
```

安装完成后**关闭并重新打开 PowerShell** 生效。

### 验证安装

执行命令检查版本，输出版本号即成功：

```bash
hermes --version
hermes doctor
```

## 四、基础配置（模型接入）

安装后需配置大模型提供商，支持国内（智谱、Kimi）、国外（OpenAI、Anthropic）及本地模型，核心命令：

```bash
hermes model
```

### 1. 国内模型配置（无需海外网络）

|模型提供商|环境变量|配置说明|
|---|---|---|
|智谱 GL|`ZHIPUAI_API_KEY`|输入官网申请的 API Key|
|Kimi（月之暗面）|`KIMI_API_KEY`|支持长上下文，适合文档分析|
|阿里云通义千问|`DASHSCOPE_API_KEY`|通过 DashScope 接入|

### 2. 国外模型配置

|模型提供商|配置方式|
|---|---|
|OpenAI|输入 `OPENAI_API_KEY`，支持 GPT-4o、GPT-3.5|
|Anthropic Claude|输入 `ANTHROPIC_API_KEY`，支持 Claude 3/4 系列|
|OpenRouter|输入 `OPENROUTER_API_KEY`，一键访问 200+ 模型|

### 3. 本地模型配置（Ollama）

1. 先安装 Ollama 并启动本地模型（如 Llama3、Qwen）

2. 执行 `hermes model` → 选择「Custom Endpoint」

3. 输入 Ollama 地址（默认 [http://localhost:11434](http://localhost:11434)）及模型名

### 配置文件说明

所有配置集中在 `~/.hermes/` 目录：

- `config.yaml`：主配置（工具、网关、终端设置）

- `.env`：存储 API Key（权限设为 600，避免泄露）

- `memories/`：持久记忆文件

- `skills/`：自动 / 手动安装的技能

## 五、首次使用（基础对话）

### 1. 启动交互式会话

终端执行命令，进入对话模式：

```bash
hermes
hermes --tui
```

出现欢迎横幅即成功，可直接输入问题：

```Plain Text
❯ 你好，帮我总结 Hermes Agent 的核心功能
```

### 2. 常用斜杠命令（输入 `/` 查看补全）

|命令|功能|
|---|---|
|`/help`|查看所有命令|
|`/model`|快速切换模型|
|`/tools`|启用 / 禁用工具（终端、文件、搜索）|
|`/save`|保存当前会话|
|`/compress`|压缩上下文，避免超限|

### 3. 核心工具调用示例

Hermes 默认支持终端、文件、网页搜索工具，直接用自然语言指令：

```bash
❯ 帮我查看当前磁盘空间，列出最大的 5 个目录

❯ 在桌面创建 test.md，写入 Hermes 入门笔记

❯ 搜索 2026 年大模型发展趋势，总结 3 个关键点
```

### 4. 会话管理

- 中断对话：`Ctrl+C` 或直接输入新指令

- 恢复会话：

```bash
hermes --continue  # 恢复最近一次会话
```

## 六、进阶功能入门

### 1. 技能管理（自动 / 手动扩展能力）

#### 自动技能

完成 5 次以上同类任务（如爬虫、代码审查），Hermes 自动提炼为技能，存入 `~/.hermes/skills/`。

#### 手动安装社区技能

```bash
hermes skills search kubernetes

hermes skills install openai/skills/k8s
```

### 2. 消息网关（接入飞书 / 钉钉）

一键配置多平台接入，实现跨平台对话：

```bash
hermes gateway setup

hermes gateway &
```

支持平台：飞书、钉钉、企业微信、Telegram、Discord 等。

### 3. Docker 沙箱部署（安全隔离）

避免工具执行影响宿主机，推荐生产环境使用：

```bash
mkdir -p ~/.hermes
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes setup

docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes gateway run
```

### 4. MCP 集成（连接外部工具）

通过 MCP（Model Context Protocol）接入 GitHub、数据库、企业内网工具，无需定制开发。
配置示例（编辑 `~/.hermes/config.yaml`）：

```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "你的令牌"
```

## 七、常见问题排查

1. **命令找不到（hermes: command not found）**
执行 `source ~/.bashrc`（或对应 shell 配置），或检查 `~/.local/bin` 是否加入环境变量。

2. **模型配置失败 / API 错误**

    - 检查 API Key 正确性

    - 执行 `hermes config show` 查看配置

    - 国内模型确认无海外网络限制。

3. **工具执行无权限**
Windows 用户优先用 WSL2；Docker 部署可解决权限隔离问题。

4. **会话上下文超限**
输入 `/compress` 压缩上下文，或切换更大上下文模型（如 Kimi 2.6、GPT-4o）。

## 八、总结

Hermes Agent 作为**自进化通用 AI 智能体**，核心价值在于 “持久记忆 + 技能沉淀 + 全场景适配”，既适合个人日常助手、代码辅助，也可用于团队自动化、企业知识库搭建。

对比 Claude Code、Codex 等专用工具，Hermes Agent 胜在**模型自由、长期记忆、自进化能力**；对比 OpenClaw，Hermes 更聚焦 “深度成长” 而非单纯 “连接广度”。

本文覆盖从安装、配置到基础使用、进阶功能的全流程，下一步可探索：

- 接入更多消息平台（飞书 / 钉钉）

- 编写自定义技能

- 部署到服务器长期运行

- 集成 MCP 工具扩展能力

更多细节可参考官方文档：[https://hermesagent.org.cn](https://hermesagent.org.cn)。
