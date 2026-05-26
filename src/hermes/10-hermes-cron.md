# Hermes Agent cron 定时任务使用教程

Hermes Agent 内置 `cron` 定时任务系统，支持**自然语言调度、标准 Cron 表达式、任务全生命周期管理**，可自动执行数据汇总、系统监控、消息推送等重复性工作，无需人工值守。本文从快速创建、生命周期管理、高级配置到场景实践，带你全面掌握定时任务用法，实现自动化办公与运维。

## 一、核心功能概览

Hermes cron 采用统一 `cronjob` 工具管理，核心能力包括：

- ✅ **多格式调度**：支持自然语言、标准 Cron 表达式、相对延迟、ISO 时间戳。

- ✅ **全生命周期**：创建、暂停、恢复、立即执行、删除、状态查询。

- ✅ **技能集成**：任务执行时自动加载技能，复用成熟工作流。

- ✅ **多渠道投递**：结果可发送至 CLI、文件、飞书、钉钉、Telegram 等。

- ✅ **环境隔离**：支持指定工作目录、用户配置文件，任务独立会话运行。

- ✅ **低成本模式**：支持纯脚本执行，无需 LLM，节省资源。

## 二、快速创建定时任务

### 2.1 自然语言创建（最便捷）

直接用日常语言描述任务与调度，Hermes 自动解析：

```Plain Text
每天早上9点汇总AI行业新闻，发送到飞书
每隔30分钟检查服务器CPU使用率，超过90%发钉钉告警
每周五下午6点生成本周工作周报，保存到本地
```

### 2.2 斜杠命令创建（对话内）

在交互式会话中用 `/cron` 命令快速创建：

```Plain Text
# 间隔任务：每2小时检查接口状态
/cron add "every 2h" "检查https://api.example.com接口可用性"

# 每日任务：工作日9点发送日报
/cron add "0 9 * * 1-5" "汇总昨日数据，生成日报"

# 一次性任务：30分钟后提醒会议
/cron add 30m "提醒10点项目会议"
```

### 2.3 CLI 命令创建（终端）

```bash
# 基础间隔任务
hermes cron create "every 6h" "备份数据库"

# 带技能任务：加载博客监控技能
hermes cron create "0 8 * * *" "汇总新博客" --skill blogwatcher

# 指定工作目录与配置文件
hermes cron create "every 1d" "审计代码" --workdir ~/project --profile dev
```

### 2.4 调度格式大全

#### 1. 相对延迟（一次性）

- `30m`：30 分钟后执行

- `2h`：2 小时后执行

- `1d`：1 天后执行

#### 2. 间隔调度（重复）

- `every 30m`：每 30 分钟

- `every 2h`：每 2 小时

- `every 1d`：每天

#### 3. 标准 Cron 表达式

```Plain Text
# 分 时 日 月 周
0 9 * * *       # 每天9点
0 9 * * 1-5     # 工作日9点
0 */6 * * *     # 每6小时
30 8 1 * *      # 每月1日8:30
```

#### 4. ISO 时间戳（一次性）

```Plain Text
2026-12-31T18:00:00  # 2026年12月31日18点执行
```

## 三、任务生命周期管理

### 3.1 查看任务列表

```bash
# 简要列表
hermes cron list

# 详细状态（含上次/下次执行时间）
hermes cron status
```

### 3.2 编辑任务

```bash
# 修改调度时间
hermes cron edit <任务ID> --schedule "every 4h"

# 修改任务内容
hermes cron edit <任务ID> --prompt "更新数据备份脚本"

# 追加技能
hermes cron edit <任务ID> --add-skill database

# 移除技能
hermes cron edit <任务ID> --remove-skill blogwatcher
```

### 3.3 暂停 / 恢复任务

```bash
# 暂停（保留配置，停止调度）
hermes cron pause <任务ID>

# 恢复（重新计算下次执行时间）
hermes cron resume <任务ID>
```

### 3.4 立即执行任务

```bash
# 跳过调度，立即运行
hermes cron run <任务ID>
```

### 3.5 删除任务

```bash
# 单个删除
hermes cron remove <任务ID>

# 批量删除已暂停任务
hermes cron remove --paused
```

## 四、高级核心配置

### 4.1 技能集成（复用工作流）

任务可加载 1 个或多个技能，自动复用成熟流程：

```bash
# 加载单个技能
hermes cron create "0 9 * * *" "汇总资讯" --skill news-watcher

# 加载多个技能
hermes cron create "every 12h" "生成报告" --skill data-process --skill report-generate
```

### 4.2 指定执行环境

#### 1. 工作目录

指定任务运行目录，自动加载目录下 `AGENTS.md` 规范：

```bash
hermes cron create "every 1d" "审计代码" --workdir ~/my-project
```

#### 2. 用户配置文件

绑定指定 Profile，使用独立配置 / 密钥：

```bash
hermes cron create "0 2 * * *" "备份数据" --profile prod
```

### 4.3 结果投递配置

支持多渠道发送结果，默认返回创建会话：

```bash
# 发送到飞书
hermes cron create "0 9 * * *" "发送日报" --deliver feishu

# 保存到本地文件
hermes cron create "every 6h" "备份日志" --deliver local

# 发送到指定Telegram群组
hermes cron create "every 1h" "监控告警" --deliver telegram:-100123456
```

### 4.4 静默模式（仅异常通知）

任务正常时不发送通知，失败 / 异常才告警：

```Plain Text
每5分钟检查Nginx状态，正常输出，异常发送告警
```

### 4.5 无 Agent 模式（纯脚本）

无需 LLM，直接执行 Shell/Python 脚本，节省资源：

```bash
# 每5分钟检查内存，脚本路径~/.hermes/scripts
hermes cron create "every 5m" --no-agent --script memory-check.sh
```

### 4.6 任务串联（依赖执行）

后一个任务继承前一个任务输出，实现流水线：

```bash
# 任务1：每日7点抓取新闻
hermes cron create "0 7 * * *" "抓取新闻" --name news-fetch

# 任务2：7:30汇总任务1结果
hermes cron create "30 7 * * *" "汇总新闻" --context-from news-fetch
```

## 五、工作原理与安全

### 5.1 调度机制

定时任务由 **Gateway 守护进程** 统一调度，每 60 秒扫描到期任务：

1. 从 `~/.hermes/cron/jobs.json` 加载任务

2. 对比当前时间，筛选到期任务

3. 独立会话运行任务，隔离上下文

4. 执行完成后投递结果，更新下次执行时间

### 5.2 安全防护

- **提示注入扫描**：拦截含恶意指令、凭证泄露的任务。

- **脚本沙箱**：无 Agent 模式脚本仅允许 `~/.hermes/scripts` 目录。

- **任务隔离**：每个任务独立会话，互不干扰。

## 六、场景实践示例

### 6.1 日常数据汇总

```bash
# 工作日9点汇总昨日业务数据，发送飞书
hermes cron create "0 9 * * 1-5" \
"查询数据库，汇总订单、用户数据，生成Markdown报表" \
--deliver feishu
```

### 6.2 系统监控告警

```bash
# 每10分钟检查服务器CPU/内存，超阈值发钉钉告警
hermes cron create "every 10m" \
"检查CPU（>90%）、内存（>85%），异常发送告警" \
--deliver dingtalk
```

### 6.3 自动化备份

```bash
# 每日2点备份数据库，保存到本地+同步到云
hermes cron create "0 2 * * *" \
"执行PostgreSQL备份，保存到~/backup并同步到阿里云OSS" \
--workdir ~/scripts
```

### 6.4 内容自动生成

```bash
# 每周五18点生成本周技术周报，保存到本地
hermes cron create "0 18 * * 5" \
"汇总本周代码提交、接口变更，生成Markdown周报" \
--deliver local
```

## 七、常见问题排查

1. **任务不执行**：检查 Gateway 是否运行（`hermes gateway status`）。

2. **技能加载失败**：确认技能已安装（`hermes skills list`）。

3. **投递失败**：检查渠道配置（如飞书 AppID / 密钥）。

4. **无 Agent 模式报错**：确认脚本存在、有执行权限。

## 八、总结

Hermes cron 以**自然语言调度、全生命周期管理、高可用集成**为核心，无需复杂配置即可实现各类自动化任务。无论是日常办公、系统运维还是数据处理，都能通过简单指令实现无人值守，大幅提升工作效率。结合技能集成、环境隔离、任务串联等高级能力，可构建完整自动化流水线，适配复杂业务场景。

