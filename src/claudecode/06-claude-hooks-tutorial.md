---
title: Claude Code Hooks 实战教程
order: 6
---

# Claude Code Hooks 实战教程

在 Claude Code 实际开发中，AI 误执行高危命令、代码格式混乱、环境配置繁琐、任务未完成就停止等问题频发，既影响效率又暗藏风险。Claude Code Hooks 作为生命周期事件拦截与自动化机制，正是解决这些问题的核心工具——它能在工具调用、权限申请、会话启停等关键节点，自动执行预设逻辑，实现安全拦截、规范统一、流程自动化，让 AI 开发更可控、更高效。

本教程以**实战为核心**，摒弃冗余理论，聚焦 Hooks 实际应用，从核心概念、配置方法、事件实战、执行类型、实战场景、最佳实践、常见问题等维度，结合可直接复用的生产级案例，帮助开发者快速上手，熟练运用 Hooks 优化 AI 开发工作流，覆盖个人开发与团队协作的各类实战需求，新手也能快速落地使用。

## 一、Hooks 核心概念（实战导向版）

### 1.1 什么是 Hooks（一句话懂）

Hooks 是 Claude Code 的**生命周期事件回调与自动化执行机制**，相当于 AI 开发工作流的“自动管家”——监听关键事件（如调用工具、启动会话），自动执行预设脚本或 LLM 决策，无需手动干预，实现“一次配置，终身受益”。

类比理解：和 Git 的 pre-commit 钩子（提交前自动 lint）、Vue 的生命周期钩子（组件渲染时执行逻辑）原理一致，核心就是“在指定节点做指定事”，重点解决 AI 开发中的安全、规范、效率问题。

### 1.2 Hooks 实战核心价值（直击痛点）

1. **安全防护（必用）**：拦截 rm -rf、git push --force 等高危命令，避免误删文件、破坏代码库（实战中 90% 的安全问题可通过 Hooks 解决）；

2. **规范统一（团队必备）**：自动格式化代码、过滤敏感词，确保 AI 生成内容符合团队规范，减少评审成本；

3. **效率提升（省时关键）**：自动加载环境变量、切换运行时版本、记录日志，省去重复手动操作；

4. **灵活管控（企业/团队适配）**：支持多级配置，既能企业统一管控，也能个人自定义，兼顾规范与灵活。

### 1.3 Hooks 与其他功能的实战区别（避免用错）

- 与 Skills 区别：Skills 是“增强 AI 能力”（如代码审查），不能独立执行；Hooks 是“管控流程”（如拦截命令），可独立触发，还能调用 Skills；

- 与 Sub-agent 区别：Sub-agent 是“完成具体任务”（如部署代码）；Hooks 是“管控任务流程”（如检查任务是否完成）；

- 与工具权限区别：工具权限是“静态禁止/允许使用工具”；Hooks 是“动态校验操作内容”（如允许使用 Bash，但禁止 rm 命令），更灵活。

## 二、Hooks 配置位置与优先级（实战配置前提）

Hooks 支持多级配置，核心是“高优先级覆盖低优先级”，实战中需根据场景选择配置位置，避免冲突，以下是重点（冗余说明省略）：

### 2.1 五大配置位置（按优先级从高到低，实战重点标红）

- **企业托管策略**：企业管理员配置，可禁用其他所有层级，适合大型团队集中管控；

- **项目本地配置（.claude/settings.local.json）**：本地私有，不提交 Git，适合个人本地调试规则；

- **项目共享配置（.claude/settings.json）**：提交 Git，团队共享，适合团队统一规范（**最常用**）；

- **用户全局配置（~/.claude/settings.json）**：所有项目生效，适合个人通用规则（如全局高危命令拦截）；

- **插件/ Skill/Sub-agent 内置 Hooks**：组件专属，生命周期内生效，适合插件内部逻辑。

### 2.2 实战配置优先级原则

企业托管策略 > 项目本地配置 > 项目共享配置 > 用户全局配置 > 内置 Hooks

实战示例：团队共享配置中拦截 rm 命令，个人本地配置中新增拦截 curl 命令，最终个人本地会同时生效两个规则（本地配置不覆盖共享配置，仅新增/覆盖同名规则）。

### 2.3 配置位置实战最佳实践（直接套用）

- 团队统一规则（如代码格式化、高危命令拦截）→ 项目共享配置；

- 个人通用规则（如所有项目加载 .env）→ 用户全局配置；

- 本地调试规则（如临时关闭某类拦截）→ 项目本地配置；

- 企业强制规则（如禁止删库）→ 企业托管策略。

## 三、Hooks 基础配置结构（实战模板+避坑）

Hooks 配置为 JSON 格式，核心结构“事件名 → 匹配器 → 执行逻辑”，实战中无需死记结构，直接套用模板，重点注意避坑点。

### 3.1 实战核心模板（直接复制使用）

```json

{
  "hooks": {
    "事件名": [
      {
        "matcher": "工具匹配规则（可选）",
        "hooks": [
          {
            "type": "command/prompt", // 二选一，实战中 command 用得最多
            "command": "Shell命令（type为command时必填）",
            "prompt": "LLM提示（type为prompt时必填）",
            "timeout": 30, // 超时时间，实战建议10-30秒
            "once": false // 仅运行一次，一般不用改
          }
        ]
      }
    ]
  }
}
    
```

### 3.2 两种实战配置结构（按需选择）

#### 3.2.1 带匹配器结构（工具类事件专用，如 PreToolUse）

适用场景：需要针对特定工具（如 Bash、Edit）配置规则，实战最常用。

实战模板（拦截 Bash 高危命令，直接复制生效）：

```json

{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash", // 只匹配 Bash 工具
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT_COMMAND\" | grep -qiE \"rm -rf|git push --force\"; then exit 2; fi",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
    
```

#### 3.2.2 无匹配器结构（全局事件专用，如 SessionStart）

适用场景：无需匹配工具，全局触发（如会话启动、用户输入提交）。

实战模板（会话启动加载 .env，直接复制生效）：

```json

{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f \"$CLAUDE_PROJECT_DIR/.env\" ]; then cat \"$CLAUDE_PROJECT_DIR/.env\" >> \"$CLAUDE_ENV_FILE\"; fi",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
    
```

### 3.3 实战核心字段（必懂，避坑关键）

- matcher：仅工具类事件用，区分大小写（如“bash”不匹配“Bash”），支持正则（如“Edit|Write”匹配两个工具）；

- type：command（Shell 脚本，确定性强，首选）、prompt（LLM 决策，复杂场景用）；

- timeout：避免脚本卡死，简单命令设 10-20 秒，复杂命令设 30-60 秒；

- command：特殊字符（如引号）需转义，支持引用环境变量（如 $CLAUDE_PROJECT_DIR，直接用）。

### 3.4 实战避坑点（重点标红）

- JSON 格式必须规范，可用在线 JSON 校验工具检查（避免逗号遗漏、引号不匹配）；

- matcher 区分大小写，工具名称必须和 Claude Code 一致（如“Bash”不能写“bash”）；

- command 中路径尽量用环境变量（如 $CLAUDE_PROJECT_DIR），避免硬编码（适配不同环境）。

## 四、Hooks 核心事件实战详解（重中之重）

先通过 mermaid 图直观了解 Hooks 生命周期及核心事件触发时机，再用表格总结事件关键信息，最后结合实战案例讲解，所有案例均可直接复制使用。

### 4.1 Hooks 生命周期图（mermaid 绘制）

```mermaid
graph TD
    A[会话启动/恢复] -->|触发 SessionStart| B[会话初始化完成]
    B --> C[用户提交输入]
    C -->|触发 UserPromptSubmit| D[AI 处理输入]
    D --> E[AI 调用工具]
    E -->|触发 PreToolUse| F[校验/拦截工具操作]
    F -->|通过，无拦截| G[执行工具]
    F -->|拦截，退出码2| H[停止工具执行，返回错误]
    G -->|工具执行成功| I[触发 PostToolUse]
    G -->|工具执行失败| J[不触发 PostToolUse，返回错误]
    I --> K[工具执行结果处理]
    K --> L[AI 生成响应/子代理执行]
    L -->|子代理完成| M[触发 SubagentStop]
    L -->|主代理完成响应| N[触发 Stop]
    M --> N
    N -->|触发 SessionEnd（可选）| O[会话结束，清理资源]
    H --> O
    J --> O
 ```

### 4.2 Hook 事件实战总结表（一目了然，直接查阅）

|事件名称|触发时机|实战核心作用|匹配器用法|实战优先级|
|---|---|---|---|---|
|PreToolUse|工具调用前|拦截高危操作、修改入参、校验权限（最常用）|支持匹配工具（如 Bash、Edit），常用正则匹配|★★★★★|
|PostToolUse|工具执行成功后|代码格式化、日志记录、结果校验|同 PreToolUse，常用 Edit|Write、Bash|★★★★☆|
|SessionStart|会话启动/恢复时|加载环境变量、切换运行时、初始化依赖|匹配场景（startup/resume/*）|★★★★☆|
|Stop/SubagentStop|主/子代理完成后|检查任务完整性、生成总结、触发后续操作|无需匹配器（全局事件）|★★★☆☆|
|PermissionRequest|AI 申请权限时|自动允许/拒绝权限，减少手动操作|同 PreToolUse，常用 Bash、Edit|★★★☆☆|
|UserPromptSubmit|用户提交输入前|过滤敏感词、注入上下文、输入校验|无需匹配器（全局事件）|★★☆☆☆|
|其他事件（Notification 等）|特定场景触发|自定义通知、上下文保护、资源清理|按场景匹配（如通知类型）|★☆☆☆☆|

### 4.3 核心事件实战案例（可直接复制生效）

#### 4.3.1 PreToolUse（工具调用前，必配）

实战场景 1：拦截多种高危 Bash 命令（覆盖删库、强制推送等，团队必配）

```json

{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "# 读取命令参数\nINPUT=$(cat)\nCOMMAND=$(echo \"$INPUT\" | jq -r '.tool_input.command // empty')\n# 高危命令清单（可按需添加）\nDANGEROUS_PATTERNS=(\n  'rm\\s+-rf\\s+/'       # 禁止 rm -rf 根目录\n  'git\\s+push\\s+.*--force' # 禁止强制推送\n  'DROP\\s+TABLE'        # 禁止删表\n  'DROP\\s+DATABASE'     # 禁止删库\n  'git\\s+reset\\s+--hard' # 禁止丢弃未提交修改\n)\n# 匹配拦截\nfor pattern in \"${DANGEROUS_PATTERNS[@]}\"; do\n  if echo \"$COMMAND\" | grep -iEq \"$pattern\"; then\n    echo \"BLOCKED: 拦截高危命令 ($pattern)\" >&2\n    echo \"原始命令: $COMMAND\" >&2\n    exit 2 # 退出码2=拦截\n  fi\ndone\nexit 0 # 退出码0=允许",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
    
```

实战场景 2：保护敏感文件不被编辑（.env、配置文件等）

```json

{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat)\nFILE_PATH=$(echo \"$INPUT\" | jq -r '.tool_input.path // empty')\n# 敏感文件清单（按需修改）\nSENSITIVE_FILES=(\".env\" \"config/prod.json\" \"src/secret.ts\")\nfor file in \"${SENSITIVE_FILES[@]}\"; do\n  if [[ \"$FILE_PATH\" == *\"$file\"* ]]; then\n    echo \"BLOCKED: 禁止编辑敏感文件 $FILE_PATH\" >&2\n    exit 2\n  fi\ndone\nexit 0",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
    
```

#### 4.3.2 PostToolUse（工具执行后，团队规范必配）

实战场景：编辑 JS/TS 文件后自动格式化（Prettier，无需手动操作）

```json

{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat)\nFILE_PATH=$(echo \"$INPUT\" | jq -r '.tool_input.path // empty')\n# 仅格式化 JS/TS/JSX/TSX 文件\nif [[ \"$FILE_PATH\" =~ \.(js|ts|jsx|tsx)$ ]]; then\n  npx prettier --write \"$FILE_PATH\"\n  echo \"格式化完成：$FILE_PATH\"\nfi\nexit 0",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
    
```

#### 4.3.3 SessionStart（会话启动，个人/团队必配）

实战场景：会话启动加载 .env + 切换 Node 版本（适配项目环境）

```json

{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup", // 仅新会话启动时触发
        "hooks": [
          {
            "type": "command",
            "command": "# 加载 .env 文件\nif [ -f \"$CLAUDE_PROJECT_DIR/.env\" ]; then\n  while IFS= read -r line; do\n    echo \"$line\" >> \"$CLAUDE_ENV_FILE\"\n  done < \"$CLAUDE_PROJECT_DIR/.env\"\n  echo \".env 文件加载完成\"\nfi\n# 切换 Node 版本到 20.x（按需修改）\nsource ~/.nvm/nvm.sh\nnvm use 20\necho \"Node 版本切换完成：$(node -v)\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

#### 4.3.4 其他常用事件实战案例（按需选用）

案例 1：PermissionRequest（自动处理权限，减少手动确认）

```json

{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat)\nCOMMAND=$(echo \"$INPUT\" | jq -r '.tool_input.command // empty')\n# 安全命令自动允许，高危命令自动拒绝\nSAFE_COMMANDS=('ls' 'pwd' 'cat' 'grep' 'npm install')\nDANGEROUS_COMMANDS=('rm' 'git push' 'curl')\n# 自动允许安全命令\nfor safe_cmd in \"${SAFE_COMMANDS[@]}\"; do\n  if echo \"$COMMAND\" | grep -qiE \"^$safe_cmd\"; then exit 0; fi\ndone\n# 自动拒绝高危命令\nfor dangerous_cmd in \"${DANGEROUS_COMMANDS[@]}\"; do\n  if echo \"$COMMAND\" | grep -qiE \"^$dangerous_cmd\"; then exit 2; fi\ndone\nexit 1 # 其他命令手动确认",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
    
```

案例 2：Stop（检查主代理任务是否完成，避免提前停止）

```json

{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "评估主代理是否完成用户所有任务，输入：$ARGUMENTS\n评估标准：1. 需求是否全部实现；2. 有无未解决错误；3. 是否需要补充操作（如测试）\n严格按此JSON返回：{\"ok\": true|false, \"reason\": \"原因\"}\nok=true：允许停止；ok=false：禁止停止并说明原因",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
    
```

## 五、Hooks 两种执行类型实战区分（选对类型少走弯路）

Hooks 仅支持 command（Shell 脚本）和 prompt（LLM 决策）两种核心类型，实战中 90% 场景用 command，复杂场景用 prompt，以下是实战对比和选择建议：

### 5.1 两种执行类型实战对比表

|执行类型|核心特点|实战适用场景|优点|缺点|实战优先级|
|---|---|---|---|---|---|
|command（Shell 脚本）|本地执行、确定性强、通过退出码控制流程|拦截命令、格式化代码、加载环境、日志记录（所有确定性场景）|速度快、无网络依赖、逻辑可控|复杂判断能力弱|★★★★★|
|prompt（LLM 决策）|调用 Haiku 模型、上下文感知、灵活判断|任务完整性检查、上下文敏感权限决策（复杂不确定场景）|复杂判断能力强、无需写复杂脚本|依赖网络、响应慢、结果不确定|★★★☆☆|

### 5.2 实战选择建议（直接套用）

- 能用水 Shell 脚本实现的（如拦截命令、格式化），优先用 command；

- 需要上下文判断的（如任务是否完成、复杂权限决策），用 prompt；

- command 核心重点：退出码 0=允许、2=拦截，必须严格遵循（否则配置失效）。

## 六、Hooks 实战场景汇总（覆盖个人/团队/企业）

以下是实际开发中最常用的 Hooks 实战场景，每个场景对应可直接复用的配置，按需组合使用：

### 6.1 个人开发实战场景（提升效率）

- 场景 1：会话启动自动加载 .env + 切换 Node 版本（复用 4.3.3 案例）；

- 场景 2：编辑代码后自动格式化（复用 4.3.2 案例）；

- 场景 3：全局拦截高危 Bash 命令（复用 4.3.1 案例）。

### 6.2 团队开发实战场景（规范统一）

- 场景 1：团队共享代码格式化、Lint 校验规则（PostToolUse 事件）；

- 场景 2：统一拦截高危命令，禁止敏感文件编辑（PreToolUse 事件）；

- 场景 3：自动处理权限申请，减少团队手动确认（PermissionRequest 事件）。

### 6.3 企业级实战场景（集中管控）

- 场景 1：企业托管策略禁用所有高危操作，强制全员遵循；

- 场景 2：会话启动强制加载企业统一环境变量，规范开发环境；

- 场景 3：所有工具调用日志统一记录，便于审计（PostToolUse 事件）。

## 七、Hooks 实战最佳实践（避坑+高效）

- 配置分层：团队规则放项目共享配置，个人规则放本地/全局，避免冲突；

- 脚本简化：command 脚本尽量简洁，复杂逻辑拆分成独立脚本，便于维护；

- 超时合理：根据脚本复杂度设置超时时间，避免过短导致失败、过长导致阻塞；

- 测试优先：新增 Hooks 后，先在本地测试（如手动触发事件），确认生效后再提交团队共享；

- 日志记录：关键 Hooks（如拦截命令、权限处理）添加日志，便于问题排查；

- 环境兼容：脚本中尽量使用环境变量，避免硬编码路径，适配不同开发环境。

## 八、常见问题实战排查（新手必看）

- 问题 1：Hooks 配置不生效？→ 排查：JSON 格式是否规范、matcher 大小写是否正确、退出码是否正确、配置位置优先级是否正确；

- 问题 2：command 脚本执行失败？→ 排查：特殊字符是否转义、环境变量是否正确、脚本权限是否足够；

- 问题 3：Hooks 拦截后无提示？→ 排查：脚本中是否用 echo 输出错误信息（>&2 表示标准错误输出）；

- 问题 4：prompt 类型 Hooks 响应慢？→ 解决方案：延长 timeout 至 30-60 秒，或改用 command 类型（若可实现）。

