# Claude Code 斜杠命令（Commands）实战使用教程
在 Claude Code 中，输入 **/** 即可唤起所有可用斜杠命令（Commands），输入 /**字母** 可快速筛选；命令支持会话内实时执行，是提升AI编程效率的核心操作。本文基于官方命令文档，按**使用频率与重要性**分级归类，全部命令可直接复制使用，快速覆盖日常开发、调试、配置全场景。

Claude Code 命令分类体系如下：

```mermaid
flowchart TD
    A["斜杠命令 /"] --> B[高频必备]
    A --> C[会话管理]
    A --> D[调试诊断]
    A --> E[插件扩展]
    A --> F[权限配置]
    A --> G[协作高级]
    
    B --> H["/clear /diff /copy"]
    C --> I["/compact /rewind /resume"]
    D --> J["/doctor /cost /status"]
    E --> K["/plugin /agents /skills"]
    F --> L["/model /permissions /config"]
    G --> M["/pr-comments /remote-control"]
```

---

## 一、高频必备命令（日常开发优先掌握）
日常编码、会话切换、文件操作最常用，建议熟记，大幅减少重复操作。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /clear | 无参数 | 清空对话历史、释放上下文 | /reset、/new |
| /diff | 无参数 | 交互式查看未提交Git变更 | 支持箭头键切换轮次差异 |
| /add-dir | /add-dir <path> | 为当前会话添加文件访问目录 | 不加载目录内.claude配置 |
| /copy | /copy [N] | 复制最近助手响应；N指定倒数第N条 | 代码块支持交互式选择 |
| /help | 无参数 | 查看所有可用命令与帮助 | 快速查遗忘命令 |
| /exit | 无参数 | 退出CLI | /quit |
| /btw | /btw <question> | 快速附加提问，不污染当前对话上下文 | 不打断当前任务流程 |

---

## 二、会话与上下文管理命令
用于控制对话状态、压缩上下文、回溯会话，避免上下文膨胀导致效率下降。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /compact | /compact [instructions] | 压缩对话历史，可指定保留重点 | 降低Token消耗 |
| /context | 无参数 | 可视化上下文占用，给出优化建议 | 排查内存膨胀问题 |
| /rewind | 无参数 | 回退对话/代码到上一节点 | /checkpoint |
| /branch | /branch [name] | 对话分支创建，不影响原会话 | /fork |
| /resume | /resume [session] | 按ID/名称恢复历史会话 | /continue |
| /rename | /rename [name] | 重命名当前会话；无参自动生成 | 便于会话管理 |

---

## 三、调试与诊断命令
定位环境问题、分析使用数据、校验配置，是排障与效率优化的关键。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /doctor | 无参数 | 诊断并校验Claude Code安装与配置 | 环境排错首选 |
| /cost | 无参数 | 显示令牌（Token）使用统计 | 订阅用户费用参考 |
| /stats | 无参数 | 可视化每日使用量、会话历史 | 分析使用习惯 |
| /insights | 无参数 | 生成会话分析报告，识别交互摩擦点 | 优化工作流 |
| /status | 无参数 | 查看版本、模型、账户与连接状态 | 无需等待响应完成 |
| /usage | 无参数 | 查看计划用量与速率限制状态 | 避免超限中断 |

---

## 四、插件、代理（Agents）与扩展命令
管理插件、代理（Agents）、MCP服务器、钩子（Hooks），适配扩展功能。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /plugin | 无参数 | 管理Claude Code插件（Plugins） | 安装、卸载、启用、禁用 |
| /reload-plugins | 无参数 | 热重载插件，无需重启 | 实时生效配置修改 |
| /agents | 无参数 | 管理代理（Agents）配置 | 查看/切换专项任务代理 |
| /skills | 无参数 | 列出所有可用技能（Skills） | 含内置与插件扩展技能 |
| /hooks | 无参数 | 查看工具事件钩子（Hooks）配置 | 自动化工作流校验 |
| /mcp | 无参数 | 管理MCP服务器连接与OAuth认证 | 对接外部服务 |

---

## 五、权限、模型与基础配置命令
调整模型、权限、主题、界面，适配个人开发偏好与安全规范。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /model | /model [model] | 切换AI模型，立即生效 | 支持Opus/Sonnet/Haiku |
| /effort | /effort [low/medium/high/max/auto] | 设置模型工作量等级 | max仅当前会话生效 |
| /permissions | 无参数 | 管理工具权限规则 | /allowed-tools |
| /config | 无参数 | 打开设置界面，调整主题/模型/样式 | /settings |
| /theme | 无参数 | 切换颜色主题 | 支持浅色/深色/色盲友好 |
| /color | /color [color/default] | 设置提示栏颜色 | 支持red/blue/green等 |
| /statusline | 无参数 | 配置状态栏样式 | 可自动适配Shell |

---

## 六、协作与高级功能命令
团队协作、远程控制、云任务、隐私设置等进阶场景专用。

| 命令（Commands） | 参数格式 | 核心用途 | 备注/别名 |
| :--- | :--- | :--- | :--- |
| /pr-comments | /pr-comments [PR] | 获取GitHub PR评论 | 需gh CLI |
| /install-github-app | 无参数 | 为仓库配置Claude GitHub Actions | 一键集成CI |
| /remote-control | 无参数 | 开启会话远程控制 | /rc |
| /schedule | /schedule [description] | 创建/管理云定时任务 | 自动化后台任务 |
| /security-review | 无参数 | 分析待提交代码安全漏洞 | 检测注入/权限/数据泄露 |
| /feedback | /feedback [report] | 提交反馈/Bug | /bug |
| /desktop | 无参数 | 切换到桌面端继续会话 | 仅macOS/Windows，/app |

---

## 七、命令使用核心技巧（实战必看）
1. **快速筛选**：输入 **/** + 字母，自动过滤匹配命令（如输入 /co 显示 copy/compact/config）。
2. **参数规则**：`<arg>` 为必填参数，`[arg]` 为可选参数，严格按格式传入。
3. **MCP动态命令**：MCP服务器会自动生成命令，格式为 `/mcp__<server>__<prompt>`，无需手动配置。
4. **权限可见**：部分命令随平台、订阅计划显示（如 /upgrade 仅Pro/Max可用，/desktop 仅桌面端）。
5. **无等待生效**：/model、/effort、/status 等命令无需等待当前响应完成，立即执行。

---

本文覆盖官方全部内置命令，按使用场景分级整理，可作为日常开发速查手册；配合插件（Plugins）与代理（Agents）扩展，能进一步释放Claude Code的自动化与定制化能力。