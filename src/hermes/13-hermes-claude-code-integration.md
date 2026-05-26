---
title: Hermes Agent 接入 Claude Code 教程
order: 13
---

# Hermes Agent 接入 Claude Code 教程

Claude Code 是 Anthropic 推出的自主编码 CLI 代理，可完成代码编写、重构、审查、测试等全流程开发任务。Hermes Agent 内置 `autonomous-ai-agents-claude-code` 技能，支持无缝接入 Claude Code，将编码任务委托给 Claude Code 独立执行，无需手动操作。本文从环境准备、两种交互模式、核心命令、实战示例到最佳实践，带你全面掌握 Hermes 接入 Claude Code 的方法。

## 一、前提条件

接入前需完成 Claude Code 安装与认证，确保 Hermes 可正常调用：

### 1. 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 2. 账号认证

- **浏览器 OAuth（推荐）**：终端输入 `claude`，按提示完成浏览器登录（Pro/Max 用户）。

- **API 密钥认证**：设置环境变量 `ANTHROPIC_API_KEY=your-key`，执行 `claude auth login --console`。

- **企业 SSO 认证**：`claude auth login --sso`。

### 3. 环境校验

```bash
# 查看认证状态
claude auth status
# 健康检查
claude doctor
# 版本要求（v2.x+）
claude --version
```

### 4. Hermes 技能启用

Claude Code 为 Hermes 内置技能，默认随框架安装，无需额外配置。

## 二、两种交互模式

Hermes 支持**打印模式（非交互式）与tmux 交互式**两种接入模式，适配不同编码场景。

### 模式一：打印模式（-p，推荐）

一次性非交互式执行，任务完成后自动退出，无交互式弹窗，适合自动化、脚本化、简单编码任务。

#### 核心用法

```bash
# 基础任务：为所有 API 调用添加错误处理
hermes chat --execute 'terminal(command="claude -p "给 src/ 下所有 API 调用添加错误处理" --allowedTools Read,Edit", workdir="/path/to/project")'

# 限制执行轮次，避免无限循环
hermes chat --execute 'terminal(command="claude -p "重构数据库层" --max-turns 10", workdir="/path/to/project")'
```

#### 适用场景

- 一次性编码任务（修复 bug、简单重构、代码审查）。

- CI/CD 自动化、脚本集成。

- 无需多轮交互的独立任务。

### 模式二：tmux 交互式

完整对话式 REPL，支持多轮迭代、后续指令、斜杠命令，适合复杂多步编码任务。

#### 核心流程

1. 创建 tmux 会话

2. 启动 Claude Code

3. 发送编码任务

4. 实时监控进度

5. 发送后续指令

6. 任务完成退出

#### 示例命令

```bash
# 1. 创建后台 tmux 会话
hermes chat --execute 'terminal(command="tmux new-session -d -s claude-dev")'

# 2. 启动 Claude Code（跳过权限确认）
hermes chat --execute 'terminal(command="tmux send-keys -t claude-dev "cd /path/to/project && claude --dangerously-skip-permissions" Enter")'

# 3. 发送编码任务：重构认证模块为 JWT
hermes chat --execute 'terminal(command="sleep 5 && tmux send-keys -t claude-dev "重构 auth 模块，替换为 JWT 认证" Enter")'

# 4. 查看执行进度
hermes chat --execute 'terminal(command="sleep 15 && tmux capture-pane -t claude-dev -p -S -50")'

# 5. 后续指令：添加单元测试
hermes chat --execute 'terminal(command="tmux send-keys -t claude-dev "为 JWT 认证添加单元测试" Enter")'

# 6. 退出会话
hermes chat --execute 'terminal(command="tmux send-keys -t claude-dev "/exit" Enter")'
```

#### 对话框处理

交互式模式需手动处理两类确认弹窗：

1. **工作区信任弹窗**：默认选择「Yes」，直接发送 `Enter`。

2. **权限确认弹窗**：需按「下箭头 + 回车」选择「Yes, I accept」。

```bash
# 自动处理权限弹窗
hermes chat --execute 'terminal(command="sleep 3 && tmux send-keys -t claude-dev Down && sleep 0.3 && tmux send-keys -t claude-dev Enter")'
```

## 三、核心 CLI 命令

### 3.1 基础命令

```bash
# 启动交互式会话
claude
# 打印模式执行任务
claude -p "任务描述"
# 恢复最近会话
claude -c
# 按 ID 恢复会话
claude -r "session-id"
```

### 3.2 常用参数

|参数|作用|
|---|---|
|`--allowedTools`|允许的工具（Read/Edit/Bash）|
|`--max-turns`|最大执行轮次（防止无限循环）|
|`--output-format json`|结构化 JSON 输出|
|`--fallback-model`|模型过载时回退（如 haiku）|
|`--dangerously-skip-permissions`|跳过权限确认（自动化必备）|

### 3.3 输出解析

打印模式返回结构化 JSON，关键字段：

```json
{
  "result": "任务执行结果",
  "session_id": "会话ID（用于恢复）",
  "num_turns": "执行轮次",
  "total_cost_usd": "消耗费用",
  "status": "success/error"
}
```

## 四、实战场景示例

### 4.1 代码审查（打印模式）

审查认证模块安全问题并生成报告：

```bash
hermes chat --execute 'terminal(command="claude -p "审查 src/auth/ 模块，检查 SQL 注入、JWT 安全问题并生成报告" --allowedTools Read --max-turns 5", workdir="/path/to/project")'
```

### 4.2 多轮重构（交互式）

「重构→测试→修复」迭代开发：

```bash
# 1. 启动会话
hermes chat --execute 'terminal(command="tmux new-session -d -s refactor && tmux send-keys -t refactor "cd /path/to/project && claude --dangerously-skip-permissions" Enter")'

# 2. 重构数据层
hermes chat --execute 'terminal(command="sleep 5 && tmux send-keys -t refactor "重构数据层，替换 ORM 为 SQLAlchemy" Enter")'

# 3. 运行测试
hermes chat --execute 'terminal(command="sleep 30 && tmux send-keys -t refactor "运行所有单元测试，修复失败用例" Enter")'
```

### 4.3 批量文件修改

批量替换项目中废弃函数：

```bash
hermes chat --execute 'terminal(command="claude -p "将 src/ 下所有 deprecated_func 替换为 new_func" --allowedTools Read,Edit", workdir="/path/to/project")'
```

## 五、高级功能

### 5.1 会话恢复

打印模式执行后可通过 `session_id` 恢复任务：

```bash
# 1. 执行任务并保存会话ID
hermes chat --execute 'terminal(command="claude -p "生成 API 文档" --output-format json > /tmp/session.json", workdir="/path/to/project")'

# 2. 恢复任务
hermes chat --execute 'terminal(command="claude -p "补充接口参数说明" --resume $(cat /tmp/session.json | jq -r .session_id)", workdir="/path/to/project")'
```

### 5.2 结构化输出

生成符合 JSON Schema 的结果，便于后续处理：

```bash
hermes chat --execute 'terminal(command="claude -p "列出 src/ 下所有接口函数" --output-format json --json-schema '{"type":"object","properties":{"apis":{"type":"array"}}}'", workdir="/path/to/project")'
```

### 5.3 MCP 集成

接入 GitHub、数据库等 MCP 工具，扩展 Claude Code 能力：

```bash
# 接入 GitHub MCP
hermes chat --execute 'terminal(command="claude mcp add github -- npx @modelcontext/server-github")'
```

## 六、配置与优化

### 6.1 权限配置

限制 Claude Code 工具使用，保障安全：

```bash
# 仅允许读/编辑文件，禁止高危命令
hermes chat --execute 'terminal(command="claude -p "修改配置文件" --allowedTools Read,Edit", workdir="/path/to/project")'
```

### 6.2 成本控制

设置费用上限，避免超额消耗：

```bash
hermes chat --execute 'terminal(command="claude -p "生成测试用例" --max-budget-usd 0.1", workdir="/path/to/project")'
```

### 6.3 模型选择

简单任务用低成本模型，复杂任务用高性能模型：

```bash
# 简单任务：haiku
hermes chat --execute 'terminal(command="claude -p "格式化代码" --model haiku", workdir="/path/to/project")'

# 复杂任务：opus
hermes chat --execute 'terminal(command="claude -p "设计系统架构" --model opus", workdir="/path/to/project")'
```

## 七、注意事项

1. 交互式模式依赖 tmux，需提前安装 `brew install tmux`（macOS）/ `apt install tmux`（Linux）。

2. 打印模式添加 `--dangerously-skip-permissions` 可跳过权限弹窗，适合自动化。

3. 每个目录首次使用需确认信任，后续无需重复确认。

4. 会话超时或中断后，可通过 `claude -c` 恢复最近会话。

5. 敏感项目建议限制工具权限，禁止 `Bash` 等高危操作。

## 总结

Hermes 接入 Claude Code 后，可将复杂编码任务全流程自动化，兼顾简单任务的高效与复杂任务的灵活。通过打印模式适配脚本化场景，交互式模式支持多轮迭代，结合会话恢复、结构化输出等高级功能，可大幅提升开发效率。合理配置权限、成本与模型，可安全高效地将 Claude Code 集成到 Hermes 工作流中，实现编码任务无人值守。
