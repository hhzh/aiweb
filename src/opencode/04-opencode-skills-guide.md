---
title: OpenCode Skills 使用教程
order: 4
---

# OpenCode Skills 使用教程

在 AI 辅助编程中，你是否反复输入同样的提示词？OpenCode 代理技能（Skills）正是为解决这一问题而生。开发者可以将高频工作流程、编码规范、专项操作指令等内容封装为独立技能文件，代理通过内置 `skill` 工具按需加载，无需重复编写提示词，有效统一团队开发流程。

技能体系支持**项目级**与**全局级**两种部署模式，同时兼容 Claude Code、传统 Agents 目录格式，对于跨工具迁移的用户十分友好。本文将系统讲解技能文件的存放规则、编写规范、调用方式、权限管控、功能禁用以及故障排查，并搭配实战案例，帮助开发者搭建可复用的技能体系。

## 一、代理技能核心概述

代理技能以 `SKILL.md` 作为核心载体，遵循**一个技能对应独立文件夹**的规则。OpenCode 会自动扫描指定目录下的技能文件，代理在执行任务时可主动发现并按需加载技能内容。

### 核心价值

1. **指令复用**：将通用提示词、操作流程封装为技能，告别重复输入；

2. **流程标准化**：团队统一技能内容，保证所有成员使用一致的开发规范；

3. **按需加载**：技能不会常驻会话上下文，仅在需要时加载，降低资源消耗；

4. **多端兼容**：原生目录兼容 Claude Code、旧版 Agents 目录，迁移无成本。

## 二、技能文件存放路径与检索规则

OpenCode 会按照固定路径扫描技能文件，分为**项目级**（仅当前项目生效）和**全局级**（本机所有项目生效），同时区分原生路径与兼容路径。所有路径均要求：**每个技能单独创建文件夹，文件夹名称与技能名称保持一致**，文件夹内放置 `SKILL.md` 文件。

### 2.1 全路径清单

|类型|分类|目录路径|生效范围|
|---|---|---|---|
|项目级|OpenCode 原生|`.opencode/skills/<技能名>/SKILL.md`|当前 Git 仓库项目|
|项目级|Claude 兼容|`.claude/skills/<技能名>/SKILL.md`|当前 Git 仓库项目|
|项目级|旧代理兼容|`.agents/skills/<技能名>/SKILL.md`|当前 Git 仓库项目|
|全局级|OpenCode 原生|`~/.config/opencode/skills/<技能名>/SKILL.md`|本机所有项目|
|全局级|Claude 兼容|`~/.claude/skills/<技能名>/SKILL.md`|本机所有项目|
|全局级|旧代理兼容|`~/.agents/skills/<技能名>/SKILL.md`|本机所有项目|

### 2.2 目录检索逻辑

1. **项目级技能检索**：OpenCode 从当前工作目录开始，向上遍历至 Git 仓库根目录，沿途加载所有合法技能；超出 Git 仓库范围后停止检索。

2. **全局级技能检索**：固定扫描全局目录，本机任意 OpenCode 会话均可加载全局技能。

3. **优先级**：项目级技能优先级高于全局级技能，同名技能会以项目内版本为准。

## 三、\[SKILL.md\]\(SKILL.md\) 编写规范

`SKILL.md` 文件由 **YAML Frontmatter（头部元数据）** 和 **正文指令内容** 两部分组成。OpenCode 仅识别规定的 Frontmatter 字段，未知字段会自动忽略。

### 3.1 Frontmatter 字段说明

#### 3.1.1 必填字段

1. `name`：技能名称，有严格格式约束：

    - 长度限制：1 ~ 64 个字符；

    - 字符规则：仅支持小写字母、数字，可使用单个连字符分隔；

    - 格式要求：不能以连字符开头、结尾，不允许连续连字符；

    - 绑定规则：必须和技能所在文件夹名称完全一致；

    - 校验正则：`^[a-z0-9]+(-[a-z0-9]+)*$`。

2. `description`：技能描述，长度限制 1 ~ 1024 字符。描述内容需精准具体，便于代理判断调用时机。

#### 3.1.2 可选字段

1. `license`：技能开源协议，例如 `MIT`、`Apache-2.0`；

2. `compatibility`：兼容工具标识，例如 `opencode`、`claude`；

3. `metadata`：自定义元数据，采用字符串键值对格式，可标注使用人群、工作流等附加信息。

### 3.2 完整编写示例

示例文件路径：`.opencode/skills/git-release/SKILL.md`

```markdown
---
name: git-release
description: 基于合并的PR生成更新日志，建议版本号并提供gh发布命令
license: MIT
compatibility: opencode
metadata:
  audience: 项目维护者
  workflow: github
---
## 技能使用场景
当需要对代码仓库进行版本打标、正式发布时使用本技能。若版本规则不明确，请主动向用户确认。

## 执行步骤
1. 读取近期合并的 PR 记录，自动整理版本更新日志；
2. 根据迭代内容，给出合理的版本号升级建议；
3. 生成可直接复制执行的 gh release 发布命令。
```

### 3.3 正文编写建议

1. 明确使用场景：标注技能适用的业务与操作场景；

2. 拆解执行步骤：按顺序划分操作流程，引导代理分步执行；

3. 补充约束规则：添加异常处理、交互要求等限制条件。

## 四、技能调用机制

### 4.1 技能自动发现

OpenCode 启动后会自动扫描所有合法目录，汇总全部可用技能。技能的名称与描述会被整合到 `skill` 工具的内置描述中，格式示例如下：

```xml
<available_skills>
  <skill>
    <name>git-release</name>
    <description>基于合并的PR生成更新日志，建议版本号并提供gh发布命令</description>
  </skill>
</available_skills>
```

### 4.2 代理调用语法

代理识别需求后，会通过标准语法调用指定技能：

```javascript
skill({ name: "git-release" })
```

调用分为两种形式：代理根据需求**自动调用**，或接收用户指令后**间接触发**。

## 五、技能全局权限配置

通过项目根目录 `opencode.json` 文件的 `skill` 节点，可统一管控全代理的技能访问权限，支持精准匹配与通配符匹配。

### 5.1 权限动作说明

|权限值|执行行为|
|---|---|
|`allow`|直接加载技能，无需人工审批|
|`deny`|对代理隐藏该技能，完全禁止访问|
|`ask`|加载前弹出审批窗口，确认后方可使用|

### 5.2 全局权限配置示例

配置支持 `*` 通配符批量管理技能，遵循**后匹配规则优先**原则：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

配置解读：默认放行所有技能；单独允许代码评审技能；禁止所有内部技能；所有实验类技能使用前需人工审批。

## 六、按代理单独覆写技能权限

当不同代理需要差异化权限时，可单独配置代理专属规则，代理权限优先级高于全局权限。分为自定义代理、内置代理两种配置方式。

### 6.1 自定义代理配置

在自定义代理的 `.md` 配置文件 Frontmatter 中设置技能权限，文件路径参考 `~/.config/opencode/agents/`：

```markdown
---
description: 代码评审专用子代理
mode: subagent
permission:
  skill:
    "documents-*": "allow"
---
# 代理指令正文
专注代码评审工作，优先使用文档类技能。
```

### 6.2 内置代理配置

在 `opencode.json` 的 `agent` 节点中，为官方内置代理配置权限：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

## 七、完全禁用技能功能

对于纯检索、纯分析类专用代理，可直接关闭 `skill` 工具。禁用后，技能列表会从工具描述中移除。

### 7.1 自定义代理禁用配置

```markdown
---
description: 代码检索只读代理
mode: subagent
tools:
  skill: false
---
# 代理指令正文
仅负责检索代码，不使用任何技能。
```

### 7.2 内置代理禁用配置

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

## 八、常见问题排查

1. 技能无法展示时，首先检查文件名：技能主文件必须为大写 `SKILL.md`，大小写错误会导致系统无法识别。

2. 校验 Frontmatter 完整性：`name` 和 `description` 为必填字段，缺失任意一个都会造成技能加载失败。

3. 保证技能名称唯一：同一检索范围内，所有技能名称不能重复，名称冲突会引发加载异常。

4. 排查权限拦截：若技能被 `deny` 规则匹配，会对代理完全隐藏，需核对全局权限、代理专属权限配置。

5. 检查目录结构：禁止将 `SKILL.md` 直接放在 `skills` 根目录，必须遵循「独立文件夹 + 内部 \[SKILL.md\]\(SKILL.md\)」的结构。

6. 确认检索范围：项目级技能仅在当前 Git 仓库内生效，切换仓库后无法读取原有项目技能。

## 九、实战技能案例

### 案例 1：项目级代码评审技能

文件路径：`.opencode/skills/code-review/SKILL.md`

```markdown
---
name: code-review
description: 对代码进行规范检查、漏洞扫描并输出评审报告
license: MIT
---
## 代码评审规则
1. 检查代码是否符合项目 ESLint + Prettier 规范；
2. 排查接口权限、参数校验、依赖引入等安全漏洞；
3. 分析代码性能问题，给出优化建议；
4. 仅输出评审结果，不自动修改代码。
```

### 案例 2：全局单元测试编写技能

文件路径：`~/.config/opencode/skills/unit-test/SKILL.md`

```markdown
---
name: unit-test
description: 基于现有代码编写标准单元测试
compatibility: opencode
---
## 执行要求
1. 分析目标函数的入参、出参与业务逻辑；
2. 覆盖正常、边界、异常三类测试场景；
3. 使用项目默认测试框架编写代码，并补充注释。
```

### 案例 3：Git 提交规范技能

文件路径：`.opencode/skills/git-commit/SKILL.md`

```markdown
---
name: git-commit
description: 按照约定式提交规范生成 commit 信息
---
## 提交规范
提交格式：<类型>(<模块>): 描述
类型包含：feat、fix、docs、style、refactor、test、chore。
根据代码改动内容，生成合规的 Git 提交文案。
```

## 十、总结

OpenCode Skills 以 `SKILL.md` 为核心文件，搭配多层目录结构、精细化权限体系，实现指令的模块化复用。项目级技能适配单项目专属流程，全局技能服务多项目通用规范，同时兼容多款主流工具，降低迁移成本。

在实际使用中，务必遵守文件命名、目录结构、Frontmatter 等基础规范，避免技能加载异常；结合权限规则区分不同代理的使用范围，高危技能可设置审批机制提升安全性。针对专用代理，可直接关闭技能功能，精简代理能力边界。

合理运用技能体系，能够大幅减少重复提示词编写工作，统一团队开发标准，充分提升 OpenCode 的使用效率。
