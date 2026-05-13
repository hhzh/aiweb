---
title: gstack AI 全流程工程使用教程
order: 4
---

# gstack AI 全流程工程使用教程

单人开发最痛苦的莫过于"一人扛全流程"——需求要自己理、架构要自己设计、代码要自己审、测试要自己跑，效率低下且质量难控。gstack 由 YC 总裁 Garry Tan 开源，能将 Claude Code 等 AI 编码助手转化为虚拟工程团队，覆盖 Think→Plan→Build→Review→Test→Ship→Reflect 全研发流程，让单人开发者实现传统 20 人团队的交付效率。采用 MIT 开源协议，完全免费。

项目地址：[https://github.com/garrytan/gstack](https://github.com/garrytan/gstack)

---

## 一、前置环境要求

gstack 依赖基础工具，安装前请确保本地已配置：

1. **Claude Code**：核心 AI 编码环境

2. **Git**：代码版本管理

3. **Bun v1.0+**：运行时依赖

4. **Windows 系统额外**：需安装 Node.js（兼容 Playwright 传输）

---

## 二、30 秒快速安装

gstack 支持**个人模式**、**团队模式**、**OpenClaw 集成**三种安装方式，按需选择。

### 2.1 个人模式（单人开发）

打开 Claude Code，直接执行以下命令，自动完成克隆、配置：

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

安装后在`CLAUDE.md`添加 gstack 配置段，声明可用技能。

### 2.2 团队模式（协作开发）

进入项目仓库，执行命令开启团队自动更新，避免版本不一致：

```bash
(cd ~/.claude/skills/gstack && ./setup --team) && ~/.claude/skills/gstack/bin/gstack-team-init required && git add .claude/ CLAUDE.md && git commit -m "require gstack for AI-assisted work"
```

- `required`：强制团队成员使用；替换为`optional`为推荐使用

- 无冗余文件、无版本漂移，会话自动静默检查更新

### 2.3 OpenClaw 集成

在 OpenClaw 代理中执行安装命令，即可直接调用 gstack 技能：

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

并在`AGENTS.md`配置编码任务默认调用 gstack 技能。

### 2.4 多 AI 代理适配

gstack 支持 Codex、Cursor、GBrain 等 10+AI 代理，指定代理安装：

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup --host <代理名称>
```

示例：`./setup --host codex`适配 OpenAI Codex CLI。

---

## 三、全流程开发实战

安装完成后，以下按研发流程顺序讲解每个阶段对应的技能命令。

gstack 遵循**Think→Plan→Build→Review→Test→Ship→Reflect**标准研发流程，每个环节对应专属技能，前后技能自动衔接上下文。

### 3.1 思考阶段：产品需求梳理

命令：`/office-hours`

- 6 个引导性问题，重构产品需求，挑战不合理预设

- 自动生成设计文档，供下游技能直接读取

- 示例：输入 “开发日历每日简报应用”，AI 会提炼核心需求、给出 3 种实现方案

### 3.2 规划阶段：分层评审

1. **CEO 视角评审**：`/plan-ceo-review`
聚焦产品战略，4 种模式（扩展 / 选择性扩展 / 控 scope / 缩减），挖掘核心价值

2. **工程架构评审**：`/plan-eng-review`
输出数据流图、状态机、异常处理、测试矩阵，明确技术方案

3. **设计体验评审**：`/plan-design-review`
维度打分、AI 低质内容检测，优化交互方案

4. **一键全流程规划**：`/autoplan`
自动执行 CEO→设计→工程→DX 评审，仅需确认审美决策

### 3.3 构建阶段：设计与编码

1. **设计系统搭建**：`/design-consultation`
从零生成完整设计系统、产品原型

2. **视觉方案探索**：`/design-shotgun`
生成 4-6 种 AI 设计稿，浏览器对比，学习用户偏好

3. **生产级 HTML 输出**：`/design-html`
设计稿转无依赖、响应式 HTML，适配 React/Vue 等框架

### 3.4 评审阶段：代码质量把关

命令：`/review`

- Staff 工程师级代码审查，自动修复基础问题

- 排查生产环境隐性 Bug，补全功能缺口

- 跨模型复核：`/codex`调用 OpenAI Codex 独立评审

### 3.5 测试阶段：真实环境验证

1. **全量测试**：`/qa <测试URL>`
启动真实 Chromium 浏览器，自动化点击流程，定位并修复 Bug，生成回归测试

2. **仅报告测试**：`/qa-only`
仅输出 Bug 报告，不修改代码

3. **安全审计**：`/cso`
执行 OWASP Top10+STRIDE 威胁建模，零误报安全检测

### 3.6 发布阶段：自动化上线

1. **代码合并发布**：`/ship`
同步主干、运行测试、覆盖率审计、推送代码、创建 PR

2. **部署验证**：`/land-and-deploy`
合并 PR、等待 CI、验证生产环境可用性

3. **发布后监控**：`/canary`
监控控制台错误、性能衰退、页面故障

### 3.7 复盘阶段：持续优化

命令：`/retro`

- 每周工程复盘，统计交付数据、测试健康度、成长点

- `retro global`跨项目、跨 AI 工具全局复盘

---

## 四、核心技能分类速查

|技能类型|核心命令|功能说明|
|---|---|---|
|规划类|`/autoplan` `/plan-eng-review`|自动完成全维度规划、架构锁定|
|设计类|`/design-shotgun` `/design-html`|视觉探索、生产级前端输出|
|评审类|`/review` `/codex`|代码审查、跨模型复核|
|测试类|`/qa` `/cso`|功能测试、安全审计|
|发布类|`/ship` `/land-and-deploy`|自动化发布、部署验证|
|安全类|`/careful` `/guard`|破坏性操作预警、编辑范围锁定|
|工具类|`/learn` `/gstack-upgrade`|记忆管理、版本自更新|

---

## 五、高级功能解锁

### 5.1 GBrain 持久化记忆

命令：`/setup-gbrain`

- 三种部署方式：Supabase 云服务、自动新建 Supabase、本地 PGLite

- 为 AI 代理提供跨会话记忆，支持仓库级权限管控（读写 / 只读 / 拒绝）

### 5.2 并行冲刺管理

通过 Conductor 并行运行多个 Claude Code 会话，同时处理 10-15 个任务：

- 一个会话做需求规划、一个做代码评审、一个做测试验证

- 流程化管控避免多代理混乱，单人管理多任务并行

### 5.3 真实浏览器能力

1. 命令：`/open-gstack-browser`
启动带反爬机制、侧边栏 AI 助手的专属浏览器，无验证码干扰

2. 会话迁移：`$B handoff`/`$B resume`
遇到验证码、MFA 时转交人工处理，完成后恢复 AI 执行

3. 跨代理协同：`/pair-agent`
多 AI 代理共享浏览器，标签隔离、安全可控

### 5.4 安全防护

- 4 层提示注入防御：本地 ML 分类器、Haudi 会话校验、令牌检测

- 紧急开关：`GSTACK\_SECURITY\_OFF=1`关闭安全防护

---

## 六、常见问题与卸载

### 6.1 常见问题

1. 技能不显示：重新执行`cd ~/.claude/skills/gstack && ./setup`

2. `/browse`失败：执行`bun install && bun run build`

3. 版本过时：运行`/gstack-upgrade`或配置`auto\_upgrade: true`

### 6.2 卸载方法

1. 自动卸载：

```bash
~/.claude/skills/gstack/bin/gstack-uninstall
```

2. 手动卸载：
停止进程→删除技能链接→清理全局状态→移除各代理集成→清理临时文件

---

## 七、总结

gstack 的核心价值是"全流程标准化 + AI 自动化"——从 `/office-hours` 需求梳理到 `/ship` 自动发布，每个环节都有专属技能，前后技能自动衔接上下文。建议从 `/autoplan` 一键全流程规划开始体验，感受 AI 虚拟团队的协作能力，再逐步深入各阶段技能的细节配置。
