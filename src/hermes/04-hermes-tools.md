---
title: Hermes Agent 工具使用教程
order: 4
---

# Hermes Agent 工具使用教程


Hermes Agent 内置强大工具系统，将网络搜索、终端执行、浏览器自动化、媒体生成等能力封装为可调用工具与工具集。本文从工具概览、启用方式、核心工具实操、终端后端配置、工具网关集成及安全管理六方面，带你全面掌握工具使用，释放智能体全能力。

## 一、工具与工具集概览

Hermes 工具按功能划分为 **8 大核心类别、47 个独立工具**，并聚合为可一键启用的 **工具集（Toolsets）**，兼顾灵活性与易用性。

### 1.1 核心工具类别

|类别|核心工具|功能说明|
|---|---|---|
|🌐 网络工具|`web_search`、`web_extract`|全网搜索、网页正文提取（支持 Markdown 输出）|
|💻 终端与文件|`terminal`、`read_file`、`patch`|命令执行、文件读写、代码补丁编辑|
|🧭 浏览器|`browser_navigate`、`browser_vision`|无头浏览器控制、页面视觉分析|
|🎨 媒体工具|`image_generate`、`text_to_speech`|AI 绘图、文本转语音（支持多模型）|
|🧠 智能体编排|`todo`、`delegate_task`|任务管理、子任务并行委托|
|📜 记忆工具|`memory`、`session_search`|持久记忆读写、历史会话全文检索|
|⏰ 自动化|`cronjob`、`send_message`|定时任务、跨平台消息推送|
|🔗 集成工具|`mcp_*`、`ha_*`|MCP 外部工具、Home Assistant 智能家居控制|

### 1.2 工具集（一键启用）

工具集是功能聚合包，无需逐个启用，常用预设：

- `web`：网络搜索 + 网页提取

- `terminal`：终端命令执行

- `file`：文件读写与编辑

- `browser`：浏览器自动化全套

- `memory`：持久记忆与会话搜索

## 二、工具启用与管理

### 2.1 命令行临时启用

启动对话时通过 `--toolsets` 指定工具集，临时生效：

```bash
hermes chat --toolsets "web,terminal"

hermes chat --toolsets "web,terminal,file,browser,memory"

hermes chat --toolsets ""
```

### 2.2 交互式配置（永久生效）

通过 `hermes tools` 进入交互式面板，按需启用 / 禁用：

```bash
hermes tools
```

### 2.3 配置文件设置

编辑 `~/.hermes/config.yaml`，默认工具集：

```yaml
toolsets:
  - web
  - terminal
  - file
  - memory
```

## 三、核心工具实操指南

### 3.1 网络工具（web_search/web_extract）

**场景**：查资料、爬取文档、实时信息获取

```Plain Text
帮我搜索2026年大模型发展趋势，总结3个核心方向

提取https://example.com/ai-report的正文，输出Markdown格式
```

### 3.2 终端工具（terminal）

**场景**：系统操作、代码编译、命令行任务

```Plain Text
帮我查看当前磁盘占用，列出最大5个目录

在桌面创建test目录，生成5个Markdown笔记文件

编译当前目录下的Go项目，输出编译日志
```

### 3.3 文件工具（read_file/patch）

**场景**：代码编辑、文档修改、配置更新

```Plain Text
读取~/projects/config.yaml，高亮关键配置

给main.py添加日志模块，保留原有逻辑
```

### 3.4 媒体工具（image_generate/tts）

**场景**：AI 绘图、语音合成

```Plain Text
生成一张科技风AI助手海报，蓝色主调，高清

把“Hermes工具使用教程”转为中文女声语音
```

### 3.5 记忆工具（memory/session_search）

**场景**：跨会话记忆、历史内容检索

```Plain Text
记住：Hermes支持200+模型，可一键切换国产/海外模型

搜索之前讨论的“大模型部署方案”相关内容
```

## 四、终端后端配置（执行环境）

终端工具支持 **7 种执行后端**，决定命令运行位置，兼顾安全与灵活性。

### 4.1 后端类型与适用场景

|后端|说明|适用场景|
|---|---|---|
|`local`（默认）|本机直接执行|开发、可信任务|
|`docker`|隔离容器执行|安全沙箱、环境隔离|
|`ssh`|远程服务器执行|远程运维、高性能计算|
|`modal`|无服务器云|弹性扩展、临时任务|

### 4.2 配置方式

#### （1）命令行设置

```bash
hermes config set terminal.backend docker
```

#### （2）配置文件（config.yaml）

```yaml
terminal:
  backend: docker  # 或 local/ssh/modal
  timeout: 300     # 命令超时（秒）
  docker_image: python:3.11-slim
  docker_volumes:  # 挂载本地目录
    - "~/projects:/workspace"
```

### 4.3 Docker 后端（安全推荐）

容器运行在 **安全强化模式**：

- 只读根文件系统、无权限提升

- PID 限制（最多 256 进程）

- 完全命名空间隔离，避免宿主机污染

## 五、Nous 工具网关（订阅集成）

**Nous 工具网关**是付费订阅专属能力，**无需单独注册 API 密钥**，一键启用网络搜索、图像生成、TTS、浏览器自动化。

### 5.1 网关包含能力

|工具|替代独立密钥|
|---|---|
|网络搜索 / 提取|`FIRECRAWL_API_KEY`|
|图像生成|`FAL_KEY`|
|文本转语音|`OPENAI_TTS_KEY`|
|浏览器自动化|`BROWSER_USE_API_KEY`|

### 5.2 启用方式

#### （1）模型配置时启用

运行 `hermes model` 选择 Nous Portal，自动提示启用网关：

```Plain Text
选择启用Nous Tool Gateway → 勾选工具 → 完成配置
```

#### （2）手动配置

编辑 `config.yaml`，启用网关：

```yaml
web:
  use_gateway: true  # 网络工具走网关
image_gen:
  use_gateway: true  # 图像生成走网关
```

### 5.3 网关优先级

- `use_gateway: true`：强制走网关，忽略本地密钥

- `use_gateway: false`：优先本地密钥，无密钥时回退网关

## 六、工具安全与权限管理

### 6.1 风险操作确认

高风险操作（删除文件、系统修改、网络请求）**自动触发确认**：

```Plain Text
帮我删除~/temp目录
→ 系统提示：确认删除？（输入y确认）
```

### 6.2 安全配置（config.yaml）

```yaml
security:
  credential_redaction: true
  website_blocklist:
    enabled: true
    domains: ["*.torrent", "192.168.0.0/16"]
```

### 6.3 容器安全（Docker 后端）

- 只读根文件系统、禁用权限提升

- 进程数量限制、资源隔离

## 七、常见问题排查

1. **工具调用失败（无权限）**

    - 本地执行：确认文件 / 命令权限

    - Docker 后端：检查容器挂载目录权限

2. **网关工具不可用**

    - 确认 Nous 订阅有效：`hermes status`

    - 重新启用网关：`hermes tools` → 勾选网关工具

3. **终端命令超时**

    - 延长超时时间：`hermes config set terminal.timeout 600`

4. **浏览器工具打不开页面**

    - 检查网络代理：关闭代理 / VPN

    - 确认浏览器镜像正常：`docker images | grep browser`

## 八、总结

Hermes 工具系统以 **分类清晰、灵活可控、安全隔离** 为核心，覆盖从日常操作到复杂自动化的全场景需求。新手可通过 `--toolsets` 快速启用常用组合，进阶用户可配置 Docker 沙箱、集成 Nous 网关或自定义 MCP 工具。掌握工具使用，才能充分释放 Hermes 自进化能力，打造全能 AI 助手。

