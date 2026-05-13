---
title: Codex 项目定制化教程
order: 13
---

# Codex 项目定制化教程：打造专属 AI 编程助手

Codex 定制化是通过**多层能力协同**，让 AI 完全适配你的项目规范、团队流程与工具生态，从 “通用助手” 升级为 “专属开发成员”。官方提供五层标准化定制能力：**AGENTS.md 持久规范、Memories 上下文记忆、Skills 复用技能、MCP 外部工具、Subagents 专业子代理**，它们互补协同，覆盖从基础规范到复杂工作流的全场景定制需求。

本文基于官方定制化概念文档，从零讲解每一层的作用、配置、实战用法与最佳实践，帮你快速搭建一套可落地、可复用、可共享的 Codex 定制体系。

---

## 一、定制化总览：五层协同架构

Codex 定制化不是单一功能，而是五层能力的有机组合：

1. **AGENTS.md**：项目级持久指令，定义 AI 必须遵守的基础规则

2. **Memories**：自动积累的上下文记忆，承接历史会话的关键信息

3. **Skills**：可复用工作流，封装重复任务的执行逻辑

4. **MCP**：外部工具连接协议，打通代码库外的系统与服务

5. **Subagents**：专业化子代理，分工并行处理复杂任务

**协作逻辑**：AGENTS.md 定基调，Memories 存上下文，Skills 做复用，MCP 连外部，Subagents 做并行，共同实现 “AI 按你的方式工作”。

---

## 二、第一层：AGENTS.md—— 持久化项目规范（定制基石）

AGENTS.md 是 Codex 的**项目宪法**，随代码库同步，在 AI 启动前自动加载，确保所有会话遵循统一规则，是最基础、最核心的定制层。

### 2.1 核心作用

固化项目 / 团队的**刚性规则**，避免 AI 重复犯错、偏离规范：

- 构建、测试、Lint 命令

- 代码审查标准、提交规范

- 项目专属编码约定

- 目录优先级、禁止行为

### 2.2 什么时候更新 AGENTS.md

- AI 反复犯同类错误时，新增规则约束

- AI 过度检索无关文件时，添加目录路由指引

- PR 审查中重复出现相同意见时，固化为规范

- 可通过 GitHub PR 评论 `@codex add this to AGENTS.md` 自动更新

### 2.3 分层配置（就近优先）

- **全局层**：`~/.codex/AGENTS.md` → 个人通用偏好（沟通风格、输出详略）

- **项目层**：仓库根目录 `AGENTS.md` → 团队共享规则

- **目录层**：子目录 `AGENTS.override.md` → 模块专项规则（覆盖上层）

### 2.4 实战案例：Node.js 后端项目 AGENTS.md

```markdown
# AGENTS.md（Node.js+Express+MongoDB 后端团队规范）
## 基础命令
- 安装依赖：pnpm install
- 本地启动：npm run start:dev
- 代码校验：npm run lint
- 单元测试：npm run test
- 数据库迁移：npm run db:migrate

## 编码约束
1. 路由文件统一放在 src/routes 目录，使用 RESTful 规范命名
2. 禁止使用 var，优先使用 const，必要时使用 let，函数命名采用 camelCase
3. 接口必须做参数校验（使用 joi 工具），异常统一抛出自定义 Error 并拦截
4. 禁止硬编码密钥、数据库地址，统一使用环境变量（.env 文件）
5. 数据库操作必须使用 Mongoose 模型，禁止直接编写原生 SQL

## 审查要求
1. 提交信息遵循 feat/fix/docs/refactor 规范
2. 接口开发必须补充单元测试，覆盖率≥75%
3. 禁止修改核心配置文件（config/index.js、mongoose.js）
4. 接口响应必须统一格式：{ code: number, message: string, data: any }
```

### 2.5 最佳实践

- 保持精简：只写 AI 会误解的规则，避免冗余

- 就近生效：规则放在生效范围最近的目录

- 配套落地：结合 pre-commit、Lint 工具双重约束

### 2.6 实战补充：AGENTS.md 更新场景案例

某 React 前端团队在使用 Codex 时，发现 AI 反复出现两个问题：一是频繁使用 var 声明变量，二是提交信息不遵循语义化规范。针对此场景，团队更新 AGENTS.md 并形成反馈闭环，具体操作如下：

```markdown

# 更新前（缺失相关约束）
## 基础命令
- 安装依赖：pnpm install
- 本地启动：npm run start:dev

# 更新后（新增约束，解决重复错误）
## 基础命令
- 安装依赖：pnpm install
- 本地启动：npm run start:dev
- 代码校验：npm run lint
- 单元测试：npm run test
- 数据库迁移：npm run db:migrate

## 编码约束
1. 禁止使用 var 声明变量，优先使用 const，仅在变量需重新赋值时使用 let
2. 提交信息必须遵循语义化规范，格式：type(scope): description
   - type 可选：feat（新功能）、fix（修复）、docs（文档）、refactor（重构）
   - scope 填写模块名（如：user、order、goods）
3. 接口参数必须使用 joi 校验，禁止未校验直接接收请求参数
4. 数据库查询必须添加异常捕获，避免服务崩溃

## 反馈闭环
# 执行 GitHub PR 评论指令，让 Codex 自动更新
@codex add the var declaration, commit message and interface validation rules to AGENTS.md
```

更新后，Codex 后续会话中不再出现 var 声明，提交信息也完全符合团队规范，无需人工反复提醒。

---

## 三、第二层：Memories—— 自动上下文记忆

Memories 是 Codex 从**历史会话中自动学习**的有用上下文，无需手动配置，用于承接过往决策、关键信息，避免重复沟通。

### 3.1 核心作用

- 记住项目结构、关键文件、历史修改

- 保留用户偏好、修复过的错误模式

- 减少重复信息传递，提升会话效率

### 3.2 特点

- 全自动积累，无需手动编写

- 随会话迭代更新，持续优化 AI 理解

- 仅作用于当前项目，不跨项目污染

> 记忆层是被动增强，无需手动配置，配合 AGENTS.md 效果最佳。
> 
> 

---

## 四、第三层：Skills—— 可复用工作流技能

Skills 是**封装重复任务的标准化能力**，将固定流程打包为可调用技能，支持隐式自动触发、显式手动调用，是定制化中 “提效” 的核心。

### 4.1 核心定位

- 编写格式：`SKILL.md` + 可选脚本 / 参考文档 / 资源

- 分发形式：本地直接使用，稳定后打包为插件共享

- 加载机制：渐进式披露（仅元数据预加载，使用时读全量指令）

### 4.2 标准目录结构

```text
my-skill/
├── SKILL.md        # 必选：元数据+执行步骤
├── scripts/        # 可选：CLI 辅助脚本
├── references/     # 可选：参考文档
└── assets/         # 可选：模板资源
```

### 4.3 实战案例：语义化提交 Skill

```markdown
---
name: commit
description: 按语义分组暂存并提交代码，用于提交前整理与分支清理
---
1. 禁止执行 git add .，按功能分组暂存文件
2. 分组规则：feat → test → docs → refactor → chore
3. 提交信息简洁，匹配修改范围
4. 单条提交专注、可独立审查
```

### 4.4 存储位置

- **全局技能**：`$HOME/.agents/skills` → 所有项目通用

- **项目技能**：`仓库/.agents/skills` → 团队项目专属

### 4.5 适用场景

- 发版流程、代码审查 routine

- 团队专属开发流程、日志分诊

- 需要示例、脚本辅助的标准化操作

### 4.6 实战补充：前端日志分诊 Skill 案例

后端项目频繁出现接口报错、数据库异常，开发人员需花费大量时间筛选服务日志、定位问题，为此封装「后端接口日志分诊」Skill，适配 Node.js+Express+MongoDB 技术栈，可直接调用使用，具体配置如下：

```markdown

---
name: backend-log-triage
description: 筛选 Node.js+Express 项目服务日志，定位接口报错、数据库异常根因，给出后端专属修复方案，适用于 src/logs 目录下的错误日志
---
1. 读取 src/logs/server.log 文件，筛选近 1 小时内的后端报错（优先处理接口请求、数据库操作、依赖包加载类错误）
2. 分类报错类型：接口参数校验错误、数据库连接异常、MongoDB 查询错误、依赖包缺失、路由匹配失败
3. 定位错误对应的接口路由/文件路径，分析根因（如：参数校验规则缺失、数据库地址配置错误、Mongoose 模型定义异常）
4. 给出后端专属修复方案，包含代码修改示例、操作步骤，贴合 Node.js+Express 编码规范
5. 标注错误等级（高危/普通/低危），高危错误（如数据库连接失败、服务崩溃）优先给出临时解决方案
6. 输出结构化报告，包含错误描述、根因、修复方案、影响范围

## 配套脚本（scripts/log-parse.js）
// 辅助脚本：提取日志中的关键信息，简化分析流程
const fs = require('fs');
const path = require('path');

const logPath = path.join(__dirname, '../../src/logs/server.log');
const logs = fs.readFileSync(logPath, 'utf8');

// 提取数据库相关报错、接口报错
const dbErrors = logs.match(/MongoDB.*?\n/g) || [];
const apiErrors = logs.match(/API Error.*?\n/g) || [];
console.log('数据库相关报错：', dbErrors);
console.log('接口相关报错：', apiErrors);

module.exports = { dbErrors, apiErrors };

## 存储位置
仓库/.agents/skills/backend-log-triage/
## 使用方式
1. 显式调用：$backend-log-triage
2. 隐式触发：“帮我分析今天的后端服务日志，定位接口和数据库报错并给出修复方案”
```

使用效果：调用该 Skill 后，Codex 可自动完成服务日志筛选、接口与数据库问题分析，输出可直接复用的修复代码（如参数校验补充、数据库配置修正），每次可节省 15-20 分钟排查时间，团队所有成员可共享使用。

---

## 五、第四层：MCP—— 外部工具连接协议

MCP（Model Context Protocol）是 Codex 连接**代码库外部系统**的标准协议，让 AI 直接调用设计工具、项目管理、文档、监控等第三方服务。

### 5.1 核心作用

- 接入 GitHub、Prometheus、Postman、Slack 等外部工具

- 获取实时数据（文档、日志、工单）

- 执行跨系统操作（设计转代码、工单状态更新）

### 5.2 MCP 与 Skills 协同

- Skills 定义**工作流**

- MCP 提供**外部工具能力**

- 依赖声明：在 `agents/openai.yaml` 中声明 MCP 依赖，实现自动装配

### 5.3 适用场景

- 需要读取代码库外的信息（监控数据、接口文档、工单）

- 需要操作外部系统（提交工单、更新文档、发送通知）

### 5.4 实战案例：后端 MCP 集成（GitHub+Prometheus）

后端开发中，需频繁查看 GitHub 代码审查记录、获取 Prometheus 服务监控数据，通过 MCP 集成这两个外部工具，无需切换平台，实现 Codex 直接调用，具体配置与使用如下：

```toml

# 集成 GitHub 服务（代码审查、PR 管理）
[mcp_servers.github]
url = "https://mcp.github.com/mcp"
bearer_token = "github-xxx-xxxx-xxxx"  # 个人 GitHub Access Token
startup_timeout_sec = 20  # 启动超时时间
description = "查看 GitHub PR 审查记录、代码提交记录，触发自动审查"

# 集成 Prometheus 服务（服务监控数据获取）
[mcp_servers.prometheus]
url = "http://localhost:9090/mcp"  # 本地 Prometheus 服务地址
startup_timeout_sec = 15
description = "获取后端服务监控数据（接口响应时间、数据库连接数、错误率），分析性能瓶颈"

# 依赖声明（agents/openai.yaml）
mcp_dependencies:
  - github
  - prometheus

## 使用场景与效果
# 场景1：查看 GitHub PR 审查记录
"@github 查看我提交的 PR（#123）的审查意见，分析需要修改的问题，给出后端代码修改方案"

# 场景2：获取 Prometheus 监控数据并分析
"@prometheus 获取近 1 小时内 /api/order 接口的响应时间、错误率数据，分析性能瓶颈，给出优化建议（贴合 Node.js+MongoDB 技术栈）"

## 核心优势
1. 无需切换平台，Codex 直接获取 PR 审查意见与监控数据，提升开发效率
2. 结合监控数据快速定位性能瓶颈，避免盲目优化
3. 同步 GitHub 审查规范，确保代码修改符合团队要求"
```

---

## 六、第五层：Subagents—— 专业化子代理

Subagents 允许你创建**角色专一、配置独立**的子代理，主代理统筹调度，子代理并行执行专项任务，适合复杂、多维度、高并发的开发场景。

### 6.1 核心价值

- 角色拆分：审查代理、探索代理、调试代理各司其职

- 配置隔离：不同子代理可使用不同模型、沙箱、MCP 服务

- 并行执行：多任务同时处理，大幅提升复杂任务效率

### 6.2 实战场景：PR 多维度审查

- 主代理：统筹任务、汇总结果

- 子代理 1（explorer）：梳理代码路径

- 子代理 2（reviewer）：检查安全与逻辑漏洞

- 子代理 3（docs-researcher）：校验接口文档一致性

### 6.3 配置位置

- 全局子代理：`~/.codex/agents/xxx.toml`

- 项目子代理：`仓库/.codex/agents/xxx.toml`

### 6.4 实战案例：后端多任务并行开发（Subagents 配置）

开发「订单管理模块」（包含订单创建、查询、修改、删除接口，以及订单数据统计），单线程开发效率低，通过配置 3 个子代理并行处理，主代理统筹汇总，具体配置与执行流程如下：

```toml

# 子代理1：explorer（代码探索，梳理结构）
# 文件：explorer.toml
name = "explorer"
description = "后端模块结构探索，梳理接口依赖、数据库模型，不编写代码"
developer_instructions = """
1. 梳理订单管理模块的接口结构，确定各接口依赖关系（如订单创建依赖用户、商品接口）
2. 确认技术方案：Node.js+Express+MongoDB，接口遵循 RESTful 规范，参数校验使用 joi
3. 列出核心文件路径（路由、控制器、模型、工具），标注各文件职责
4. 输出结构梳理报告，供其他子代理参考
"""
model_reasoning_effort = "medium"
sandbox_mode = "read-only"  # 只读模式，不修改代码

# 子代理2：api-worker（接口开发）
# 文件：api-worker.toml
name = "api-worker"
description = "后端接口开发，专注订单 CRUD 接口，贴合接口规范与数据校验要求
developer_instructions = """
1. 开发订单创建（POST /api/order）、查询（GET /api/order）、修改（PUT /api/order/:id）、删除（DELETE /api/order/:id）接口
2. 遵循团队编码规范，接口参数使用 joi 校验，响应格式统一
3. 实现接口异常处理，捕获数据库操作、参数校验相关错误
4. 开发完成后，执行 npm run test 校验接口单元测试通过
"""
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"  # 允许写入工作区
mcp_dependencies = ["github"]  # 依赖 GitHub 服务同步审查规范

# 子代理3：data-worker（数据处理与统计）
# 文件：data-worker.toml
name = "data-worker"
description = "后端数据处理开发，专注订单数据统计、数据库查询优化
developer_instructions = """
1. 开发订单数据统计接口（GET /api/order/statistic），支持按时间范围、订单状态筛选
2. 优化 MongoDB 查询语句，添加索引提升查询效率
3. 复用项目已有的数据库工具（src/utils/mongoose.js）
4. 编写接口单元测试，确保数据统计准确、查询响应快速
"""
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
mcp_dependencies = ["prometheus"]  # 依赖 Prometheus 监控查询性能

## 执行流程
1. 主代理创建会话，触发 3 个子代理并行执行
2. 子代理1 先完成结构梳理，输出报告给其他两个子代理
3. 子代理2、子代理3 并行开发接口与数据统计逻辑
4. 所有子代理完成后，主代理整合接口联动逻辑，完成订单管理模块开发

## 效果
原本需要 8 小时的开发任务，通过子代理并行处理，4 小时即可完成，且代码符合规范、接口响应稳定，无需反复返工
```

---

## 七、官方推荐：定制化构建顺序

按以下顺序搭建，成本最低、效果最稳：

1. **先配 AGENTS.md**：固化项目基础规则，确保 AI 不偏离规范

2. **复用插件 / 技能**：有现成插件直接安装，无插件则自建 Skills

3. **接入 MCP**：需要外部工具时，配置 MCP 服务

4. **启用 Subagents**：复杂任务需要并行分工时，使用子代理

---

## 八、完整实战：Node.js 后端项目一站式定制

5. **AGENTS.md**：编写团队构建、编码、审查规范（贴合后端技术栈）

6. **Skills**：创建语义化提交、版本发布、后端日志分诊技能

7. **MCP**：接入 GitHub（代码审查）、Prometheus（服务监控）

8. **Subagents**：配置代码审查、接口开发、数据处理三类子代理

9. **自动化**：将稳定流程设为定时任务（每日代码巡检、PR 自动审查）

最终效果：Codex 完全遵循后端团队规范，自动完成重复工作（日志分诊、接口校验），连接所有后端常用工具，并行处理复杂接口开发任务，成为标准化的团队开发成员。

### 8.1 实战补充：后端定制化完整配置示例

结合前文所有案例，整理后端项目 Codex 定制化完整配置清单，可直接复制落地：

```text

# 一、AGENTS.md 配置（仓库根目录）
参考 2.4、2.6 案例，包含基础命令、编码约束、提交规范、更新反馈闭环（贴合 Node.js+Express+MongoDB）

# 二、Skills 配置（仓库/.agents/skills/）
1. commit：语义化提交技能（4.3 案例）
2. backend-log-triage：后端日志分诊技能（4.6 案例）
3. version-release：版本发布技能（新增，封装发版流程：测试→数据库迁移→打包→部署）

# 三、MCP 配置（config.toml + agents/openai.yaml）
1. 集成 GitHub（代码审查）、Prometheus（服务监控）（5.4 案例）
2. 声明 MCP 依赖，实现自动装配

# 四、Subagents 配置（仓库/.codex/agents/）
1. explorer：结构探索子代理
2. api-worker：接口开发子代理
3. data-worker：数据处理子代理（6.4 案例）

# 五、自动化配置（Codex App）
1. 每日 9:00 执行日志分诊，推送报错报告到团队 Slack
2. PR 提交时，自动触发子代理审查（代码规范+接口校验+数据库操作规范）

# 六、配套工具
1. pre-commit 钩子：配合 AGENTS.md 约束代码提交
2. ESLint+Prettier：自动校验代码格式，与 Codex 规范一致
3. Jest：接口单元测试工具，确保接口开发质量
4. Prometheus+Grafana：服务监控工具，配合 MCP 实现性能分析
```

落地后，团队开发效率提升 40% 以上，Codex 可独立完成日志排查、组件开发、PR 审查等重复任务，开发人员专注核心业务逻辑。

---

## 九、总结

Codex 定制化的核心是**把团队流程变成 AI 可执行的规则**：

- AGENTS.md 定底线

- Memories 做积累

- Skills 提效率

- MCP 扩边界

- Subagents 增能力

五层能力协同，无需复杂开发，即可让 AI 完美适配你的项目与团队，真正实现 “AI 按你的方式工作”。

