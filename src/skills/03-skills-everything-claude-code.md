---
title: Everything Claude Code 安装指南
order: 3
---

# Everything Claude Code 安装指南：一键部署 AI 编程全能力

还在为 Claude Code 配置繁琐、功能单一而困扰？Everything Claude Code（简称 ECC）给出了完美解决方案——作为 Anthropic 黑客马拉松获奖项目，它是一套经 10 个月实战迭代打磨的生产级 AI 编程配置系统，无需复杂调试，一键解锁超强能力：内置 **47 个专项子智能体**、**181 个可复用技能模块**、**79 个快捷命令**，覆盖技能体系、记忆持久化、持续学习、安全扫描全场景，兼容 Claude Code、Cursor、OpenCode、Gemini 等主流 AI 编程工具，让你的 AI 编程效率翻倍。

本文将手把手教你完成环境准备、快速安装、核心解析与进阶优化，轻松部署ECC，解锁AI编程的全量潜力。官网地址：[https://github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

---

## 前置环境要求

- Claude Code CLI ≥ **v2.1.0**（执行 `claude --version` 查看）

- 已安装 Git、Node.js（用于脚本与依赖管理）

- 支持 Windows/macOS/Linux 全平台

---

## 2 分钟快速上手（推荐插件安装）

### 步骤 1：安装 ECC 插件

```bash

# 添加 ECC 插件市场
/plugin marketplace add affaan-m/everything-claude-code
# 安装 ECC 核心插件
/plugin install ecc@ecc
```

💡 说明：复制整段命令，在Claude Code终端中逐行执行，执行完成后即可完成插件主体安装。

### 步骤 2：安装规则（必需，上游限制无法自动分发）

规则是编码规范、工作流约束的核心，必须手动安装。

#### macOS/Linux

```bash

# 克隆仓库（若克隆失败，可直接下载仓库压缩包解压后进入目录）
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
# 安装依赖（任选包管理器，npm/pnpm/yarn/bun均可）
npm install
# 完整安装所有规则（推荐新手）
./install.sh --profile full
# 或仅安装指定语言（如 TS/Python/Go，按需选择）
./install.sh typescript python golang
```

💡 说明：复制整段命令，在终端中逐行执行；克隆失败解决方案：打开ECC官网（[https://github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)），点击「Code」→「Download ZIP」，解压后进入解压目录，再执行后续命令。

✅ 验证安装：执行 `ls ~/.claude/rules`，若能看到common及所选语言目录，说明规则安装成功。

#### Windows（PowerShell）

```powershell

# 克隆仓库（若克隆失败，可直接下载仓库压缩包解压后进入目录）
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code
npm install
# 完整安装所有规则（推荐新手）
.\install.ps1 --profile full
# 或仅安装指定语言（如 TS/Python/Go，按需选择）
.\install.ps1 typescript python golang
```

💡 说明：复制整段命令，在PowerShell中逐行执行；克隆失败解决方案：打开ECC官网（[https://github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)），点击「Code」→「Download ZIP」，解压后进入解压目录，再执行后续命令。

✅ 验证安装：执行 `Get-ChildItem ~/.claude/rules`，若能看到common及所选语言目录，说明规则安装成功。

### 步骤 3：开始使用

```bash

# 插件安装用命名空间命令（需求描述可自定义，如"实现登录接口"）
/ecc:plan "添加用户认证模块"
# 查看全部可用命令（了解ECC所有功能）
/plugin list ecc@ecc
```

💡 说明：执行第一条命令可快速生成需求的实现方案，第二条命令可查看所有79个快捷命令的详细说明。

安装完成即可使用 **47 个代理、181 个技能、79 个命令**。

### 步骤 4：multi-* 命令额外配置

`/multi-plan`/`multi-execute` 等多智能体编排命令需额外运行时：

```bash

npx ccg-workflow
```

💡 说明：安装完成后，/multi-plan、/multi-execute等多智能体编排命令即可正常使用，用于复杂任务的拆解与协同执行。

---

## 手动安装（精细化控制）

适合需要自定义组件的场景，逐模块复制配置：

```bash

# 克隆仓库（克隆失败可下载压缩包解压）
git clone https://github.com/affaan-m/everything-claude-code.git
# 复制代理（47个专项子智能体，按需复制）
cp everything-claude-code/agents/*.md ~/.claude/agents/
# 复制规则（通用+语言专属，保证路径完整）
mkdir -p ~/.claude/rules
cp -r everything-claude-code/rules/common ~/.claude/rules/
cp -r everything-claude-code/rules/typescript ~/.claude/rules/
# 复制技能（181个可复用技能模块，核心技能必复制）
cp -r everything-claude-code/skills/* ~/.claude/skills/
# 复制兼容命令（79个快捷命令，保留传统斜杠命令支持）
mkdir -p ~/.claude/commands
cp everything-claude-code/commands/*.md ~/.claude/commands/
```

💡 说明：适合有自定义需求的用户，可选择性复制组件（如仅复制核心技能和常用代理），避免冗余。

⚠️ 手动安装需将 `hooks/hooks.json` 配置合并到 `~/.claude/settings.json`，插件安装则无需操作，避免重复加载。

---

## 核心模块全解析

ECC 由六大核心组件构成，协同打造完整 AI 编程工作流。

|组件|核心作用|典型内容|通俗解读|
|---|---|---|---|
|**Agents（子智能体）**|按角色分工处理专项任务|架构师、代码审查、安全审计、构建错误修复、TDD 指导等 47+ 专用代理|相当于专属开发小助手，各司其职，无需手动分配任务|
|**Skills（技能）**|封装可复用工作流与领域知识|前后端模式、TDD 流程、安全扫描、持续学习、框架最佳实践（Django/SpringBoot/Laravel）181+|提前封装好的开发模板，直接调用，不用重复写流程|
|**Commands（命令）**|斜杠快捷指令||

---

## 进阶配置优化

### 包管理器自定义

ECC 自动检测 npm/pnpm/yarn/bun，可手动指定优先级：

```bash
# 环境变量指定
export CLAUDE_PACKAGE_MANAGER=pnpm
# 全局配置
node scripts/setup-package-manager.js --global pnpm
# 项目级配置
node scripts/setup-package-manager.js --project bun
```

### 钩子运行时控制

```bash
# 设置严格度（standard/strict/off）
export ECC_HOOK_PROFILE=standard
# 禁用指定钩子
export ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"
```

### 上下文窗口管理（关键）

- 单次启用 MCP 不超过 **10 个**，总工具数＜80

- 用 `disabledMcpServers` 关闭未使用服务，避免上下文从 200k 压缩至 70k

- 优先保留核心 MCP，按需启用

---

## 生态工具：效率与安全加倍

### 技能创建器：从项目生成专属能力

```bash
# 本地分析 Git 历史生成技能
/skill-create
# 生成直觉用于持续学习
/skill-create --instincts
```

### AgentShield 安全审计

黑客松获奖安全工具，1282 项测试、98% 覆盖率，检测配置漏洞与注入风险：

```bash
# 快速扫描
npx ecc-agentshield scan
# 自动修复
npx ecc-agentshield scan --fix
# Claude 内直接使用
/security-scan
```

### 持续学习 v2

自动从会话提取开发模式，支持直觉导入 / 导出 / 聚类：

```bash
/instinct-status  # 查看学习状态
/instinct-export  # 导出直觉
/evolve           # 聚类为技能
```

---

## 常用实战命令速查

|命令|功能|
|---|---|
|`/ecc:plan "需求描述"`|生成功能实现方案|
|`/code-review`|代码质量与安全审查|
|`/build-fix`|自动修复构建错误|
|`/tdd`|启动测试驱动开发流程|
|`/security-scan`|执行安全审计|
|`/multi-plan`|多智能体任务拆解|
|`/sessions`|会话历史管理|

---

## 常见问题避坑

1. **钩子重复加载错误**
不在 `.claude-plugin/plugin.json` 中添加 `hooks` 字段，Claude Code v2.1+ 自动加载 `hooks/hooks.json`。

2. **规则不生效**
复制整个语言目录（如 `rules/common`），而非单个文件，保证路径引用正常。

3. **multi- 命令报错**
未安装 `ccg-workflow` 运行时，执行 `npx ccg-workflow` 修复。

4. **MCP 冲突**
用 `ECC_DISABLED_MCPS` 环境变量禁用重复服务。

---

## 总结

Everything Claude Code 不是简单的配置合集，而是一套**生产级 AI 编程工作流系统**，通过角色化智能体、标准化技能、自动化钩子与强制规则，大幅提升 Claude Code 等工具的工程化能力，适配全语种、全框架开发场景。

建议先按插件方式快速安装，再根据技术栈定制规则与技能，结合 AgentShield 与持续学习能力，打造专属的 AI 辅助开发体系。

