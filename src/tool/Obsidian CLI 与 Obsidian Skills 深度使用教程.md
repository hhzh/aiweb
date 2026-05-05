# Obsidian CLI 与 Obsidian Skills 深度使用教程

**项目地址**：[https://github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)

obsidian-skills 是**Obsidian 官方适配**的 AI 智能体专用技能库，完美兼容 Claude Code、Codex CLI、OpenCode 等主流 AI 工具，让智能体精准理解并操作 Obsidian 的专有语法、画布、数据库与命令行。相比通用提示词，它能让 AI 以原生方式读写笔记、管理知识库、开发插件，是搭建 AI 驱动本地知识库的核心工具。

本文从安装、核心技能、**obsidian-cli 深度使用**到实战全流程讲解，帮你打通 AI 与 Obsidian 的无缝协作。

---

## 一、项目核心概览

obsidian-skills 遵循 Agent Skills 规范，提供 5 项 Obsidian 专属能力，开箱即用：

- obsidian-markdown：支持双链、标注、前置元数据、嵌入等 Obsidian 扩展语法

- obsidian-bases：读写 Obsidian 数据库文件（.base）

- json-canvas：创建与编辑 JSON Canvas 可视化画布

- **obsidian-cli**：通过命令行操控 Obsidian，支持笔记管理、插件开发、知识库操作

- defuddle：网页内容提纯，生成干净 Markdown

---

## 二、3 种安装方式

### 方式 1：插件市场（最简）

```bash
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### 方式 2：npx skills（跨工具通用）

```bash
npx skills add git@github.com:kepano/obsidian-skills.git
```

### 方式 3：手动安装（分工具）

1. **Claude Code**
克隆到 Obsidian 仓库根目录的 `.claude` 文件夹

```bash
git clone https://github.com/kepano/obsidian-skills.git /你的仓库路径/.claude
```

2. **Codex CLI**
复制 skills 目录到 Codix 技能路径

```bash
cp -r skills ~/.codex/skills
```

3. **OpenCode**
完整克隆到技能目录（勿只复制内层 skills）

```bash
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

---

## 三、核心技能速览

|技能|核心用途|
|---|---|
|obsidian-markdown|编写 Obsidian 专属 Markdown，支持双链、标注、元数据|
|obsidian-bases|创建 / 编辑 Obsidian 数据库视图、筛选、公式|
|json-canvas|生成 / 修改 JSON Canvas 可视化节点与连线|
|**obsidian-cli**|**命令行操控 Obsidian，插件开发、批量笔记管理**|
|defuddle|网页去噪，输出精简 Markdown 节约 Token|

---

## 四、重点：obsidian-cli 技能全解（核心）

obsidian-cli 是 obsidian-skills 的**能力核心**，让 AI 智能体通过命令行直接与 Obsidian 交互，无需打开 GUI，实现自动化、批量化操作。

### 4.1 前置准备

1. 升级 Obsidian 到 **v1.12+**

2. 开启 CLI：`设置 → 通用 → Command line interface → Register`

3. 终端验证：`obsidian --version` 显示版本即为成功

### 4.2 核心能力

1. 笔记批量创建 / 修改 / 查询

2. 插件与主题开发、编译、调试

3. 知识库检索、反向链接查询、元数据读写

4. 与 AI 智能体联动实现本地 RAG（检索增强生成）

### 4.3 AI 智能体常用调用指令

```bash
# 新建笔记（指定仓库、标题、内容）
obsidian new "笔记标题" --content "笔记内容" --vault "仓库名"

# 搜索笔记（返回结构化数据）
obsidian search "关键词" --vault "仓库名" --json

# 查看反向链接
obsidian backlinks "目标笔记" --vault "仓库名"

# 打开指定笔记
obsidian open "笔记名称" --vault "仓库名"
```

### 4.4 插件开发专属指令

```bash
# 初始化插件项目
obsidian plugin init "插件名"

# 编译插件
obsidian plugin build

# 调试插件
obsidian plugin dev
```

### 4.5 AI 调用规范

在 Claude Code / OpenCode 中直接触发：

```Plain Text
使用 obsidian-cli 技能，在我的「Knowledge」仓库中搜索「AI 知识库」并返回所有笔记，生成总结
```

智能体会自动调用对应 CLI 命令，完成检索→分析→输出全流程。

---

## 五、配套核心技能：obsidian-markdown（必学）

配合 CLI 使用，让 AI 生成标准 Obsidian 笔记：

### 5.1 核心语法

1. **双链（内部链接）**
`[[笔记名]]`、`[[笔记名#标题]]`、`[[笔记名\|显示文本]]`

2. **嵌入内容**
`\![[嵌入笔记]]`、`\![[图片.png\|宽度]]`

3. **标注（Callout）**

```Plain Text
> [!note] 提示
> 标注内容
```

4. **前置元数据**

```yaml
---
title: 笔记标题
date: 2026-05-01
tags: [AI, Obsidian]
---
```

### 5.2 AI 生成示例

```Plain Text
使用 obsidian-markdown 技能，创建一篇关于 obsidian-cli 的教程笔记，包含前置元数据、标注、双链和代码块
```

---

## 六、实战案例（AI+obsidian-cli 落地）

### 案例 1：AI 自动维护知识库

1. AI 调用 `obsidian search` 检索指定主题笔记

2. 智能分析内容、提取要点

3. 调用 `obsidian new` 生成汇总笔记并添加双链

4. 定期自动更新，无需手动整理

### 案例 2：AI 辅助 Obsidian 插件开发

1. 调用 `obsidian plugin init` 初始化插件项目

2. AI 编写插件核心代码

3. 调用 `obsidian plugin dev` 实时调试

4. 自动生成插件说明文档

### 案例 3：本地 RAG 问答（无云端依赖）

1. 用户提问 → AI 调用 `obsidian search` 精准检索笔记

2. AI 读取笔记内容并理解语义

3. 生成答案并标注来源笔记，全程本地运行、数据安全

---

## 七、常见问题

1. **CLI 命令不生效**
检查 Obsidian 版本≥v1.12，确认已在设置中注册 CLI 环境变量

2. **AI 无法调用技能**
确认技能已安装到对应 AI 工具的技能目录，重启 AI 工具

3. **生成的笔记语法错误**
强制 AI 使用 `obsidian-markdown` 技能，遵循 Obsidian 专有规范

---

## 八、总结

obsidian-skills 是 AI 智能体操控 Obsidian 的**官方级桥梁**，而 **obsidian-cli** 则是这套工具的**能力中枢**。它让 AI 从 “只能读写文本” 升级为 “原生管理 Obsidian 知识库”，搭配批量操作、插件开发、本地 RAG 等能力，彻底解放笔记管理与知识沉淀的效率。

无论是个人知识库自动化、插件开发，还是企业级本地知识问答，obsidian-skills 都能让 AI 与 Obsidian 的协作效率提升 10 倍以上，是知识工作者与开发者的必备工具。

