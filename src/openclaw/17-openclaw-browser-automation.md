---
title: OpenClaw 浏览器自动化操作手册
order: 17
---

# OpenClaw 浏览器自动化操作手册

OpenClaw Browser 是专为智能体打造的**隔离式浏览器自动化引擎**，基于 Chromium 生态，提供托管隔离、扩展中继、远程 CDP、节点代理四种运行模式，支持标签页管控、网页交互、AI 快照、截图/PDF、环境模拟、登录持久化全能力，且全程与个人浏览器环境物理隔离，是智能体实现"看得见、点得准、可登录、能自治"的网页操作核心工具。本文基于官方文档，完整覆盖配置、CLI、智能体调用、多环境适配、登录安全、沙箱兼容与故障排查，提供一站式可落地操作手册。

## 一、核心定位与设计理念

### 1.1 核心价值

OpenClaw Browser 不是日常浏览工具，而是**智能体专属安全浏览器**：

- **完全隔离**：独立用户数据目录，不读取、不污染个人浏览器配置与登录态
- **确定性控制**：基于 ref 定位元素，不依赖脆弱 CSS 选择器
- **多模式兼容**：本地托管、复用现有浏览器、远程节点、云端托管全覆盖
- **智能体友好**：AI 快照输出结构化页面，支持点击/输入/上传/下载全交互
- **安全可控**：仅回环接口访问，支持沙箱隔离、权限白名单、令牌安全管理

### 1.2 两大基础配置文件（必知）

OpenClaw 默认提供两套配置，开箱即用：

1. **openclaw**：托管隔离配置（橙色主题），独立实例，推荐自动化使用
2. **chrome**：扩展中继配置，复用系统现有 Chrome，需安装扩展

## 二、四大运行模式全覆盖

### 2.1 托管模式（推荐，最安全）

- 独立 Chromium 实例，独立用户数据目录，完全隔离
- 无需扩展，无需手动登录干预
- 默认端口 18800，橙色主题标识
- 适合智能体全自动自动化、登录态持久化、敏感操作

### 2.2 扩展中继模式

- 复用本机已安装的 Chrome/Brave/Edge
- 通过 OpenClaw Browser Relay 扩展接管标签页
- 适合调试、快速验证、无需独立浏览器场景
- 限制：无法跨设备，需手动点击扩展附加标签

### 2.3 远程 CDP 模式

- 连接远端 Chromium 实例（局域网/云端）
- 支持 `cdpUrl` 配置，支持令牌/基础认证
- 适合分布式网关、无图形化服务器场景

### 2.4 节点代理模式（零配置）

- 节点主机自动暴露本地浏览器能力
- Gateway 自动路由操作，无需额外配置
- 适合网关在服务器、浏览器在本地设备的场景

## 三、全局配置详解（openclaw.json）

浏览器配置位于 `~/.openclaw/openclaw.json`，完整配置与说明如下：

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "color": "#FF4500",
    "headless": false,
    "noSandbox": false,
    "attachOnly": false,
    "executablePath": "",
    "remoteCdpTimeoutMs": 1500,
    "remoteCdpHandshakeTimeoutMs": 3000,
    "profiles": {
      "openclaw": { "cdpPort": 18800, "color": "#FF4500" },
      "work": { "cdpPort": 18801, "color": "#0066CC" },
      "remote": { "cdpUrl": "http://10.0.0.42:9222", "color": "#00AA00" },
      "browserless": { "cdpUrl": "https://production-sfo.browserless.io?token=TOKEN", "color": "#00AA00" }
    }
  }
}
```

### 3.1 核心配置项说明

- `enabled`：是否启用浏览器工具，默认 true
- `defaultProfile`：默认配置文件，推荐设为 `openclaw`
- `headless`：无头模式（无界面），服务器环境必开
- `noSandbox`：禁用浏览器沙箱，Linux/WSL 环境常用
- `attachOnly`：仅附加不启动，适合手动启动浏览器场景
- `executablePath`：指定浏览器可执行文件路径，覆盖自动检测
- `profiles`：多配置文件定义，支持本地端口、远程 CDP 两种类型

### 3.2 浏览器自动检测顺序

系统自动寻找第一个可用的 Chromium 浏览器：

Chrome → Brave → Edge → Chromium → Chrome Canary

## 四、CLI 全命令实操（从基础到高级）

所有命令支持 `--browser-profile <name>` 指定配置文件，`--json` 输出结构化数据。

### 4.1 基础管控命令

```bash
# 查看浏览器状态
openclaw browser status
# 启动浏览器（默认 openclaw 配置）
openclaw browser start
# 停止浏览器
openclaw browser stop
# 指定配置文件启动
openclaw browser --browser-profile work start
```

### 4.2 标签页管理命令

```bash
# 列出所有标签页
openclaw browser tabs
# 新建标签页
openclaw browser tab new
# 切换到第2个标签页
openclaw browser tab select 2
# 关闭指定标签页（ID/序号）
openclaw browser close 123
openclaw browser tab close 2
# 打开URL并聚焦
openclaw browser open https://example.com
openclaw browser focus abcd1234
```

### 4.3 页面快照与截图（智能体核心能力）

快照是 Browser 工具的**灵魂**，输出结构化页面元素，提供稳定 ref 用于交互。

```bash
# AI 快照（默认，数字ref，如1/2/3）
openclaw browser snapshot
# 交互角色快照（e开头ref，如e12，推荐操作使用）
openclaw browser snapshot --interactive
# 精简高效快照（低token）
openclaw browser snapshot --efficient
# 指定CSS选择器/iframe快照
openclaw browser snapshot --selector "#main"
openclaw browser snapshot --frame "iframe#main"
# 带截图标注的快照
openclaw browser snapshot --labels

# 截图（当前视图）
openclaw browser screenshot
# 整页截图
openclaw browser screenshot --full-page
# 导出PDF
openclaw browser pdf
```

### 4.4 网页交互命令（基于 ref）

**所有操作必须使用快照返回的 ref**，不支持 CSS 选择器，保证稳定。

```bash
# 点击元素（数字ref/角色ref）
openclaw browser click 12
openclaw browser click e12
# 双击
openclaw browser click e12 --double

# 输入文本并提交
openclaw browser type 23 "内容"
openclaw browser type 23 "内容" --submit

# 键盘按键
openclaw browser press Enter
openclaw browser press "Ctrl+A"

# 悬停/拖拽/下拉选择
openclaw browser hover 44
openclaw browser drag 10 11
openclaw browser select 9 选项1 选项2

# 等待元素/文本/URL/加载状态
openclaw browser wait --text "完成"
openclaw browser wait "#main" --url "**/dash" --load networkidle
```

### 4.5 文件上传与下载

```bash
# 预备文件上传（先执行，再点击上传按钮）
openclaw browser upload /path/file.pdf
# 直接设置文件输入框
openclaw browser upload /path/file.pdf --input-ref 23

# 下载文件
openclaw browser download e12 /tmp/report.pdf
# 等待下载完成
openclaw browser waitfordownload /tmp/report.pdf
```

### 4.6 环境模拟命令

```bash
# 设置Cookie
openclaw browser cookies set session token --url "https://example.com"
# 清空Cookie
openclaw browser cookies clear

# 模拟地理位置
openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"
# 暗黑模式
openclaw browser set media dark
# 设置时区/语言
openclaw browser set timezone Asia/Shanghai
openclaw browser set locale zh-CN
# 模拟手机设备
openclaw browser set device "iPhone 14"
# 自定义视口
openclaw browser resize 1280 720
```

### 4.7 调试与日志命令

```bash
# 查看控制台错误
openclaw browser console --level error
# 查看网络请求
openclaw browser requests --filter api
# 清空错误/请求日志
openclaw browser errors --clear
openclaw browser requests --clear

# 录制操作轨迹（调试用）
openclaw browser trace start
openclaw browser trace stop

# 高亮元素（定位目标）
openclaw browser highlight e12
```

## 五、智能体 browser 工具集成

智能体通过 `browser` 工具实现全自动化网页操作，参数与 CLI 完全对齐。

### 5.1 工具核心参数

- `profile`：指定配置文件（openclaw/work/remote）
- `target`：运行目标（sandbox/host/node）
- `action`：动作（status/tabs/open/snapshot/act 等）
- `ref`：元素引用（来自快照）
- `url`：网页地址

### 5.2 典型工具调用

```json
{
  "tool": "browser",
  "params": {
    "profile": "openclaw",
    "action": "snapshot",
    "format": "interactive"
  }
}
```

### 5.3 target 运行目标（沙箱关键）

- `host`：主机浏览器（默认非沙箱）
- `sandbox`：沙箱浏览器（默认沙箱会话）
- `node`：节点主机浏览器

沙箱会话使用主机浏览器需开启配置：

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "browser": { "allowHostControl": true }
      }
    }
  }
}
```

## 六、多配置文件管理

OpenClaw 支持无限多配置文件，按场景隔离环境（工作/个人/远程）。

### 6.1 配置文件类型

1. **本地托管**：`cdpPort` 指定端口，独立数据目录
2. **远程 CDP**：`cdpUrl` 指定远端地址
3. **扩展中继**：`driver: extension`，复用本地标签

### 6.2 创建自定义配置文件

```bash
openclaw browser create-profile \
  --name my-profile \
  --driver local \
  --cdp-port 18802 \
  --color "#00FF00"
```

### 6.3 Browserless 云端托管集成

适合无本地浏览器的服务器，完全云端运行：

```json
{
  "browser": {
    "defaultProfile": "browserless",
    "profiles": {
      "browserless": {
        "cdpUrl": "https://production-sfo.browserless.io?token=你的令牌"
      }
    }
  }
}
```

## 七、登录安全与账号保护（核心规范）

### 7.1 手动登录最佳实践（强制）

**严禁将账号密码提供给模型**，避免触发反机器人与账号风控：

```bash
# 启动托管浏览器
openclaw browser start
# 打开目标网站
openclaw browser open https://x.com
# 手动登录，登录态持久保存
```

登录后会话永久保留，后续智能体可直接使用。

### 7.2 反机器人规避

- 沙箱会话易触发风控，敏感平台（X/Twitter）优先用主机浏览器
- 避免全自动高频操作，搭配人工验证环节
- 优先使用官方 CLI / 技能（如 bird CLI）替代浏览器操作

### 7.3 登录态隔离

不同配置文件登录态完全隔离，工作/个人账号互不干扰。

## 八、沙箱会话兼容

沙箱是 OpenClaw 安全核心，浏览器工具默认适配沙箱：

- 沙箱会话 → 默认使用 `target=sandbox` 隔离浏览器
- 需要访问主机浏览器 → 开启 `allowHostControl: true`
- 生产环境公共智能体 → 强制沙箱浏览器，禁止主机访问

## 九、Playwright 依赖说明

Browser 工具高级功能依赖 Playwright：

- 必需功能：AI 快照、点击/输入、PDF、元素截图
- 安装命令（服务器环境）：

```bash
# 标准安装
npx playwright install chromium
# Docker 安装
docker compose run --rm openclaw-cli \
  node /app/node_modules/playwright-core/cli.js install chromium
```

缺失 Playwright 会返回 501 错误，仅保留基础截图能力。

## 十、全平台适配与故障排查

### 10.1 各平台配置

- **macOS**：自动检测 `/Applications` 下的 Chromium 浏览器
- **Windows**：检测默认安装路径，路径使用双反斜杠
- **Linux**：推荐安装官方 Chrome，规避 Snap 限制

### 10.2 Linux Snap Chromium 报错修复

**问题**：Failed to start Chrome CDP on port 18800

**原因**：Snap AppArmor 限制干扰进程管理

**解决方案**：

1. 安装官方 Chrome deb 包（推荐）

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

2. 配置 `executablePath` + `noSandbox: true`

```json
{
  "browser": {
    "executablePath": "/usr/bin/google-chrome-stable",
    "noSandbox": true,
    "headless": true
  }
}
```

### 10.3 扩展中继无标签连接修复

**问题**：extension relay running but no tab connected

**解决方案**：

1. 安装扩展：`openclaw browser extension install`
2. Chrome 开启开发者模式，加载已解压扩展
3. 点击目标标签页的扩展图标，显示 ON 即附加成功

### 10.4 远程 CDP 连接失败

- 检查网络互通、端口开放
- 确认 `cdpUrl` 正确，包含认证信息
- 调整超时：`remoteCdpTimeoutMs` 设为 2000

## 十一、安全最佳实践

1. **隔离优先**：自动化始终使用 `openclaw` 托管配置，不混用个人浏览器
2. **令牌安全**：远程 CDP/Browserless 令牌使用环境变量，不硬编码配置
3. **最小权限**：公共智能体强制沙箱浏览器，禁用主机访问
4. **登录规范**：手动登录，禁止模型输入密码
5. **网络隔离**：Gateway / 节点仅部署在私有网络，不暴露公网
6. **定期清理**：清理过期 Cookie、无用配置文件，避免信息泄露

## 十二、总结

OpenClaw Browser 工具以**隔离安全、确定性操作、多模式兼容、智能体友好**为核心，彻底解决 AI 智能体网页交互"不可靠、不安全、不可控"的痛点。从本地轻量调试到云端分布式自动化，从简单信息获取到复杂表单登录，均可通过标准化配置与命令实现。遵循隔离、安全、手动登录三大原则，即可搭建稳定、安全、可持续的智能体网页自动化能力，是 OpenClaw 从"对话助手"升级为"网页执行助手"的核心基础设施。
