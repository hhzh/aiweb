# Codex 基础配置教程：一站式上手

Codex 本地客户端支持**全局 + 项目**双层 TOML 配置，可自定义默认模型、执行权限、沙箱安全、网页搜索、功能开关等核心行为，CLI 与 IDE 扩展共用一套配置规则。本文基于官方基础配置文档，整理**文件位置、优先级、高频参数、功能启用**的完整入门指南，新手可直接复制配置快速落地。

---

## 一、配置文件基础：位置与加载规则

Codex 配置采用**分层覆盖**设计，全局默认 + 项目个性化，安全可控。

1. **用户级配置（全局）**
路径：`~/.codex/config.toml`
作用：所有项目共用的默认配置，优先级低于项目配置。

2. **项目级配置（局部）**
路径：`项目根目录/.codex/config.toml`
作用：仅对当前项目生效，**仅当项目被标记为信任时才会加载**，未信任项目会跳过该层配置，保障代码安全。

3. **快速打开配置**
IDE 扩展：点击右上角齿轮 → Codex Settings → Open config.toml
CLI / 桌面端：直接编辑上述路径的 TOML 文件即可。

4. **配置共享**
CLI 命令行、IDE 扩展、桌面端共用同一套配置层，修改一处全端生效。

---

## 二、配置优先级：谁说了算？

Codex 按**从高到低**顺序读取配置，高优先级覆盖低优先级：

1. CLI 命令行参数 / `--config` 临时覆盖

2. 配置档案（`--profile <名称>` 指定）

3. 项目级配置（`.codex/config.toml`，仅信任项目，就近目录优先）

4. 用户级配置（`~/.codex/config.toml`）

5. 系统级配置（Unix 系统：`/etc/codex/config.toml`）

6. 内置默认值

**安全提示**：标记为**未信任**的项目，会完全跳过项目级 `.codex/` 相关配置、钩子与规则，仅加载用户 / 系统配置。

---

## 三、高频常用配置（直接复制可用）

以下是开发中最常修改的核心参数，直接写入 `config.toml` 即可生效。

### 1. 默认模型

指定 CLI/IDE 默认使用的大模型

```toml
model = "gpt-5.5"
```

### 2. 执行审批策略

控制 Codex 执行生成命令前是否弹窗确认，保障安全

```toml
# 可选值：untrusted（仅未信任项目提示）/ on-request（请求时提示）/ never（从不提示）
approval_policy = "on-request"
```

### 3. 沙箱安全模式

限制 Codex 的文件系统 / 网络访问权限

```toml
# 可选值：workspace-write（仅工作区可写，推荐）/ danger-full-access（完全访问，谨慎使用）
sandbox_mode = "workspace-write"
```

### 4. Windows 原生沙箱

Windows 系统专属权限配置

```toml
[windows]
# elevated：管理员权限（推荐）；unelevated：普通权限（无管理员时降级用）
sandbox = "elevated"
```

### 5. 网页搜索模式

控制 Codex 联网搜索的行为

```toml
# cached：默认，读取缓存结果（更安全）；live：实时联网；disabled：关闭搜索
web_search = "cached"
```

### 6. 模型推理力度

调整模型的思考深度（支持该参数的模型生效）

```toml
model_reasoning_effort = "high"
```

### 7. 沟通风格

设置 Codex 的回复语气

```toml
# friendly：友好；pragmatic：务实；none：无风格
personality = "pragmatic"
```

### 8. 命令环境变量

控制 Codex 执行命令时转发的环境变量

```toml
[shell_environment_policy]
include_only = ["PATH", "HOME"]
```

### 9. 日志目录

自定义本地日志存储路径

```toml
# 绝对路径
log_dir = "/absolute/path/to/codex-logs"
# CLI 临时覆盖：codex -c log_dir=./.codex-log
```

---

## 四、功能开关：启用 / 关闭实验特性

通过 `[features]` 节点开启 / 关闭进阶功能，支持**配置文件**和**CLI 命令**两种方式。

### 1. 常用功能清单（核心稳定项）

```toml
[features]
shell_snapshot = true       # 加速重复命令（稳定）
codex_hooks = true          # 开启生命周期钩子（稳定）
fast_mode = true            # 快速模式（稳定）
multi_agent = true          # 多助手协作（稳定）
undo = false                # 开启Git快照撤销（稳定，默认关闭）
```

### 2. 启用 / 禁用方法

- 配置文件：在 `[features]` 下设置 `功能名 = true/false`

- CLI 命令：

    ```bash
    # 启用单个功能
    codex --enable undo
    # 启用多个功能
    codex --enable shell_snapshot --enable memories
    # 禁用：配置文件设为false
    ```

---

## 五、新手通用配置模板

直接复制到 `~/.codex/config.toml`，覆盖全局默认配置，安全又实用：

```toml
# 全局默认模型
model = "gpt-5.5"

# 执行审批与沙箱（安全基线）
approval_policy = "on-request"
sandbox_mode = "workspace-write"

# 网页搜索（安全缓存模式）
web_search = "cached"

# 沟通与推理
personality = "pragmatic"
model_reasoning_effort = "high"

# 环境变量限制
[shell_environment_policy]
include_only = ["PATH", "HOME"]

# 核心功能开启
[features]
shell_snapshot = true
codex_hooks = true
fast_mode = true
multi_agent = true
```

---

## 六、配置生效与注意事项

1. 配置修改后**重启 Codex 客户端**（IDE/CLI/ 桌面端）即可生效。

2. 项目级配置仅对**信任项目**加载，敏感代码库建议不开启项目配置。

3. 企业 / 托管设备可能通过 `requirements.toml` 强制约束配置（如禁止 `approval_policy = "never"`）。

4. 临时覆盖配置：用 CLI `--config` 参数，适合单次任务调试。

