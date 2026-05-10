---
title: Superpowers Skills 使用教程
order: 4
---

# Superpowers Skills 使用教程

在 AI 编码工具普及的当下，很多开发者面临"AI 盲目生成代码、缺乏工程规范、开发流程混乱"的痛点。Superpowers 作为一套面向 AI 编码智能体的标准化软件开发方法论，通过可组合的 Skills 技能集，让 Claude、Cursor、Codex、Copilot CLI、Gemini 等工具具备系统化开发能力，无需手动干预即可遵循规范流程完成开发任务。本文基于官方仓库 `obra/superpowers`核心内容，整理从安装部署到实操落地的全流程教程，帮助开发者快速上手并发挥其核心价值。

## 核心认知：Superpowers 与 Skills 是什么？

### 核心定位

Superpowers 并非单一插件，而是一套完整的 AI 编码工程框架，核心是通过"技能触发+流程强制"，让 AI 编码智能体从"单纯生成代码"升级为"具备工程思维的自主开发者"。其核心组件是 Skills（技能集），每个 Skill 对应开发流程中的一个标准化环节，可自动触发、组合执行，覆盖开发全生命周期。

### 设计理念

Superpowers 坚守四大核心工程理念，所有 Skills 均围绕这些理念设计，确保开发过程规范、高效、可维护：

- Test-Driven Development（TDD）：强制"先写测试、再写代码"，遵循红-绿-重构闭环；

- Systematic over ad-hoc：用标准化流程替代随机编码，减少人为失误；

- Complexity reduction：以简洁为核心目标，避免冗余代码，遵循 YAGNI（你不需要它）和 DRY（不重复造轮子）原则；

- Evidence over claims：所有功能必须经过验证，确保落地效果与预期一致。

### 运行逻辑

Superpowers 无需手动调用技能，启动 AI 编码智能体后会自动触发完整流程，核心逻辑如下：

1. 需求澄清：智能体启动后，不直接写代码，而是通过提问细化需求，提炼清晰的需求规格；

2. 方案设计：将需求转化为可落地的设计方案，分块展示供开发者确认，避免理解偏差；

3. 计划拆解：将开发任务拆分为 2-5 分钟可完成的微小任务，明确每个任务的文件路径、代码要求和验证步骤；

4. 自主开发：启动子代理驱动开发，为每个任务分配独立子代理，执行双阶段审查（规格合规性→代码质量）；

5. 质量管控：全程强制执行 TDD 流程，任务间自动进行代码审查，致命问题直接阻塞进度；

6. 收尾归档：任务完成后校验测试结果，提供分支合并、PR 提交等选项，自动清理工作区。

## 多平台安装指南（一键上手）

Superpowers 支持主流 AI 编码工具，安装流程简洁，无需额外配置，按对应工具执行以下操作即可完成安装：

|开发工具|安装步骤/命令|
|---|---|
|Claude Code（官方市场）|在 Claude Code 中执行命令：`/plugin install superpowers@claude-plugins-official`|
|Claude Code（第三方市场）|1. 注册市场：`/plugin marketplace add obra/superpowers-marketplace`2. 安装插件：`/plugin install superpowers@superpowers-marketplace`|
|OpenAI Codex CLI|1. 执行 `/plugins` 打开插件面板；2. 搜索 `superpowers`，点击「Install Plugin」完成安装。|
|OpenAI Codex App|1. 点击侧边栏「Plugins」；2. 在 Coding 分类中找到「Superpowers」；3. 点击「+」号，跟随提示完成安装。|
|Cursor|方式一：在 Agent 聊天框输入 `/add-plugin superpowers`；方式二：在插件市场搜索「superpowers」并安装。|
|OpenCode|向 OpenCode 发送指令：`Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md`，按提示完成安装（详细文档可参考`docs/README.opencode.md`）。|
|GitHub Copilot CLI|1. 添加市场：`copilot plugin marketplace add obra/superpowers-marketplace`2. 安装插件：`copilot plugin install superpowers@superpowers-marketplace`|
|Gemini CLI|安装：`gemini extensions install https://github.com/obra/superpowers`更新：`gemini extensions update superpowers`|

## 核心工作流实操（必走流程）

Superpowers 的所有 Skills 均为强制工作流，AI 智能体执行开发任务时会自动触发，无需手动调用，全程遵循"7步闭环"，确保开发流程规范：

### Step 1：brainstorming（需求头脑风暴）

编码前自动激活，智能体通过苏格拉底式提问，细化开发者提出的模糊需求，排除歧义。同时探索替代方案，将设计方案分块展示，供开发者确认后保存设计文档，避免后续开发偏离需求。

### Step 2：using-git-worktrees（Git 隔离工作区）

设计方案确认后，自动新建独立分支和隔离工作区，完成项目初始化操作，并校验测试基线是否干净（无异常依赖、无冗余文件），为后续开发提供纯净环境。

### Step 3：writing-plans（编写执行计划）

将整体开发任务拆分为微小单元（每个任务 2-5 分钟可完成），每个任务均明确：目标文件路径、完整代码示例、验证步骤（如何确认任务完成），确保子代理可直接执行，无需额外沟通。

### Step 4：子代理开发/执行计划

开发者输入「go」后，智能体启动以下两种模式之一（自动适配场景）：

- subagent-driven-development：为每个任务分配独立子代理，执行双阶段审查（先校验是否符合需求规格，再检查代码质量）；

- executing-plans：批量执行任务，设置人工检查点，开发者可在关键节点确认进度，平衡自主开发与人工管控。

实际使用中，Claude 等智能体可连续自主工作数小时，不偏离预设计划。

### Step 5：test-driven-development（测试驱动开发）

全程强制执行红-绿-重构（RED-GREEN-REFACTOR）闭环，具体流程：

1. 先编写失败的测试用例，运行测试并确认失败；

2. 编写最简代码，确保测试用例运行通过；

3. 对代码进行重构，优化可读性和性能；

4. 自动删除测试用例编写前生成的所有代码，避免无效冗余。

### Step 6：requesting-code-review（代码审查）

每个任务完成后自动触发审查，按问题严重程度（致命、警告、建议）分类上报，其中致命问题会直接阻塞开发进度，必须修复后才能继续，确保代码质量符合规范。

### Step 7：finishing-a-development-branch（开发分支收尾）

所有任务完成后，自动校验所有测试用例是否通过，然后提供四种分支处理选项：合并到主分支、提交 PR、保留分支、丢弃分支，选择后自动清理隔离工作区，完成开发闭环。

## Skills 技能库全解析

Superpowers 的 Skills 按开发场景分类封装，覆盖测试、调试、协作、高阶扩展四大类，可自动组合执行，以下是核心技能详解：

### 测试类技能（核心必备）

- `test-driven-development`：核心技能，实现红-绿-重构 TDD 闭环，附带测试反模式参考（避免常见测试误区）。

### 调试类技能（问题排查）

- `systematic-debugging`：4 阶段根因定位流程，包含根因追踪、深度防御、条件等待等实用技巧，帮助快速定位并解决问题；

- `verification-before-completion`：问题修复后自动二次校验，确保问题彻底解决，避免复发。

### 协作类技能（流程管控）

此类技能覆盖开发全流程，是 Superpowers 流程标准化的核心，包括：

- `brainstorming`：需求澄清与方案优化；

- `writing-plans`：细粒度任务计划编写；

- `executing-plans`：批量任务执行与人工检查点设置；

- `dispatching-parallel-agents`：子代理并发调度，提升开发效率；

- `requesting-code-review`：代码预审查，提供审查清单；

- `receiving-code-review`：审查反馈响应规范，确保反馈有效落地；

- `using-git-worktrees`：并行开发分支管理，隔离开发环境；

- `finishing-a-development-branch`：分支收尾与工作区清理；

- `subagent-driven-development`：子代理双阶段审查，快速迭代开发。

### 元技能（高阶扩展）

面向需要自定义技能的开发者，提供技能扩展能力：

- `writing-skills`：按最佳实践创建新技能，包含技能测试方法论，确保新技能兼容所有支持的编码智能体；

- `using-superpowers`：Superpowers 技能系统入门指引，帮助开发者快速熟悉核心功能。

## 快速上手实操案例（Claude Code 后端开发实战）

本案例以「在 Claude Code 中开发一个简单的用户管理后端接口（基于 Node.js + Express）」为例，完整演示 Superpowers 从安装到落地的全流程，包含具体命令、请求示例，可直接复制实操。

核心需求：开发 2 个后端接口（查询所有用户、新增用户），遵循 TDD 开发模式，确保接口可正常请求、测试用例通过，全程使用 Superpowers 自动流程管控。

1. 安装 Superpowers（Claude Code 官方市场）：
打开 Claude Code 会话窗口，直接输入以下命令并发送，完成插件安装（无需额外配置）：
`/plugin install superpowers@claude-plugins-official`提示「Plugin installed successfully」即为安装完成。

2. 启动开发会话：
在 Claude Code 聊天框中，发送启动指令，同时明确后端开发需求：
`启动 Superpowers，开发一个 Node.js + Express 后端，实现两个接口：1. GET /api/users 查询所有用户；2. POST /api/users 新增用户（参数：username、age），遵循 TDD 开发，生成完整代码和测试用例。`

3. 需求澄清（brainstorming 自动触发）：
Claude Code 会自动触发 brainstorming 技能，通过提问细化需求，示例提问及回复如下（直接复制回复即可）：
提问1：「查询用户接口是否需要分页？返回字段包含哪些？」
回复：「不需要分页，返回字段：id（自增）、username、age、createTime」

4. 提问2：「新增用户接口是否需要参数校验？比如 age 必须为数字？」
回复：「需要参数校验，username 非空、age 为正整数，校验失败返回 400 错误」

5. 提问3：「是否需要持久化存储？用什么存储方式？」
回复：「用临时内存存储（数组模拟），无需数据库，方便快速测试」

6. 确认方案与 Git 环境准备（using-git-worktrees 自动触发）：
方案确认后，Superpowers 自动触发 using-git-worktrees 技能，无需手动输入命令，会自动完成以下操作：
新建独立分支：superpowers-user-api

7. 初始化 Node.js 项目（生成 package.json）

8. 安装依赖（express、jest 用于测试）

9. 校验测试基线（确保环境无异常）

完成后会提示「Git worktree 已创建，测试基线干净，可进入计划编写阶段」。

10. 执行计划生成（writing-skills 自动触发）：
系统自动拆分任务（每个任务 2-5 分钟可完成），生成的任务清单如下（无需手动操作，仅需确认）：
```
任务1：创建 server.js 文件，初始化 Express 服务，配置基础路由；
任务2：编写测试用例（jest），覆盖两个接口的正常请求、异常请求场景；
任务3：实现 GET /api/users 接口，模拟内存存储用户数据；
任务4：实现 POST /api/users 接口，添加参数校验逻辑；
任务5：执行测试用例，修复代码中的问题，确保所有测试通过；
任务6：审查代码，确认符合规范，无冗余逻辑`发送「确认计划，go」启动自主开发。
```

11. 自主开发与测试（subagent-driven-development + TDD 自动触发）：
输入「go」后，Superpowers 启动子代理开发，全程自动执行，关键步骤及手动配合操作如下：
子代理自动编写测试用例（test.js），执行测试（自动触发 TDD 红-绿-重构），首次测试会失败（无接口实现）；

12. 子代理编写 server.js 代码，实现接口逻辑和参数校验，再次执行测试，直至测试通过；

13. 开发完成后，系统自动触发代码审查，提示「无致命问题，可进行接口测试」。

14. 接口实战测试（手动执行，复制以下命令即可）：
打开终端，进入项目目录（Superpowers 会提示项目路径），执行以下命令启动服务：
`node server.js` 服务启动后（提示「Server running on port 3000」），执行以下请求测试接口：
- ① 测试 GET /api/users（查询所有用户）：`curl http://localhost:3000/api/users`预期返回（初始无数据）：`{"code":200,"data":[],"msg":"查询成功"}`
- ② 测试 POST /api/users（新增用户）：`curl -X POST -H "Content-Type: application/json" -d '{"username":"test1","age":20}' http://localhost:3000/api/users`预期返回：`{"code":200,"data":{"id":1,"username":"test1","age":20,"createTime":"2026-04-29T00:00:00.000Z"},"msg":"新增成功"}`
- ③ 再次查询用户，验证新增效果：`curl http://localhost:3000/api/users`预期返回：`{"code":200,"data":[{"id":1,"username":"test1","age":20,"createTime":"2026-04-29T00:00:00.000Z"}],"msg":"查询成功"}


15. 分支收尾（finishing-a-development-branch 自动触发）：
接口测试通过后，系统自动触发收尾技能，提示以下选项：
`请选择分支处理方式：1. 合并到主分支；2. 提交 PR；3. 保留分支；4. 丢弃分支`发送「1. 合并到主分支」，系统自动完成分支合并、清理工作区，提示「开发完成，分支已合并，工作区已清理」。

提问结束后，Claude 会生成分块的设计方案，发送「确认方案，继续」即可进入下一步。

完成后会提示「Git worktree 已创建，测试基线干净，可进入计划编写阶段」。

至此，基于 Claude Code + Superpowers 的后端接口开发实战完成，全程遵循 Superpowers 强制流程，无需手动管控开发规范，仅需配合确认需求和执行测试命令即可。

## 更新与维护

- 自动更新：多数平台（Claude Code、Codex App、Cursor）支持 Superpowers 自动更新，无需手动操作；

- 手动更新：Gemini CLI 需执行`gemini extensions update superpowers`，其他平台可在插件市场找到"更新"按钮，点击即可完成；

- 问题排查：若技能无法正常触发，可检查插件安装是否完整，或在官方 Issues（https://github.com/obra/superpowers/issues）提交问题。

## 总结

Superpowers 核心价值在于"给 AI 编码工具注入工程素养"，通过标准化的 Skills 技能集和强制流程，解决 AI 编码"无序、跑偏、质量差"的痛点。无论是新手开发者还是资深工程师，都能借助它提升开发效率，让 AI 真正成为"可靠的开发助手"。只要完成对应平台的安装，即可享受全流程自动化的规范开发体验，无需额外学习复杂操作。
