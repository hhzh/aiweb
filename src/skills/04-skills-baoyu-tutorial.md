---
title: baoyu-skills 完整使用教程
order: 4
---

# baoyu-skills 完整使用教程

想把一段文字变成小红书卡片、信息图、PPT 幻灯片甚至漫画？baoyu-skills 是专为 Claude Code 打造的开源效率技能集，聚焦内容创作、AI 生成与实用工具三大场景，支持将文本快速转化为多媒体内容，也支持一键发布至社交媒体与格式转换。

---

## 前置准备

使用 baoyu-skills 需先满足以下基础环境：

1. 已安装 **Node.js** 环境

2. 可正常执行 `npx bun` 命令

确认环境就绪后，即可开始安装。

---

## 安装与更新

环境就绪后，以下三种方式任选其一完成安装。

### 快速安装（推荐）

打开终端，执行一键安装命令：

```bash
npx skills add jimliu/baoyu-skills
```

### 注册为 Claude Code 插件市场

在 Claude Code 中直接运行命令，将仓库添加到插件市场：

```bash
/plugin marketplace add JimLiu/baoyu-skills
```

### 三种安装技能方式

#### 方式 1：界面可视化安装

1. Claude Code 中选择 **Browse and install plugins**

2. 找到 `baoyu-skills` 并选择

3. 点击 **Install now** 完成安装

#### 方式 2：命令行直接安装

```bash
# 安装完整技能集
/plugin install baoyu-skills@baoyu-skills
```

#### 方式 3：Agent 智能安装

直接告知 Claude Code：

```Plain Text
Please install Skills from github.com/JimLiu/baoyu-skills
```

### 技能更新

1. Claude Code 中运行 `/plugin`

2. 切换到 **Marketplaces** 标签页

3. 选择 `baoyu-skills` → **Update marketplace**

4. 可开启 **auto-update** 自动同步最新版本

---

## 核心技能分类与实战用法

安装完成后，按场景选用技能。baoyu-skills 分为三大类，共 20+ 细分技能。

baoyu-skills 分为三大类，共 20+ 细分技能，覆盖全场景效率需求。

### 内容创作技能（Content Skills）

专注内容生成、可视化与发布，是自媒体、办公、知识分享的核心工具。

#### 1）baoyu-xhs-images：小红书图片卡片生成

将文本拆解为 1-10 张卡通风格卡片，支持风格、布局、调色板自定义。

```bash
# 自动匹配风格与布局
/baoyu-xhs-images posts/ai-future/article.md
# 指定风格+布局+调色板
/baoyu-xhs-images posts/ai-future/article.md --style notion --layout list --palette macaron
# 直接输入文本生成
/baoyu-xhs-images 今日星座运势
```

- 风格：cute、fresh、warm、notion、chalkboard 等 11 种

- 布局：sparse、balanced、dense、list、comparison、flow

#### 2）baoyu-infographic：专业信息图生成

支持 21 种布局 + 17 种视觉风格，自动分析内容推荐组合，输出可发布级信息图。

```bash
# 自动推荐组合
/baoyu-infographic path/to/content.md
# 指定布局+风格+比例
/baoyu-infographic path/to/content.md --layout funnel --style corporate-memphis --aspect 16:9
```

#### 3）baoyu-diagram：SVG 架构图 / 流程图生成

直接编写 SVG 代码，支持深色模式自适应，无需调用图像模型。

```bash
# 自动分析生成 JWT 认证流程图
/baoyu-diagram "how JWT authentication works" --type flowchart --lang zh
# 生成微服务架构图
/baoyu-diagram "微服务架构" --type structural --out docs/micro-service.svg
```

#### 4）baoyu-slide-deck：PPT 幻灯片生成

自动生成大纲并输出幻灯片图片，合并为 PPTX/PDF，支持 16 种风格预设。

```bash
# 从 Markdown 生成商务风 PPT，15 页
/baoyu-slide-deck path/to/article.md --style corporate --slides 15
# 仅生成大纲，不生成图片
/baoyu-slide-deck path/to/article.md --outline-only
```

#### 5）baoyu-comic：知识漫画生成

支持漫画风格、色调、分镜自定义，把干货文本转为可视化漫画。

```bash
# 自动选择风格生成
/baoyu-comic posts/turing-story/source.md
# 指定漫画风格+色调+布局
/baoyu-comic posts/turing-story/source.md --art manga --tone warm --layout cinematic
```

#### 6）其他内容技能

- **baoyu-cover-image**：文章封面图生成，支持 5 维自定义

- **baoyu-article-illustrator**：文章自动配图，识别插图位置并生成

- **baoyu-post-to-wechat**：一键发布至微信公众号，支持图文 / 文章模式

- **baoyu-post-to-weibo**：发布微博 / 头条文章，支持图文、视频

- **baoyu-post-to-x**：发布至 X（Twitter），支持长文

### AI 生成技能（AI Generation Skills）

内容创作之外，AI 图像生成技能提供统一的文生图入口，集成多家服务商。

集成多家主流 AI 图像生成接口，统一调用入口，支持文生图、参考图、批量生成。

#### baoyu-imagine：多平台 AI 图像生成

支持 OpenAI、Azure、Google、通义万象、MiniMax、豆包 Seedream 等服务商。

```bash
# 基础文生图（自动选择服务商）
/baoyu-imagine --prompt "一只可爱的猫" --image cat.png
# 指定阿里云通义万象+自定义尺寸
/baoyu-imagine --prompt "科技风海报" --image banner.png --provider dashscope --size 2048x872
# 使用豆包 Seedream 生成
/baoyu-imagine --prompt "工作室肖像" --image portrait.png --provider seedream --ar 3:2
```

### 实用工具技能（Utility Skills）

创作和生成之外，日常办公中的格式转换、内容抓取等琐碎任务也有对应技能。

专注格式转换、内容抓取、效率优化，解决日常办公琐碎问题。

1. **baoyu-youtube-transcript**：下载 YouTube 字幕与封面，支持多语言翻译

2. **baoyu-url-to-markdown**：网页转纯净 Markdown，支持动态页面

3. **baoyu-danger-x-to-markdown**：X（Twitter）推文 / 长文转 Markdown

4. **baoyu-compress-image**：图片压缩，保持画质同时减小体积

5. **baoyu-format-markdown**：Markdown 格式化，自动优化标题、列表、代码块

6. **baoyu-markdown-to-html**：Markdown 转微信适配 HTML

7. **baoyu-translate**：多模式翻译，支持快速 / 标准 / 精修三种精度

---

## API 密钥环境配置

AI 生成与社交媒体发布技能需要配置对应平台的 API 密钥，支持用户级与项目级两种配置方式。

部分 AI 生成与发布技能需配置对应平台 API 密钥，支持**用户级**与**项目级**配置。

### 创建配置目录

```bash
# 用户级配置（全局生效）
mkdir -p ~/.baoyu-skills
# 项目级配置（仅当前项目生效）
mkdir -p .baoyu-skills
```

### 编写 .env 配置文件

在配置目录下创建 `.env` 文件，填入对应密钥：

```env
# OpenAI
OPENAI_API_KEY=sk-xxx
# Azure OpenAI
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_BASE_URL=https://your-resource.openai.azure.com
# 阿里云通义万象
DASHSCOPE_API_KEY=sk-xxx
# 豆包 Seedream
ARK_API_KEY=xxx
# MiniMax
MINIMAX_API_KEY=xxx
```

配置优先级：CLI 环境变量 > 项目级 .env > 用户级 .env。

---

## 个性化自定义

默认参数不满足需求时，可通过 EXTEND.md 自定义样式、配色与预设。

所有技能支持通过 `EXTEND.md` 自定义样式、配色、预设，满足品牌化需求。

### 创建扩展文件

```bash
# 项目级自定义
mkdir -p .baoyu-skills/baoyu-cover-image
touch .baoyu-skills/baoyu-cover-image/EXTEND.md
```

### 自定义示例（封面图调色板）

```markdown
## Custom Palettes
### corporate-tech
- Primary colors: #1a73e8, #4A90D9
- Background: #F5F7FA
- Accent colors: #00B4D8, #48CAE4
- Best for: SaaS, enterprise, technical
```

技能执行时会自动加载扩展配置，覆盖默认参数。

---

## 使用小贴士

1. 安装后重启 Claude Code，技能加载更稳定

2. 复杂场景可组合技能使用：如网页转 Markdown → 生成信息图 → 发布公众号

3. 批量生成时用 `--yes` 参数跳过确认，适合定时任务

4. 社交媒体发布优先配置 API 模式，速度更快更稳定

---

## 总结

baoyu-skills 把 Claude Code 从纯文本对话工具升级为多媒体内容创作平台，尤其适合中文场景的自媒体运营、知识科普、商务演示。建议从 `/baoyu-xhs-images` 或 `/baoyu-infographic` 入手体验内容创作能力，再按需配置 AI 生成与社交媒体发布技能。

项目地址：[https://github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)
