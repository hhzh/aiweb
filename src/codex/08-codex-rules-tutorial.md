---
title: Codex Rules 使用教程
order: 8
---

# Codex Rules：命令权限精细化管控与安全防线构建

在使用 OpenAI Codex 进行本地开发时，**命令执行权限管控**是保障系统与代码安全的核心环节。Codex Rules 是官方提供的实验性权限控制机制，用于精准定义 Codex 在**沙箱外**可执行、需审批或禁止运行的命令，从根源避免 `rm -rf`、`sudo`、`git push` 等高风险操作被误执行。本文基于官方规则文档，从零讲解 Rules 文件创建、语法、测试、实战示例与最佳实践，所有配置可直接复制落地。

## 一、Rules 核心认知：是什么与为什么需要

Codex Rules 是一套基于 **Starlark**（类 Python 安全脚本语言）的命令权限规则体系，作用是**约束 Codex 在沙箱环境外的命令执行行为**，弥补沙箱模式的权限边界管控不足。

- 核心价值：实现命令级别的**允许 / 提示 / 禁止**三级管控，杜绝危险命令、规范操作流程；

- 适用场景：管控 Git 操作、CLI 工具（gh/npm）、系统命令、Shell 复合命令；

- 状态说明：目前为实验性功能，语法与逻辑可能后续迭代，但已可稳定用于日常权限管控；

- 规则优先级：多个规则匹配时，采用**最严格决策**：`forbidden`（禁止） > `prompt`（提示） > `allow`（允许）。

## 二、Rules 文件创建与存放规范

Rules 配置通过 `.rules` 文件生效，支持**全局级**与**项目级**双层配置，加载规则与安全强绑定。

### 1. 配置文件路径

- **全局规则（所有项目生效）**：`~/.codex/rules/xxx.rules`，默认创建 `default.rules` 即可；

- **项目规则（仅当前项目生效）**：`项目根目录/.codex/rules/xxx.rules`，**仅当项目被标记为信任时才加载**，未信任项目自动跳过，防止恶意规则注入；

- 加载时机：Codex 启动时扫描所有激活配置层的 `rules/` 目录，包括团队配置与用户层配置。

### 2. 快速创建规则文件

```bash
# 创建全局规则目录
mkdir -p ~/.codex/rules
# 创建默认规则文件
touch ~/.codex/rules/default.rules
```

## 三、核心语法：prefix_rule 完整字段详解

所有规则通过 `prefix_rule()` 函数定义，是 Rules 的唯一核心语法，支持 4 个关键字段，以下为完整解析与官方标准示例。

### 1. 字段清单

|字段|必选|说明|
|---|---|---|
|`pattern`|是|命令前缀匹配列表，支持字面量、多选匹配|
|`decision`|否（默认`allow`）|匹配后动作：`allow`/`prompt`/`forbidden`|
|`justification`|否|规则说明，审批 / 拦截时展示给用户|
|`match`|否|正向测试用例，验证规则匹配正确性|
|`not_match`|否|反向测试用例，排除误匹配场景|

### 2. 标准规则示例（官方推荐）

```python
# 示例：执行 gh pr view 前弹窗提示审批
prefix_rule(
    # 匹配命令前缀：gh → pr → view
    pattern = ["gh", "pr", "view"],
    # 动作：每次执行前提示用户确认
    decision = "prompt",
    # 规则说明，弹窗中展示
    justification = "查看 PR 需人工确认，防止误操作",
    # 正向用例：这些命令会匹配
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
        "gh pr view 7888 --json title,body,comments",
    ],
    # 反向用例：这些命令不匹配
    not_match = [
        "gh pr --repo openai/codex view 7888",
    ],
)
```

### 3. 关键语法细节

- **`pattern`**** 多选匹配**：同一位置支持多个可选参数，简化规则编写

    ```python
    # 匹配 git pull 或 git fetch
    pattern = ["git", ["pull", "fetch"]],
    ```

- **`decision`**** 三档动作**

    - `allow`：直接执行，无提示；

    - `prompt`：弹窗审批，用户确认后执行；

    - `forbidden`：直接拦截，无审批入口。

- **`match/not_match`**** 作用**：Codex 启动时自动校验，提前发现规则编写错误，避免上线后失效。

## 四、特殊命令处理：Shell 复合命令与包装器

Codex 对 `bash -c`/`zsh -c` 等 Shell 包装命令做了**安全拆分处理**，防止危险命令被 “夹带” 在安全命令中执行。

### 1. 安全拆分场景

仅当脚本满足以下条件时，Codex 会自动拆分为独立命令分别校验：

- 纯文本命令，无变量、通配符、赋值；

- 仅用 `&&`/`||`/`/`/`;` 连接。

示例：`git add . && rm -rf /`
会被拆分为 `["git", "add", "."]` 和 `["rm", "-rf", "/"]`，分别匹配规则，**最严格结果生效**，即便允许 `git add`，也会因 `rm -rf` 被拦截而整体拒绝。

### 2. 不拆分场景

若脚本包含以下高级特性，Codex 不解析、不拆分，**整体作为一条命令校验**：

- 重定向（`>`/`>>`）、命令替换（`$()`）；

- 环境变量、通配符（`*`/`?`）；

- 流程控制（`if`/`for`）。

此时需直接对 `["bash", "-c", "完整脚本"]` 编写规则，保障安全兜底。

## 五、规则测试工具：codex execpolicy check

规则编写完成后，无需重启 Codex，通过官方命令行工具**实时验证规则有效性**，是调试规则的核心手段。

### 1. 基础用法

```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- 待测试的命令
```

### 2. 实战测试示例

```bash
# 测试 gh pr view 7888 是否匹配规则
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888
```

### 3. 输出解读

返回 JSON 格式结果，包含**最终决策**、**匹配的规则**、**规则说明**，快速定位规则是否生效。

## 六、高频实用规则示例（直接复制使用）

以下为开发中最常用的三类规则，覆盖安全管控核心场景，可直接写入 `default.rules` 生效。

### 1. 允许类规则（安全只读命令）

```python
# 允许 git status 直接执行
prefix_rule(
    pattern = ["git", "status"],
    decision = "allow",
    justification = "查看仓库状态为安全操作，无需审批",
    match = ["git status", "git status --porcelain"],
)

# 允许 ls 查看文件
prefix_rule(
    pattern = ["ls"],
    decision = "allow",
    justification = "文件列表查看为安全操作",
)
```

### 2. 提示类规则（需人工确认）

```python
# git push 需审批
prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "代码推送需确认，防止误推至远程仓库",
    match = ["git push origin main", "git push"],
)

# npm install 需审批
prefix_rule(
    pattern = ["npm", "install"],
    decision = "prompt",
    justification = "安装依赖需确认，避免恶意包",
)
```

### 3. 禁止类规则（高风险命令）

```python
# 禁止 rm -rf 递归删除
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "禁止递归删除文件，防止数据丢失，建议手动删除",
    match = ["rm -rf node_modules", "rm -rf /"],
)

# 禁止 sudo 提权操作
prefix_rule(
    pattern = ["sudo"],
    decision = "forbidden",
    justification = "禁止提权执行命令，保障系统安全",
)

# 禁止 bash -c 执行复合命令
prefix_rule(
    pattern = ["bash", "-c"],
    decision = "forbidden",
    justification = "禁止直接执行bash -c复合命令，防止恶意脚本",
)
```

## 七、管理员强制规则：requirements.toml

企业场景下，管理员可通过 `requirements.toml` **强制下发限制性规则**，用户无法覆盖或修改，实现团队统一权限管控。

```toml
# requirements.toml 强制规则示例
[rules]
prefix_rules = [
    { pattern = ["sudo"], decision = "forbidden", justification = "企业禁止提权操作" },
    { pattern = ["rm", "-rf"], decision = "forbidden", justification = "企业禁止递归删除" },
]
```

## 八、Rules 配置最佳实践

1. **最小权限原则**：默认禁用高风险命令，仅开放必要操作，逐步放宽权限；

2. **必加测试用例**：所有规则都配置 `match`/`not_match`，启动时自动校验，避免规则失效；

3. **项目规则慎用**：仅对可信仓库启用项目级 `.codex/rules`，防止第三方代码注入恶意规则；

4. **复合命令谨慎处理**：对 `bash -c`/`zsh -c` 优先禁止，确需使用则严格管控；

5. **定期测试验证**：新增规则后必用 `codex execpolicy check` 测试，确保生效；

6. **拒绝无脑允许**：禁止对 `git`/`npm` 等工具全量 `allow`，仅开放子命令；

7. **配合沙箱使用**：Rules 与 `sandbox_mode = workspace-write` 配合，形成双层安全防护。

## 九、总结

Codex Rules 是 AI 编程本地安全的**最后一道防线**，通过命令级精细化管控，彻底解决 Codex 本地执行的权限风险。从规则文件创建、语法编写、测试验证到实战示例，本文覆盖了 Rules 配置的全流程，新手可直接复制示例落地，团队可通过管理员规则统一规范。

尽管 Rules 目前为实验性特性，但其权限管控逻辑已足够成熟，配合 Codex 沙箱、审批策略，可构建**安全、可控、高效**的 AI 编程工作流，让开发者放心使用 Codex 处理本地开发任务。

