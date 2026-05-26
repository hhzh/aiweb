---
title: Hermes 代理技能使用教程
order: 16
---

# Hermes 代理技能使用教程

Hermes Agent 技能（Skills）是**可复用的标准化工作流与知识单元**，遵循 `agentskills.io` 开放标准，支持按需加载、自动触发、跨会话复用，是智能体扩展能力的核心机制。本文从技能核心概念、格式规范、安装管理、自定义开发、高级特性五方面，带你全面掌握技能使用，快速扩展智能体专属能力。

## 一、技能核心概念

### 1.1 什么是技能

技能是封装**特定任务流程、知识文档、工具调用逻辑**的可复用模块，以 `SKILL.md` 为核心文件，包含触发条件、操作步骤、依赖工具、注意事项等内容。智能体可根据用户指令**自动匹配并加载对应技能**，无需重复编写逻辑，实现 "一次开发、处处复用"。

### 1.2 核心价值

- ✅ **标准化复用**：遵循开放标准，支持跨项目 / 跨实例共享

- ✅ **渐进加载**：三级加载机制，最小化 Token 消耗

- ✅ **自动触发**：匹配指令自动加载，无需手动调用

- ✅ **生态丰富**：官方 + 社区海量技能，覆盖开发、研究、办公等场景

- ✅ **动态扩展**：支持自定义开发、在线安装、自动更新

### 1.3 技能存储结构

所有技能默认存储在 `~/.hermes/skills/` 目录，按分类组织：

```Plain Text
~/.hermes/skills/
├── productivity/       # 生产力类技能
│   └── research/       # 深度研究技能
│       ├── SKILL.md    # 技能核心文件（必填）
│       ├── references/ # 参考文档
│       └── templates/  # 输出模板
├── development/        # 开发类技能
└── .hub/               # 技能仓库缓存
```

## 二、技能格式规范（\[SKILL.md\](SKILL.md)）

每个技能必须包含 `SKILL.md`，采用 **YAML 前置元数据 + Markdown 正文** 格式，定义技能属性与执行逻辑。

### 2.1 完整格式示例

```markdown
---
name: go-code-review          # 技能唯一名称（必填）
description: Go代码审查技能，专注性能与安全检查  # 简短描述（必填）
version: 1.0.0                 # 语义化版本（必填）
platforms: [macos, linux]      # 支持平台（可选）
metadata:
  tags: [golang, code-review] # 分类标签
  category: development         # 技能分类
  requires_toolsets: [terminal, file] # 依赖工具集
---

## 适用场景
当需要审查Go代码、排查性能问题、检查安全漏洞时使用。

## 操作步骤
1. 读取目标Go文件
2. 检查错误处理（不忽略error）
3. 分析并发安全（goroutine/互斥锁）
4. 评估内存分配性能
5. 生成结构化审查报告

## 注意事项
- 区分必须修复的高危问题与优化建议
- 遵循Go官方编码规范
- 重点检查并发场景数据竞争
```

### 2.2 关键字段说明

|字段|类型|说明|
|---|---|---|
|`name`|字符串|技能唯一标识，命令调用 / 匹配依据|
|`description`|字符串|简短描述，L0 加载时展示|
|`version`|字符串|语义化版本，用于更新管理|
|`platforms`|数组|限制运行平台（macos/linux/windows）|
|`metadata.tags`|数组|搜索 / 匹配标签，用于模糊查找|
|`requires_toolsets`|数组|依赖工具集，不满足则隐藏技能|

### 2.3 渐进加载机制

技能采用**三级加载**，平衡功能完整性与 Token 消耗：

- **L0（列表级）**：仅加载名称、描述、标签（≈3k Token），会话启动时加载

- **L1（内容级）**：匹配指令后，加载完整 `SKILL.md`

- **L2（资源级）**：需引用文档时，加载 `references/` 等辅助文件

## 三、技能安装与管理

Hermes 支持**官方 / 社区 / GitHub 等多来源安装**，提供完整命令行工具管理技能。

### 3.1 常用管理命令

```bash
# 1. 浏览技能仓库（官方+社区）
hermes skills browse

# 2. 搜索技能（按名称/标签）
hermes skills search go

# 3. 安装技能（官方）
hermes skills install official/go-code-review

# 4. 从GitHub安装
hermes skills install github:xxx/go-code-review

# 5. 查看技能详情
hermes skills show go-code-review

# 6. 列出已安装技能
hermes skills list

# 7. 更新技能
hermes skills update go-code-review

# 8. 卸载技能
hermes skills uninstall go-code-review
```

### 3.2 技能来源与信任级别

支持**7 大官方来源**，采用分级信任机制保障安全：

- `official`：官方内置，最高信任

- `skills-sh`：Vercel 公共技能库

- `github`：GitHub 仓库直接安装

- `clawhub`：社区技能市场

### 3.3 安全扫描机制

所有第三方技能安装前**自动安全扫描**，检测注入、恶意命令等风险：

- 危险项：直接拦截

- 警告项：需 `--force` 强制安装

- 官方技能：免扫描

## 四、技能使用方法

### 4.1 触发方式（3 种）

#### （1）斜杠命令（精准调用）

```bash
# 格式：/技能名称 参数
/go-code-review 审查~/api/main.go
```

#### （2）自然语言匹配（自动触发）

直接对话，智能体自动匹配技能：

```Plain Text
帮我审查这个Go文件：~/api/main.go
```

#### （3）预加载技能（会话生效）

```bash
# 启动时预加载
hermes chat -s go-code-review
```

### 4.2 条件激活（按需显示）

技能支持**条件显示**，根据工具可用性自动隐藏 / 显示：

```yaml
metadata:
  fallback_for_toolsets: [web] # 无web工具时显示
  requires_toolsets: [terminal] # 有terminal工具时显示
```

### 4.3 外部技能目录

支持挂载**共享技能目录**，复用团队 / 公共技能：

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/team-skills # 团队共享目录
    - /opt/public-skills # 公共目录
```

## 五、自定义技能开发

### 5.1 快速创建

```bash
# 生成技能目录与基础文件
hermes skills create my-python-review
```

### 5.2 编写逻辑

编辑 `~/hermes/skills/development/my-python-review/SKILL.md`，定义场景、步骤、注意事项。

### 5.3 测试技能

```bash
# 本地调用测试
/hermes chat -s my-python-review
/ my-python-review 审查~/app.py
```

### 5.4 发布共享

```bash
# 发布到GitHub
hermes skills publish my-python-review --repo xxx/skills
```

## 六、高级特性

### 6.1 Agent 自动生成

智能体完成 **5 + 步复杂任务**后，自动提炼工作流为技能：

- 任务成功后：保存流程为新技能

- 任务失败后：记录避坑方案

- 用户纠正后：优化技能逻辑

### 6.2 技能配置

支持自定义配置，存储在 `config.yaml`：

```yaml
metadata:
  config:
    max_files: 10 # 自定义参数
```

### 6.3 版本管理

```bash
# 查看版本
hermes skills show go-code-review --version

# 升级版本
hermes skills update go-code-review
```

## 七、最佳实践

1. **规范命名**：技能名小写 + 连字符（如 `python-lint`）

2. **精简描述**：描述≤50 字，清晰说明用途

3. **依赖校验**：合理配置 `requires_toolsets`，避免依赖缺失

4. **版本迭代**：重大更新升级版本，兼容旧版

5. **安全优先**：第三方技能先扫描，危险项不强制安装

6. **分类管理**：按 `development/productivity` 分类，便于检索

## 总结

Hermes 技能系统以**标准化、轻量化、生态化**为核心，通过简单的 `SKILL.md` 即可封装复杂工作，支持多来源安装、自动触发、动态扩展。无论是官方技能开箱即用，还是自定义开发专属能力，都能快速提升智能体实用性，是扩展 Hermes 能力的核心入口。
