---
title: OpenCode Rule 使用教程
order: 7
---

# OpenCode Rule 使用教程

在使用 OpenCode 进行 AI 辅助编程时，默认行为往往难以匹配不同项目的技术栈、编码规范与协作要求。为此 OpenCode 推出 **Rule（规则）体系**，开发者可通过 `AGENTS.md` 规则文件自定义 LLM 行为，将项目约束、开发规范、架构说明等内容注入对话上下文，让 AI 深度适配当前项目。该功能对标 Cursor 规则体系，同时兼容 Claude Code 规则文件，支持项目级、全局两级配置，还可扩展加载本地 / 远程指令文件，是团队统一 AI 编码风格、提升协作效率的核心功能。

本文将从零讲解 OpenCode Rule 的核心概念、规则文件创建、分级配置、加载优先级、Claude Code 兼容设置、外部指令引用以及实战案例与最佳实践，帮助个人开发者与团队快速落地规则配置。

## 一、核心概念：规则文件概述

OpenCode 的规则本质是**自定义指令集合**，所有指令会被加载至 LLM 运行上下文，约束 AI 的编码逻辑、文件操作、命令执行等行为。核心载体为 `AGENTS.md`，同时兼容传统的 `CLAUDE.md` 文件。

规则文件分为两大使用维度：

1. **项目级规则**：作用于单个项目，由团队共享，统一项目内 AI 行为；

2. **全局级规则**：作用于本机所有 OpenCode 会话，多用于配置个人编码习惯、通用要求。

规则支持纯手动编写、命令自动生成、外部文件引用、远程指令加载等多种创建方式，灵活性极高，适配单体项目、多仓库 Monorepo、大型团队等各类场景。

## 二、规则文件快速创建与初始化

`AGENTS.md` 是 OpenCode 规则的核心文件，提供**命令自动生成**和**手动创建**两种方式，推荐优先使用命令初始化，减少基础配置工作量。

### 2.1 命令自动初始化（推荐）

借助 OpenCode TUI 内置的 `/init` 命令，可自动扫描项目目录、技术栈、文件结构，智能生成 `AGENTS.md` 基础内容；若项目已存在该文件，命令会在原有内容基础上补充优化。

1. 启动 OpenCode TUI：

```bash
opencode
```

2. 在交互界面中执行初始化命令：

```Plain Text
/init
```

3. 补充说明

- 生成的 `AGENTS.md` 会放置在**项目根目录**；

- 团队协作场景下，务必将该文件提交至 Git 仓库，保证所有成员使用同一套项目规则；

- 命令仅生成基础框架，开发者需根据项目实际补充编码规范、目录约束等细节。

### 2.2 手动创建规则文件

若需从零定制规则，可直接在对应目录新建 `AGENTS.md` 文件，使用标准 Markdown 语法编写指令，无特殊语法限制，文本内容会完整作为指令传入 LLM。

```bash
# 进入项目根目录，手动创建项目级规则文件
touch AGENTS.md

# 进入全局配置目录，手动创建全局规则文件
mkdir -p ~/.config/opencode && touch ~/.config/opencode/AGENTS.md
```

## 三、规则文件分级与生效范围

OpenCode 区分**项目级**和**全局级**两类规则文件，同时兼容 Claude Code 旧版规则文件，不同文件拥有独立存放路径、生效范围与使用场景，下面分类详解。

### 3.1 项目级规则文件

1. **文件路径**：项目根目录 `AGENTS.md`

2. **生效范围**：仅在当前项目及所有子目录启动的 OpenCode 会话生效

3. **使用场景**：定义项目专属架构、编码规范、目录权限、项目命令、已知问题等，是团队协作的核心规则文件。

4. **协作要求**：必须纳入 Git 版本控制，保证团队所有成员规则统一。

### 3.2 全局级规则文件

1. **文件路径**：`~/.config/opencode/AGENTS.md`（Linux / macOS）

2. **生效范围**：本机**所有** OpenCode 会话，不受项目目录限制

3. **使用场景**：配置个人通用编码习惯、全局禁用行为、通用工具使用规范等**个人专属规则**。

4. **协作要求**：该文件仅保存在本地，不提交 Git，仅作用于当前设备。

### 3.3 Claude Code 兼容规则文件

为方便从 Claude Code 迁移的用户，OpenCode 原生兼容 Claude Code 的规则文件与技能文件，作为降级方案使用：

1. **项目降级规则**：项目根目录 `CLAUDE.md`（项目无 `AGENTS.md` 时自动启用）

2. **全局降级规则**：`~/.claude/CLAUDE.md`（全局无 `~/.config/opencode/AGENTS.md` 时自动启用）

3. **技能文件兼容**：`~/.claude/skills/` 目录下的技能文件可正常加载

### 3.4 关闭 Claude Code 兼容功能

若无需兼容 Claude Code，可通过环境变量关闭对应能力，分为全量关闭、单独关闭规则 / 技能兼容三类配置：

#### 3.4.1 临时生效（当前终端会话）

```bash
# 关闭所有 Claude Code 兼容能力（规则 + 技能）
export OPENCODE_DISABLE_CLAUDE_CODE=1

# 仅关闭全局 ~/.claude/CLAUDE.md 规则兼容
export OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1

# 仅关闭 ~/.claude/skills 技能文件兼容
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1
```

#### 3.4.2 永久生效

将上述环境变量写入 Shell 配置文件（`~/.bashrc`、`~/.zshrc` 等），执行 `source` 命令刷新后永久生效。

## 四、规则文件加载优先级

当本地同时存在多份规则文件时，OpenCode 会按照固定顺序检索、加载规则，**匹配到第一个有效文件后停止检索**，优先级从高到低如下：

1. **本地项目目录遍历**：从当前目录向上逐级查找 `AGENTS.md`，优先于同目录下的 `CLAUDE.md`；

2. **OpenCode 全局规则**：加载 `~/.config/opencode/AGENTS.md`；

3. **Claude 全局降级规则**：加载 `~/.claude/CLAUDE.md`（已关闭兼容则跳过）。

**举例说明**：

- 项目根目录同时存在 `AGENTS.md` 和 `CLAUDE.md`：仅加载 `AGENTS.md`；

- 项目无任何规则文件，本机存在两份全局规则：优先加载 `~/.config/opencode/AGENTS.md`；

- 关闭 Claude 兼容后：系统会直接跳过 `CLAUDE.md` 相关文件检索。

## 五、\[AGENTS.md\]\(AGENTS.md\) 编写规范与实战示例

`AGENTS.md` 采用标准 Markdown 格式，内容无强制语法，建议按照「项目介绍 → 目录结构 → 技术栈 → 编码规范 → 常用命令 → 约束要求」的结构编写，提升可读性与实用性。以下提供多场景可直接复用的实战模板。

### 5.1 通用基础模板（适用于绝大多数项目）

```markdown
# 项目全局规则
## 一、项目概述
简述项目用途、技术定位、核心业务。

## 二、目录结构约定
- `src/`：核心源码目录（允许修改）
- `public/`：静态资源目录（仅新增文件，不修改原有内容）
- `config/`：项目配置文件（修改前必须确认）
- `tests/`：单元测试目录，代码变更必须同步更新测试用例

## 三、技术栈规范
- 编程语言：TypeScript 5.0+
- 框架：React 18 + Vite
- 代码检查：ESLint + Prettier
- 禁止使用废弃 API 和实验性功能。

## 四、编码规则
1. 组件统一使用函数式组件，禁止类组件；
2. 所有变量、函数必须补充 TypeScript 类型定义；
3. 注释使用 JSDoc 规范，公共函数必须编写注释。

## 五、常用开发命令
- 本地启动：npm run dev
- 代码格式化：npm run format
- 单元测试：npm run test
- 生产打包：npm run build

## 六、风险约束
1. 禁止直接删除目录与核心配置文件；
2. 修改数据库相关代码必须额外说明风险；
3. 遇到未知问题优先输出排查思路，而非直接修改代码。
```

### 5.2 Monorepo 多仓库项目示例

针对 PNPM / Bun 管理的 Monorepo 项目，重点补充分包规则、导入规范：

```markdown
# SST v3 Monorepo 项目规则
## 项目说明
基于 TypeScript + Bun Workspaces 构建的 Monorepo 全栈项目，使用 SST 做云服务编排。

## 目录结构
- `packages/`：所有业务分包（functions、core、web）
- `infra/`：云服务基础设施配置（按服务拆分文件）
- `sst.config.ts`：项目主配置文件

## 代码标准
1. 全局启用 TypeScript Strict 严格模式；
2. 公共通用代码统一存放至 `packages/core`；
3. 后端函数代码统一存放至 `packages/functions`；
4. 基础设施配置拆分至 `infra` 下独立文件。

## 导入规范
跨分包导入必须使用工作空间别名：@my-app/core/xxx，禁止相对路径跨包引用。
```

### 5.3 后端 Java 项目示例

```markdown
# Java SpringBoot 项目规则
## 技术栈
Java 17 + SpringBoot 3.2 + MyBatis-Plus + MySQL

## 目录约束
- `controller`：接口层，仅处理参数接收与响应返回
- `service`：业务逻辑层，核心代码存放目录
- `mapper` / `entity`：数据库映射层，禁止随意修改表结构

## 编码规范
1. 接口返回统一使用全局 Result 封装类；
2. SQL 语句禁止写在代码中，统一存放至 XML 映射文件；
3. 新增接口必须补充接口注释与参数说明。

## 操作约束
1. 修改数据库字段前，先输出 SQL 变更语句；
2. 生产环境相关配置禁止直接修改。
```

## 六、自定义指令扩展（instructions 配置）

当规则内容较多、需要模块化管理，或是需要复用团队公共规则时，可通过 `opencode.json` 配置文件中的 `instructions` 字段，批量加载**本地文件**、**通配符目录**、**远程网络文件**，所有加载的指令会自动与 `AGENTS.md` 内容合并生效。该功能是大型项目、团队公共规则复用的最佳方案。

### 6.1 基础配置语法

在项目根目录或全局配置 `~/.config/opencode/opencode.json` 中添加 `instructions` 数组，支持三种资源类型：本地单独文件、Glob 通配符目录、远程 HTTP 链接。

> 补充说明：远程指令文件获取超时时间为 5 秒，网络不佳时建议优先使用本地文件。
> 
> 

### 6.2 实战配置示例

#### 6.2.1 加载多个本地规则文件

加载项目内开发规范、贡献指南等文档作为补充指令：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/development-guidelines.md",
    "docs/api-standard.md"
  ]
}
```

#### 6.2.2 使用 Glob 通配符批量加载（Monorepo 推荐）

匹配指定目录下所有规则文件，无需逐个手动填写路径，适配多分包项目：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "packages/*/AGENTS.md",
    ".cursor/rules/*.md"
  ]
}
```

#### 6.2.3 加载远程公共规则文件

从团队 Git 仓库加载公共编码规范，实现全团队规则统一更新：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "https://raw.githubusercontent.com/team-name/public-rules/main/ts-standard.md"
  ]
}
```

## 七、外部文件引用两种实现方案

当规则文件体量庞大、需要模块化拆分时，OpenCode 提供两种外部文件引用方案，可根据项目复杂度选择。

### 7.1 方案一：opencode.json instructions（官方推荐）

优先使用 `instructions` 字段做文件引用，优势是配置简单、支持通配符、维护成本低，适合 Monorepo、多文档项目，具体配置参考 **6.2 小节**。

### 7.2 方案二：\[AGENTS.md\]\(AGENTS.md\) 内手动指令引用

若希望在规则文件中显性声明文件依赖，可在 `AGENTS.md` 中编写自定义指令，引导 AI 主动读取指定外部文件，支持递归引用。

#### 示例：模块化规则引用

```markdown
# TypeScript 项目主规则
## 外部文件加载规则
重要约束：
1. 遇到 @xxx 格式的文件引用时，按需使用 Read 工具加载对应文件；
2. 禁止提前加载所有引用文件，采用懒加载模式；
3. 被引用文件内容优先级高于当前文件默认规则；
4. 支持递归读取多层引用文件。

## 专项规范引用
1. TypeScript 编码规范：@docs/typescript-rules.md
2. React 组件规范：@docs/react-pattern.md
3. 接口设计规范：@docs/api-rules.md
4. 通用基础规范：@rules/base-guideline.md
```

## 八、最佳实践

结合不同使用场景，总结个人开发、团队协作、大型 Monorepo 项目的规则配置最佳实践，规避常见问题。

### 8.1 个人开发者

1. 全局 `AGENTS.md` 配置个人通用编码习惯（如代码注释风格、工具偏好），一次配置全局生效；

2. 小型项目优先使用 `/init` 命令生成基础规则，少量补充细节即可；

3. 无需复杂拆分，单份 `AGENTS.md` 维护全部项目规则。

### 8.2 中小型团队协作

1. 强制将项目 `AGENTS.md` 纳入 Git 管理，禁止本地差异化修改；

2. 规则内容聚焦**项目独有约束**，通用编码规范可抽离为公共文档，通过 `instructions` 加载；

3. 定期迭代规则文件，将高频踩坑问题补充至规则中。

### 8.3 大型 Monorepo 项目

1. 根目录编写全局项目规则，各分包目录维护独立 `AGENTS.md`；

2. 使用 Glob 通配符 `packages/*/AGENTS.md` 批量加载分包规则；

3. 团队公共规范托管至远程 Git，通过远程链接加载，统一全仓库规则。

### 8.4 迁移自 Claude Code 的用户

1. 短期过渡：保留原有 `CLAUDE.md`，不关闭兼容功能；

2. 长期迁移：逐步将 `CLAUDE.md` 内容迁移至 `AGENTS.md`，并关闭 Claude 兼容能力；

3. `~/.claude/skills` 技能文件可继续使用，或迁移至 OpenCode 标准技能目录。

## 九、常见问题与排查

### 9.1 规则文件不生效

1. 排查路径：确认文件存放位置符合分级要求，项目规则必须在**根目录**；

2. 优先级问题：检查是否存在更高优先级的 `AGENTS.md` 覆盖了当前规则；

3. 格式问题：规则文件使用纯 Markdown，避免特殊加密字符、非可见符号。

### 9.2 远程指令文件加载失败

1. 网络问题：远程文件超时时间为 5 秒，内网 / 弱网环境建议改用本地文件；

2. 链接有效性：验证 HTTP 链接可正常访问，确保文件为纯文本格式；

3. 跨域限制：私有内网链接需保证当前设备可正常访问。

### 9.3 关闭 Claude 兼容后仍加载 \[CLAUDE.md\]\(CLAUDE.md\)

1. 检查环境变量是否正确设置，执行 `env | grep CLAUDE` 验证；

2. 重启 OpenCode TUI / 服务，环境变量修改后需重启会话生效。

### 9.4 多份指令内容冲突

加载多个文件时，**后加载的指令会覆盖先加载的同名约束**，建议统一规则口径，避免相互矛盾的配置。

## 十、总结

OpenCode Rule 体系以 `AGENTS.md` 为核心，搭配分级配置、Claude 兼容、外部指令扩展等能力，构建了一套完整的 AI 行为管控方案。核心要点总结如下：

1. **文件分级**：项目级规则用于团队协作，全局规则用于个人习惯配置，二者各司其职；

2. **创建方式**：优先使用 `/init` 命令自动生成基础文件，提升效率；

3. **优先级**：本地项目 `AGENTS.md` \> 全局 `AGENTS.md` \> 各类兼容 `CLAUDE.md`；

4. **扩展能力**：通过 `opencode.json` 的 `instructions` 字段可加载本地、通配符、远程文件，适配大型项目模块化需求；

5. **兼容策略**：迁移用户可临时使用 Claude 规则文件，长期使用建议切换为原生 `AGENTS.md` 并关闭兼容。

合理配置规则文件，能够让 OpenCode 深度贴合项目与团队的开发标准，减少 AI 输出不符合规范的代码，大幅降低人工修正成本，是提升 AI 辅助编程效率的关键配置。
