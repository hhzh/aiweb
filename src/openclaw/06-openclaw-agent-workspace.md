---
title: OpenClaw Agent Workspace 智能体工作区详解
order: 6
---

# OpenClaw Agent Workspace 智能体工作区详解

智能体工作区（Agent Workspace）是 OpenClaw 智能体的核心运行目录，作为文件工具与上下文处理的**唯一工作目录（cwd）**，承载智能体的人格、记忆、指令、技能与运行资产，是智能体的 "数字家园"。本文基于官方文档，完整拆解工作区的定位、配置、文件体系、隔离机制、备份迁移与最佳实践。

## 一、工作区核心定位

工作区是智能体执行所有文件操作、读取人格配置、加载技能的专属目录，与存储配置、凭证、会话的 `~/.openclaw/` 系统目录完全分离，二者职责边界清晰：

- **工作区**：存储智能体的人格、记忆、操作指令、技能、运行产出等业务数据

- `~/.openclaw/`：存储系统配置、模型鉴权、渠道凭证、会话日志等底层数据

工作区默认并非硬性沙箱，工具可基于工作区解析相对路径，启用 `agents.defaults.sandbox` 后，非主会话会在独立沙箱工作区运行，实现完全隔离。

## 二、默认位置与自定义配置

### 2.1 默认路径

- 基础默认：`~/.openclaw/workspace`

- 多 Profile 场景：设置 `OPENCLAW_PROFILE` 且非 `default` 时，路径变为 `~/.openclaw/workspace-<profile>`

### 2.2 自定义配置

通过 `~/.openclaw/openclaw.json` 覆盖默认路径：

```json
{
  "agent": {
    "workspace": "~/.openclaw/workspace"
  }
}
```

### 2.3 工作区初始化

执行以下命令可自动创建工作区并填充引导文件：

- `openclaw onboard`

- `openclaw configure`

- `openclaw setup`

## 三、工作区标准文件体系

工作区包含固定的核心文件，每个文件承担专属职能，OpenClaw 会在会话启动时自动加载：

|文件 / 目录|核心作用|加载时机|
|---|---|---|
|`AGENTS.md`|智能体操作说明、记忆使用规则|每次会话开始|
|`SOUL.md`|人设、语气、能力边界|每次会话|
|`USER.md`|用户身份信息、称呼偏好|每次会话|
|`IDENTITY.md`|智能体名称、风格、表情符号|引导流程创建 / 更新|
|`TOOLS.md`|本地工具使用约定与说明|每次会话|
|`HEARTBEAT.md`|心跳运行检查清单|心跳执行时|
|`BOOT.md`|网关重启检查清单|Gateway 重启时|
|`BOOTSTRAP.md`|首次运行初始化仪式|仅全新工作区|
|`memory/YYYY-MM-DD.md`|每日记忆日志|会话启动可选加载|
|`MEMORY.md`|长期整理记忆|仅主私有会话|
|`skills/`|工作区专属技能|智能体加载技能时|
|`canvas/`|节点 UI 渲染文件|节点连接时|

## 四、文件截断与缺失处理

1. **大小限制**
单文件最大字符由 `agents.defaults.bootstrapMaxChars` 控制（默认 20000），总注入最大字符由 `agents.defaults.bootstrapTotalMaxChars` 控制（默认 150000）。

2. **截断规则**
超大文件会自动截断并添加标记，不会中断会话启动流程。

3. **缺失处理**
文件缺失时，系统会注入 "缺失文件" 标记并继续运行。

4. **修复命令**
`openclaw setup` 可重新创建缺失的默认文件，且不会覆盖现有内容。

## 五、沙箱隔离机制

### 5.1 基础规则

工作区默认不是硬性沙箱，绝对路径可访问主机其他位置；启用沙箱后可实现强隔离：

```json
{
  "agent": {
    "sandbox": true
  }
}
```

### 5.2 沙箱工作区路径

启用沙箱且 `workspaceAccess!="rw"` 时，工具会在 `~/.openclaw/sandboxes` 下的独立沙箱目录运行，不接触主机主工作区。

### 5.3 沙箱种子规则

沙箱仅复制工作区内的常规文件，指向工作区外部的符号链接、硬链接会被直接忽略。

## 六、引导文件禁用与管理

若需要自行管理工作区文件，可通过配置禁用自动引导文件创建：

```json
{
  "agent": {
    "skipBootstrap": true
  }
}
```

## 七、多工作区管理与清理

### 7.1 冗余工作区清理

旧版本安装可能创建 `~/openclaw` 目录，多个活动工作区会导致鉴权混乱、状态漂移。

- 建议仅保留**一个活动工作区**

- 冗余目录可归档或删除：`trash ~/openclaw`

- `openclaw doctor` 会自动检测额外工作区并发出警告

### 7.2 多工作区切换

通过修改 `agents.defaults.workspace` 配置项，切换当前活动工作区，确保配置路径与实际目录一致。

## 八、Git 备份与安全规范

工作区存储私密记忆与配置，**必须使用私有 Git 仓库备份**，严格遵循数据安全原则：

### 8.1 初始化备份

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md memory/
git commit -m "初始化OpenClaw智能体工作区"
```

### 8.2 推送私有仓库

仅使用 GitHub/GitLab 私有仓库，禁止推送到公共仓库：

```bash
git branch -M main
git remote add origin 私有仓库HTTPS地址
git push -u origin main
```

### 8.3 安全忽略规则

必须配置 `.gitignore`，禁止提交敏感数据：

```Plain Text
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

### 8.4 禁止提交内容

- API 密钥、OAuth 令牌、密码等鉴权信息

- `~/.openclaw/` 目录下的所有系统文件

- 原始聊天记录、敏感业务附件

## 九、工作区迁移到新机器

### 9.1 迁移步骤

1. 克隆私有工作区仓库到新机器默认路径：`~/.openclaw/workspace`

2. 修改 `~/.openclaw/openclaw.json` 配置工作区路径

3. 执行修复命令补全缺失文件：`openclaw setup --workspace <目标路径>`

4. 单独复制会话数据（如需保留）：`~/.openclaw/agents/<agentId>/sessions/`

### 9.2 迁移验证

执行 `openclaw doctor` 检查工作区状态，确认文件完整、配置生效。

## 十、高级工作区配置

### 10.1 多智能体路由

多智能体场景下，可为不同智能体分配独立工作区，通过渠道路由配置实现智能体间数据隔离。

### 10.2 按会话沙箱工作区

启用沙箱后，非主会话自动使用 `agents.defaults.sandbox.workspaceRoot` 下的专属目录，实现会话级运行隔离。

## 十一、工作区最佳实践

1. 工作区包含私密数据，仅使用私有仓库备份，严禁公开分享

2. 定期提交 Git 变更，避免记忆与配置丢失

3. 精简引导文件大小，防止自动截断丢失关键信息

4. 生产环境强制启用沙箱隔离，防止工具越权访问主机文件

5. 定期执行 `openclaw doctor` 检查工作区状态，清理冗余目录

6. 迁移时优先备份工作区，再单独迁移会话数据

7. 首次运行完成后删除 `BOOTSTRAP.md`，避免重复执行初始化流程
