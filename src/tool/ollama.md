# Ollama 全面使用教程：本地+云端高效运行大模型

Ollama 是一款开源、轻量且高效的大模型本地运行工具，支持 Windows、macOS、Linux 全平台，能够一键部署 Llama 3、Qwen2.5、DeepSeek、Gemma 4 等上百款主流大语言模型，无需复杂配置，即可实现本地对话、代码生成等功能，同时还支持云端模型调用，解决低配设备无法运行大参数量模型的痛点。本文将聚焦 Ollama 运行大模型的核心场景，从安装到实战，手把手教你玩转 Ollama，覆盖新手必备的全流程操作。

## 一、前置准备：了解 Ollama 核心特性与硬件要求

### 1.1 核心特性

Ollama 之所以成为本地运行大模型的首选工具，核心优势在于简洁高效、兼容性强，具体特性如下：

- 一键部署：一行命令即可完成模型安装与启动，无需手动配置依赖环境；

- 跨平台支持：完美适配 Windows、macOS、Linux，操作逻辑统一，降低学习成本；

- 模型丰富：内置上百款开源模型，涵盖通用对话、代码生成、专业领域模型，同时支持自定义模型；

- API 兼容：自带 OpenAI 格式 API，现有 AI 项目可直接迁移适配；

- 云端拓展：支持调用 Ollama 自带 Cloud 模型，无需本地显存，轻松运行超大参数量模型；

- 安全可靠：支持 API 密钥认证，可限制本地访问，避免未授权调用。

### 1.2 硬件要求

Ollama 运行模型的流畅度，主要取决于设备的显存和内存，不同规模模型的硬件要求如下（推荐配置），可根据自身设备选择合适的模型：

|模型规模|显存要求|内存要求|推荐场景|
|---|---|---|---|
|3B（轻量型）|3GB+|8GB+|低配设备、快速测试、简单对话|
|7B（推荐型）|4-6GB|16GB+|日常开发、个人使用、代码辅助|
|13B（进阶级）|10-12GB|32GB+|专业应用、团队协作、复杂任务处理|
|30B+（专业型）|24GB+|64GB+|企业部署、深度研究、复杂场景推理|

注：若设备显存不足，可选择 Ollama Cloud 模型，无需依赖本地硬件资源。

## 二、Ollama 安装教程（Windows + macOS）

Ollama 安装流程简洁，Windows 和 macOS 均支持一键安装，以下是详细步骤，确保安装后能正常启动服务。

### 2.1 Windows 系统安装（Win10/11 适用）

#### 步骤 1：下载安装包

访问 Ollama 官方网站（[https://ollama.com/download](https://ollama.com/download)），滑动至页面下方，找到 Windows 版本，点击下载 `OllamaSetup.exe` 安装包（约 1.8GB）。

#### 步骤 2：运行安装

双击下载好的 `OllamaSetup.exe`，按照安装向导提示操作，**务必勾选「Add to PATH」选项**（将 Ollama 加入系统环境变量，方便后续命令行调用），然后点击「Install」完成安装。

#### 步骤 3：验证安装与启动服务

安装完成后，打开 PowerShell 或 CMD 命令行工具，输入以下命令验证安装是否成功：

```bash
ollama --version
```

若输出类似「ollama version is 0.12.0」的版本信息，说明安装成功。

Ollama 安装后会自动启动服务，可在系统托盘查看 Ollama 图标；若未自动启动，在命令行输入以下命令手动启动服务：

```bash
ollama serve
```

注意：启动服务的终端窗口需保持打开，后续操作需新开一个终端窗口执行。

### 2.2 macOS 系统安装（Monterey 及以上适用）

macOS 提供两种安装方式，推荐新手使用官网下载方式，便捷高效；开发者可选择 Homebrew 安装。

#### 方式 1：官网下载安装（推荐）

1. 访问 Ollama 官方网站（[https://ollama.com/download](https://ollama.com/download)），点击「Download for macOS」下载安装包；

2. 下载完成后解压，将 `Ollama.app` 拖入「应用程序」文件夹；

3. 双击打开 `Ollama.app`，菜单栏会出现 Ollama 图标，说明服务已成功启动；

4. 打开「终端」，输入 `ollama --version`，验证安装成功。

#### 方式 2：Homebrew 安装（开发者推荐）

若已安装 Homebrew，直接在终端输入以下命令一键安装：

```bash
brew install ollama
```

安装完成后，输入以下命令启动服务：

```bash
ollama serve
```

若需后台运行服务（不占用终端窗口），输入：

```bash
ollama serve 
```

### 2.3 国内加速配置（必做）

由于 Ollama 官方模型库在国内访问较慢，建议配置国内镜像加速，避免下载模型时卡顿或失败。

#### Windows（PowerShell）

```bash
# 临时配置（当前终端有效）
$env:OLLAMA_MODEL_SERVER="https://mirror.ollama.com"

# 永久配置（全局有效）
# 1. 右键「此电脑」→「属性」→「高级系统设置」→「环境变量」
# 2. 在「用户变量」中新建：
# 变量名：OLLAMA_MODEL_SERVER
# 变量值：https://mirror.ollama.com
```

#### macOS / Linux

```bash
# 临时配置（当前终端有效）
export OLLAMA_MODEL_SERVER=https://mirror.ollama.com

# 永久配置（全局有效）
nano ~/.bashrc # 或 ~/.zshrc（根据自己的终端配置选择）
# 在文件中添加：export OLLAMA_MODEL_SERVER=https://mirror.ollama.com
# 保存后重新加载配置：
source ~/.bashrc # 或 source ~/.zshrc
```

## 三、安装并运行开源模型

Ollama 内置上百款开源模型，支持通过命令行一键拉取（下载）和运行，操作简单，无需额外配置。以下是常用开源模型的安装与运行方法，涵盖通用对话、代码生成等场景。

### 3.1 核心操作逻辑

Ollama 操作模型的核心命令的是 `pull`（拉取模型）和 `run`（运行模型），基本语法如下：

```bash
# 拉取模型（格式：ollama pull 模型名称:版本，版本可省略，默认最新版）
ollama pull 模型名称[:版本]

# 运行模型（拉取成功后，直接运行，自动进入交互模式）
ollama run 模型名称[:版本]
```

### 3.2 常用开源模型安装与运行示例

#### 示例 1：通用对话模型（Qwen2.5 7B，推荐新手）

Qwen2.5 是阿里开源的通用大模型，响应速度快，适配中文场景，7B 版本适合大多数个人设备：

```bash
# 拉取 Qwen2.5 7B 模型
ollama pull qwen2.5:7b

# 运行模型，进入交互对话模式
ollama run qwen2.5:7b
```

运行成功后，输入问题即可与模型对话，例如输入「介绍一下 Ollama」，模型会自动生成回复；输入 `/exit` 或按下`Ctrl+D` 可退出交互模式。

#### 示例 2：代码生成模型（CodeLlama 7B）

CodeLlama 是 Meta 开源的代码生成模型，支持多种编程语言，适合开发者辅助编码：

```bash
# 拉取 CodeLlama 7B 模型
ollama pull codellama:7b

# 运行模型，专注代码生成
ollama run codellama:7b
```

进入交互模式后，可输入代码需求，例如「用 Python 写一个快速排序算法」，模型会生成完整代码并附带注释。

#### 示例 3：进阶模型（Gemma 4，适合中高配设备）

Gemma 4 是 Google 开源的大模型，性能强劲，支持多场景任务，可根据设备显存选择版本：

```bash
# 拉取 Gemma 4 轻量版（3B，适合显存 3GB+ 设备）
ollama pull gemma4:3b

# 拉取 Gemma 4 标准版（9.6GB，适合显存 16GB+ 设备）
ollama pull gemma4:e4b

# 运行 Gemma 4 模型
ollama run gemma4:e4b
```

### 3.3 模型管理技巧

- 查看本地已安装模型：`ollama list`（或 `ollama ls`），会显示模型名称、版本和占用空间；

- 删除不需要的模型：`ollama rm 模型名称[:版本]`，例如 `ollama rm qwen2.5:7b`；

- 查看模型详细信息：`ollama show 模型名称[:版本]`，包括模型参数量、存储路径等；

- 模型存储路径：Windows 默认路径为 `C:\\Users\\你的用户名\\.ollama\\models`，可通过环境变量 `OLLAMA_MODELS` 修改。

## 四、运行 Claude Code、OpenClaw 等工具

Ollama 可与 Claude Code、OpenClaw 等 AI 工具串联使用，无需依赖在线 API 和 Token，全部在本地运行，不产生任何费用，适合开发者高效办公。以下是详细步骤（以 Windows 为例，macOS 操作逻辑一致）。

### 4.1 前置准备

- 确保 Ollama 已安装并启动服务；

- 安装 Node.js（强烈建议使用 v22 版本，v24 版本可能导致 OpenClaw 无法正常运行），下载地址：[https://nodejs.org/en/download/](https://nodejs.org/en/download/)；

- 安装合适的模型（推荐 Gemma 4 系列，性能更适配代码生成和工具调用）。

### 4.2 运行 Claude Code

Claude Code 是一款专注于代码生成、调试的工具，通过 Ollama 本地模型驱动，无需订阅付费方案：

1. 打开 Ollama 应用（Windows 系统托盘点击 Ollama 图标），左侧菜单选择「Launch」；

2. 在应用列表中找到「Claude Code」，复制其启动指令；

3. 以管理员身份打开 PowerShell（或终端），粘贴启动指令并执行；

4. 启动成功后，选择已安装的模型（如 Gemma 4:e4b），确认后即可进入 Claude Code 界面，开始代码生成、调试等操作。

### 4.3 运行 OpenClaw

OpenClaw 是一款多功能 AI 工具，支持对话、代码、文档生成等，与 Ollama 串联后可实现本地无 Token 运行：

1. 访问 OpenClaw 官方网站（[https://openclaw.ai/](https://openclaw.ai/)），复制对应系统的安装指令；

2. 以管理员身份打开 PowerShell（macOS 打开终端），粘贴安装指令并执行，按提示完成安装；

3. 打开 Ollama 应用，左侧「Launch」中找到「OpenClaw」，复制启动指令；

4. 在 PowerShell 中粘贴启动指令，选择已安装的模型（如 Gemma 4:26b），确认后复制生成的 URL；

5. 将 URL 粘贴到浏览器打开，即可使用 OpenClaw，界面会显示当前使用的模型，说明串联成功。

注：macOS 用户可直接通过终端执行 OpenClaw 安装指令，步骤与 Windows 一致，无需额外配置。

## 五、选择并使用 Ollama 自带 Cloud 模型

如果你的设备显存不足，无法运行 13B 及以上规模的模型，可使用 Ollama 自带的 Cloud 模型——无需本地硬件资源，通过云端算力运行超大参数量模型，使用方式与本地模型完全一致，且仅占用少量本地存储空间（几 KB）。

### 5.1 前置条件

需要在 Ollama 官方网站（[https://ollama.com/](https://ollama.com/)）注册一个账户，用于认证云端模型访问权限。

### 5.2 查找并运行 Cloud 模型

1. 打开终端（Windows PowerShell / macOS 终端），输入以下命令登录 Ollama 账户（按提示输入官网注册的邮箱和密码）：

```bash
ollama signin
```

1. 登录成功后，即可查找 Cloud 模型——所有带 `:cloud` 后缀的模型均为云端模型，例如：

- minimax-m2.7:cloud（轻量云端模型，适合快速对话）；

- DeepSeek-V3.1:cloud（超大参数量模型，适合复杂推理）；

- Qwen3-Coder:cloud（云端代码模型，适合专业编码）。

1. 直接运行 Cloud 模型，语法与本地模型一致：

```bash
# 运行 minimax-m2.7 云端模型
ollama run minimax-m2.7:cloud
```

运行后，模型会通过云端算力响应，无需本地显存支持，交互方式与本地模型完全相同，输入 `/exit` 即可退出。

### 5.3 Cloud 模型优势与注意事项

- 优势：无需本地硬件配置，可运行 671B 等超大参数量模型，响应速度快，不占用本地存储空间；

- 注意事项：需要联网使用，登录状态有效期有限，若提示未授权，重新执行 `ollama signin` 即可。

## 六、Ollama 常用命令与进阶使用方式

掌握 Ollama 常用命令，可大幅提升操作效率，以下分类整理核心命令，涵盖模型管理、服务控制、进阶配置等场景，新手可直接复制使用。

### 6.1 核心常用命令（必记）

|命令|功能说明|示例|
|---|---|---|
|ollama --version|查看 Ollama 版本|ollama --version|
|ollama serve|启动 Ollama 服务|ollama serve（后台运行：ollama serve &）|
|ollama pull 模型名|拉取（下载）模型|ollama pull qwen2.5:7b|
|ollama run 模型名|运行模型，进入交互模式|ollama run gemma4:e4b|
|ollama list|查看本地已安装模型|ollama list（或 ollama ls）|
|ollama rm 模型名|删除本地模型|ollama rm codellama:7b|
|ollama show 模型名|查看模型详细信息|ollama show qwen2.5:7b|
|ollama stop|停止当前运行的模型和服务|ollama stop|
|ollama help|查看所有命令帮助|ollama help（或 ollama --help）|
|ollama signin|登录 Ollama 账户（用于 Cloud 模型）|ollama signin|

### 6.2 进阶使用方式

#### 方式 1：通过 API 调用模型（开发者必备）

Ollama 自带 OpenAI 格式 API，可通过 HTTP 请求调用模型，适配各类开发项目，以 Python 为例：

```python
import requests

# API 调用地址（默认本地服务端口 11434）
url = "http://localhost:11434/api/generate"

# 请求参数
payload = {
    "model": "qwen2.5:7b",  # 模型名称
    "prompt": "用 Python 写一个简单的爬虫程序",  # 提问内容
    "stream": False  # 是否流式输出，False 表示一次性返回结果
}

# 发送请求并获取响应
response = requests.post(url, json=payload)
result = response.json()

# 打印模型回复
print(result["response"])
```

#### 方式 2：自定义模型（进阶需求）

可通过编写 Modelfile 配置文件，自定义模型参数（如量化配置、上下文长度），创建属于自己的模型：

1. 创建 Modelfile 文件，内容如下（以基于 Llama3 自定义为例）：

```bash
FROM llama3:7b  # 基础模型
# 自定义上下文长度（默认 4096）
PARAMETER context_length 8192
# 自定义模型描述
SYSTEM "我是一个专注于代码生成的AI助手，擅长多种编程语言。"
```

1. 执行以下命令，创建自定义模型（模型名自定义，如 my-code-model）：

```bash
ollama create my-code-model -f ./Modelfile
```

1. 运行自定义模型：

```bash
ollama run my-code-model
```

#### 方式 3：Docker 部署 Ollama（macOS / Linux 开发者）

若需隔离运行环境，可通过 Docker 部署 Ollama，以 macOS 为例：

```bash
# 1. 创建本地模型存储目录
mkdir -p ~/ollama/ollama-data

# 2. 启动 Ollama Docker 容器（后台运行，开机自启）
docker run -d \
 --name ollama \
 --platform linux/arm64 \
 --restart unless-stopped \
 -p 11434:11434 \
 -v ~/ollama/ollama-data:/root/.ollama \
 -e OLLAMA_HOST=0.0.0.0 \
 ollama/ollama:latest

# 3. 进入容器，拉取并运行模型
docker exec -it ollama bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
```

## 七、常见问题排查

新手使用 Ollama 时，可能会遇到服务启动失败、模型下载卡顿、无法运行等问题，以下是高频问题及解决方案：

- 问题 1：执行命令提示「ollama: command not found」？
  解决方案：Windows 安装时未勾选「Add to PATH」，重新安装并勾选该选项；macOS 可执行`source ~/.bashrc` 重新加载环境变量。

- 问题 2：启动服务提示「Error: ollama server not responding」？
  解决方案：确认已执行`ollama serve` 启动服务；检查端口 11434 是否被占用（Windows：`netstat -ano \| findstr :11434`；macOS：`lsof -i :11434`），关闭占用端口的程序后重新启动服务。

- 问题 3：模型下载速度慢、下载失败？
  解决方案：配置国内镜像加速（参考本文 2.3 节），更换网络或重新执行 `ollama pull` 命令。

- 问题 4：运行模型时提示显存不足？
  解决方案：更换更小规模的模型（如 3B、7B 版本），或使用 Ollama Cloud 模型（参考本文第五章）。

- 问题 5：OpenClaw 无法启动？
  解决方案：确认 Node.js 版本为 v22，卸载 v24 版本后重新安装；检查 Ollama 服务是否正常启动。

## 八、总结

Ollama 作为一款轻量高效的大模型运行工具，极大降低了本地部署大模型的门槛——无论是新手想要体验 AI 对话，还是开发者需要本地调试代码、对接项目，都能通过 Ollama 快速实现。本文涵盖了 Windows/macOS 安装、开源模型部署、Claude Code/OpenClaw 运行、Cloud 模型使用及常用命令，基本覆盖了绝大多数用户的核心需求。

后续可根据自身需求，探索自定义模型、API 对接等进阶功能，充分发挥 Ollama 的灵活性和高效性，让大模型真正服务于日常学习和工作。如果遇到其他问题，可通过 `ollama help` 查看命令帮助，或访问 Ollama 官方文档获取更多支持。
