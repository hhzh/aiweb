## 一、Playwright CLI 介绍

### 1.1 什么是 Playwright CLI

Playwright CLI 是 Playwright 提供的命令行接口工具，通过简洁的命令实现浏览器自动化、测试执行、会话管理等功能，专为编码代理（如 Claude Code、GitHub Copilot）设计，同时也支持手动操作。它以 SKILLS 为核心，主打“令牌高效”，避免加载冗余数据到模型上下文，更适合高吞吐量的编码代理工作流，兼顾浏览器自动化与大型代码库、测试用例的高效处理。

### 1.2 Playwright CLI vs Playwright MCP

两者均为 Playwright 的代理相关工具，但适用场景不同，核心区别如下：

- **Playwright CLI**：以 CLI + SKILLS 为核心，令牌效率高，无需将页面数据强制传入大语言模型（LLM），适合高吞吐量编码代理，平衡浏览器自动化与有限上下文窗口内的推理任务，是现代编码代理的首选。

- **Playwright MCP**：适用于需要持久状态、丰富内省和页面结构迭代推理的场景，例如探索性自动化、自修复测试、长期运行的自主工作流等，这类场景中维持持续浏览器上下文的优先级高于令牌成本。

### 1.3 核心特性

Playwright CLI 的核心优势的在于“令牌高效”，同时具备以下特性，适配代理与手动操作需求：

- 无需将页面数据强制传入 LLM，减少冗余，提升执行效率；

- 支持多浏览器、多平台、多语言适配（依托 Playwright 核心能力）；

- 会话管理灵活，支持持久化浏览器配置，多会话并行；

- 提供丰富的命令集，覆盖页面操作、元素交互、存储管理、网络模拟等场景；

- 支持可视化监控，可实时查看和控制运行中的浏览器会话。

### 1.4 运行要求

使用 Playwright CLI 需满足以下基础环境要求，缺一不可：

- Node.js 18 或更高版本；

- 编码代理工具（如 Claude Code、GitHub Copilot 等），用于 SKILLS 调用（手动操作可无需代理）。

## 二、安装教程（基础入门）

### 2.1 环境准备

首先确认 Node.js 版本符合要求，打开终端执行以下命令检查 Node.js 版本：

```bash
node -v
```

若版本低于 18.x，需先升级 Node.js（推荐使用 nvm 或官方安装包升级）。

### 2.2 全局安装（推荐）

使用 npm 全局安装 Playwright CLI，终端执行以下命令：

```bash
npm install -g @playwright/cli@latest
```

安装完成后，验证安装是否成功：

```bash
playwright-cli --help
```

若终端输出 Playwright CLI 的命令列表及帮助信息，说明安装成功。

### 2.3 本地安装（备选）

若无法全局安装（如无管理员权限），可使用 npx 临时调用或本地安装：

```bash
# 临时调用（无需安装）
npx --no-install playwright-cli --version

# 本地安装（仅当前项目可用）
npm install @playwright/cli@latest
```

本地安装后，所有命令需替换为 `npx playwright-cli`（例如 `npx playwright-cli open https://demo.playwright.dev/todomvc/`）。

### 2.4 SKILLS 安装

Playwright CLI 的 SKILLS 无需手动下载，编码代理（如 Claude Code、GitHub Copilot）会自动读取本地安装的 SKILLS，也可手动触发安装：

```bash
playwright-cli install --skills
```

### 2.5 无 SKILLS 运行

无需提前安装 SKILLS，编码代理可通过 `playwright-cli --help` 自动读取可用命令，手动操作时也可直接通过帮助命令查看并使用所有功能。

## 三、基础使用（核心命令实操）

本章节覆盖日常最常用的基础命令，结合实操案例说明，适合新手快速上手。所有命令均支持全局安装后的 `playwright-cli` 或本地安装的 `npx playwright-cli`。

### 3.1 浏览器基础操作

#### 3.1.1 打开浏览器与页面

默认以无头模式（无界面）打开浏览器，可通过 `--headed` 参数显示浏览器界面（便于调试）：

```bash
# 无头模式打开指定页面（默认）
playwright-cli open https://demo.playwright.dev/todomvc/

# 显示浏览器界面（headed 模式）打开页面
playwright-cli open https://playwright.dev --headed

# 仅打开浏览器，不跳转页面
playwright-cli open
```

#### 3.1.2 页面导航

打开浏览器后，可通过以下命令实现页面跳转、后退、前进、刷新：

```bash
# 跳转到指定 URL
playwright-cli goto https://example.com

# 后退到上一页
playwright-cli go-back

# 前进到下一页
playwright-cli go-forward

# 刷新当前页面
playwright-cli reload
```

#### 3.1.3 关闭页面/浏览器

```bash
# 关闭当前页面（浏览器仍在运行）
playwright-cli close

# 关闭所有浏览器进程（强制关闭）
playwright-cli kill-all
```

### 3.2 元素交互（核心操作）

元素交互需先获取元素引用（ref），可通过快照（snapshot）获取，也可直接使用 CSS 选择器、Playwright 定位器。

#### 3.2.1 获取元素引用（快照）

```bash
# 生成当前页面快照（包含所有元素 ref），默认保存为时间戳命名的文件
playwright-cli snapshot

# 自定义快照文件名
playwright-cli snapshot --filename=page-snapshot.yml

# 仅快照指定元素（如 CSS 选择器 #main）
playwright-cli snapshot "#main"

# 限制快照深度（提升效率）
playwright-cli snapshot --depth=4
```

快照生成后，可在输出中找到元素 ref（如 e15、e21），用于后续交互。

#### 3.2.2 常用元素操作

```bash
# 点击元素（支持 ref、CSS 选择器、定位器）
playwright-cli click e15  # 通过 ref 点击
playwright-cli click "#submit-btn"  # 通过 CSS 选择器点击
playwright-cli click "getByRole('button', { name: 'Submit' })"  # 通过角色定位器点击

# 双击元素
playwright-cli dblclick e35

# 输入文本（定位可编辑元素）
playwright-cli type "Buy groceries"

# 填充文本到指定元素（比 type 更精准，适合输入框）
playwright-cli fill "#todo-input" "Water flowers"
playwright-cli fill "#todo-input" "Walk dog" --submit  # 填充后按 Enter 提交

# 勾选/取消勾选复选框/单选框
playwright-cli check e21
playwright-cli uncheck e21

# 悬停元素
playwright-cli hover e18

# 下拉框选择
playwright-cli select "#city-select" "Beijing"
```

### 3.3 键盘与鼠标操作

```bash
# 按下单个键盘按键（如 Enter、ArrowLeft）
playwright-cli press Enter
playwright-cli press arrowleft

# 键盘按下/松开（单独控制）
playwright-cli keydown a
playwright-cli keyup a

# 鼠标移动到指定坐标（x,y）
playwright-cli mousemove 100 200

# 鼠标按下/松开
playwright-cli mousedown left  # 左键按下
playwright-cli mouseup left

# 鼠标滚轮滚动（dx 水平滚动，dy 垂直滚动）
playwright-cli mousewheel 0 100  # 向下滚动 100 像素
```

### 3.4 页面保存（截图、PDF）

```bash
# 截取当前页面截图（默认时间戳命名）
playwright-cli screenshot

# 截取指定元素截图
playwright-cli screenshot e15

# 自定义截图文件名
playwright-cli screenshot --filename=todo-page.png

# 将当前页面保存为 PDF
playwright-cli pdf
playwright-cli pdf --filename=example.pdf  # 自定义 PDF 文件名
```

### 3.5 实操案例：测试 TodoMVC 新增任务流程

结合上述基础命令，完整模拟“打开 TodoMVC 页面 → 新增任务 → 勾选任务 → 截图”的流程：

```bash
# 1. 以 headed 模式打开 TodoMVC 演示页面
playwright-cli open https://demo.playwright.dev/todomvc/ --headed

# 2. 输入第一个任务并提交
playwright-cli type "Buy groceries"
playwright-cli press Enter

# 3. 输入第二个任务并提交
playwright-cli type "Water flowers"
playwright-cli press Enter

# 4. 勾选两个任务（假设 ref 为 e21、e35，可通过 snapshot 获取）
playwright-cli check e21
playwright-cli check e35

# 5. 截图保存结果
playwright-cli screenshot --filename=todo-done.png
```

## 四、高阶使用（进阶功能）

本章节覆盖会话管理、存储控制、网络模拟、监控等高阶功能，适用于复杂自动化场景和代理工作流优化。

### 4.1 会话管理（多浏览器并行、持久化）

Playwright CLI 默认将浏览器配置保存在内存中，会话结束后数据丢失；支持命名会话、持久化配置，实现多项目并行操作。

#### 4.1.1 命名会话（多项目隔离）

```bash
# 启动名为 todo-app 的会话，打开 TodoMVC 页面
playwright-cli -s=todo-app open https://demo.playwright.dev/todomvc/

# 启动名为 example 的会话，打开 example.com，启用持久化（保存配置到磁盘）
playwright-cli -s=example open https://example.com --persistent

# 查看所有活跃会话
playwright-cli list

# 关闭指定会话
playwright-cli -s=example close

# 删除指定会话的用户数据
playwright-cli -s=example delete-data
```

#### 4.1.2 环境变量指定会话

编码代理可通过环境变量指定会话，无需每次添加 `-s=` 参数：

```bash
# 设置环境变量，指定会话为 todo-app
PLAYWRIGHT_CLI_SESSION=todo-app claude .
```

#### 4.1.3 会话批量管理

```bash
# 列出所有会话（活跃/非活跃）
playwright-cli list

# 关闭所有浏览器会话
playwright-cli close-all

# 强制杀死所有浏览器进程（解决会话异常无法关闭的问题）
playwright-cli kill-all
```

### 4.2 可视化监控（实时查看会话）

当编码代理在后台运行自动化任务时，可通过 `show`命令打开可视化仪表盘，实时观察进度、控制会话：

```bash
playwright-cli show
```

仪表盘包含两个核心视图：

- 会话网格：按工作区分组显示所有活跃会话，包含实时屏幕预览、会话名称、当前 URL、页面标题，点击可放大查看。

- 会话详情：显示选中会话的实时视图，包含标签栏、导航控制（后退、前进、刷新）、地址栏，可点击视口接管鼠标/键盘操作（按 Escape 释放）。

从仪表盘可直接关闭活跃会话、删除非活跃会话的数据。

### 4.3 存储管理（Cookies、LocalStorage 等）

支持对浏览器存储数据的全面控制，包括 Cookies、LocalStorage、SessionStorage，可用于持久化登录状态、清理测试数据。

#### 4.3.1 Cookies 管理

```bash
# 列出所有 Cookies（可指定域名）
playwright-cli cookie-list
playwright-cli cookie-list --domain=example.com

# 获取指定名称的 Cookie
playwright-cli cookie-get session-id

# 设置 Cookie（名称、值）
playwright-cli cookie-set session-id "abc123xyz"

# 删除指定 Cookie
playwright-cli cookie-delete session-id

# 清空所有 Cookies
playwright-cli cookie-clear
```

#### 4.3.2 LocalStorage 管理

```bash
# 列出所有 LocalStorage 条目
playwright-cli localstorage-list

# 获取指定键的 LocalStorage 值
playwright-cli localstorage-get username

# 设置 LocalStorage（键、值）
playwright-cli localstorage-set username "test-user"

# 删除指定键的 LocalStorage 条目
playwright-cli localstorage-delete username

# 清空所有 LocalStorage
playwright-cli localstorage-clear
```

#### 4.3.3 SessionStorage 管理（与 LocalStorage 命令类似）

```bash
playwright-cli sessionstorage-list
playwright-cli sessionstorage-get token
playwright-cli sessionstorage-set token "def456"
playwright-cli sessionstorage-delete token
playwright-cli sessionstorage-clear
```

#### 4.3.4 存储状态保存与加载

可将当前存储状态（Cookies、LocalStorage 等）保存到文件，后续加载复用（如跳过登录流程）：

```bash
# 保存存储状态到文件
playwright-cli state-save login-state.json

# 加载存储状态（复用登录信息）
playwright-cli state-load login-state.json
```

### 4.4 网络模拟（请求拦截、Mock）

支持拦截和 Mock 网络请求，用于测试异常场景（如接口失败、数据异常），无需依赖真实后端。

```bash
# 拦截指定模式的网络请求（如所有 API 请求）
playwright-cli route "https://api.example.com/**"

# 查看所有活跃的请求拦截规则
playwright-cli route-list

# 移除指定拦截规则（无参数则移除所有）
playwright-cli unroute "https://api.example.com/**"
playwright-cli unroute
```

### 4.5 调试与追踪（进阶排错）

提供追踪录制、视频录制、控制台日志查看等功能，帮助定位自动化过程中的问题。

#### 4.5.1 追踪录制（捕获执行详情）

```bash
# 开始追踪录制（用于排错）
playwright-cli tracing-start

# 执行自动化操作（如元素点击、页面跳转）
playwright-cli click e15
playwright-cli goto https://example.com

# 停止追踪录制（自动保存追踪数据）
playwright-cli tracing-stop
```

追踪数据包含执行屏幕录制、DOM 快照、操作记录等，可用于复盘失败原因。

#### 4.5.2 视频录制

```bash
# 开始视频录制（自定义文件名）
playwright-cli video-start todo-automation.mp4

# 为视频添加章节标记（便于定位关键操作）
playwright-cli video-chapter "新增任务"

# 停止视频录制
playwright-cli video-stop
```

#### 4.5.3 调试工具

```bash
# 查看页面控制台日志（可指定最小级别）
playwright-cli console info

# 查看页面加载后的所有网络请求
playwright-cli network

# 执行任意 Playwright 代码片段
playwright-cli run-code "console.log(document.title)"

# 运行文件中的 Playwright 代码
playwright-cli run-code --filename=test-script.js
```

### 4.6 配置文件（全局优化）

可通过 JSON 配置文件统一管理 Playwright CLI 的参数，避免每次命令重复输入。

#### 4.6.1 配置文件使用

```bash
# 指定配置文件运行命令
playwright-cli --config path/to/config.json open example.com
```

默认情况下，Playwright CLI 会自动读取当前目录下的 `.playwrightcli.config.json` 文件，无需手动指定。

#### 4.6.2 配置文件示例（参考）

```json
{
  "browser": "chrome",  // 默认浏览器
  "headed": false,      // 默认无头模式
  "persistent": true,   // 默认持久化配置
  "profile": "./my-profile"  // 自定义浏览器配置路径
}
```

### 4.7 高级元素定位

除了 ref 和 CSS 选择器，Playwright CLI 支持 Playwright 原生定位器，更精准、更稳定，适合复杂页面：

```bash
# 角色定位器（按角色和名称定位）
playwright-cli click "getByRole('button', { name: 'Submit' })"

# 测试 ID 定位（推荐，不受页面结构变化影响）
playwright-cli click "getByTestId('submit-button')"

# 文本定位（按元素文本定位）
playwright-cli click "getByText('登录')"

# 占位符定位（输入框占位符）
playwright-cli fill "getByPlaceholderText('请输入用户名')" "test-user"
```

## 五、常见问题与注意事项

### 5.1 常见问题排查

- **命令执行失败，提示“command not found”**：检查 Node.js 版本是否达标，全局安装后是否配置环境变量，本地安装需使用 npx 前缀。

- **元素无法定位**：先通过 `playwright-cli snapshot` 获取最新元素 ref，确认元素选择器或 ref 正确；若页面动态加载，可适当增加操作间隔（无需手动加延时，Playwright 自动等待元素可交互）。

- **会话无法关闭**：使用 `playwright-cli kill-all` 强制关闭所有浏览器进程，清除异常会话。

- **快照生成失败**：检查页面是否正常加载，网络是否通畅，可通过 `playwright-cli goto` 重新跳转页面后再生成快照。

### 5.2 注意事项

- Playwright CLI 默认无头模式运行，调试时需添加 `--headed` 参数，便于观察操作过程。

- 持久化会话（--persistent）会将浏览器配置保存到磁盘，多次运行后需定期清理，避免占用过多空间。

- 编码代理使用时，建议通过环境变量指定会话，提升工作流效率。

- 执行复杂自动化流程时，建议开启追踪录制（tracing-start），便于后续排错。

## 六、总结

Playwright CLI 是一款高效、灵活的浏览器自动化工具，核心优势在于令牌高效，适配编码代理与手动操作，覆盖从基础页面交互到高阶会话管理、网络模拟的全场景。通过本教程的学习，可快速掌握其安装、基础使用和高阶功能，用于自动化测试、页面操作、代理工作流等场景。

如需进一步了解某一功能的细节，可执行 `playwright-cli --help` 查看完整命令说明，或参考 Playwright 官方文档补充学习。

