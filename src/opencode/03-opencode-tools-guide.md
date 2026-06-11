---
title: OpenCode 工具使用教程
order: 3
---

# OpenCode 工具使用教程

OpenCode 的核心优势在于其强大的工具体系，让大语言模型能够深度操作本地代码库——完成文件读写、命令执行、代码编辑、网络检索、代码格式化等全流程开发操作。工具是 OpenCode 实现自动化编码、项目运维的核心能力，默认所有工具均处于启用状态，同时支持精细化权限管控、工具扩展与代码风格统一配置。

本文将全面讲解 OpenCode **工具权限配置**、**内置工具功能详解**、**自定义工具**、**MCP 扩展工具**、**文件忽略规则**以及**代码格式化工具**的使用方法与实战配置，帮助开发者根据项目场景管控工具权限、合理使用各类工具，规范项目代码风格。

## 一、工具基础与权限管控

### 1.1 工具概述

OpenCode 工具分为三大类：内置原生工具、自定义工具、MCP（Model Context Protocol）扩展工具。工具可赋能 LLM 在项目中执行读写文件、运行终端命令、检索网络、代码分析等操作。为保障项目安全，官方提供精细化权限配置能力，可单独管控每一个工具的使用权限。

### 1.2 权限规则说明

所有工具的权限通过项目根目录 `opencode.json` 配置文件中的 `permission` 字段管理，共支持三种权限策略：

1. `allow`：允许 LLM 直接使用该工具，无需人工审批（默认策略）；

2. `deny`：禁止使用该工具，LLM 无法调用；

3. `ask`：每次调用该工具前，向用户发起审批询问，确认后方可执行。

### 1.3 基础权限配置示例

#### 1.3.1 单工具权限配置

针对单个工具单独设置权限，是最常用的配置方式。例如禁止文件编辑、要求执行终端命令前审批、允许网页拉取：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "deny",
    "bash": "ask",
    "webfetch": "allow"
  }
}
```

#### 1.3.2 通配符批量配置

使用 `*` 通配符可批量管控一类工具，常用于统一管理 MCP 服务器下的所有扩展工具。例如要求名为 `mymcp` 的 MCP 所有工具调用前必须审批：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "mymcp_*": "ask"
  }
}
```

## 二、内置工具全解

OpenCode 内置十余款开箱即用的工具，覆盖文件操作、终端命令、代码检索、网络查询、交互问答等场景，部分工具存在权限关联、环境变量依赖等特殊规则，下面按功能分类逐一说明。

### 2.1 文件操作类工具

1. **read**

    - 功能：读取项目内文件内容，支持指定文件行范围读取大文件，避免一次性加载冗余内容。

    - 权限归属：独立权限 `read`，默认 `allow`。

    - 适用场景：代码查看、逻辑解读、配置文件读取。

2. **edit**

    - 功能：通过精准字符串替换修改已有文件，是 LLM 修改代码的核心工具。

    - 权限关联：`edit` 为总控权限，同时管控 `write`、`patch`、`multiedit` 等所有文件修改类工具。

    - 适用场景：代码逻辑修改、注释补充、配置调整。

3. **write**

    - 功能：创建新文件，若目标文件已存在则直接覆盖。

    - 权限规则：无独立权限，受 `edit` 权限统一管控。

    - 适用场景：新建代码文件、配置文件、文档。

4. **patch**

    - 功能：将补丁文件（diff 差异内容）应用到项目代码中。

    - 权限规则：受 `edit` 权限统一管控。

    - 适用场景：合并代码补丁、应用第三方代码修改方案。

### 2.2 检索与查询类工具

1. **grep**

    - 功能：基于正则表达式检索文件内容，支持文件过滤。

    - 权限归属：独立权限 `grep`，默认 `allow`。

    - 适用场景：全局查找关键字、接口、函数、错误日志。

2. **glob**

    - 功能：通过 Glob 通配符模式匹配项目文件，返回按修改时间排序的文件路径。

    - 权限归属：独立权限 `glob`，默认 `allow`。

    - 示例匹配规则：`**/*.js` 匹配所有 JS 文件、`src/**/*.ts` 匹配 src 目录下所有 TS 文件。

### 2.3 终端与脚本类工具

**bash**

- 功能：在项目环境中执行 Shell 终端命令，支持 `npm`、`git`、`pip` 等各类项目命令。

- 权限归属：独立权限 `bash`，建议生产 / 敏感项目设置为 `ask` 防止高危命令执行。

- 适用场景：安装依赖、查看 Git 状态、运行测试脚本、打包项目。

### 2.4 代码智能分析工具（实验性）

**lsp**

- 功能：对接 LSP（语言服务协议）服务器，实现代码定义跳转、引用查找、悬停提示、调用层级查看等 IDE 级智能能力。

- 启用条件：必须设置环境变量 `OPENCODE_EXPERIMENTAL_LSP_TOOL=true` 或全局开启实验功能 `OPENCODE_EXPERIMENTAL=true`。

- 支持操作：`goToDefinition`（跳转到定义）、`findReferences`（查找引用）、`hover`（悬停信息）、调用层级查询等。

- 权限归属：独立权限 `lsp`。

### 2.5 网络能力类工具

1. **webfetch**

    - 功能：根据指定 URL 拉取并读取网页原文内容。

    - 适用场景：查阅官方文档、解析指定网页教程、获取接口文档。

2. **websearch**

    - 功能：基于 Exa AI 实现全网信息检索，用于获取实时资讯、最新技术方案（突破模型训练数据时间限制）。

    - 启用条件：设置环境变量 `OPENCODE_ENABLE_EXA=1`（任意真值均可），无需额外配置 API 密钥。

    - 区分说明：需要**检索关键词找资源**使用 `websearch`；已有**明确 URL 读取内容**使用 `webfetch`。

### 2.6 辅助管理与交互工具

1. **skill**

    - 功能：加载项目内 `SKILL.md` 技能文件，并将内容载入对话上下文，复用预设编码规范与技能。

    - 权限归属：独立权限 `skill`。

2. **todowrite**

    - 功能：创建、更新待办任务列表，用于拆解复杂多步骤开发任务、跟踪进度。

    - 特殊规则：默认对子代理禁用，可手动配置开启。

3. **question**

    - 功能：LLM 在执行任务过程中主动向用户提问，收集需求、确认方案、澄清模糊指令。

    - 交互形式：支持单选选项与自定义文本输入，多问题可自由切换浏览。

## 三、工具扩展方案

当内置工具无法满足业务需求时，OpenCode 提供**自定义工具**、**MCP 服务器集成**两类主流扩展方式，同时配套文件检索规则，灵活适配个性化业务场景。

### 3.1 自定义工具

自定义工具是开发者自行编写、供 LLM 调用的扩展函数，可对接业务逻辑、第三方脚本、内部服务等，和 `read`、`bash` 等内置工具协同工作。工具定义文件优先使用 TypeScript/JavaScript 编写，同时支持调用 Python、Shell 等任意语言的脚本。

#### 3.1.1 工具存放路径

自定义工具分为**项目级**和**全局级**，路径区分明确，生效范围不同：

1. 项目级工具：存放于项目目录下 `.opencode/tools/`，仅对当前项目生效；

2. 全局级工具：存放于用户全局目录 `~/.config/opencode/tools/`，本机所有 OpenCode 会话均可使用。

#### 3.1.2 基础单工具定义

推荐使用官方提供的 `tool()` 辅助函数编写工具，该函数自带类型校验与参数校验，开发体验更佳。**工具文件名即为工具名称**。

示例：编写数据库查询工具（`.opencode/tools/database.ts`）

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Query the project database",
  args: {
    query: tool.schema.string().describe("SQL query to execute"),
  },
  async execute(args) {
    // 此处编写数据库查询业务逻辑
    return `Executed query: ${args.query}`
  },
})
```

#### 3.1.3 单文件多工具

单个 TS/JS 文件可导出多个独立工具，命名规则为 `文件名_导出变量名`。
示例：数学计算工具（`.opencode/tools/math.ts`）

```typescript
import { tool } from "@opencode-ai/plugin"

// 加法工具，最终名称：math_add
export const add = tool({
  description: "Add two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return args.a + args.b
  },
})

// 乘法工具，最终名称：math_multiply
export const multiply = tool({
  description: "Multiply two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return args.a * args.b
  },
})
```

上述文件会生成 `math_add`、`math_multiply` 两个独立工具。

#### 3.1.4 工具名称冲突规则

自定义工具与内置工具重名时，**自定义工具优先级更高，会直接覆盖内置工具**。

- 场景 1：主动覆盖（如需改造原有 bash 能力）
示例：自定义受限版 bash 工具，拦截高危命令（`.opencode/tools/bash.ts`）

    ```typescript
    import { tool } from "@opencode-ai/plugin"
    export default tool({
      description: "Restricted bash wrapper",
      args: {
        command: tool.schema.string(),
      },
      async execute(args) {
        return `blocked: ${args.command}`
      },
    })
    ```

- 场景 2：规避冲突 / 禁用内置工具
若无覆盖需求，建议使用独特工具名；若需要保留内置工具、仅禁用自定义工具，可通过 `permission` 权限配置管控。

#### 3.1.5 参数定义方式

工具参数基于 **Zod** 校验框架，支持两种写法，均可实现参数类型、描述定义：

1. 基于 `tool.schema`（官方封装，推荐，自带类型提示）

    ```typescript
    args: {
      query: tool.schema.string().describe("SQL query to execute")
    }
    ```

2. 原生导入 Zod（灵活适配复杂参数结构）

    ```typescript
    import { z } from "zod"
    export default {
      description: "Tool description",
      args: {
        param: z.string().describe("Parameter description"),
      },
      async execute(args, context) {
        // 工具逻辑
        return "result"
      },
    }
    ```

#### 3.1.6 会话上下文（context）

工具执行函数可接收第二个 `context` 参数，获取当前会话、目录、Git 工作区等全局信息，常用字段如下：

- `agent`：当前运行的代理名称

- `sessionID`：当前会话 ID

- `messageID`：当前消息 ID

- `directory`：会话工作目录

- `worktree`：Git 工作区根目录

示例：获取项目与会话信息（`.opencode/tools/project.ts`）

```typescript
import { tool } from "@opencode-ai/plugin"
export default tool({
  description: "Get project information",
  args: {},
  async execute(args, context) {
    const { agent, sessionID, messageID, directory, worktree } = context
    return `Agent: ${agent}, Session: ${sessionID}, Directory: ${directory}`
  },
})
```

#### 3.1.7 调用其他语言脚本

自定义工具的定义文件仅负责逻辑调度，可调用 Python、Shell 等任意语言编写的脚本。下面以 **Python 两数相加** 为例：

1. 第一步：编写 Python 脚本（`.opencode/tools/add.py`）

    ```python
    import sys
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    print(a + b)
    ```

2. 第二步：编写 TS 调度工具（`.opencode/tools/python-add.ts`）

    ```typescript
    import { tool } from "@opencode-ai/plugin"
    import path from "path"
    
    export default tool({
      description: "Add two numbers using Python",
      args: {
        a: tool.schema.number().describe("First number"),
        b: tool.schema.number().describe("Second number"),
      },
      async execute(args, context) {
        // 拼接脚本路径
        const script = path.join(context.worktree, ".opencode/tools/add.py")
        // 调用 Python 脚本（基于 Bun 执行命令）
        const result = await Bun.$`python3 ${script} ${args.a} ${args.b}`.text()
        return result.trim()
      },
    })
    ```

### 3.2 MCP 服务器集成

MCP（Model Context Protocol）服务器是官方推荐的外部扩展方案，可对接数据库、第三方 API、云端服务等外部系统，大幅拓展 OpenCode 能力边界。所有 MCP 扩展工具均可通过前文**通配符权限规则**统一管控。

### 3.3 底层检索规则与 .ignore 文件

`grep`、`glob` 等检索工具底层基于 ripgrep，默认遵循项目 `.gitignore` 规则，自动忽略配置中指定的文件 / 目录（如 `node_modules`、`dist`）。

若需要强制检索被 `.gitignore` 排除的目录，可在项目根目录创建 `.ignore` 文件，使用反向语法 `!` 放行指定路径。配置示例：

```ignore
# 强制允许检索 node_modules、dist、build 目录
!node_modules/
!dist/
!build/
```

## 四、代码格式化工具

OpenCode 支持**自动代码格式化**，在 LLM 编辑、创建文件后，会自动调用对应语言的格式化工具，统一项目代码风格，避免人工二次整理。本节讲解内置格式化工具、配置规则与自定义方案。

### 4.1 格式化工具工作原理

1. OpenCode 完成文件编辑 / 写入后，自动根据文件后缀匹配对应的格式化工具；

2. 执行格式化命令并应用修改；

3. 全程后台自动化执行，无需人工干预。

### 4.2 内置格式化工具清单

|格式化工具|支持文件后缀|使用前置要求|
|---|---|---|
|air|.R|系统安装 `air` 命令|
|biome|.js/.jsx/.ts/.tsx/.html/.css/.md/.json 等|项目存在 `biome.json(c)` 配置文件|
|cargofmt / rustfmt|.rs|系统安装 `cargo fmt` 命令|
|clang\-format|.c/.cpp/.h/.hpp 等|项目存在 `.clang-format` 配置文件|
|cljfmt|.clj/.cljs/.edn|系统安装 `cljfmt` 命令|
|dart|.dart|系统安装 `dart` 命令|
|gofmt|.go|系统安装 `gofmt` 命令|
|ktlint|.kt/.kts|系统安装 `ktlint` 命令|
|prettier|前端全类型文件|项目 `package.json` 包含 `prettier` 依赖|
|ruff / uv|.py/.pyi|系统安装对应命令及配置|
|shfmt|.sh/.bash|系统安装 `shfmt` 命令|
|terraform|.tf/.tfvars|系统安装 `terraform` 命令|
|zig|.zig/.zon|系统安装 `zig` 命令|
|oxfmt（实验性）|.js/.jsx/.ts/.tsx|项目依赖 `oxfmt` + 开启实验环境变量|

### 4.3 格式化工具基础配置

所有格式化相关配置统一在 `opencode.json` 的 `formatter` 字段中设置，支持全局禁用、单独禁用指定工具。

#### 4.3.1 全局禁用所有格式化工具

适用于项目有独立格式化流程，不需要 OpenCode 自动处理的场景：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": false
}
```

#### 4.3.2 单独禁用指定格式化工具

仅关闭某一款格式化工具，其余工具保持自动生效：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "prettier": {
      "disabled": true
    }
  }
}
```

### 4.4 自定义格式化工具

支持修改现有格式化工具的执行命令、环境变量、适配后缀，也可新增自定义格式化工具。配置字段说明：

- `disabled`：布尔值，是否禁用工具；

- `command`：数组，格式化执行命令，`$FILE` 为文件路径占位符（运行时自动替换）；

- `environment`：对象，执行命令时附加的环境变量；

- `extensions`：数组，该工具匹配的文件后缀。

#### 4.4.1 改写现有格式化工具

修改 Prettier 的执行命令与环境变量：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "prettier": {
      "command": ["npx", "prettier", "--write", "$FILE"],
      "environment": {
        "NODE_ENV": "development"
      },
      "extensions": [".js", ".ts", ".jsx", ".tsx"]
    }
  }
}
```

#### 4.4.2 新增自定义格式化工具

示例：为 Markdown 文件新增基于 Deno 的自定义格式化工具：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "custom-markdown-formatter": {
      "command": ["deno", "fmt", "$FILE"],
      "extensions": [".md"]
    }
  }
}
```

## 五、综合实战配置案例

结合权限管控、自定义工具、格式化、忽略规则，提供多场景落地配置，可直接适配前端、后端、安全管控类项目。

### 案例 1：安全管控配置（服务端 / 敏感项目）

限制高危终端命令、禁止自动修改文件，仅允许读取与查询，所有网络操作需审批：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": "ask",
    "edit": "deny",
    "write": "deny",
    "websearch": "ask",
    "webfetch": "ask"
  },
  "formatter": false
}
```

### 案例 2：前端项目完整配置

启用 Prettier 格式化，放行 node\_modules 检索，开启网络能力：

1. opencode.json 配置

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": "allow",
    "edit": "allow"
  },
  "formatter": {
    "prettier": {
      "command": ["npx", "prettier", "--write", "$FILE"],
      "extensions": [".js", ".ts", ".vue", ".css"]
    }
  }
}
```

2. .ignore 配置（强制检索 node\_modules）

```ignore
!node_modules/
```

### 案例 3：开启 LSP 实验工具 + Rust 后端项目

启用实验性 LSP 工具，使用 rustfmt 自动格式化 Rust 代码：

1. 环境变量（启动时临时生效）

```bash
OPENCODE_EXPERIMENTAL_LSP_TOOL=true opencode
```

2. opencode.json 配置

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "lsp": "allow",
    "bash": "ask"
  },
  "formatter": {
    "rustfmt": {
      "extensions": [".rs"]
    }
  }
}
```

### 案例 4：结合自定义工具的综合配置

场景：项目全局启用自定义数据库工具，限制 bash 权限，保留默认格式化：

1. 自定义工具文件：`.opencode/tools/database.ts`（前文数据库查询工具）

2. opencode.json 全局配置

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": "ask",
    "database": "allow"
  }
}
```

## 六、总结

OpenCode 的工具体系分为**功能工具**、**自定义工具**、**MCP 扩展工具**与**格式化工具**四大模块，相辅相成支撑自动化编码工作：

1. 权限管控是安全使用的前提，通过 `permission` 字段可灵活限制文件修改、终端命令、网络访问等高风险操作，通配符可批量管理扩展工具；

2. 内置工具覆盖文件操作、代码检索、网络查询、交互问答等全开发场景，需区分工具权限关联、环境变量依赖等特殊规则；

3. 自定义工具支持 TS/JS 开发，可调用任意第三方脚本，支持单文件多工具、上下文获取，且优先级高于内置工具，可按需改造原有能力；

4. 借助 `.ignore` 文件可突破 `.gitignore` 限制，灵活控制文件检索范围；

5. 自动化格式化工具可统一团队代码风格，支持全局禁用、单独配置、自定义新增，适配不同技术栈项目。

在实际使用中，个人开发项目可默认开启全部工具提升效率；企业 / 生产项目建议收紧 `bash`、`edit` 等高危工具权限，合理规划自定义工具命名避免冲突，搭配自动化格式化规范代码风格，兼顾效率与项目安全。
