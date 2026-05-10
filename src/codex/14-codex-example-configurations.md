---
title: Codex 示例配置教程
order: 14
---

# Codex 示例配置教程｜从基础到进阶，可直接复制套用

Codex 的配置核心是 `config.toml` 文件，支持用户级、项目级两层配置，覆盖从个人开发到企业部署的全场景需求。本文基于 OpenAI 官方 `config-reference` 和 `config-sample` 文档，整理了最实用的示例配置，按「基础入门→进阶优化→专项场景→完整模板」分类，所有示例均可直接复制到本地使用，同时详解每一项配置的作用、取值范围和适用场景，帮助开发者快速上手，避免踩坑。
本文所有示例均遵循 Codex 最新配置规范，兼容 CLI、IDE 扩展、桌面端等所有使用形态，配置修改后重启 Codex 即可生效。新手建议从基础示例开始，逐步添加进阶配置；资深开发者可直接定位到对应专项场景，复制示例快速适配需求。

## 一、基础入门示例（新手必用，直接复制）

基础示例覆盖 Codex 核心功能，满足日常开发的基本需求，配置简洁、安全、易维护，适合刚接触 Codex 的新手。将以下内容复制到 `~/.codex/config.toml`（全局配置），即可快速启用 Codex 基础功能。

```toml
# 基础入门示例：新手友好，安全高效
# 1. 全局默认模型（推荐 gpt-5.4，兼顾性能与效果）
model = "gpt-5.4"
# 模型提供商（默认 openai，无需修改）
model_provider = "openai"

# 2. 安全基线配置（核心必配，避免误操作）
# 审批策略：请求时弹窗确认（平衡安全与效率）
approval_policy = "on-request"
# 沙箱模式：仅工作区可写（推荐，防止篡改系统文件）
sandbox_mode = "workspace-write"
# 禁止登录shell（降低安全风险）
allow_login_shell = false

# 3. 环境变量管控（防止密钥泄露）
[shell_environment_policy]
# 仅继承 PATH、HOME 两个基础环境变量
inherit = "core"
include_only = ["PATH", "HOME"]
# 屏蔽所有含 KEY/SECRET/TOKEN 的敏感变量
exclude = ["*KEY*", "*SECRET*", "*TOKEN*"]

# 4. 基础功能开关（启用稳定功能）
[features]
shell_snapshot = true  # 加速重复命令执行
multi_agent = true     # 启用多助手协作
fast_mode = true       # 启用快速模式
undo = true            # 启用 Git 快照撤销功能

# 5. 历史记录与文件打开器
[history]
persistence = "save-all"  # 保存所有会话历史
max_bytes = 104857600     # 历史文件上限 100MB
# 点击日志中的文件链接，用 VS Code 打开（可替换为 cursor/windsurf）
file_opener = "vscode"

# 6. 网页搜索配置（安全缓存模式）
web_search = "cached"  # 优先读取缓存，更安全、更快

```

【使用说明】：此示例无需修改，复制后重启 Codex 即可生效。核心作用是保障基础安全，启用常用功能，适合日常编码、简单脚本开发等场景。

## 二、进阶示例配置（高频场景，按需添加）

进阶示例针对开发中高频场景设计，可在基础示例的基础上，按需复制对应模块添加到 `config.toml` 中，实现个性化优化。每个模块独立存在，互不影响。

### 2.1 多模型提供商配置（多厂商切换、私有化部署）

支持接入 OpenAI、Azure、Ollama、Mistral 等多种模型提供商，可快速切换模型来源，适配私有化部署需求。

```toml
# 多模型提供商示例（可按需启用）
# 默认使用自定义代理提供商
model_provider = "proxy"

# 1. 自定义 OpenAI 代理（解决国内无法直连问题）
[model_providers.proxy]
name = "OpenAI Proxy"       # 提供商显示名称
base_url = "http://proxy.example.com/v1"  # 代理地址
env_key = "OPENAI_API_KEY"  # 从环境变量读取 API Key

# 2. 本地 Ollama 模型（私有化部署，无需联网）
[model_providers.local_ollama]
name = "Local Ollama"
base_url = "http://localhost:11434/v1"  # Ollama 本地地址
# 无需 API Key，本地模型直接调用

# 3. Azure OpenAI 配置（企业级场景）
[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }  # Azure 版本参数

# 4. 本地开源模型默认配置（运行 codex --oss 时生效）
oss_provider = "ollama"

```

### 2.2 精细安全管控配置（企业级安全需求）

针对企业场景，实现更精细的审批策略、沙箱管控和权限限制，保障代码和系统安全。

```toml
# 精细安全管控示例
# 1.  granular 审批策略（精准控制不同类型的审批）
approval_policy = { granular = {
  sandbox_approval = true,    # 沙箱升级需要审批
  rules = true,               # 执行策略规则需要审批
  mcp_elicitations = false,   # 自动拒绝 MCP 诱导提示
  request_permissions = false,# 自动拒绝权限请求提示
  skill_approval = false      # 自动拒绝技能脚本审批
} }
# 审批者：使用自动审核子代理（可改为 user 手动审核）
approvals_reviewer = "auto_review"

# 2. 沙箱精细配置（workspace-write 模式增强）
[sandbox_workspace_write]
writable_roots = ["/Users/you/.pyenv/shims"]  # 额外可写目录
network_access = false  # 禁用沙箱内网络访问（高安全需求）
exclude_slash_tmp = true  # 禁止写入 /tmp 目录

# 3. 自定义权限配置（精细化控制文件和网络访问）
[permissions.dev]
# 文件系统权限：仅允许读写项目根目录和特定路径
[permissions.dev.filesystem]
":project_roots" = { "." = "write", "**/*.env" = "none" }  # 项目根可写，.env 文件禁止访问
"/Users/you/Documents/code" = "read"  # 仅允许读取该目录

# 网络权限：仅允许访问特定域名
[permissions.dev.network]
enabled = true
mode = "limited"
domains = { "github.com" = "allow", "npmjs.com" = "allow", "*" = "deny" }

```

### 2.3 可观测性配置（监控与日志）

启用 OpenTelemetry（OTel）链路追踪、日志自定义，方便企业级部署后的监控和问题排查。

```toml
# 可观测性示例
# 1. OpenTelemetry 链路追踪（企业级监控）
[otel]
environment = "prod"  # 环境标记（prod/dev/test）
# OTLP HTTP 导出器（对接企业监控系统）
[otel.exporter.otlp-http]
endpoint = "https://otel.example.com/v1/logs"
headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }  # 从环境变量读取 Token
log_user_prompt = false  # 不导出原始用户提示（脱敏）

# 2. 日志配置（自定义日志目录）
log_dir = "/absolute/path/to/codex-logs"  # 日志存储路径
# 关闭匿名指标采集（企业数据安全需求）
[analytics]
enabled = false

# 3. 任务完成通知（执行完任务触发脚本通知）
notify = ["python3", "/path/to/notify.py"]  # 通知脚本路径

```

### 2.4 TUI 终端界面优化（提升命令行使用体验）

针对 CLI 使用者，优化终端界面（TUI）的显示、通知和交互体验。

```toml
# TUI 界面优化示例
[tui]
animations = false  # 关闭终端动画（提升流畅度）
alternate_screen = "never"  # 保留终端回滚历史
show_tooltips = false  # 关闭新手提示
# 通知配置：仅当终端未聚焦时提示
notification_condition = "unfocused"
notification_method = "auto"  # 自动选择通知方式
# 启用特定类型的通知
notifications = ["agent-turn-complete", "approval-requested"]
# 自定义终端标题（显示项目名称和任务状态）
terminal_title = ["project", "spinner"]

```

### 2.5 多环境切换配置（Profiles 特性）

通过 Profiles 定义多套配置，一键切换开发、评审、生产等不同环境，无需手动修改配置文件。

```toml
# 多环境切换示例（Profiles）
# 全局默认配置
model = "gpt-5.4"
approval_policy = "on-request"

# 1. 深度评审环境（用于代码评审，推理力度高）
[profiles.deep-review]
model = "gpt-5-pro"
model_reasoning_effort = "high"  # 高推理力度
approval_policy = "never"  # 评审时无需重复审批

# 2. 轻量开发环境（用于快速迭代，性能优先）
[profiles.lightweight]
model = "gpt-4.1"
model_reasoning_effort = "low"  # 低推理力度
web_search = "cached"  # 缓存模式，加快速度

# 3. 生产环境（高安全，严格管控）
[profiles.prod]
sandbox_mode = "workspace-write"
network_access = false
approval_policy = { granular = { sandbox_approval = true, rules = true } }

# 设置默认环境（启动时自动加载）
profile = "lightweight"

```

【使用方法】：通过 CLI 命令切换环境，例如 `codex --profile deep-review`，即可加载对应环境的配置。

## 三、专项场景示例（针对性适配）

针对不同使用场景，整理专属示例配置，直接复制套用，无需额外修改。

### 3.1 本地私有化部署示例（无网络依赖）

```toml
# 本地私有化部署示例（依赖 Ollama 本地模型）
model = "llama3:70b"  # 本地 Ollama 模型
model_provider = "local_ollama"
oss_provider = "ollama"

# 禁用网络相关功能，完全离线运行
web_search = "disabled"
[sandbox_workspace_write]
network_access = false

# 关闭所有云端相关功能
[analytics]
enabled = false
[otel]
exporter = "none"

# 本地日志与历史配置
log_dir = "./.codex/logs"
[history]
persistence = "save-all"
max_bytes = 52428800  # 50MB 历史上限

```

### 3.2 企业团队协作示例（统一配置，安全可控）

```toml
# 企业团队协作示例
# 全局统一模型与提供商
model = "gpt-5.4"
model_provider = "azure"
[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://team-azure-openai.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }

# 团队统一安全策略
approval_policy = "on-request"
approvals_reviewer = "auto_review"
sandbox_mode = "workspace-write"

# 环境变量统一管控
[shell_environment_policy]
inherit = "none"
include_only = ["PATH", "HOME", "TEAM_ENV"]
set = { TEAM_PROJECT = "codex-team" }  # 统一设置团队环境变量

# 团队共享功能开关
[features]
codex_hooks = true  # 启用生命周期钩子，统一团队工作流
multi_agent = true
undo = true
shell_snapshot = true

# 可观测性（对接团队监控）
[otel]
environment = "team-prod"
[otel.exporter.otlp-http]
endpoint = "https://team-otel.example.com/v1/logs"
headers = { "x-otlp-api-key" = "${TEAM_OTLP_TOKEN}" }

```

### 3.3 新手调试示例（友好提示，便于排查）

```toml
# 新手调试示例（开启详细提示，便于排查问题）
model = "gpt-4.1"  # 新手推荐使用更稳定的模型
model_reasoning_effort = "medium"
# 显示原始推理过程，便于理解 Codex 操作逻辑
show_raw_agent_reasoning = true
hide_agent_reasoning = false

# 审批策略：每次请求都提示，避免误操作
approval_policy = "on-request"
approvals_reviewer = "user"  # 手动审批，加深理解

# 开启详细日志
log_dir = "./.codex/debug-logs"
# 保留所有历史，便于回溯操作
[history]
persistence = "save-all"

# 启用新手友好功能
[features]
show_tooltips = true  # 显示 TUI 新手提示
undo = true  # 可撤销操作，降低试错成本
```

## 四、完整可复制配置模板（新手/企业版）

整理两套完整模板，直接复制到 `~/.codex/config.toml` 即可使用，无需额外修改，按需选择对应版本。

### 4.1 新手完整版模板

```toml
# Codex 新手完整版配置模板（直接复制使用）
# 基础模型配置
model = "gpt-5.4"
model_provider = "openai"
openai_base_url = "https://us.api.openai.com/v1"

# 安全配置
approval_policy = "on-request"
approvals_reviewer = "user"
sandbox_mode = "workspace-write"
allow_login_shell = false

# 环境变量管控
[shell_environment_policy]
inherit = "core"
include_only = ["PATH", "HOME"]
exclude = ["*KEY*", "*SECRET*", "*TOKEN*"]

# 功能开关
[features]
shell_snapshot = true
multi_agent = true
fast_mode = true
undo = true
show_tooltips = true

# 历史与文件配置
[history]
persistence = "save-all"
max_bytes = 104857600
file_opener = "vscode"

# 网页搜索与 TUI
web_search = "cached"
[tui]
animations = true
notification_condition = "unfocused"
notifications = ["agent-turn-complete"]

# 日志配置
log_dir = "~/.codex/logs"

```

### 4.2 企业完整版模板

```toml
# Codex 企业完整版配置模板（直接复制使用）
# 基础配置
model = "gpt-5.4"
model_provider = "azure"
profile = "prod"

# 多环境配置（Profiles）
[profiles.dev]
model = "gpt-5.4"
web_search = "live"
approval_policy = "on-request"

[profiles.prod]
model = "gpt-5.4"
web_search = "cached"
approval_policy = { granular = { sandbox_approval = true, rules = true } }
sandbox_mode = "workspace-write"

[profiles.review]
model = "gpt-5-pro"
model_reasoning_effort = "high"
approval_policy = "never"

# 模型提供商（Azure）
[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }

# 安全管控
[sandbox_workspace_write]
writable_roots = ["/opt/team/code"]
network_access = false
exclude_slash_tmp = true

[permissions.team]
[permissions.team.filesystem]
":project_roots" = { "." = "write", "**/*.env" = "none" }
[permissions.team.network]
enabled = true
domains = { "github.com" = "allow", "npmjs.com" = "allow", "*" = "deny" }

# 环境变量管控
[shell_environment_policy]
inherit = "none"
include_only = ["PATH", "HOME", "TEAM_ENV"]
set = { TEAM_PROJECT = "enterprise-codex" }

# 可观测性
[otel]
environment = "prod"
[otel.exporter.otlp-http]
endpoint = "https://otel.example.com/v1/logs"
headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }
log_user_prompt = false

[analytics]
enabled = false

# 功能开关
[features]
codex_hooks = true
multi_agent = true
undo = true
shell_snapshot = true

# 日志与通知
log_dir = "/var/log/codex"
notify = ["python3", "/opt/team/notify/codex-notify.py"]

# TUI 配置
[tui]
animations = false
alternate_screen = "never"
notifications = ["agent-turn-complete", "approval-requested"]

```

## 五、示例配置使用说明

### 5.1 配置文件路径

- 全局配置：`~/.codex/config.toml`（所有项目共用，优先级低于项目配置）

- 项目配置：`项目根目录/.codex/config.toml`（仅当前项目生效，需标记项目为信任）

### 5.2 配置生效方法

修改配置后，重启 Codex 客户端（CLI/IDE/桌面端）即可生效；CLI 临时覆盖配置可使用 `--config` 参数，例如 `codex --config model='"gpt-5-pro"'`。

### 5.3 注意事项

- 项目级配置仅在项目被标记为「信任」时加载，未信任项目会跳过项目级配置，保障安全。

- 所有示例中的路径、API Key、代理地址等，需替换为自身实际信息后再使用。

- 避免使用`sandbox_mode = "danger-full-access"`（完全访问模式），仅在隔离测试环境使用。

- 配置中的环境变量（如 `OPENAI_API_KEY`），需提前在系统环境变量中配置，避免直接写入配置文件。

## 六、常见问题排查（配置相关）

- 配置不生效：检查配置文件路径是否正确，是否重启 Codex；项目级配置需确认项目已信任。

- 模型调用失败：检查 `model_provider` 和 `base_url` 是否正确，API Key 是否有效。

- 沙箱报错：检查 `sandbox_mode`配置，确认是否有足够的读写权限，是否禁用了必要的网络访问。

- Profiles 切换失败：检查 Profiles 定义是否正确，CLI 命令是否正确（`--profile <名称>`）。

## 七、总结

本文所有示例均基于 OpenAI 官方配置规范，覆盖从新手入门到企业部署的全场景，所有代码均可直接复制使用，无需复杂修改。开发者可根据自身需求，选择基础模板快速启用，或添加进阶模块实现个性化优化。

核心原则：配置以「安全优先、简洁实用」为前提，优先使用官方推荐的默认值，按需添加个性化配置。如需更复杂的配置，可参考 OpenAI 官方 `config-reference` 文档，结合本文示例进行扩展。

