---
title: Codex Plugins 使用教程
order: 7
---

# Codex plugins 使用教程｜从零上手插件安装、实战与自定义构建

Codex plugins（插件）是 OpenAI 为 Codex 打造的可扩展能力框架，核心作用是将「可复用技能、第三方应用集成、MCP 服务器」打包为标准化工作流，让 Codex 突破原生编程能力边界——无需复杂配置，即可对接 Gmail、GitHub、Figma、Slack 等工具，实现代码开发、协作管理、自动化办公的全流程升级。本文基于官方文档，结合最新跨AI协同插件特性，完整讲解插件的安装、使用、实战场景、自定义构建及问题排查，所有操作可直接复制落地，帮助开发者快速解锁 Codex 的全场景能力。
## 一、核心认知：Codex 插件是什么？

Codex 插件本质是「能力扩展包」，通过标准化的封装方式，将特定场景的技能、工具连接逻辑、MCP 服务集成在一起，让 Codex 能够快速调用外部工具、复用复杂工作流，无需开发者手动编写集成代码。

### 1.1 插件的核心组成（3大模块）

- **Skills（技能）**：可复用的任务指令集合，Codex 可根据需求自动加载，确保执行特定任务时遵循统一步骤、引用正确的辅助脚本或规范。例如，GitHub 插件的「PR 分诊技能」，可自动遵循团队 PR 审核流程。

- **Apps（应用集成）**：与第三方工具的连接通道，让 Codex 能够读取外部工具的数据、执行操作。例如，Gmail 插件可让 Codex 读取邮件、起草回复；Slack 插件可总结频道内容、生成消息草稿。

- **MCP 服务器**：对接外部工具或共享信息的服务载体，通常用于连接本地项目外的系统（如 Figma 设计服务、云端文档），是 Codex 与外部工具通信的核心桥梁，与此前讲解的 Codex MCP 协议完全兼容。

### 1.2 插件的核心价值

- 提效降本：复用成熟工作流，避免重复编写集成代码，减少开发与协作成本；

- 能力扩展：突破 Codex 原生编程能力，对接办公、设计、部署等全场景工具；

- 标准化协作：通过插件统一团队工作规范（如 PR 审核、文档管理流程）；

- 跨AI协同：最新插件支持 Codex 与其他 AI 编程工具（如 Claude Code）联动，实现优势互补。

### 1.3 插件的分类（按来源）

- 官方精选插件（OpenAI Curated）：由 OpenAI 官方开发维护，适配性强、安全性高，如 GitHub、Gmail、Figma 等插件，可直接在插件市场安装；

- 社区插件：由开发者社区贡献，覆盖各类细分场景（如特定语言调试、自动化部署）；

- 自定义插件：开发者根据自身团队需求，自行构建的专属插件，用于适配内部工具或业务流程；

- 跨AI协同插件：OpenAI 最新推出的特殊插件（如 codex-plugin-cc），可实现 Codex 与 Claude Code 等竞争对手工具的联动，突破单一 AI 工具的能力局限。

## 二、快速上手：插件的安装与基础管理（App + CLI 双方式）

Codex 插件支持「图形化 App 操作」和「命令行 CLI 操作」两种方式，配置一次即可在 CLI、桌面端、IDE 扩展中共享生效，新手优先使用 App 方式，进阶用户可通过 CLI 实现精细化管理。

### 2.1 App 端安装与管理（推荐新手）

Codex App 提供可视化插件目录，无需输入命令，点击即可完成安装、授权与管理。

1. 打开 Codex App，在左侧导航栏找到「Plugins」（插件）选项，进入插件目录；

2. 插件目录按「官方精选」「社区推荐」「分类筛选」组织，可通过搜索框快速查找目标插件（如 GitHub、Figma）；

3. 点击插件卡片进入详情页，点击「Add to Codex」（添加到 Codex），完成安装；

4. 若插件需要对接外部应用（如 Gmail、Figma），会提示进行授权登录，按照引导完成账号关联即可；部分插件会在首次使用时才要求授权，无需提前配置；

5. 安装完成后，在「Installed Plugins」（已安装插件）列表中，可查看所有已安装插件，点击可启用/禁用、卸载插件。

### 2.2 CLI 端安装与管理（进阶用户）

通过 Codex CLI 命令，可快速完成插件的安装、卸载、列表查看等操作，适合批量管理或远程操作。

```bash
# 1. 打开 CLI 插件浏览器（核心命令）
codex /plugins

# 2. 常用管理命令
codex plugin install <插件名称>  # 安装指定插件（如 codex plugin install github）
codex plugin list                # 查看所有已安装插件
codex plugin uninstall <插件名称> # 卸载指定插件
codex plugin enable <插件名称>   # 启用已安装插件
codex plugin disable <插件名称>  # 禁用已安装插件（保留插件，不删除）

```

CLI 插件浏览器操作说明：打开插件浏览器后，可通过方向键浏览插件，按 Enter 查看插件详情，按 Space 切换插件启用状态，按 Esc 退出浏览器。插件会按市场来源分组，可切换标签页查看不同来源的插件。

### 2.3 插件启用/禁用的手动配置

若需精细化控制插件状态，可直接编辑 Codex 配置文件，手动设置插件的启用状态，修改后需重启 Codex 生效。

```toml
# 配置文件路径：~/.codex/config.toml（macOS/Linux）、%USERPROFILE%.codex\config.toml（Windows）
# 示例：禁用 gmail 插件
[plugins."gmail@openai-curated"]
enabled = false

# 示例：启用 github 插件
[plugins."github@openai-curated"]
enabled = true

```

## 三、实战示例：高频插件使用场景（可直接复制操作）

以下覆盖 4 类高频插件（官方精选+跨AI协同），结合真实开发与协作场景，给出具体操作指令与效果，新手可直接复制使用，快速掌握插件用法。

### 示例 1：GitHub 插件（代码协作核心）

核心功能：PR 分诊、Issues 管理、CI 状态查看、代码发布流程简化，是开发团队协同的必备插件。

```bash
# 1. 安装 GitHub 插件（CLI 方式）
codex plugin install github

# 2. 授权：首次使用会提示关联 GitHub 账号，完成 OAuth 授权
# 3. 常用操作指令（直接在 Codex 会话中输入）
# 查看最新 PR 的评论并总结变更
"@github 查看我最新 PR 的所有评论，并总结核心变更点"

# 分诊 Issues，标记优先级
"@github 筛选当前仓库中未处理的 Issues，按紧急程度排序并标记优先级"

# 查看 CI 构建状态
"@github 查看 main 分支最新 CI 构建结果，若失败请分析原因"

```

关键说明：GitHub 插件会自动关联当前工作目录的 Git 仓库，无需手动指定仓库地址，所有操作均遵循团队 GitHub 权限规范。

### 示例 2：Figma 插件（设计转代码）

核心功能：读取 Figma 设计稿的样式、布局信息，自动生成匹配的前端代码（React、Vue 等），减少设计与开发的沟通成本。

```bash
# 1. 安装 Figma 插件
codex plugin install figma

# 2. 授权：输入 Figma Access Token（在 Figma 账号设置中获取）
# 3. 核心操作（Codex 会话中输入）
"@figma 读取我 Figma 中「登录页设计」的文件，生成 React + TailwindCSS 组件代码"

# 进阶：指定代码风格
"@figma 读取 Figma 设计稿，生成 Vue3 组件，要求代码符合 ESLint 规范，包含 props 类型定义"

```

补充：Figma 插件依赖 MCP 服务，安装后会自动配置 MCP 服务器，无需额外手动配置，若启动失败可查看 MCP 连接状态（输入 /mcp 命令）。

### 示例 3：Slack 插件（团队协作沟通）

核心功能：总结 Slack 频道内容、起草消息回复、筛选特定主题的对话，适合远程团队协作时快速获取沟通重点。

```plaintext
# 1. 安装 Slack 插件并完成授权（关联 Slack 工作区）
# 2. 常用操作指令
"@slack 总结今天 #dev-team 频道的核心讨论内容，重点标注任务分配"
"@slack 帮我起草一条回复，回复 #product 频道中关于「需求变更」的消息，语气正式且简洁"
"@slack 查找 #tech-support 频道中过去 3 天关于「插件报错」的对话，整理解决方案"

```

### 示例 4：codex-plugin-cc（跨AI协同，最新特性）

codex-plugin-cc 是 OpenAI 官方 2026 年 3 月推出的跨AI协同插件，可将 Codex 植入 Claude Code 中，实现两大 AI 编程工具的优势互补——Claude Code 负责复杂架构推理，Codex 负责代码生成、审查，无需切换终端即可完成双模型协同。

```bash
# 1. 前置条件：安装 Node.js 18.18+、Codex CLI，拥有 ChatGPT 账户或 OpenAI API 密钥
npm install -g @openai/codex
codex login  # 登录 Codex（使用 OpenAI API 密钥或 ChatGPT 账号）

# 2. 在 Claude Code 中安装插件（4条指令，全程5分钟）
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup  # 验证配置，打印版本号即成功

# 3. 核心操作指令（Claude Code 中输入）
# 对抗式代码审查（挑战设计逻辑，找出深层漏洞）
/codex:adversarial-review --base main challenge whether this retry and caching design handles partial failures

# 后台委托 Codex 排查 bug（不中断当前开发）
/codex:rescue --background investigate why the integration tests started failing

# 查看后台任务状态与结果
/codex:status  # 查看任务进度
/codex:result  # 查看任务执行结果

# 取消正在运行的后台任务
/codex:cancel

```

关键注意：该插件并非免费工具，调用时会消耗 Codex 的使用额度（按 GPT-5.4 定价），可通过指定模型（如 gpt-5.4-mini）和努力程度（medium）降低成本；其「审查门」功能（拦截 Claude Code 输出并由 Codex 审查）威力极强，但可能导致双模型互相调用，消耗大量额度，需谨慎启用。

## 四、进阶：自定义插件构建（基于官方规范）

若官方插件和社区插件无法满足团队专属需求（如对接内部工具、自定义工作流），可按照 OpenAI 官方规范构建自定义插件。以下是核心构建流程与示例，基于官方 build 文档梳理，确保可落地。

### 4.1 自定义插件的核心结构

一个完整的 Codex 插件需包含 3 个核心文件，目录结构如下：

```plaintext
my-custom-plugin/          # 插件根目录
├── plugin.json            # 插件清单（必选，描述插件基本信息、依赖、配置）
├── skills/                # 技能目录（存放可复用技能脚本）
│   └── my-skill.js        # 自定义技能脚本
└── mcp/                   # MCP 服务器配置（可选，对接外部工具时需配置）
    └── mcp-config.toml    # MCP 服务配置文件

```

### 4.2 核心文件配置示例（最小可用插件）

#### 1. plugin.json（插件清单，必选）

```json
{
  "name": "my-custom-log-plugin",  # 插件名称（唯一标识）
  "version": "1.0.0",              # 版本号
  "description": "自定义日志记录插件，记录 Codex 会话操作日志",  # 插件描述
  "author": "your-name",           # 作者
  "dependencies": {},              # 依赖（如无依赖可留空）
  "skills": [                      # 插件包含的技能
    {
      "name": "log-record",        # 技能名称
      "description": "记录 Codex 会话操作日志到本地文件",
      "entry": "skills/my-skill.js"# 技能脚本入口
    }
  ],
  "mcp": false                     # 是否依赖 MCP 服务器（此处为false，无需配置）
}

```

#### 2. skills/my-skill.js（技能脚本，核心逻辑）

```javascript
// 核心功能：记录 Codex 会话操作日志到本地 ~/.codex/logs/custom-log.log
const fs = require('fs');
const path = require('path');

// 插件入口函数，接收 Codex 传入的会话信息
async function run(input) {
  const { session_id, prompt, response } = input;
  const logContent = `[${new Date().toISOString()}] 会话ID: ${session_id}\n用户输入: ${prompt}\nCodex 响应: ${response}\n\n`;
  
  // 日志文件路径
  const logPath = path.join(process.env.HOME, '.codex', 'logs', 'custom-log.log');
  
  // 写入日志
  fs.appendFileSync(logPath, logContent, 'utf8');
  
  return {
    message: "日志记录成功",
    success: true
  };
}

// 导出技能函数，供 Codex 调用
module.exports = { run };

```

### 4.3 自定义插件的安装与测试

```bash
# 1. 进入插件根目录
cd my-custom-plugin

# 2. 本地安装插件（CLI 方式）
codex plugin install ./

# 3. 启用插件
codex plugin enable my-custom-log-plugin

# 4. 测试插件（在 Codex 会话中调用技能）
"@my-custom-log-plugin 记录当前会话日志"

# 5. 验证效果（查看日志文件）
cat ~/.codex/logs/custom-log.log

```

### 4.4 自定义插件的发布（可选）

若需将自定义插件共享给团队或社区，可按照官方规范打包，提交到 Codex 插件市场：

1. 执行 `codex plugin package` 命令，将插件打包为 zip 压缩包；

2. 访问 OpenAI Codex 插件市场开发者平台，注册开发者账号；

3. 上传打包后的插件，填写插件详情、权限说明，提交审核；

4. 审核通过后，插件将在市场上线，可被其他用户搜索安装。

## 五、插件权限与数据安全说明

使用 Codex 插件时，需注意权限管控与数据安全，避免敏感信息泄露或误操作：

- 权限继承：安装插件后，其操作权限继承自 Codex 现有审批设置，不会额外提升权限；

- 授权管理：对接外部应用的插件（如 Gmail、GitHub），授权信息由外部应用管理，Codex 不会存储敏感授权凭证；

- 数据共享：当 Codex 通过插件向外部应用发送数据时，将遵循该外部应用的隐私政策与数据共享规则；

- 卸载残留：卸载插件仅删除 Codex 中的插件bundle，其关联的外部应用授权、本地缓存数据不会自动删除，需手动在对应应用中取消授权；

- 自定义插件安全：构建自定义插件时，避免在代码中硬编码敏感信息（如 API 密钥），建议通过环境变量注入；限制插件的文件访问权限，遵循最小权限原则。

## 六、常见问题与排查方法

- **插件安装失败**：检查网络连接（确保能访问 OpenAI 插件市场）；确认 Codex 版本更新至最新（旧版本可能不支持部分插件）；CLI 安装时，检查插件路径是否正确。

- **插件授权失败**：确认外部应用账号权限足够（如 GitHub 账号需有仓库读写权限）；清除浏览器缓存，重新发起授权；部分插件需科学上网才能完成授权。

- **插件调用无响应**：检查插件是否已启用（通过 codex plugin list 查看状态）；若插件依赖 MCP 服务器，输入 /mcp 查看 MCP 连接状态，重启 MCP 服务；检查插件是否需要更新。

- **codex-plugin-cc 配置失败**：确认 Node.js 版本≥18.18；检查 Codex 登录状态（codex login 重新登录）；Claude Code 版本需≥v2.0.x（旧版本不支持 Codex 插件）。

- **自定义插件无法调用**：检查 plugin.json 配置是否正确（无语法错误、技能入口路径正确）；确认插件已启用，重启 Codex 后重试；查看 Codex 日志（~/.codex/log/codex-tui.log）排查错误。

- **插件冲突**：若同时启用多个插件出现异常，可逐一禁用插件，定位冲突插件；避免同时启用功能重复的插件（如多个日志类插件）。

## 七、插件使用最佳实践

- 按需安装：仅安装日常使用的插件，过多插件会占用资源，可能导致 Codex 运行缓慢；

- 定期更新：及时更新插件至最新版本，修复已知漏洞，获取新增功能；

- 技能复用：将团队常用的工作流程（如 PR 审核、代码规范检查）封装为自定义技能，通过插件共享，统一协作标准；

- 成本控制：使用 codex-plugin-cc 等付费插件时，合理指定模型和努力程度，避免过度调用导致额度消耗过快；

- 安全优先：不安装来源不明的社区插件，避免恶意插件窃取敏感信息；定期检查插件授权状态，取消无用的授权；

- 协同搭配：结合 Codex MCP、AGENTS.md 与插件，构建「规范管控+能力扩展+跨AI协同」的全流程开发工作流。

## 八、总结

Codex 插件是扩展 Codex 能力的核心载体，通过标准化的封装的方式，让 Codex 无缝对接第三方工具、复用复杂工作流，甚至实现跨AI协同，从单一编程助手升级为全流程开发协作中枢。本文从基础认知、安装管理、实战示例，到自定义构建、问题排查，覆盖了插件使用的全流程，新手可通过官方精选插件快速上手，进阶用户可通过自定义插件适配团队专属需求。

随着 OpenAI 对插件生态的持续优化，未来将有更多场景化插件推出，结合 Codex 的原生编程能力、MCP 协议与 AGENTS.md 规范，将进一步提升开发效率、标准化协作流程，让 AI 编程真正融入日常开发的每一个环节。

