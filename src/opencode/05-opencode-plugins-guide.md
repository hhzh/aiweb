---
title: OpenCode 插件使用教程
order: 5
---

# OpenCode 插件使用教程

## 开篇

OpenCode 插件是扩展平台能力的核心解决方案。开发者可以借助插件监听系统事件、拦截工具执行、注入自定义逻辑、集成外部服务，或是修改 OpenCode 默认行为。插件支持**本地文件**和**NPM 包**两种部署形式，同时拥有庞大的社区生态，提供大量开箱即用的第三方插件。

本文结合官方文档，全面讲解 OpenCode 插件的加载规则、部署方式、依赖管理、开发规范、事件钩子、实战案例，同时整理官方生态插件与第三方项目清单，并梳理使用与开发过程中的注意事项，帮助普通用户快速使用插件，也助力开发者自主编写定制化插件。

## 一、插件核心基础

### 1.1 插件定位

OpenCode 插件基于**事件钩子（Hook）** 机制运行，能够在命令执行、文件编辑、工具调用、会话变更等全生命周期中介入逻辑。它区别于自定义工具、MCP 服务：自定义工具偏向单次功能调用，MCP 偏向外部服务对接，而插件更擅长全局行为拦截、事件监听与流程改造。插件支持 JavaScript、TypeScript 两种主流编写语言。

### 1.2 插件加载顺序

OpenCode 会按照固定优先级依次加载插件与配置，**加载顺序决定了钩子执行顺序**，具体规则如下：

1. 全局配置文件：`~/.config/opencode/opencode.json` 中声明的 NPM 插件

2. 项目配置文件：当前项目 `opencode.json` 中声明的 NPM 插件

3. 全局插件目录：`~/.config/opencode/plugins/` 下的本地插件

4. 项目插件目录：`.opencode/plugins/` 下的本地插件

**重复加载规则**

- 同名同版本的 NPM 包仅会加载一次，避免重复执行；

- 本地插件与名称相似的 NPM 插件相互独立，会分别加载、依次执行。

## 二、插件加载方式

OpenCode 提供两种主流插件加载方案：本地文件加载（适合自定义私有插件）、NPM 包加载（适合社区开源插件），可根据使用场景灵活选择。

### 2.1 本地文件加载

将 JS/TS 插件文件放入指定目录，OpenCode 启动时会自动扫描并加载，无需额外配置。分为**项目级插件**和**全局插件**：

1. **项目级插件**
仅对当前项目生效，目录：`.opencode/plugins/`
适用场景：项目专属定制逻辑、团队内部私有插件。

2. **全局插件**
对本机所有 OpenCode 会话生效，目录：`~/.config/opencode/plugins/`
适用场景：个人通用配置、全设备共享插件。

> 示例：在项目中创建本地插件文件
> 目录结构：
> 
> ```Plain Text
> 你的项目/
> └── .opencode/
>     └── plugins/
>         └── my-plugin.js  # 本地插件文件
> ```
> 
> 

### 2.2 NPM 包加载

社区开源插件可直接通过 NPM 包形式引入，只需在项目 / 全局 `opencode.json` 中声明包名即可。

#### 2.2.1 配置语法

在 `opencode.json` 的 `plugin` 数组中填写 NPM 包名，支持普通包与作用域包：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "opencode-wakatime",
    "opencode-helicone-session",
    "@my-org/custom-plugin"
  ]
}
```

#### 2.2.2 安装与缓存规则

- OpenCode 启动时会自动使用 Bun 下载并安装声明的 NPM 插件；

- 插件及依赖会统一缓存到 `~/.cache/opencode/node_modules/` 目录，下次启动直接复用缓存，提升加载速度。

## 三、插件依赖管理

本地插件如果需要引用第三方 NPM 包（如工具库、SDK），不能直接导入，需要在对应目录创建 `package.json` 管理依赖。

### 3.1 配置步骤

1. 在插件所在目录（项目级：`.opencode/`、全局：`~/.config/opencode/`）新建 `package.json`；

2. 在 `dependencies` 字段声明所需依赖；

3. OpenCode 启动时自动执行 `bun install` 安装依赖。

### 3.2 示例配置

以引入 `shescape` 命令转义库为例：

1. 依赖配置文件（`.opencode/package.json`）

```json
{
  "dependencies": {
    "shescape": "^2.1.0"
  }
}
```

2. 插件中导入依赖并使用（`.opencode/plugins/shell-escape.ts`）

```typescript
import { escape } from "shescape"

export const ShellEscapePlugin = async (ctx) => {
  return {
    "tool.execute.before": async (input, output) => {
      // 转义 bash 命令，防止注入风险
      if (input.tool === "bash") {
        output.args.command = escape(output.args.command)
      }
    },
  }
}
```

## 四、插件开发详解

### 4.1 基础代码结构

插件本质是一个异步 JS/TS 模块，导出异步插件函数，函数接收**上下文对象**，最终返回钩子集合。

#### 4.1.1 JavaScript 基础模板

```javascript
// .opencode/plugins/example.js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  console.log("插件初始化完成");
  // 在此处编写各类事件钩子
  return {};
};
```

#### 4.1.2 上下文参数说明

插件函数的上下文内置多个核心对象，覆盖项目、终端、SDK 等能力：

|参数|作用|
|---|---|
|`project`|当前项目基础信息|
|`directory`|Open 运行的工作目录|
|`worktree`|Git 工作树根路径|
|`client`|OpenCode SDK 客户端，用于日志、AI 交互|
|`$`|Bun Shell API，可直接执行终端命令|

### 4.2 TypeScript 类型支持

官方提供专用类型包 `@opencode-ai/plugin`，可实现完整类型校验与代码提示：

```typescript
// .opencode/plugins/example.ts
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  // 类型安全的钩子逻辑
  return {};
};
```

### 4.3 全量事件钩子列表

插件可订阅 OpenCode 全生命周期事件，按功能分类整理如下，所有钩子均可在插件中监听使用：

1. **命令事件**

    - `command.executed`：终端 / TUI 命令执行后触发

2. **文件事件**

    - `file.edited`：文件被编辑时触发

    - `file.watcher.updated`：文件监听器检测到文件变更时触发

3. **安装事件**

    - `installation.updated`：插件 / 依赖安装更新时触发

4. **LSP 事件**

    - `lsp.client.diagnostics`：LSP 诊断信息更新

    - `lsp.updated`：LSP 服务状态变更

5. **消息事件**

    - `message.part.removed` / `message.part.updated`：消息片段删除 / 更新

    - `message.removed` / `message.updated`：整条消息删除 / 更新

6. **权限事件**

    - `permission.asked`：触发权限审批弹窗

    - `permission.replied`：用户完成权限选择

7. **服务器事件**

    - `server.connected`：服务连接成功

8. **会话事件**

    - `session.created` / `session.deleted`：会话创建 / 删除

    - `session.compacted`：会话上下文压缩

    - `session.diff`：会话内容差异变更

    - `session.error` / `session.idle`：会话报错 / 空闲

    - `session.status` / `session.updated`：会话状态 / 内容更新

9. **待办事件**

    - `todo.updated`：待办列表变更

10. **Shell 事件**

    - `shell.env`：Shell 环境变量加载时触发

11. **工具事件**

    - `tool.execute.before`：工具执行**前置钩子**（拦截修改参数）

    - `tool.execute.after`：工具执行**后置钩子**（处理返回结果）

12. **TUI 事件**

    - `tui.prompt.append`：输入框追加内容

    - `tui.command.execute`：TUI 斜杠命令执行

    - `tui.toast.show`：TUI 弹出提示消息

13. **实验性事件**

    - `experimental.session.compacting`：会话压缩自定义钩子

## 五、实战插件案例

本节提供官方原生插件案例，覆盖通知、安全防护、环境注入、自定义工具、会话压缩等高频场景，所有代码均可直接部署使用。

### 案例 1：系统桌面通知插件（macOS）

监听会话空闲事件，通过系统弹窗发送通知：

```javascript
// .opencode/plugins/notification.js
export const NotificationPlugin = async ({ $ }) => {
  return {
    event: async ({ event }) => {
      // 会话进入空闲状态时触发通知
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "会话执行完成！" with title "OpenCode"'`;
      }
    },
  };
};
```

### 案例 2：.env 隐私文件防护插件

拦截 `read` 工具读取 `.env` 配置文件，保护密钥、账号等敏感信息：

```javascript
// .opencode/plugins/env-protection.js
export const EnvProtection = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      // 拦截读取 .env 相关文件的请求
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("禁止读取 .env 隐私配置文件");
      }
    },
  };
};
```

### 案例 3：全局 Shell 环境变量注入

在所有 Shell 执行前注入自定义环境变量：

```javascript
// .opencode/plugins/inject-env.js
export const InjectEnvPlugin = async () => {
  return {
    "shell.env": async (input, output) => {
      // 注入自定义密钥与项目根路径
      output.env.MY_API_KEY = "xxxxxx";
      output.env.PROJECT_ROOT = input.cwd;
    },
  };
};
```

### 案例 4：插件内注册自定义工具

在插件中直接创建 OpenCode 自定义工具，无需单独编写工具文件：

```typescript
// .opencode/plugins/custom-tools.ts
import { type Plugin, tool } from "@opencode-ai/plugin"

export const CustomToolsPlugin: Plugin = async () => {
  return {
    tool: {
      // 定义自定义工具
      mytool: tool({
        description: "示例自定义工具",
        args: {
          foo: tool.schema.string().describe("自定义入参"),
        },
        async execute(args, context) {
          return `当前目录：${context.directory}，入参：${args.foo}`;
        },
      }),
    },
  };
};
```

### 案例 5：自定义会话压缩规则

修改会话压缩逻辑，追加自定义上下文，也可完全替换压缩提示词：

#### 方式 1：追加自定义上下文

```typescript
// .opencode/plugins/compaction.ts
import type { Plugin } from "@opencode-ai/plugin"

export const CompactionPlugin: Plugin = async () => {
  return {
    "experimental.session.compacting": async (input, output) => {
      // 向压缩上下文追加自定义内容
      output.context.push(`
## 项目专属上下文
- 当前任务：代码重构
- 活跃文件：src/main.ts
`);
    },
  };
};
```

#### 方式 2：完全替换压缩提示词

```typescript
// .opencode/plugins/custom-compaction.ts
import type { Plugin } from "@opencode-ai/plugin"

export const CustomCompaction: Plugin = async () => {
  return {
    "experimental.session.compacting": async (input, output) => {
      // 完全重写压缩规则
      output.prompt = `
请精简会话内容，保留：1. 当前任务 2. 已修改文件 3. 待办步骤
输出结构化摘要，支持会话续接。
`;
    },
  };
};
```

### 案例 6：结构化日志插件

使用官方 SDK 日志接口，替代原生 `console.log`，支持分级日志：

```typescript
// .opencode/plugins/log-plugin.ts
import type { Plugin } from "@opencode-ai/plugin"

export const LogPlugin: Plugin = async ({ client }) => {
  // 初始化日志
  await client.app.log({
    body: {
      service: "custom-plugin",
      level: "info",
      message: "插件加载成功",
      extra: { version: "1.0.0" },
    },
  });
  return {};
};
```

日志级别支持：`debug`、`info`、`warn`、`error`。

## 六、OpenCode 生态资源汇总

OpenCode 拥有丰富的社区生态，包含开源插件、第三方集成项目、专用代理，以下为官方整理的生态清单，可直接选用。

### 6.1 社区插件列表

|插件名称|功能描述|
|---|---|
|opencode-daytona|在 Daytona 隔离沙箱运行会话，支持 Git 同步与实时预览|
|opencode-helicone-session|自动注入 Helicone 会话头，用于请求分组|
|opencode-type-inject|自动注入 TS/Svelte 类型到文件读取逻辑|
|opencode-openai-codex-auth|复用 ChatGPT Plus/Pro 订阅，替代独立 API 额度|
|opencode-gemini-auth|复用 Gemini 套餐，降低计费成本|
|opencode-vibeguard|替换机密信息为占位符，保护隐私|
|opencode-websearch-cited|增强网页搜索，采用 Google 检索风格|
|opencode-pty|支持 AI 运行后台交互式进程|
|opencode-shell-strategy|优化 Shell 命令，防止 TTY 挂起|
|opencode-wakatime|接入 Wakatime 统计使用时长|
|opencode-md-table-formatter|自动格式化 LLM 生成的 Markdown 表格|
|opencode-notificator|会话事件桌面通知与声音提醒|
|opencode-supermemory|实现跨会话持久记忆|
|opencode-scheduler|基于 cron 语法定时执行任务|

### 6.2 第三方集成项目

|项目名称|功能描述|
|---|---|
|kimaki|基于 SDK 开发的 Discord 会话管理机器人|
|opencode.nvim|Neovim 编辑器插件，提供感知式提示词|
|portal|移动端优先 Web UI，支持 Tailscale/VPN 访问|
|OpenChamber|OpenCode 桌面 / Web/VS Code 一体化扩展|
|OpenWork|Claude Cowork 开源替代方案|
|ocx|扩展管理器，支持隔离式可移植配置|

### 6.3 开源代理

|代理名称|功能描述|
|---|---|
|Agentic|结构化开发专用模块化代理与命令|
|opencode-agents|增强工作流的配置、提示词与代理合集|

## 七、进阶使用技巧

1. **日志规范**：开发插件时优先使用 `client.app.log` 接口，而非原生 `console.log`，日志可分级、结构化，便于问题排查。

2. **钩子执行顺序**：加载顺序靠前的插件，其钩子会优先执行；可利用该特性实现 “前置拦截 + 后置处理” 的组合逻辑。

3. **插件隔离**：团队项目优先使用**项目级插件**，个人习惯类插件使用**全局插件**，避免配置互相干扰。

4. **错误处理**：`tool.execute.before` 钩子中抛出异常可直接拦截工具执行，常用于安全校验。

## 八、重要注意事项

1. **加载顺序风险**：依赖全局插件逻辑的项目插件，需保证全局插件优先加载；同名 NPM 包仅加载一次，升级插件后建议手动清理缓存。

2. **命名冲突**：插件内自定义工具、钩子名称若与内置能力重名，**插件逻辑会优先覆盖内置逻辑**，需谨慎命名，避免功能异常。

3. **依赖问题**：本地插件的 `package.json` 必须放置在 `.opencode/` 或全局根目录，而非 `plugins` 子目录，否则依赖无法正常安装。

4. **隐私安全**：编写 Shell、文件相关插件时，禁止硬编码密钥、密码等敏感信息；使用 `.env` 防护类插件是生产环境必备操作。

5. **实验性事件**：`experimental` 开头的事件属于内测功能，官方可能随时调整，正式项目谨慎使用。

6. **跨环境迁移**：Windows、macOS、Linux 路径存在差异，编写路径相关插件时建议使用 `worktree`、`directory` 内置变量，避免硬编码绝对路径。

7. **NPM 插件网络**：部分海外社区插件下载较慢，可手动下载包放入缓存目录，或切换国内镜像源。

8. **终端命令限制**：使用 `$` 执行系统命令时，遵循系统权限规则，禁止编写高危删除、格式化类命令。

## 总结

OpenCode 插件体系依托灵活的事件钩子、双加载模式和丰富社区生态，既满足普通用户开箱即用的需求，也支持开发者深度定制。对于普通使用者，优先选用社区成熟 NPM 插件，快速实现通知、统计、隐私防护等能力；对于团队与开发者，可基于本地插件编写项目专属逻辑，结合依赖管理实现复杂功能。

在实际使用中，个人场景推荐全局插件统一习惯，团队项目推荐项目级插件保证协作一致性；开发插件时严格遵循加载规则、类型规范与安全要求，合理使用事件钩子，区分正式功能与实验性功能。借助插件能力，可大幅拓展 OpenCode 的边界，打造适配自身工作流的一体化 AI 编码环境。
