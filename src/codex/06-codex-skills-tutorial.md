# Codex Skills：打造可复用工作流与扩展 AI 编程能力

Codex Skills（技能）是用于封装**专项任务工作流**的可复用单元，能将固定指令、参考资料、脚本与规范打包，让 Codex 在处理同类任务时稳定遵循统一流程。它是自定义 AI 编程行为的核心方式，也是插件的核心组成部分 —— 你先用 Skills 设计工作流，再打包为插件分发给团队复用。本文基于官方文档完整讲解 Skills 的创建、存储、调用、管理与分发，覆盖从个人提效到团队标准化的全场景用法。

## 一、Skills 核心基础概念

### 1.1 什么是 Skills

Skill 是一个标准化目录，以`SKILL.md`为核心，可包含指令、脚本、参考文档与资源，让 Codex 可靠执行某一类专项任务（如代码审查、项目初始化、接口调试）。它遵循开放智能体技能标准，支持 CLI、IDE 扩展、桌面端全平台使用。

### 1.2 Skills 与 Plugins 的关系

- **Skills**：专注工作流本身的设计与编写，是可复用的指令逻辑载体；

- **Plugins**：是 Skills、应用集成、MCP 服务的**分发安装包**，用于跨项目 / 跨团队共享 Skills。
简单说：**本地用 Skills，分享用 Plugins**。

### 1.3 两种调用方式

1. **显式调用**：在提示中直接指定技能，CLI/IDE 输入`/skills`查看列表，或输入`$技能名`触发；

2. **隐式调用**：Codex 根据你的任务描述，自动匹配技能`description`触发，无需手动指定。

### 1.4 高效加载机制：渐进式披露

Codex 启动时仅加载技能的**名称、描述、路径**，不会立即读取完整`SKILL.md`，仅在决定使用该技能时才加载完整指令。

- 初始技能列表限制为模型上下文窗口的 2%（约 8000 字符），避免挤占有效上下文；

- 描述过长会优先缩短，技能过多时部分会被省略并弹出提示；

- 选中技能后，仍会完整加载该技能的所有指令，保障执行效果。

## 二、Skill 标准目录结构

一个完整 Skill 包含**必选文件**与**可选扩展文件**，结构清晰、易于维护：

```text
my-skill/                # 技能根目录
├── SKILL.md             # 【必选】元数据+执行指令
├── scripts/             # 【可选】可执行脚本
├── references/          # 【可选】参考文档/规范
├── assets/              # 【可选】模板、图标等资源
└── agents/
    └── openai.yaml       # 【可选】UI元数据、策略、依赖
```

### 核心文件：[SKILL.md](SKILL.md) 规范

`SKILL.md`分为两部分：**YAML 前端数据**（必选 name+description）+ **Markdown 执行指令**。

```markdown
---
name: react-code-review
description: 对React函数组件做代码审查，检查Hooks规范、性能、可访问性，仅适用于TSX文件
---
## 执行步骤
1. 读取目标文件，确认是React TSX函数组件
2. 检查Hooks调用顺序与依赖项完整性
3. 校验组件是否做不必要重渲染，给出优化建议
4. 验证可访问性（alt文本、语义化标签）
5. 输出简洁的审查报告，标注问题等级与修改方案
## 禁止行为
- 不修改业务逻辑，仅做规范与性能审查
- 不生成无关代码，仅输出建议
```

## 三、快速创建 Skill（两种方式）

### 方式 1：使用内置创建器（推荐新手）

Codex 自带`$skill-creator`，交互式生成技能，无需手动搭建目录：

1. 启动 Codex，输入：

```bash
$skill-creator
```

2. 按提示回答：

    - 技能用途

    - 触发场景

    - 是否需要脚本

    - 仅指令还是包含脚本

3. 创建器自动生成目录与`SKILL.md`，直接编辑即可。

### 方式 2：手动创建（精准控制）

1. 创建技能目录：

```bash
# 创建用户级技能目录
mkdir -p ~/.agents/skills/react-code-review
cd ~/.agents/skills/react-code-review
```

2. 创建并编写`SKILL.md`（参考上文示例）；

3. 按需添加 scripts、references 等目录；

4. 修改后重启 Codex 即可生效。

## 四、Skill 存储位置与作用域

Codex 从四个层级加载技能，就近优先、互不覆盖，相同名称技能会同时显示。

|作用域|路径|适用场景|
|---|---|---|
|REPO（项目级）|当前项目 /.agents/skills|项目专属技能，团队共享|
|REPO（父目录）|项目上级目录 /.agents/skills|多模块共用技能|
|REPO（根目录）|项目根目录 /.agents/skills|全项目通用技能|
|USER（用户级）|~/.agents/skills|个人所有项目通用|
|ADMIN（系统级）|/etc/codex/skills|机器所有用户共用|
|SYSTEM（官方）|Codex 内置|基础通用技能（skill-creator 等）|

> 注意：项目级技能仅在仓库被标记为**信任**时加载；支持符号链接，方便技能共享。
> 
> 

## 五、Skill 调用与使用

### 5.1 显式调用（精准触发）

适合明确需要某技能的场景：

1. 查看所有可用技能：

```bash
/skills
```

2. 直接调用技能：

```bash
$react-code-review src/components/Button.tsx
```

### 5.2 隐式调用（自动匹配）

Codex 根据任务描述匹配`description`触发，无需手动指定：

- 好的描述：**明确用途 + 触发条件 + 适用范围**；

- 示例描述：`对React TSX组件做代码审查，检查Hooks、性能、可访问性`；

- 触发提示：`帮我审查这个Button组件的代码规范`。

### 关键规则

隐式调用完全依赖`description`，建议**前置核心关键词**，即便描述被缩短也能正确匹配。

## 六、Skill 管理：安装、启用与禁用

### 6.1 安装第三方技能

使用`$skill-installer`快速安装官方 / 社区技能：

```bash
# 安装 linear 技能
$skill-installer linear
```

支持从 Git 仓库下载，安装后自动检测，不生效则重启 Codex。

### 6.2 禁用技能（不删除）

在`~/.codex/config.toml`中配置，禁用指定技能：

```toml
[[skills.config]]
path = "/Users/xxx/.agents/skills/react-code-review/SKILL.md"
enabled = false
```

修改后**必须重启 Codex**生效。

## 七、高级配置：agents/openai.yaml

用于配置技能 UI 展示、调用策略与工具依赖，提升使用体验：

```yaml
interface:
  display_name: "React代码审查"
  short_description: "审查React组件规范与性能"
  icon_small: "./assets/icon.svg"
  brand_color: "#61dafb"
policy:
  allow_implicit_invocation: false  # 禁止隐式调用，仅允许显式触发
dependencies:
  tools:
    - type: "mcp"
      value: "eslint-mcp"
      description: "ESLint检查服务"
```

- `allow_implicit_invocation: false`：强制手动`$技能名`调用，避免误触发；

- `dependencies`：声明 MCP 等依赖，Codex 会自动检查依赖状态。

## 八、技能分发：打包为插件

如需跨项目 / 跨团队共享技能，将其打包为 Codex 插件：

1. 新建插件目录，放入技能文件夹；

2. 在`.codex-plugin/plugin.json`声明技能路径：

```json
{
  "name": "frontend-skills",
  "version": "1.0.0",
  "description": "前端团队通用技能包",
  "skills": "./skills/"
}
```

3. 共享插件目录，他人通过`codex plugin install ./路径`安装使用。

## 九、最佳实践

1. **单技能单职责**：一个技能只做一件事，避免逻辑臃肿，便于维护与匹配；

2. **指令优先，脚本为辅**：优先用 Markdown 指令描述流程，仅在需要确定性行为时用脚本；

3. **指令步骤化**：用 imperative 句式，明确输入、执行步骤、输出格式；

4. **描述精准**：前置触发关键词，确保隐式调用准确率；

5. **作用域分离**：个人技能放 USER 目录，团队技能放 REPO 根目录，避免冲突；

6. **禁止隐式高危技能**：涉及删除、构建、发布的技能，关闭隐式调用，仅允许显式触发；

7. **持续迭代**：根据使用反馈优化`SKILL.md`指令，提升执行稳定性。

## 十、常见问题排查

1. **技能不显示**

    - 检查路径是否在加载目录中，目录命名是否为`.agents/skills`；

    - 确认`SKILL.md`包含必填的`name`和`description`；

    - 重启 Codex 重新扫描技能。

2. **隐式调用不触发**

    - 优化`description`，更明确描述触发场景；

    - 检查`openai.yaml`是否关闭了隐式调用；

    - 技能过多被省略，清理无用技能。

3. **技能修改不生效**

    - 技能修改自动检测，未生效则重启 Codex；

    - 检查文件路径是否正确，无语法错误。

4. **项目级技能不加载**

    - 确认当前项目已被标记为**信任**；

    - 检查技能路径在项目内`.agents/skills`。

5. **技能冲突**

    - 同名技能会同时显示，调用时指定完整路径；

    - 禁用重复或无用技能，减少列表干扰。

## 十一、总结

Skills 是 Codex 实现**个性化、标准化、可复用**工作流的核心能力，通过目录化管理、双模式调用、分层加载，既能满足个人提效需求，也能支撑团队规范落地。从简单的代码审查，到复杂的项目初始化、自动化部署，都可以封装为 Skill，让 Codex 始终按你的预期执行任务。配合 [AGENTS.md](AGENTS.md)、MCP 与 Plugins，可构建完整可控的 AI 开发工作流，大幅降低重复沟通与指令编写成本。

