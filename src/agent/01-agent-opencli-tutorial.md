---
title: OpenCLI AI 统一命令行自动化工具教程
order: 1
---

# OpenCLI AI 统一命令行自动化工具教程

你想用 AI 智能体自动操作小红书、B站、知乎等网站，却发现每次都要手动处理登录、验证码、Cookie？OpenCLI 正是为解决这些痛点而生——它将网站、浏览器会话、Electron 应用与本地工具转化为确定性 CLI 接口，复用浏览器登录状态，让人类与 AI 智能体用相同方式操控任意平台，零 Token 运行成本，90+ 内置适配器开箱即用。

---

## 一、核心特性

- **AI 智能体原生**：内置适配 Claude、Cursor 等 AI 编码助手的技能，自然语言即可驱动浏览器操作、编写适配器。

- **账号安全**：直接复用 Chrome/Chromium 登录状态，凭证不会离开浏览器环境。

- **零 LLM 运行成本**：运行时不消耗 Token，可无限次执行。

- **确定性输出**：相同命令固定输出结构，支持管道、脚本与 CI 集成。

- **全场景覆盖**：内置 90+ 平台适配器、支持 Electron 桌面应用控制、可对接任意本地 CLI。

- **开箱即用**：无需复杂配置，安装后直接调用主流平台（B 站、小红书、知乎、GitHub 等）指令。

---

## 二、环境准备

- 运行环境：**Node.js ≥ 21.0.0** 或 **Bun ≥ 1.0**

- 浏览器：Chrome/Chromium（需提前登录目标网站，复用登录态）

- 可选：yt-dlp（用于 B 站等视频下载）

---

## 三、快速安装与初始化

### 1. 全局安装 OpenCLI

```bash
npm install -g @jackwener/opencli
```

### 2. 安装浏览器桥接扩展

OpenCLI 通过轻量扩展与本地守护进程连接浏览器，两种安装方式：

- **推荐**：Chrome 应用商店安装 **OpenCLI Browser Bridge**

- **手动**：从 GitHub Releases 下载扩展压缩包 → 开启 Chrome 开发者模式 → 加载已解压扩展

### 3. 环境校验

```bash
# 自动检测扩展连接、依赖、环境配置
opencli doctor
```

### 4. 查看可用命令

```bash
# 列出所有内置平台与指令
opencli list
```

---

## 四、基础使用（人类用户）

环境就绪后，直接调用内置适配器即可上手，无需编写代码。

直接调用内置适配器，无需编写代码：

```bash
# 查看 HackerNews Top5 内容
opencli hackernews top --limit 5

# 查看 B 站热榜（JSON 格式输出）
opencli bilibili hot --limit 5 -f json

# 导出知乎文章为 Markdown
opencli zhihu download "https://zhuanlan.zhihu.com/p/xxx" --download-images

# 下载小红书笔记媒体文件
opencli xiaohongshu download "笔记链接" --output ./xhs
```

支持输出格式：`table`\(默认\)、`json`、`yaml`、`md`、`csv`，适配数据导出与二次处理。

---

## 五、AI 智能体深度集成

基础使用覆盖人类操作场景，而 OpenCLI 的核心设计目标是 AI 智能体——搭配 Claude Code/Cursor 可实现自然语言操控浏览器、自动生成适配器、修复失效指令。

OpenCLI 专为 AI 智能体设计，搭配 Claude Code/Cursor 可实现**自然语言操控浏览器、自动生成适配器、修复失效指令**，全程无需手动写代码。

### 1. 安装 AI 技能

```bash
# 安装全部 OpenCLI 技能
npx skills add jackwener/opencli

# 按需安装单个技能
npx skills add jackwener/opencli --skill opencli-adapter-author
npx skills add jackwener/opencli --skill opencli-autofix
npx skills add jackwener/opencli --skill opencli-browser
```

### 2. 核心技能说明

|技能|适用场景|示例提示词|
|---|---|---|
|opencli-adapter-author|实时操作网站 / 编写新适配器|帮我查看小红书通知 / 写一个抖音热榜适配器|
|opencli-autofix|修复失效的内置指令|opencli zhihu hot 返回空，帮我修复|
|opencli-browser|浏览器自动化底层操作|用浏览器命令抓取页面内容|
|opencli-usage|命令速查|OpenCLI 支持 Twitter 的哪些命令|

### 3. Claude 实战案例（可直接复制）

#### 案例 1：AI 自动操控小红书查看通知

1. 打开 Claude Code，确保已安装技能

2. 输入提示词：

```text
用 OpenCLI 帮我打开小红书，查看我的未读通知，提取标题和时间，以表格输出
```

3. Claude 自动执行底层指令：

```bash
opencli browser open https://xiaohongshu.com
opencli browser click 通知按钮
opencli browser extract 通知列表
```

4. 直接获取结构化结果，无需手动操作浏览器。

#### 案例 2：AI 自动编写抖音热榜适配器

1. 提示词：

```text
帮我为抖音写一个热榜适配器，获取前10条热榜内容，包含标题、链接、点赞数，验证并输出可用的 CLI 命令
```

2. Claude 完成全流程：

- 站点探测与接口分析

- 认证策略配置（复用浏览器登录态）

- 适配器代码生成

- 执行 `opencli browser verify` 校验

- 输出可用命令：`opencli douyin trending --limit 10`

#### 案例 3：AI 修复失效指令

当内置指令因网页改版失效时：

1. 提示词：

```text
opencli zhihu hot 命令返回空数据，帮我定位问题并修复适配器
```

2. Claude 自动排查：网络拦截、字段解析、选择器更新，输出修复后的适配器代码。

---

## 六、核心能力详解

AI 集成之外，OpenCLI 还提供浏览器自动化、自定义适配器开发、CLI 统一枢纽、桌面应用控制等核心能力。

### 1. AI 驱动浏览器自动化

智能体通过 `opencli browser` 底层原语操作浏览器，支持：

- 导航、点击、输入、截图、滚动、标签页管理

- 等待元素、提取结构化数据、拦截网络请求

- 全程复用登录态，无验证码 / 登录繁琐流程

### 2. 自定义适配器开发

无内置适配器的平台，AI 可一键生成：

```bash
# 初始化适配器脚手架
opencli browser init 站点名/指令名
# 编写后校验
opencli browser verify 站点名/指令名
```

适配器存储于 `~/.opencli/clis/`，可复用与分享。

### 3. CLI 统一枢纽

对接任意本地 CLI，统一发现与执行：

```bash
# 注册本地工具
opencli register mycli
# 调用 GitHub CLI
opencli gh pr list --limit 5
# 调用 Docker
opencli docker ps
```

### 4. Electron 桌面应用控制

直接操控 Cursor、ChatGPT、Notion 等桌面应用：

```bash
# 控制 Notion 搜索页面
opencli notion search query="AI 自动化"
# 向 Cursor 发送指令
opencli cursor send "分析项目代码"
```

### 5. 批量下载能力

支持多平台媒体 / 内容导出：

```bash
# B 站视频下载（需 yt-dlp）
opencli bilibili download BV1xxx --output ./videos
# Twitter 用户媒体下载
opencli twitter download elonmusk --limit 20 --output ./twitter
```

---

## 七、OpenCLI vs 传统自动化

|维度|OpenCLI|传统爬虫 / Playwright|
|---|---|---|
|登录处理|复用浏览器登录态|手动处理 Cookie / 验证码|
|AI 适配|原生支持智能体操控|需额外封装接口|
|开发成本|AI 自动生成适配器|手动编写定位与逻辑|
|运行成本|零 Token 消耗|需调用 LLM 解析|
|确定性|固定输出结构|易受页面结构影响|

---

## 八、常见问题与排查

1. **扩展未连接**：确认扩展已启用，重启 Chrome 或执行 `opencli doctor`

2. **无数据 / 权限错误**：Chrome 中重新登录目标网站，复用最新登录态

3. **视频下载失败**：安装 yt-dlp（`brew install yt-dlp`）

4. **Node 版本报错**：升级至 Node ≥21 或使用 Bun

5. **指令失效**：用 `opencli-autofix` 技能让 AI 自动修复

---

## 九、总结

OpenCLI 的核心价值是"CLI 统一接口 + 浏览器登录态复用 + AI 原生适配"——以命令行作为人类与 AI 的共同操作入口，依托浏览器登录态免去验证码与 Cookie 烦恼，通过 AI 技能实现自动生成适配器与修复失效指令。建议从内置适配器（如 `opencli bilibili hot`）体验基础能力，再安装 AI 技能（`npx skills add jackwener/opencli`）解锁自然语言操控与自动适配器开发。
