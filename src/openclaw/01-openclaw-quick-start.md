---
title: OpenClaw 快速入门指南
order: 1
---

# OpenClaw 快速入门指南：打造你的私有化 AI 智能体网关

## 一、OpenClaw 简介：不止于聊天的 AI 执行引擎

OpenClaw（中文社区昵称 "龙虾"）是一款**自托管的 AI 智能体网关**，核心定位是连接你的聊天应用（如 Telegram、WhatsApp、Discord 等）与 AI 模型，构建具备持久记忆、主动执行能力的私有化 AI 助手。它由 Peter Steinberger 开发，采用 MIT 开源许可证，核心开发语言为 TypeScript。

### 核心价值

| 特性 | 说明 |
| --- | --- |
| **自托管** | 运行在你的硬件上，数据完全掌控，无第三方泄露风险 |
| **多渠道集成** | 一个网关同时支持 10+ 主流聊天平台，随时随地通过手机交互 |
| **智能体原生** | 专为 AI 智能体设计，支持工具调用、会话管理、多智能体路由 |
| **模块化扩展** | 通过 Skills 系统实现功能无限扩展，ClawHub 市场提供 9000+ 现成插件 |
| **跨平台兼容** | 支持 macOS、Windows、Linux 全平台部署，轻量高效 |

### 适用场景

- **个人效率提升**：文件处理、浏览器自动化、日程管理、代码生成与调试

- **企业办公自动化**：客服自动回复、合同处理、数据报表生成、内部知识库查询

- **开发者工具链**：服务器监控、日志分析、CI/CD 流程触发、API 测试

- **智能家居控制**：通过自然语言指令控制智能设备，实现场景化自动化

## 二、系统准备：环境配置与依赖安装

### 1. 核心系统要求

| 组件 | 最低版本 | 推荐版本 |
| --- | --- | --- |
| Node.js | 22.14+ LTS | 24.x (最新稳定版) |
| 内存 | 4GB | 8GB+ (运行本地模型建议 16GB) |
| 存储空间 | 1GB | 5GB+ (用于模型缓存和插件) |
| 网络 | 稳定互联网连接 | 支持 WebSocket 的高速网络 |

### 2. 依赖安装（可选）

- **Docker**（推荐）：用于容器化部署，隔离运行环境

- **Git**：用于获取最新源码和插件

- **Python 3.10+**：部分技能插件可能需要 Python 环境

## 三、快速安装

OpenClaw 提供 5 种安装方式，最常用的两种：

### 方式 1：一键脚本安装（推荐）

```bash
# macOS/Linux
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 方式 2：npm 全局安装

```bash
npm install -g openclaw@latest
openclaw --version
```

> 其他安装方式（pnpm/bun/源码/Docker）及安装故障排除，请参考 [全流程安装·更新·迁移·卸载教程](./02-openclaw-installation-guide.md)。

## 四、新手引导：5 分钟完成核心配置

安装完成后，执行**onboard 向导**进行初始化配置：

```bash
# 启动引导并安装守护进程（开机自启）
openclaw onboard --install-daemon
```

### 1. 选择 AI 模型提供商

向导会列出支持的模型选项，包括：

- **OpenAI**（GPT-4o、GPT-4 Turbo）

- **Anthropic**（Claude 3 Opus/Sonnet）

- **本地模型**（如 Llama 3、Qwen 3.5，需提前部署）

- **内置 Pi**（OpenClaw 原生智能体，无需 API 密钥）

输入 API 密钥并测试连接，确保模型配置成功。

### 2. 配置聊天渠道（Telegram 最快）

选择你常用的聊天平台，以 Telegram 为例：

1. 搜索并关注 `@BotFather` 创建新机器人

2. 获取 API 令牌（格式：`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）

3. 输入令牌完成连接

4. 发送 `/start` 到你的机器人开始交互

其他支持渠道：WhatsApp、Discord、飞书、钉钉、Slack 等

### 3. 启用基础技能（可选）

选择需要的核心技能：

- **文件处理**：读取/写入本地文件、PDF 解析

- **浏览器控制**：自动化网页浏览、表单填写

- **系统命令**：执行 Shell 命令（谨慎启用，建议设置权限）

- **日程管理**：创建日历事件、发送提醒

### 4. 启动网关与控制 UI

配置完成后，网关自动启动。通过以下命令打开 Web 控制界面：

```bash
openclaw dashboard  # 默认访问地址：http://127.0.0.1:18789/
```

## 五、基础使用：从聊天到执行的全流程

### 1. 多端交互方式

| 交互方式 | 操作步骤 | 适用场景 |
| --- | --- | --- |
| **Web 控制 UI** | 执行 `openclaw dashboard` 访问 | 桌面端操作、配置管理 |
| **Telegram 机器人** | 发送消息到你的机器人 | 移动端快速指令、远程控制 |
| **WhatsApp** | 扫码配对后直接聊天 | 日常高频使用、文件传输 |
| **CLI 命令行** | `openclaw chat` | 服务器环境、脚本集成 |

### 2. 核心指令示例

#### （1）文件处理

```Plain Text
请帮我分析这个CSV文件：/Users/me/data/sales.csv
要求：
1. 计算总销售额
2. 按产品类别分组统计
3. 生成可视化图表保存为PNG
```

#### （2）浏览器自动化

```Plain Text
帮我完成以下任务：
1. 打开浏览器访问GitHub官网
2. 搜索"openclaw"仓库
3. 统计Star数量和最近更新时间
4. 将结果发送到我的邮箱
```

#### （3）系统命令执行（需提前授权）

```Plain Text
在~/projects目录下创建一个新的Node.js项目，包含package.json和index.js文件
```

### 3. 会话管理与记忆功能

OpenClaw 会自动保存会话历史并建立长期记忆：

- 每个用户/渠道拥有独立会话

- 支持上下文引用（如 "之前那个文件"）

- 可通过 `/forget` 命令清除当前会话记忆

- 可通过 `/save` 命令保存重要信息到知识库

## 六、实战案例：3 个实用场景快速上手

### 案例 1：自动生成周报（办公效率）

**指令**：

```Plain Text
帮我生成本周周报，内容包括：
1. 从Notion获取本周任务完成情况
2. 从GitHub统计提交代码行数
3. 分析邮件中客户反馈的主要问题
4. 按公司模板格式输出为Markdown文件
```

**实现步骤**：

1. 配置 Notion、GitHub、邮件技能插件

2. 授予必要的 API 访问权限

3. 发送指令，等待生成结果

4. 直接在聊天窗口接收或下载文件

### 案例 2：服务器监控与告警（运维场景）

**指令**：

```Plain Text
帮我设置服务器监控：
1. 每小时检查CPU使用率、内存占用和磁盘空间
2. 当CPU使用率超过80%或内存占用超过90%时发送告警
3. 告警同时执行自动扩容脚本
4. 每天生成性能报告发送到运维邮箱
```

**实现步骤**：

1. 启用系统命令和定时任务技能

2. 编写扩容脚本并配置执行权限

3. 设置告警阈值和通知方式

4. 验证监控和告警功能正常工作

### 案例 3：本地模型私有化部署（隐私优先）

**指令**：

```Plain Text
帮我在本地部署Qwen 3.5 7B模型并接入OpenClaw：
1. 检查系统环境是否满足要求
2. 下载模型权重并配置Ollama
3. 测试模型推理性能
4. 将模型设置为OpenClaw默认智能体
```

**实现步骤**：

1. 安装 Ollama（`curl https://ollama.ai/install.sh | sh`）

2. 拉取模型（`ollama pull qwen:3.5-7b-chat`）

3. 在 OpenClaw 配置中选择本地模型

4. 测试聊天功能，确保模型正常响应

## 七、高级配置：安全与性能优化

### 1. 安全加固（必做）

编辑配置文件 `~/.openclaw/openclaw.json`，添加以下安全设置：

```json
{
  "channels": {
    "telegram": {
      "allowFrom": ["+8613800138000"],
      "requireMention": true
    },
    "whatsapp": {
      "allowFrom": ["+8613900139000"],
      "groups": { "*": { "requireMention": true } }
    }
  },
  "skills": {
    "system": {
      "allowCommands": ["ls", "cat", "grep"]
    }
  },
  "security": {
    "enableAuth": true,
    "password": "your_secure_password"
  }
}
```

### 2. 性能优化

- **内存管理**：设置会话超时时间（默认 30 分钟）

    ```json
    { "session": { "timeout": 1800 } }
    ```

- **模型缓存**：启用本地模型缓存，减少重复下载

    ```json
    { "model": { "cacheDir": "~/.openclaw/models", "cacheSize": "10GB" } }
    ```

- **并行处理**：调整最大并发任务数（根据 CPU 核心数设置）

    ```json
    { "concurrency": { "maxTasks": 4 } }
    ```

### 3. 自定义技能开发

OpenClaw 支持纯 Markdown 编写自定义技能，无需代码门槛：

1. 创建技能目录：`mkdir -p ~/.openclaw/workspace/skills/hello-greeting`
2. 编写 `SKILL.md`，声明名称、描述与触发规则
3. 重启网关或 `/new` 新会话即可生效

> 完整技能开发教程、SKILL.md 格式、ClawHub 生态与安全规范，请参考 [Skills 技能系统详解](./14-openclaw-skills-system.md)。

## 八、常见问题与故障排除

### 1. 安装失败

- **权限问题**（Linux/macOS）：使用 `sudo` 重新安装或修改 npm 权限

    ```bash
    sudo npm install -g openclaw@latest
    ```

- **网络问题**：切换国内镜像源

    ```bash
    npm config set registry https://registry.npmmirror.com
    ```

### 2. 模型连接失败

- 检查 API 密钥是否正确

- 确认网络可以访问模型提供商（如 OpenAI、Anthropic）

- 查看日志获取详细错误信息：`openclaw logs`

### 3. 聊天渠道无响应

- Telegram：检查机器人令牌是否正确，确保已发送 `/start` 命令

- WhatsApp：确认已完成扫码配对，网络连接正常

- 检查配置文件中的 `allowFrom` 设置是否包含你的号码

### 4. 性能问题

- 减少并发任务数

- 关闭不必要的技能插件

- 升级硬件（特别是运行本地模型时）

## 九、进一步学习资源

1. **官方文档**：https://docs.openclaw.ai/zh-CN（最权威的参考资料）

2. **ClawHub 插件市场**：https://clawhub.ai（9000+ 现成技能插件）

3. **GitHub 仓库**：https://github.com/openclaw/openclaw（提交 Issue 和 PR）

## 总结

OpenClaw 的核心价值在于**私有化部署 + 自动化执行**，让 AI 真正成为你可以随时调用的个人助手，而不仅仅是聊天工具。通过本教程，你已经掌握了从安装配置到基础使用的全流程，接下来可以根据自己的需求探索更多高级功能和自定义开发。

记住，OpenClaw 的潜力在于其模块化设计和强大的社区生态——随着你不断学习和使用，它将成为你提升效率、解决问题的得力助手。
