---
title: Hermes Agent 开源自进化 AI 智能体框架教程
order: 2
---

# Hermes Agent 开源自进化 AI 智能体框架教程

传统 AI 智能体需要手动编写技能、无法自我优化，用久了还是"老样子"。Hermes Agent 打破了这个局限——它内置闭环学习循环，能从交互经验中自主创建技能、在使用中持续优化，用得越多越聪明。同时支持 200+ 模型自由切换、6 种终端后端部署、Telegram/Discord/Teams 等多平台接入，采用 MIT 开源协议。

项目开源地址：[https://github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)

## 一、框架核心特性

Hermes Agent 区别于传统 AI 智能体的核心优势的是“自进化能力”，同时具备多场景适配、高灵活性等特点，具体核心特性如下：

- **闭环自进化学习循环**：唯一内置学习循环的 AI 智能体，可从交互经验中自主创建技能，在使用过程中持续优化技能效果；具备周期性记忆强化机制，能搜索自身过往对话记录，构建用户画像，实现跨会话的知识沉淀与复用，兼容 agentskills.io 开放标准。

- **多模型自由切换**：支持 Nous Portal、OpenRouter（200+ 模型）、NVIDIA NIM（Nemotron）、小米 MiMo、Kimi/ moonshot、MiniMax、Hugging Face、OpenAI 等主流模型，也可接入自定义模型端点，通过 `hermes model` 命令即可切换，无需修改代码，无模型锁定限制。

- **全终端无缝交互**：支持 CLI 终端交互与多消息平台接入，包括 Telegram、Discord、Slack、WhatsApp、Signal 等，新增 Microsoft Teams 平台适配（v0.12.0 特性），可通过单一网关进程实现跨平台对话连续性，支持语音备忘录转录，满足不同场景下的交互需求。

- **内置调度自动化**：集成 cron 调度器，可通过自然语言配置定时任务，如每日报告、夜间备份、每周审计等，任务执行结果可推送至任意接入平台，实现无人值守自动化运行。

- **子代理并行处理**：可生成独立子代理，实现多工作流并行执行；支持通过 Python 脚本调用工具 RPC 接口，将多步骤流程简化为零上下文成本的操作，提升任务处理效率。

- **全场景部署适配**：支持 6 种终端后端，包括本地部署、Docker、SSH、Daytona、Singularity、Modal，其中 Daytona 和 Modal 提供无服务器持久化能力，闲置时自动休眠，唤醒响应迅速，可运行于 5 美元 VPS 或高性能 GPU 集群。

- **研究级就绪能力**：内置批量轨迹生成、Atropos RL 环境、轨迹压缩功能，可用于下一代工具调用模型的训练，适配科研人员的实验需求；新增 WebResearchEnv RL 环境（v0.12.0 特性），支持多步骤网页研究任务。

## 二、环境准备

了解了核心特性后，接下来准备运行环境。

### 2.1 支持平台

- 支持系统：Linux、macOS、WSL2、Android（通过 Termux）

- 不支持系统：原生 Windows（需安装 WSL2 后使用）

### 2.2 依赖要求

- 基础依赖：curl、git（用于安装与克隆项目）

- Python 环境：Python 3.11+（推荐，适配 uv 虚拟环境管理）

- 可选依赖：yt-dlp（用于媒体相关功能）、uv（Python 包管理工具，自动安装）

- Android/Termux 额外说明：需安装 Termux 应用，Hermes 会自动安装适配 Android 的`.[termux]` 扩展包，避免语音依赖冲突。

## 三、快速安装与初始化

### 3.1 一键安装（推荐）

适用于 Linux、macOS、WSL2，执行以下命令即可完成自动安装，安装脚本会处理平台特异性配置，自动适配最新 v0.12.0 版本：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

### 3.2 安装后初始化

安装完成后，需重载 shell 环境以加载 Hermes 命令，执行以下命令：

```bash
# Bash 终端
source ~/.bashrc
# Zsh 终端
source ~/.zshrc
```

初始化完成后，启动 Hermes 交互界面：

```bash
hermes
```

### 3.3 手动安装（开发者推荐）

适用于需要自定义配置、参与开发的场景，步骤如下：

```bash
# 克隆项目仓库
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 安装 uv 包管理工具（自动适配系统）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建并激活虚拟环境
uv venv venv --python 3.11
source venv/bin/activate

# 安装完整依赖（含开发与研究相关依赖）
uv pip install -e ".[all,dev]"

# 启动 Hermes（无需手动激活虚拟环境，自动检测）
./hermes
```

### 3.4 Android/Termux 安装

1. 安装 Termux 应用（可从 F-Droid 下载）；

2. 执行一键安装命令（与桌面端一致）：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

3. 安装完成后直接启动：`hermes`，Termux 环境会自动适配，避免语音依赖冲突。

### 3.5 环境校验与更新

安装完成后，可通过以下命令校验环境是否正常：

```bash
hermes doctor
```

更新 Hermes 至最新版本（当前为 v0.12.0）：

```bash
hermes update
```

## 四、基础使用指南

安装完成后，以下命令覆盖日常交互的核心场景。

### 4.1 核心 CLI 命令

Hermes 提供简洁的 CLI 命令，覆盖初始化、配置、交互等核心场景，常用命令如下：

```bash
# 启动交互式 CLI 对话（核心命令）
hermes

# 配置 LLM 提供商与模型
hermes model

# 配置启用的工具集
hermes tools

# 单个配置项设置
hermes config set

# 启动消息网关（对接 Telegram、Discord 等）
hermes gateway

# 执行全量设置向导（配置所有参数，适合首次使用）
hermes setup

# 诊断环境问题
hermes doctor
```

### 4.2 交互界面使用

#### 4.2.1 CLI 交互（实战案例）

执行 `hermes` 启动后，进入 TUI 交互界面，以下为 3 个高频实战场景，可直接复制指令执行：

```
# 启动交互后，输入自然语言指令
hermes
# 输入：帮我生成一份 Hermes Agent 基础使用清单（含3个核心命令）
# 执行后，输入 /skills 查看自动生成的技能（命名类似“generate-hermes-basic-usage”）
# 后续可直接输入 /generate-hermes-basic-usage 快速调用该技能
```

```
# 启动交互后，切换至 Kimi 模型处理中文文案
/model kimi:moonshot-v1
# 输入：帮我撰写一段 Hermes Agent 的中文推广文案（50字以内）
# 再切换至 OpenAI GPT-4 处理技术总结
/model openai:gpt-4
# 输入：总结 Hermes Agent 与传统 AI 智能体的3个核心区别
```

```
# 启动交互时添加 --yolo  flag，无需手动确认即可执行任务
hermes --yolo
# 输入：批量删除 ~/.hermes/skills 下30天未使用的技能
# 系统将直接执行，无需二次确认，适合自动化脚本场景
```

补充操作：多行编辑、命令自动补全；使用 slash 命令：`/new`（新建对话）、`/reset`（重置对话）、`/model [provider:model]`（切换模型）；中断当前任务：`Ctrl+C` 或直接发送新消息；查看技能：`/skills` 或直接输入 `/<skill-name>`。

#### 4.2.2 消息平台交互（实战案例）

需先启动网关，才能通过 Telegram、Discord、Microsoft Teams 等平台交互，以下为 Telegram 和 Teams 两个高频场景案例：

```bash
# 1. 通用网关配置（首次使用）
hermes gateway setup
# 按提示选择平台（如Telegram），输入Bot Token完成配置
# 启动网关进程
hermes gateway start
```

```bash
# 配置每日18:00推送系统状态报告至Telegram
hermes cron add "每日系统状态" "0 18 * * *" "生成今日系统CPU、内存使用率报告" --platform telegram
# 启动网关后，每日18:00将自动接收报告，无需手动操作
```

```bash
# 配置Teams平台（需先获取Teams Bot Token）
hermes gateway setup --platform teams
# 启动网关后，在Teams群聊中发送指令
# 输入：/model nous:hermes-3-pro 切换至Nous自研模型
# 输入：帮我整理群聊中今日的核心讨论要点，生成简洁总结
```

启动后，通过对应平台发送消息即可与 Hermes 交互，支持的 slash 命令与 CLI 一致，部分平台专属命令：`/status`（查看网关状态）、`/sethome`（设置默认交互目录）。

### 4.3 CLI 与消息平台命令对比

|操作|CLI 方式|消息平台方式|
|---|---|---|
|启动对话|`hermes`|启动网关后发送消息|
|新建对话|`/new` 或 `/reset`|`/new` 或 `/reset`|
|切换模型|`/model [provider:model]`|`/model [provider:model]`|
|设置人格|`/personality [name]`|`/personality [name]`|
|中断任务|`Ctrl+C`或新消息|`/stop` 或新消息|

## 五、高级功能详解

掌握了基础交互，接下来是 Hermes 的核心差异化能力——自进化学习、调度自动化、子代理并行和部署方案。

### 5.1 自进化学习循环实战（核心案例）

Hermes Agent 的核心能力是自进化，无需手动编写技能，以下为两个实战案例，覆盖科研与日常自动化场景：

```
# 启动交互，输入多步骤科研任务
hermes --yolo
# 输入：使用 WebResearchEnv RL 环境（v0.12.0新特性），批量生成10条多步骤网页研究轨迹，每条轨迹包含5个步骤，生成完成后用/compress命令压缩轨迹文件，保存至~/hermes/research-trajectories目录
# 执行过程：
# 1. Hermes 自动调用 WebResearchEnv 环境，生成轨迹
# 2. 完成后自主创建“generate-rl-trajectories”技能
# 3. 执行 /compress 压缩轨迹，优化存储
# 后续复用：直接输入 /generate-rl-trajectories 即可快速执行相同任务，Hermes 会根据过往经验优化生成速度
```

```
# 启动交互，输入任务
hermes
# 输入：帮我提取今日 Chrome 浏览器的浏览记录，按“网站名称-访问时间-页面标题”整理成表格，排除广告类网站，保存为markdown文件至~/hermes/daily-browsing.md
# 执行后：
# 1. Hermes 自动调用浏览器接口提取记录，筛选有效内容
# 2. 生成“organize-browser-history”技能，存储于~/.hermes/skills/
# 3. 重复执行3次后，Hermes 会自动优化筛选规则，减少无效内容，提升整理效率
# 记忆强化：输入 /insights --days 1 查看今日交互洞察，确认技能优化效果
```

核心流程总结：执行复杂任务 → 自动创建技能 → 重复使用优化技能 → 记忆强化沉淀知识。

### 5.2 调度自动化（定时任务实战案例）

利用内置 cron 调度器，可实现多场景无人值守自动化，以下为3个高频案例：

```bash
# 案例1：每日23:00自动备份 Hermes 数据并推送备份结果至Discord
hermes cron add "Hermes数据备份" "0 23 * * *" "备份~/.hermes目录至~/hermes-backup，压缩为zip文件，检查备份完整性，推送结果至Discord" --platform discord

# 案例2：每周一9:00生成上周系统运行报告（CPU、内存、磁盘使用率）
hermes cron add "每周系统报告" "0 9 * * 1" "采集上周系统运行数据，生成可视化报告（markdown格式），发送至指定邮箱" --platform email --email xxx@xxx.com

# 案例3：每小时检查网关状态，异常时自动重启并通知管理员
hermes cron add "网关状态监控" "0 * * * *" "检查hermes gateway进程状态，若未运行则自动启动，发送状态通知至Telegram管理员" --platform telegram

# 查看所有定时任务
hermes cron list

# 删除指定定时任务
hermes cron delete "网关状态监控"
```

### 5.3 子代理并行处理（实战案例）

当需要同时处理多个任务时，可生成子代理并行执行，提升效率，以下为两个典型场景：

```bash
# 案例1：并行处理“数据采集+报告生成”任务
# 主代理：生成子代理处理数据采集，自身等待接收数据并生成报告
hermes
# 输入：生成子代理“data-collector”，采集3个指定科技网站的最新文章标题、链接、发布时间，并行执行；主代理等待数据采集完成后，整理成表格报告，保存为csv文件
# 查看子代理状态
hermes delegate list
# 查看子代理执行日志
hermes delegate logs "data-collector"
# 终止子代理（若任务异常）
hermes delegate stop "data-collector"

# 案例2：多子代理并行处理不同平台消息回复
# 生成2个子代理，分别处理Telegram和Discord的用户消息，主代理监控整体状态
hermes delegate "telegram-reply" "自动回复Telegram用户的基础咨询，调用Hermes基础技能库" --parallel
hermes delegate "discord-reply" "自动回复Discord用户的安装问题，提供步骤指引" --parallel
# 查看所有子代理执行情况
hermes delegate list
```

### 5.4 Docker 部署（生产环境实战案例）

Hermes 提供完善的 Docker 部署支持，避免环境依赖冲突，以下为生产环境持久化部署案例（含数据挂载、网关自启动）：

```bash
# 1. 克隆项目
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 2. 修改docker-compose.yml，实现数据持久化（关键配置）
# 找到volumes配置，添加以下内容（挂载Hermes配置、技能、数据目录）
volumes:
  hermes-data:
    driver: local
    driver_opts:
      type: 'none'
      o: 'bind'
      device: '/root/.hermes'  # 本地目录，根据实际情况修改

# 3. 启动Docker容器（后台运行，网关自启动）
docker-compose up -d

# 4. 进入容器交互，配置模型与网关
docker exec -it hermes-agent hermes
# 配置OpenAI模型
/model set openai:gpt-4
# 配置Telegram网关
gateway setup --platform telegram
# 启动网关并设置开机自启
gateway start --auto-restart

# 5. 查看容器运行状态
docker ps
# 查看Hermes日志
docker logs -f hermes-agent

# 6. 停止容器（如需维护）
docker-compose down
```

补充说明：可修改 `docker-compose.yml` 配置端口、挂载目录，实现数据持久化与自定义配置；若需部署多个Hermes实例，可通过修改容器名称和挂载目录实现。

### 5.5 模型切换与配置（实战案例）

切换模型无需修改代码，直接通过命令配置，以下为多场景模型切换案例，覆盖不同任务需求：

```bash
# 案例1：切换模型处理不同类型任务
# 切换至Kimi模型（擅长中文文案），撰写产品推广文案
hermes model set kimi:moonshot-v1
hermes -p "帮我撰写一段Hermes Agent的中文推广文案，突出自进化和多平台部署优势，50字以内"

# 切换至Nous Portal模型（自研模型，适配Hermes最优），处理技能创建任务
hermes model set nous:hermes-3-pro
hermes -p "帮我创建一个技能，用于每周五自动整理本周的交互日志，生成总结报告"

# 切换至NVIDIA NIM模型（擅长科研计算），处理RL轨迹分析任务
hermes model set nvidia:nemotron-4
hermes -p "分析~/hermes/research-trajectories目录下的轨迹文件，生成可视化分析报告"

# 案例2：查看模型列表与当前模型
hermes model list  # 列出所有支持的模型（含OpenRouter 200+模型）
hermes model current  # 查看当前使用的模型

# 案例3：配置自定义模型端点
hermes model set custom:my-model --endpoint http://localhost:8080/v1/completions --api-key my-api-key
# 验证自定义模型是否可用
hermes -p "测试自定义模型，输出'Hello Hermes'"
```

## 六、从 OpenClaw 迁移指南

如果之前使用 OpenClaw，Hermes 可自动迁移配置、记忆、技能等数据，支持两种迁移方式，以下为实战迁移案例：

### 6.1 首次安装迁移（新手推荐）

执行 `hermes setup` 启动设置向导时，系统会自动检测 `~/.openclaw` 目录，提示是否迁移，点击确认即可完成全量迁移，迁移完成后会生成迁移报告，示例如下：

```bash
hermes setup
# 系统提示：检测到OpenClaw数据目录，是否进行全量迁移？(Y/n)
# 输入Y，等待迁移完成
# 迁移报告示例：
# 迁移成功：人格文件(SOUL.md)、记忆数据(MEMORY.md)、技能(12个)、配置信息已迁移至~/.hermes/
# 迁移失败：无（若有失败项，会列出具体原因）
```

### 6.2 手动迁移（任意时间，进阶用户）

```bash
# 案例1：交互式全量迁移（推荐，可查看迁移进度）
hermes claw migrate
# 按提示操作，可实时查看迁移的文件类型和数量

# 案例2：预览迁移内容（不实际执行，避免误操作）
hermes claw migrate --dry-run
# 输出示例：将迁移人格文件1个、记忆数据2个、技能12个、密钥3个，无冲突项

# 案例3：仅迁移用户数据（不迁移密钥，适合多设备迁移）
hermes claw migrate --preset user-data

# 案例4：覆盖现有冲突数据（迁移时若有同名文件，强制覆盖）
hermes claw migrate --overwrite
```

### 6.3 迁移内容说明

- 人格文件：SOUL.md

- 记忆数据：MEMORY.md 和 USER.md 中的记录

- 技能：用户创建的技能会迁移至 `~/.hermes/skills/openclaw-imports/`

- 配置信息：命令白名单、消息平台配置、工作目录

- 密钥：Telegram、OpenRouter、OpenAI 等平台的 API 密钥

## 七、常见问题与排查

- **安装失败**：检查网络连接，确保 curl、git 已安装；Windows 用户需确认已安装 WSL2；Termux 用户需更新 Termux 至最新版本。

- **启动后无响应**：执行 `hermes doctor` 诊断环境，检查 Python 版本是否达标（≥3.11），或重启终端重新加载环境。

- **模型切换失败**：确认模型提供商的 API 密钥已配置，执行 `hermes config set` 检查密钥配置，或更换其他可用模型。

- **网关启动失败**：检查消息平台的配置是否正确（如 Telegram Bot Token），确保网络可访问对应平台，执行 `hermes gateway setup` 重新配置；Teams 网关失败需确认 Bot Token 权限是否足够。

- **迁移失败**：检查 `~/.openclaw` 目录是否存在，执行 `hermes claw migrate --dry-run` 查看冲突项，使用 `--overwrite` 覆盖冲突。

- **技能无法创建**：确保执行的任务为多步骤复杂任务，简单任务不会触发自动技能创建；检查 `~/.hermes/skills/` 目录权限。

- **--yolo flag 无效**：确认 Hermes 版本≥v0.12.0，执行 `hermes update` 更新至最新版本。

## 八、总结

Hermes Agent 的核心差异化在于”自进化”——执行复杂任务后自动创建技能，重复使用时持续优化，配合周期性记忆强化实现跨会话知识沉淀。建议从 CLI 交互入手，体验一次多步骤任务后通过 `/skills` 查看自动生成的技能，再逐步扩展到消息平台接入、调度自动化和 Docker 部署等高级场景。
