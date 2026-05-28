---
title: Awesome Claude Skills 使用教程
order: 3
---

# Awesome Claude Skills：一键部署全场景自动化技能

Claude 能生成文本，但你真正想要的是让它替你执行操作——发邮件、改数据库、建工单、发 Slack 消息。Awesome Claude Skills 正是为此而生：由 ComposioHQ 维护的开源精选技能库，封装可直接复用的定制工作流，覆盖文档处理、开发运维、数据分析、商业营销、跨应用自动化等场景，支持在 [Claude.ai](Claude.ai)、Claude Code、Claude API 全平台使用。官方仓库地址：[https://github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

---

## 核心概念：什么是 Claude Skills？

了解技能库之前，先理解 Skills 的运行机制——它决定了你后续如何使用和自定义技能。

Claude Skills 是**可复用、标准化的定制工作流**，通过封装指令、脚本、模板与工具集成，让 Claude 按固定流程完成特定任务，无需重复编写提示词。

核心特性：

- 跨平台兼容：一套技能可在 [Claude.ai](Claude.ai)、Claude Code、API 无缝使用

- 智能触发：支持自动识别任务场景调用，也可手动命令触发

- 轻量化加载：采用渐进式披露机制，仅按需加载内容，节省 Token

- 强拓展性：可集成脚本、第三方 API、1000+ 应用工具

---

## 快速上手：3 种平台一键使用

概念明确后，选择你常用的平台按步骤操作即可启用技能。

### 在 [Claude.ai](Claude.ai) 网页端使用

1. 打开 [Claude.ai](Claude.ai) 对话界面

2. 从技能市场添加 Awesome Claude Skills 中的技能，或上传自定义技能包

3. 发起任务时，Claude 自动匹配并激活对应技能。**实战案例**：若需提取PDF中的表格数据，直接发送”提取这份PDF中的所有表格并整理成Excel格式”，Claude会自动激活pdf技能，完成提取、格式转换，无需额外提示。

### 在 Claude Code 本地使用

1. 克隆技能库

    ```bash
    git clone https://github.com/ComposioHQ/awesome-claude-skills.git
    ```

2. 创建技能目录并复制技能

    ```bash
    mkdir -p ~/.config/claude-code/skills/
    cp -r 技能名称 ~/.config/claude-code/skills/
    ```

3. 验证并启动 Claude Code

    ```bash
    head ~/.config/claude-code/skills/技能名称/SKILL.md
    claude
    ```

4. 技能自动加载，相关任务会自动触发。**实战案例**：克隆仓库后，将”changelog-generator”技能复制到指定目录，启动Claude Code后，输入”根据当前Git仓库的提交记录，生成一份用户可看懂的更新日志”，Claude会自动调用该技能，分析commit信息并生成简洁易懂的 changelog，无需手动编写格式。

### 通过 Claude API 调用

```python
import anthropic
client = anthropic.Anthropic(api_key=”你的API密钥”)

response = client.messages.create(
    model=”claude-3-5-sonnet-20241022”,
    skills=[“postgres”], # 填入Awesome Claude Skills中的技能标识（此处以postgres为例）
    messages=[{“role”: “user”, “content”: “查询postgres数据库中user表的近7天新增用户数量，返回简洁结果”}]
)
```

---

## 核心技能分类：场景化快速选用

技能安装完成后，按场景选用是关键。以下 9 大类覆盖绝大多数办公与开发需求。

Awesome Claude Skills 按场景分为 9 大类，覆盖绝大多数办公与开发需求，每类技能搭配实战案例，帮你快速掌握用法：

|分类|核心技能|功能说明|
|---|---|---|
|**文档处理**|docx/pdf/pptx/xlsx、Markdown 转 EPUB|读写、编辑、格式转换、批注 Office 全格式文档；Markdown 批量转 EPUB；法律文档分类筛选与关键条款提取|
|**开发工具**|artifacts-builder、MCP Builder、Changelog 生成|前端组件构建、MCP 服务开发、Git 提交日志自动化；Chrome Relay 驱动本地浏览器；LangSmith Fetch 追踪代理执行瓶颈|
|**数据分析**|CSV 汇总、PostgreSQL 查询、根因追踪|自动分析 CSV 数据并生成图表；安全查询数据库（排除敏感字段）；执行报错根因定位；多步骤市场调研|
|**商业营销**|品牌规范、竞品广告提取、域名 brainstorm|统一品牌视觉与排版规范；提取竞品广告素材与文案关键词；生成并验证可用域名；潜在客户挖掘与 outreach 策略|
|**创意媒体**|Canvas 设计、图片增强、Slack GIF 生成|视觉设计输出 PNG；图片清晰度与锐度优化；制作平台适配动图；YouTube 字幕提取带时间戳笔记|
|**效率办公**|文件整理、发票管理、抽奖工具|智能归类文件并重命名；发票扫描归档生成台账；安全随机抽奖；根据 JD 优化简历|
|**协作管理**|Git 操作、Google 工作区集成|自动化 git add/commit/push 流程；创建谷歌日历事件并发邀请；操作 Outline wiki 创建页面；测试用例失败定位与修复|
|**安全系统**|数字取证、安全删文件、威胁狩猎|文件元数据提取溯源；Sigma 规则威胁检测；可疑文件操作记录追溯；安全删除确保不可恢复|
|**跨应用自动化**|Connect 插件、78 款 SaaS 集成|对接 Gmail/Slack/GitHub/Notion/Zoom/Shopify 等 1000+ 应用，支持 PR 通知、任务同步、会议创建、订单查询等跨平台自动化|

---

## 进阶：用 Composio 实现 1000+ 应用自动化

内置技能之外，通过 Composio Connect 插件可将 Claude 对接真实应用，执行发邮件、建工单、改数据库等操作，而非仅生成文本。

Awesome Claude Skills 核心亮点是**通过 Composio 实现真实应用操作**，而非仅生成文本，支持发邮件、建工单、发消息、改数据库等动作。

### 快速连接 500+ 应用

1. 安装 connect-apps 插件

    ```bash
    claude --plugin-dir ./connect-apps-plugin
    ```

2. 执行初始化配置

    ```bash
    /connect-apps:setup
    ```

3. 粘贴 Composio 免费 API 密钥（platform.composio.dev 获取）

4. 重启 Claude 即可完成授权，测试发送邮件验证。

### 常用 SaaS 自动化覆盖

库中内置 78 款应用预构建流程，无需二次开发：

- 协作：Slack、Notion、Jira、Trello

- 开发：GitHub、GitLab、Vercel、Sentry

- 办公：Gmail、Google Drive、Outlook

- 营销：Mailchimp、HubSpot、Twitter/X

- 数据：Airtable、Google Sheets、PostgreSQL

---

## 自定义：创建专属 Claude Skills

当内置技能不满足需求时，可按标准结构创建专属技能。

### 标准技能结构

```Plain Text
技能名称/
├── SKILL.md       # 必需：元数据+执行指令（YAML 前置 + Markdown 正文）
├── scripts/       # 可选：Python/Bash 辅助脚本
├── templates/     # 可选：文档/代码模板
└── resources/     # 可选：参考文件
```

### 最简技能模板

```markdown
---
name: 文本翻译技能
description: 用于将中文文本翻译成英文、日文，支持批量翻译，保留原文格式，适用于文档、邮件翻译场景
---
# 文本翻译技能
## 使用场景
- 单个句子、段落的快速翻译
- 批量翻译Word、TXT文档中的中文内容
- 邮件正文翻译，保留邮件格式
- 网页文章提取后翻译（搭配article-extractor技能）

## 执行指令
1. 接收用户输入的中文文本或文档（支持docx、txt格式）
2. 确认用户需要翻译的目标语言（默认英文，可指定日文）
3. 翻译过程中保留原文的标点、段落格式，不添加额外内容
4. 翻译完成后，返回翻译结果，若为文档则生成新的翻译后文档
5. 若用户提供网页链接，先调用article-extractor技能提取文本，再进行翻译

## 示例
用户输入：“Awesome Claude Skills 是一款高效的AI技能工具，可帮助用户提升工作效率。”
技能执行：自动识别中文内容，默认翻译成英文，返回结果：“Awesome Claude Skills is an efficient AI skill tool that can help users improve work efficiency.”
用户输入：“请翻译附件中的中文文档，目标语言为日文”，上传docx文档，技能自动翻译并生成日文版docx文档。
用户输入：“提取这个网页的文章内容，翻译成英文：https://example.com/article”，技能先提取网页文本，再完成翻译，保留原文段落结构。
```

### 开发最佳实践

- 聚焦**单一重复任务**，避免大而全

- 描述包含**触发关键词**，提升自动匹配率

- 补充边界情况与错误处理

- 跨 [Claude.ai/Claude](Claude.ai/Claude) Code/API 三端测试

- 记录依赖与前置条件

---

## 常见问题

6. **跨应用授权失败？**
核对 Composio API 密钥，重启 Claude 并重试配置。**实战案例1**：授权Slack自动化时失败，检查Composio API密钥是否正确（从platform.composio.dev获取），若密钥无误，关闭Claude终端，重新执行claude命令启动，再次执行/connect-apps:setup重新授权，一般可解决问题；
**实战案例2**：授权GitHub Automation技能失败，提示”API密钥无效”，登录platform.composio.dev重新生成密钥，替换旧密钥后，重启Claude并重新授权，授权成功。

7. **技能跨平台不生效？**
移除平台专属脚本，遵循通用技能规范。**实战案例1**：在Claude.ai中可正常使用的技能，在Claude Code中不生效，检查技能的scripts文件夹中是否包含仅适用于网页端的脚本，删除平台专属脚本，保留通用指令，重新加载技能即可跨平台使用；
**实战案例2**：video-downloader技能在Claude Code中可正常使用，在Claude.ai中无法触发，检查发现技能包含本地脚本，删除本地脚本，补充网页端可执行的下载指令，重新上传后，Claude.ai可正常触发。

8. **技能不自动触发？**
检查 [SKILL.md](SKILL.md) 描述是否包含清晰触发关键词，确保文件路径正确。**实战案例1**：若changelog-generator技能不触发，检查SKILL.md中是否包含”changelog””更新日志””commit记录”等关键词，若缺失可补充，同时确认技能文件夹已正确复制到~/.config/claude-code/skills/目录下，重启Claude Code即可；
**实战案例2**：若twitter-algorithm-optimizer技能不触发，输入”优化这条推文提升曝光率”，未触发技能，检查SKILL.md发现未包含”推文优化””曝光率”等关键词，补充后重新加载，再次输入即可触发。

---

## 总结

Awesome Claude Skills 把复杂工作流封装为即用型技能，搭配 Composio 跨应用能力，让 Claude 从文本生成工具升级为**可执行、可复用、可定制**的生产力工具。建议从文档处理或开发工具类技能入手体验单技能能力，再通过 Composio Connect 解锁跨应用自动化。
