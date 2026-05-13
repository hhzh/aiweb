---
title: Codex 高级配置教程
order: 2
---

# Codex 高级配置教程：全面解析与配置指南

当你的团队需要多环境切换、接入私有模型、管控企业安全、或部署全链路监控时，基础配置就不够用了。**高级配置**面向多环境切换、企业安全管控、私有化部署、多模型厂商接入、全链路可观测等复杂场景。本文系统讲解配置档案（Profiles）、自定义模型提供商、精细审批沙箱、OpenTelemetry 监控、TUI 优化等核心能力，提供可直接复制的配置模板，帮助开发者实现 Codex 的私有化与企业级落地。

---

## 一、配置体系进阶：优先级、临时覆盖与配置档案

Codex 采用**多层级覆盖**的配置体系，高级用法可实现单任务临时覆盖、多环境快速切换、全局 / 项目 / 命令行三级管控。

### 1. 完整配置优先级（从高到低）

高优先级配置会覆盖低优先级，明确规则可避免冲突：

1. CLI 标志 / `--config` 单次覆盖

2. Profile 配置（`--profile <name>`）

3. 项目配置（`.codex/config.toml`，仅信任项目，就近目录优先）

4. 用户全局配置（`~/.codex/config.toml`）

5. 系统配置（Unix：`/etc/codex/config.toml`）

6. 内置默认值

### 2. CLI 单次临时覆盖（`-c/--config`）

无需修改配置文件，单次运行指定参数，支持**点表示法**嵌套赋值：

```bash
# 专用参数
codex --model gpt-5.4
# 通用覆盖（值为 TOML 格式）
codex --config model='"gpt-5.4"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

### 3. 配置档案 Profiles（实验特性）

Profiles 用于保存多套命名配置，一键切换环境，**暂不支持 IDE 扩展**。

- 定义：在 `config.toml` 中添加 `[profiles.<name>]`

- 切换：`codex --profile <name>`

- 设为默认：顶层添加 `profile = "deep-review"`

示例：

```toml
# 全局默认
model = "gpt-5.4"
approval_policy = "on-request"

# 深度评审 profile
[profiles.deep-review]
model = "gpt-5-pro"
model_reasoning_effort = "high"
approval_policy = "never"

# 轻量任务 profile
[profiles.lightweight]
model = "gpt-4.1"
approval_policy = "untrusted"
```

---

## 二、项目级高级配置：根目录、项目配置与 Hooks

### 1. 自定义项目根目录识别

Codex 默认以含 `.git` 的目录为项目根，可自定义标记：

```toml
# 包含任一标记即视为根目录
project_root_markers = [".git", ".hg", ".sl"]
# 禁用向上查找，当前目录为根
project_root_markers = []
```

### 2. 项目级配置（`.codex/config.toml`）

- 从项目根到当前目录，**就近目录配置优先**

- 仅**信任项目**加载，未信任项目跳过，保障安全

- 项目内相对路径以 `.codex/` 为基准解析

### 3. 生命周期 Hooks（实验特性）

Hooks 可绑定任务生命周期事件，实现前置 / 后置处理：

- 存放位置：`~/.codex/hooks.json` 或 `<repo>/.codex/hooks.json`

- 启用：

```toml
[features]
codex_hooks = true
```

---

## 三、自定义模型提供商：多厂商、代理、Azure 与私有化

Codex 支持接入 OpenAI 官方、Azure、Ollama、Mistral 等任意兼容 OpenAI 协议的模型服务，实现多模型调度与私有化部署。

### 1. 核心规则

- 不可覆盖内置 ID：`openai`/`ollama`/`lmstudio`

- 快速代理官方服务：直接配置 `openai_base_url`

```toml
openai_base_url = "https://us.api.openai.com/v1"
```

### 2. 自定义提供商示例

```toml
model = "gpt-5.4"
model_provider = "proxy"

# LLM 代理
[model_providers.proxy]
name = "OpenAI Proxy"
base_url = "http://proxy.example.com/v1"
env_key = "OPENAI_API_KEY"

# 本地 Ollama
[model_providers.local_ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"

# Mistral
[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"
```

### 3. 自定义请求头与命令认证

```toml
# 自定义请求头
[model_providers.example]
http_headers = { "X-Example" = "value" }
env_http_headers = { "X-Feature" = "FEATURE_FLAG" }

# 外部命令获取 Token（无 stdin，输出 token）
[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

### 4. Azure 与数据驻留配置

```toml
# Azure OpenAI
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"

# 数据驻留（Data Residency）
[model_providers.openaidr]
name = "OpenAI DR"
base_url = "https://us.api.openai.com/v1"
```

### 5. OSS 开源模型模式

对接本地开源模型（Ollama/LM Studio）：

```toml
# --oss 默认使用的提供商
oss_provider = "ollama"
# 运行：codex --oss
```

---

## 四、安全与权限：精细审批、沙箱与环境变量管控

### 1. 精细审批策略

支持**粒度控制**与**自动审核**，满足企业合规：

```toml
# 基础策略：untrusted/on-request/never/granular
approval_policy = "on-request"
# 自动审核
approvals_reviewer = "auto_review"

# 精细审批示例
approval_policy = { granular = {
  sandbox_approval = true,
  rules = true,
  mcp_elicitations = true,
  request_permissions = false,
  skill_approval = false
} }

[sandbox_workspace_write]
writable_roots = ["/Users/you/.pyenv/shims"]
network_access = false  # 禁用网络
```

### 2. 沙箱模式

- `workspace-write`：仅工作区可写，`.git/.codex` 只读（推荐）

- `danger-full-access`：完全访问（仅隔离环境使用）

```toml
sandbox_mode = "workspace-write"
# Windows 沙箱权限
[windows]
sandbox = "elevated"  # 管理员权限（推荐）
```

### 3. Shell 环境变量策略

严控环境变量转发，防止密钥泄露：

```toml
[shell_environment_policy]
inherit = "none"  # 清空继承
include_only = ["PATH", "HOME"]
exclude = ["AWS_*", "AZURE_*"]  # 通配符屏蔽敏感变量
set = { MY_FLAG = "1" }
```

---

## 五、模型推理高级调优

```toml
# 推理力度：high/medium/low
model_reasoning_effort = "high"
# 推理摘要：none/simple/full
model_reasoning_summary = "none"
# 响应简洁度：low/medium/high（仅 Responses API）
model_verbosity = "low"
# 上下文窗口
model_context_window = 128000
# 隐藏/显示原始推理
hide_agent_reasoning = true
show_raw_agent_reasoning = false
```

---

## 六、可观测性：监控、日志、通知与历史

### 1. OpenTelemetry（OTel）链路追踪

```toml
[otel]
environment = "prod"
exporter = { otlp-http = {
  endpoint = "https://otel.example.com/v1/logs",
  headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }
}}
log_user_prompt = false  # 脱敏用户提示
```

### 2. 关闭匿名指标采集

```toml
[analytics]
enabled = false
```

### 3. 外部通知（任务完成触发）

```toml
# 执行外部脚本
notify = ["python3", "/path/to/notify.py"]
```

### 4. 历史记录与文件打开器

```toml
# 历史持久化：none/jsonl
[history]
persistence = "jsonl"
max_bytes = 104857600  # 100MB 上限

# 可点击文件链接：vscode/cursor/windsurf/none
file_opener = "vscode"
```

---

## 七、TUI 终端界面高级配置

```toml
[tui]
notifications = ["agent-turn-complete", "approval-requested"]
notification_method = "auto"  # auto/osc9/bel
notification_condition = "unfocused"  # unfocused/always
animations = false
alternate_screen = "never"  # 保留终端回滚
show_tooltips = false
```

---

## 八、企业级完整高级配置模板

```toml
# 全局基础
model = "gpt-5.4"
openai_base_url = "https://us.api.openai.com/v1"
profile = "default"

# 项目根
project_root_markers = [".git"]

# 安全基线
approval_policy = "on-request"
sandbox_mode = "workspace-write"
allow_login_shell = false

# 环境变量管控
[shell_environment_policy]
include_only = ["PATH", "HOME"]
exclude = ["AWS_*", "AZURE_*", "GITHUB_TOKEN"]

# 模型调优
model_reasoning_effort = "high"
model_verbosity = "low"

# 自定义提供商
[model_providers.local_ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"
oss_provider = "ollama"

# 可观测性
[otel]
environment = "prod"
exporter = "none"
[analytics]
enabled = false

# TUI
[tui]
animations = false
notification_condition = "unfocused"

# 功能开关
[features]
codex_hooks = true
multi_agent = true
undo = true
```

---

## 九、高级配置最佳实践

1. **多环境隔离**：用 Profiles 区分开发 / 评审 / 生产环境，避免手动改配置

2. **安全底线**：生产环境禁用 `danger-full-access`，启用 `approval_policy=on-request`

3. **密钥防护**：用 `shell_environment_policy` 屏蔽敏感环境变量，禁止转发密钥

4. **可观测必开**：企业部署启用 OTel，监控 API 调用、工具执行、审批记录

5. **项目信任**：敏感仓库不标记信任，禁用项目级配置，防止恶意配置篡改

6. **临时覆盖优先**：单任务调试用 `--config`，不污染全局配置

---

## 十、总结

Codex 高级配置构建了**多模型接入、全维度安全、可观测监控、灵活环境切换**的企业级能力。通过配置分层、自定义提供商、精细沙箱审批、OTel 监控，可实现从个人开发到团队协作、从公有云到私有化部署的全场景适配。

**下一步**：建议结合 [Codex 示例配置教程](./14-codex-example-configurations.md) 直接复制企业级完整配置模板，或阅读 [Codex 项目定制化教程](./13-codex-project-customization.md) 了解 AGENTS.md、Skills、MCP、Subagents 五层定制体系。

