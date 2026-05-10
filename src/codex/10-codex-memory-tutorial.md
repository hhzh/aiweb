# Codex 记忆功能使用教程：自动留存上下文，告别重复指令

Codex 记忆（Memories）是用于**跨线程留存有用上下文**的本地能力，可自动记住你的技术栈、项目规范、工作流偏好与常见坑点，让你无需在每次对话中重复交代背景；搭配增强模块 **Chronicle**，还能从屏幕上下文自动补全信息，进一步降低上下文重复输入成本。本文基于官方文档完整讲解记忆功能的启用、配置、控制、安全使用与故障排查，覆盖基础记忆与屏幕增强记忆全场景。

---

## 一、基础记忆（Memories）核心认知

### 1.1 功能定位

- 记忆是**本地上下文缓存层**，从历史会话中提取稳定偏好、技术栈、项目惯例、常用工作流等信息

- 与 `AGENTS.md` 互补：**强制规则写在 [AGENTS.md](AGENTS.md)**，**个人 / 临时偏好由记忆自动学习**

- 默认关闭；欧洲经济区（EEA）、英国、瑞士暂不支持

### 1.2 核心价值

- 跨会话复用上下文，不用反复说明 “我用 Node.js+Express+MongoDB”“接口统一返回格式”

- 后台异步更新，不影响会话响应速度

- 自动脱敏密钥等敏感信息，保障基础安全

---

## 二、启用基础记忆（两种方式）

### 方式 1：Codex App 可视化启用

1. 打开 Codex App → 进入 **Settings（设置）**

2. 找到 **Personalization（个性化）** 板块

3. 开启 **Memories** 开关

### 方式 2：配置文件手动启用

编辑用户级配置 `~/.codex/config.toml`，在 `[features]` 下开启：

```toml
[features]
memories = true
```

---

## 三、记忆工作原理与存储

### 3.1 工作流程

1. 开启后，Codex 会从已结束、非临时的会话中提取有效上下文

2. 自动脱敏密钥、Token 等敏感信息

3. 后台异步生成 / 更新记忆文件，会话结束后不会立即更新（等待会话空闲足够久）

4. 新会话自动注入相关记忆，减少重复说明

### 3.2 存储位置

所有记忆文件以本地明文 Markdown 存储，路径：

```text
~/.codex/memories/
```

包含：会话摘要、持久条目、最近输入、依据片段等。

> 建议仅用于排查问题时查看，不推荐手动编辑作为主要管理方式。
> 
> 

---

## 四、线程级记忆精细控制

可对**当前线程**单独设置记忆行为，不影响全局配置：
在 Codex TUI 或 App 中输入命令：

```text
/memories
```

可控制两项权限：

1. 当前线程是否**使用已有的记忆**

2. 当前线程是否**允许被用来生成未来记忆**

---

## 五、记忆相关完整配置项

在 `~/.codex/config.toml` 的 `[memories]` 板块精细控制行为：

```toml
[memories]
# 是否允许用新线程生成记忆
generate_memories = true
# 新会话是否加载已有记忆
use_memories = true
# 使用过 MCP/网页搜索时，禁止生成记忆（防止外部污染）
disable_on_external_context = true
# 记忆提取模型（可选）
extract_model = "gpt-5.4-mini"
# 记忆合并整理模型（可选）
consolidation_model = "gpt-5.4-mini"
```

兼容别名：`memories.no_memories_if_mcp_or_web_search = true`

---

## 六、增强记忆：Chronicle（屏幕上下文）

### 6.1 什么是 Chronicle

Chronicle 是**屏幕上下文增强记忆**，属于选择性加入的研究预览功能，可从屏幕内容自动补充工作上下文，进一步减少手动交代信息。

### 6.2 适用限制

- 仅支持：**macOS 系统 + ChatGPT Pro 订阅**

- 欧洲经济区（EEA）、英国、瑞士暂不可用

- 需要开启基础记忆（Memories）才能使用

### 6.3 启用 Chronicle

1. 确保已开启 Memories

2. Codex App → Settings → Personalization → 找到 **Chronicle** 并开启

3. 按提示授权：**屏幕录制 + 辅助功能（Accessibility）**

4. 授权后重启 App 生效

### 6.4 暂停 / 关闭

- 临时暂停：点击菜单栏 Codex 图标 → **Pause Chronicle**

- 恢复：**Resume Chronicle**

- 完全关闭：Settings → Personalization → 关闭 Chronicle

### 6.5 数据与存储

- 临时截图缓存：`$TMPDIR/chronicle/screen_recording/`，超过 6 小时自动删除

- Chronicle 记忆文件：`~/.codex/memories_extensions/chronicle/`（未加密 Markdown）

- 截图仅本地临时处理，不会长期保存在 OpenAI 服务器

---

## 七、隐私、安全与使用规范

1. **不要在记忆中存放密钥**：即便自动脱敏，共享 `~/.codex` 前仍需审查记忆文件

2. **敏感内容暂停 Chronicle**：会议、涉密界面操作前，先暂停 Chronicle

3. **提示注入风险**：Chronicle 会读取屏幕内容，浏览含恶意指令的页面可能被误导

4. **速率限制**：Chronicle 后台沙箱代理消耗速率较快，高负载场景慎用

5. **权限最小化**：仅在需要时开启 Chronicle，不用时关闭

---

## 八、常见问题排查

### 问题 1：找不到 Memories/Chronicle 开关

- 确认地区不在 EEA / 英国 / 瑞士（暂不支持）

- Chronicle 需满足：macOS + ChatGPT Pro + 最新版 Codex App

- 先开启基础 Memories，才会显示 Chronicle

### 问题 2：Chronicle 无法授权

打开 macOS 系统设置 → 隐私与安全性 → 屏幕录制 / 辅助功能 → 勾选 Codex

### 问题 3：记忆不生效 / 不更新

- 确认 `memories = true` 已配置

- 会话需结束并空闲足够久才会生成记忆

- 用过 MCP / 网页搜索且开启 `disable_on_external_context = true`，不会生成记忆

### 问题 4：想删除某条记忆

直接删除对应记忆文件：

```text
rm ~/.codex/memories/xxx.md
rm ~/.codex/memories_extensions/chronicle/xxx.md
```

---

## 九、总结

Codex 记忆（Memories）把重复的上下文交代交给 AI 自动完成，基础记忆满足通用上下文留存，Chronicle 进一步从屏幕补全信息，大幅提升协作效率。使用时遵循**规则入 AGENTS、偏好入记忆、敏感内容关 Chronicle** 的原则，即可在安全前提下，让 Codex 更懂你的项目与工作习惯。

