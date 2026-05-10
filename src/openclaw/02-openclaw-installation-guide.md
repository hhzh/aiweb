---
title: OpenClaw 全流程安装·更新·迁移·卸载教程
order: 2
---

# OpenClaw 全流程安装·更新·迁移·卸载教程

OpenClaw 是跨平台 AI 智能体 Gateway 网关，支持 WhatsApp、Telegram、Discord 等多渠道接入。本文基于官方文档，完整覆盖**安装、更新、迁移、卸载**全生命周期操作，适配 macOS/Linux/WSL/Windows 全系统。

## 一、系统要求

- **Node.js**：推荐 24.x，兼容 22.14+ LTS

- **操作系统**：macOS、Linux、Windows（原生 / WSL2，WSL2 更稳定）

- **依赖**：Git（安装脚本自动补装）；源码构建需 pnpm

## 二、安装教程

OpenClaw 提供**5 种安装方式**，优先推荐官方一键脚本，新手零配置快速部署。

### 方式 1：官方一键脚本（推荐，全自动）

自动检测系统、安装 Node、部署 OpenClaw 并启动引导。

- **macOS/Linux/WSL2**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

- **Windows（PowerShell）**

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

- 跳过新手引导：添加 `--no-onboard` 参数

    - macOS/Linux/WSL2：`curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard`

    - Windows：`& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard`

### 方式 2：npm/pnpm/bun 手动安装（已有 Node 环境）

- npm 安装

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

- pnpm 安装（需显式批准构建）

```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

- bun 安装（仅 CLI，网关推荐 Node）

```bash
bun add -g openclaw@latest
openclaw onboard --install-daemon
```

- sharp 构建错误修复：`SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest`

### 方式 3：本地前缀安装（无系统依赖）

将 Node + OpenClaw 统一安装到 `~/.openclaw`，无需 root 权限：

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

### 方式 4：源码安装（开发者 / 定制化）

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm ui:build && pnpm build
pnpm link --global
openclaw onboard --install-daemon
```

### 方式 5：Docker 容器部署（服务器 / 无头环境）

```bash
docker pull openclaw/openclaw:latest
docker run -d -p 18789:18789 -v ~/.openclaw:/root/.openclaw --name openclaw openclaw/openclaw:latest
```

### 安装验证

执行以下命令确认部署成功：

```bash
openclaw --version       # 查看版本
openclaw doctor          # 检查配置
openclaw gateway status  # 验证网关运行状态
```

### 安装故障排除（基础）

**故障：找不到 openclaw**

如果安装成功，但终端中提示"openclaw: command not found"，按以下步骤排查：

- 检查 Node.js 是否正常安装：`node -v`（需显示 22.14+ 版本）

- 查看 npm 全局软件包安装路径：`npm prefix -g`

- 检查全局 bin 目录是否在系统 PATH 中：`echo "$PATH"`

若 `$(npm prefix -g)/bin` 不在你的 $PATH 中，请将其添加到 shell 启动文件（~/.zshrc 或 ~/.bashrc）中，执行以下命令：

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

添加后重启终端，或执行 `source ~/.zshrc`（zsh 终端）、`source ~/.bashrc`（bash 终端）使配置立即生效。

## 三、更新教程

OpenClaw 迭代快速，**优先重新运行安装脚本**实现原地升级，无需重新配置。

### 推荐更新：一键脚本升级

- 全局安装更新

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

- 源码安装更新（添加 git 模式）

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-onboard
```

### 全局安装手动更新

```bash
# npm 更新
npm i -g openclaw@latest
# pnpm 更新
pnpm add -g openclaw@latest

# 更新后检查并重启网关
openclaw doctor
openclaw gateway restart
openclaw health
```

### 源码安装更新

```bash
# 自动更新（推荐）
openclaw update

# 手动更新
git pull
pnpm install && pnpm build && pnpm ui:build
openclaw doctor
openclaw gateway restart
```

### 切换更新渠道

支持 stable/beta/dev 三渠道切换：

```bash
openclaw update --channel stable  # 稳定版
openclaw update --channel beta    # 测试版
openclaw update --channel dev     # 开发版
```

### 版本回滚 / 固定

- 全局安装固定版本

```bash
npm i -g openclaw@指定版本号
openclaw doctor
openclaw gateway restart
```

- 源码安装按日期回滚

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before="2026-01-01" origin/main)"
pnpm install && pnpm build
openclaw gateway restart
```

## 四、迁移教程

无缝迁移到新机器，保留**配置、凭证、会话、工作区**，无需重新配对渠道。

### 迁移内容

- 配置文件：`~/.openclaw/openclaw.json`

- 鉴权凭证：`~/.openclaw/credentials/`、`auth-profiles.json`

- 会话历史、渠道登录状态、工作区文件

### 迁移步骤

1. **旧机器停止网关并备份**

```bash
openclaw gateway stop
cd ~
tar -czf openclaw-state.tgz .openclaw
```

2. **新机器安装 OpenClaw**（执行任意安装方式）

3. **新机器恢复备份**

```bash
cd ~
tar -xzf openclaw-state.tgz
```

4. **验证迁移**

```bash
openclaw doctor
openclaw gateway restart
openclaw status
```

### 迁移注意事项

- 保持新旧机器**profile / 状态目录**一致，否则渠道会登出、会话丢失

- 仅复制 `openclaw.json` 无效，必须迁移整个 `~/.openclaw` 目录

- 备份文件包含敏感凭证，需加密存储

## 五、卸载教程

分 **CLI 可用（简单卸载）** 和 **CLI 已删（手动卸载）** 两种场景，彻底清理服务与数据。

### 方式 1：简单卸载（CLI 正常使用）

```bash
# 一键卸载（清理服务+配置+数据）
openclaw uninstall

# 非交互全自动卸载
openclaw uninstall --all --yes --non-interactive
```

### 方式 2：手动卸载（CLI 已删除）

1. **停止并卸载网关服务**

- macOS（launchd）

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

- Linux（systemd）

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

- Windows（计划任务）

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE.openclaw\gateway.cmd"
```

2. **删除配置与数据**

```bash
rm -rf ~/.openclaw
```

3. **卸载 CLI**

```bash
npm rm -g openclaw
# pnpm：pnpm remove -g openclaw
# bun：bun remove -g openclaw
```

### 源码安装卸载

先执行卸载命令清理服务，再删除源码目录与状态目录：

```bash
openclaw uninstall
rm -rf ~/openclaw  # 源码目录
rm -rf ~/.openclaw # 状态目录
```

## 六、常见故障排除

1. **命令找不到**

    - 检查 Node：`node -v`

    - 查看 npm 全局路径：`npm prefix -g`

    - 添加 PATH：`export PATH="$(npm prefix -g)/bin:$PATH"`（写入 `~/.zshrc`/`~/.bashrc`）

2. **Windows 提示 npm 错误 spawn git**

    - 安装 Git for Windows，重启 PowerShell 后重新安装

3. **sharp/libvips 构建失败**

    - 安装时添加环境变量：`SHARP_IGNORE_GLOBAL_LIBVIPS=1`

4. **网关启动失败**

    - 执行 `openclaw doctor` 自动修复配置

    - 重启网关：`openclaw gateway restart`
