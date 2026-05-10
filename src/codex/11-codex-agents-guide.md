---
title: Codex AGENTS 加载指令详解
order: 11
---

# Codex AGENTS 加载指令详解与最佳实践

[AGENTS.md](AGENTS.md) 是 OpenAI Codex 的**项目持久化指令文件**，相当于给 AI 编程助手编写的 “项目说明书与行为规范”。它会在 Codex 启动时自动加载，把编码规范、测试要求、目录规则、协作流程等上下文注入会话，让你无需在每次提问中重复说明，实现全局统一、项目专属、目录精细化的指令管控。本文基于官方指南，完整讲解 [AGENTS.md](AGENTS.md) 的加载逻辑、全局 / 项目配置、高级定制、验证调试与最佳实践，帮助你用一份文档驯服 Codex。

## 一、核心加载原理：Codex 如何读取 [AGENTS.md](AGENTS.md)

Codex 采用**全局 + 项目分层叠加**的机制加载指令，遵循固定优先级与合并规则，确保指令有序生效且不冲突。

1. **优先级顺序（从低到高）**

    - 全局层：优先读取 `~/.codex/AGENTS.override.md`，不存在则读 `~/.codex/AGENTS.md`；

    - 项目层：从仓库根目录向下遍历到当前工作目录，每个目录依次查找 `AGENTS.override.md` → `AGENTS.md` → 自定义 fallback 文件；

    - 合并规则：根目录文件先加载，子目录文件后加载，**靠近当前目录的指令会覆盖上层同名规则**。

2. **加载约束**

    - 跳过空文件，不加载无效内容；

    - 总大小默认上限 **32 KiB**，超出后自动截断，可通过配置调高；

    - 项目本地文件仅在仓库被标记为**信任**时加载，未信任项目跳过项目层指令。

## 二、快速上手：配置全局通用指令

全局 [AGENTS.md](AGENTS.md) 存放于用户目录，对所有项目生效，适合放置个人编码习惯、通用规范与跨项目规则。

1. 创建全局目录

```bash
mkdir -p ~/.codex
```

2. 编写全局指令文件
新建 `~/.codex/AGENTS.md`，写入通用规则：

```markdown
# 全局 Codex 工作规范
## 通用约定
1. 修改代码后必须运行对应测试，确保不破坏现有逻辑
2. 依赖安装优先使用 pnpm，禁止随意添加生产依赖
3. 代码风格遵循项目原有规范，不擅自重构格式
4. 敏感信息禁止硬编码，所有密钥从环境变量读取
## Git 规范
1. 提交信息简洁清晰，使用英文描述
2. 禁止强制推送（force push）到远程主分支
3. 修改完成后保持工作区干净，执行 git status 检查
```

3. 临时全局覆盖
如需临时替换全局规则，创建 `~/.codex/AGENTS.override.md`，删除后自动恢复原全局指令。

4. 验证生效
执行命令让 Codex 输出已加载指令：

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

## 三、项目分层配置：精细化目录指令管控

项目层支持**根目录通用规则 + 子目录专项覆盖**，适合 monorepo、多模块项目，让不同目录遵循专属规范。

### 1. 仓库根目录通用规则

在项目根目录创建 `AGENTS.md`，定义项目整体规范：

```markdown
# 项目级 Codex 规范
## 项目基础信息
- 技术栈：React + TypeScript + Vite
- 包管理：pnpm
## 构建与校验
1. 代码提交前必须执行 npm run lint
2. 前端改动需验证页面渲染正常
3. 公共工具函数修改必须同步更新文档
## 目录说明
- src/components：通用UI组件
- src/hooks：自定义 Hooks
- src/utils：工具函数
```

### 2. 子目录覆盖规则

针对特殊模块（如支付、核心服务）创建子目录 `AGENTS.override.md`，覆盖上层规则：

```markdown
# 支付服务专项规范
## 测试要求
- 必须使用 make test-payments 执行测试，禁止通用 npm test
## 安全约束
- 禁止随意修改密钥配置、轮换凭证需通知安全组
- 支付逻辑仅允许最小改动，禁止大范围重构
## 禁止操作
- 禁止删除支付日志、修改交易流水相关代码
```

### 3. 验证分层效果

进入子目录执行校验命令：

```bash
codex --cd services/payments --ask-for-approval never "List the instruction sources you loaded."
```

预期输出：全局指令 → 项目根指令 → 子目录覆盖指令，顺序加载且子目录规则优先生效。

## 四、高级定制：自定义 fallback 与大小限制

若项目已使用自定义说明文件（如 `TEAM_GUIDE.md`），可通过配置让 Codex 识别；同时可调整指令文件大小上限，避免截断。

1. 修改配置文件
编辑 `~/.codex/config.toml`，添加 fallback 文件名与大小配置：

```toml
# 自定义 fallback 文件名，按优先级顺序查找
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
# 调高指令大小上限至 64 KiB
project_doc_max_bytes = 65536
```

2. 生效规则
配置后 Codex 查找顺序变为：
`AGENTS.override.md` → `AGENTS.md` → `TEAM_GUIDE.md` → `.agents.md`，兼容现有项目文档。

3. 自定义 CODEX_HOME
如需切换独立配置环境，使用环境变量指定配置目录：

```bash
CODEX_HOME=$(pwd)/.codex codex exec "List active instruction sources"
```

## 五、验证与调试：确保指令正确加载

日常使用中，可通过三种方式快速校验 [AGENTS.md](AGENTS.md) 是否生效，避免规则遗漏。

1. 指令摘要校验

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

2. 指令来源校验

```bash
codex --ask-for-approval never "Show which instruction files are active."
```

3. 日志排查
查看日志确认加载文件列表，路径：

```bash
cat ~/.codex/log/codex-tui.log
```

日志中会记录本次会话加载的所有 [AGENTS.md](AGENTS.md) 路径与内容片段。

## 六、常见问题与快速排查

1. **指令完全不加载**

    - 确认当前目录在 Git 仓库内，`codex status` 查看工作区根目录；

    - 检查文件非空，空文件会被自动跳过；

    - 项目文件需确认仓库已标记为信任。

2. **加载错误指令**

    - 检查上层目录是否存在 `AGENTS.override.md`，重命名或删除即可恢复；

    - 确认 `CODEX_HOME` 环境变量未指向其他配置目录。

3. **Fallback 文件不生效**

    - 核对 `project_doc_fallback_filenames` 配置无拼写错误；

    - 重启 Codex 让新配置加载。

4. **指令被截断**

    - 调高 `project_doc_max_bytes` 配置；

    - 拆分大文件到子目录，避免单文件过大。

## 七、高质量 [AGENTS.md](AGENTS.md) 模板与最佳实践

### 1. 通用标准模板（直接复制使用）

```markdown
# AGENTS.md
## 项目概览
- 技术栈：XXX
- 核心目录：src/xxx（业务逻辑）、docs/（文档）、tests/（测试）
## 常用命令
- 安装依赖：pnpm install
- 本地启动：npm run dev
- 代码校验：npm run lint
- 执行测试：npm run test
## 编码规范
1. 变量命名使用驼峰式，禁止无意义缩写
2. 函数必须添加注释，说明功能、参数、返回值
3. 禁止硬编码敏感信息，使用环境变量
## 交付要求
1. 业务逻辑修改必须补充单元测试
2. 公共组件修改需验证所有引用场景
3. 完成任务后列出改动点与验证结果
## 禁止行为
1. 禁止擅自修改核心配置文件
2. 禁止直接修改主分支代码
3. 禁止删除日志、历史记录相关文件
```

### 2. 最佳实践

- **精简有效**：只写 Codex 无法自行推断的规则，避免冗余常识内容；

- **分层清晰**：全局放通用规则，项目放整体规范，子目录放专项约束；

- **持续迭代**：AI 重复犯错时，将纠正规则写入 [AGENTS.md](AGENTS.md)，形成闭环优化；

- **版本管理**：项目 [AGENTS.md](AGENTS.md) 纳入 Git 管理，团队共享统一规范；

- **安全优先**：禁止在指令中写入密钥、令牌等敏感信息。

## 八、总结

[AGENTS.md](AGENTS.md) 是 Codex 从 “通用助手” 变为 “项目专属开发者” 的核心配置，通过**全局 + 项目 + 子目录**的分层指令体系，实现规范自动化、上下文持久化、协作标准化。从个人通用习惯到团队项目规范，再到精细化目录约束，一份清晰的 [AGENTS.md](AGENTS.md) 能大幅降低沟通成本、减少 AI 失误、统一开发标准。配合 Codex 的沙箱、规则与钩子体系，可构建完整可控的 AI 编程工作流，让 Codex 始终按你的预期完成开发任务。

