---
title: Hermes Agent 代码工具使用教程
order: 11
---

# Hermes Agent 代码工具（execute_code）使用教程

`execute_code` 是 Hermes Agent 的核心程序化工具，允许智能编写 Python 脚本并在**隔离沙箱子进程**中执行，通过 RPC 调用各类工具，将多步骤复杂工作流合并为单次 LLM 调用，大幅减少 Token 消耗，提升批量任务处理效率。本文从核心原理、快速上手、实用示例、配置优化、安全机制到场景对比，带你全面掌握代码工具用法。

## 一、核心工作原理

`execute_code` 采用**沙箱隔离 + RPC 通信**架构，确保安全的同时实现工具程序化调用：

1. **脚本生成**：智能体编写含 `from hermes_tools import ...` 的 Python 脚本，声明所需工具。

2. **沙箱启动**：Hermes 创建独立子进程，生成 `hermes_tools.py` 存根模块，开启 Unix 域套接字（UDS）监听 RPC 请求。

3. **脚本执行**：子进程运行脚本，工具调用通过 UDS 回传给主进程处理。

4. **结果返回**：仅脚本 `print()` 输出返回给 LLM，中间工具结果不进入上下文，节省 Token。

### 核心优势

- ✅ **批量处理**：支持循环、条件分支，一次性处理大量数据。

- ✅ **Token 高效**：仅返回最终结果，中间过程不占用上下文。

- ✅ **安全隔离**：独立沙箱，默认过滤密钥，避免环境泄露。

- ✅ **逻辑可控**：支持自定义脚本逻辑，适配复杂多步骤工作流。

### 可用内置工具

脚本内可调用 Hermes 核心工具：

- `web_search`/`web_extract`：全网搜索与网页正文提取

- `read_file`/`write_file`/`patch`：文件读写与代码补丁

- `search_files`：文件批量搜索

- `terminal`：前台终端命令（不支持后台 /pty 模式）

## 二、快速上手

### 2.1 基础调用

直接向 Hermes 发送任务，智能体自动生成并执行脚本：

```Plain Text
搜索2025年Rust异步运行时对比，提取前5篇文章核心观点并汇总
```

### 2.2 手动触发（对话内）

显式调用 `execute_code`，指定脚本逻辑：

```Plain Text
execute_code:
from hermes_tools import web_search, web_extract
# 搜索并汇总
results = web_search("Rust async runtime 2025", limit=5)
summaries = []
for r in results["data"]["web"]:
    content = web_extract([r["url"]])["results"][0]["content"][:500]
    summaries.append({"title": r["title"], "summary": content})
print(summaries)
```

## 三、实用场景示例

### 3.1 批量文件处理

**场景**：批量替换 Python 项目中废弃 API

```Plain Text
execute_code:
from hermes_tools import search_files, patch
# 搜索并替换
matches = search_files("old_api_call", path="src/", file_glob="*.py")
fixed = 0
for m in matches.get("matches", []):
    res = patch(path=m["path"], old_string="old_api_call(", new_string="new_api_call(")
    if "error" not in str(res): fixed += 1
print(f"修复完成：{fixed}/{len(matches)} 个文件")
```

### 3.2 网络研究汇总

**场景**：多源搜索并提取网页核心内容

```Plain Text
execute_code:
from hermes_tools import web_search, web_extract
import json
# 搜索AI Agent最新进展
res = web_search("2025 AI Agent 技术进展", limit=5)
summary = []
for item in res["data"]["web"]:
    content = web_extract([item["url"]])["results"][0]["content"][:800]
    summary.append({"title": item["title"], "content": content})
print(json.dumps(summary, indent=2, ensure_ascii=False))
```

### 3.3 测试报告生成

**场景**：运行测试并解析结果生成报告

```Plain Text
execute_code:
from hermes_tools import terminal
# 运行pytest测试
res = terminal("cd /project && python -m pytest --tb=short", timeout=120)
output = res["output"]
# 解析结果
report = {
    "passed": output.count("passed"),
    "failed": output.count("failed"),
    "errors": output.count("error"),
    "summary": output[-500:]
}
print(report)
```

## 四、核心配置优化

### 4.1 资源限制

默认配置可修改，避免脚本失控：

```yaml
# ~/.hermes/config.yaml
code_execution:
  timeout: 300          # 超时时间（秒，默认300）
  max_tool_calls: 50    # 最大工具调用次数（默认50）
```

### 4.2 执行模式

支持两种执行模式，适配不同场景：

```yaml
code_execution:
  mode: project  # project（默认，继承会话工作目录）/ strict（独立临时目录）
```

- **project 模式**：继承会话目录，可访问项目文件、虚拟环境。

- **strict 模式**：独立临时目录，隔离项目环境，适合安全敏感任务。

### 4.3 环境变量透传

默认过滤密钥类变量，可白名单自定义变量：

```yaml
terminal:
  env_passthrough:
    - MY_CUSTOM_KEY  # 透传自定义变量
```

## 五、安全机制

### 5.1 环境过滤

自动过滤含 `KEY`/`TOKEN`/`SECRET` 等敏感环境变量，仅保留 `PATH`/`HOME` 等安全变量。

### 5.2 沙箱隔离

- 脚本运行于**独立临时目录**，执行后自动清理。

- 独立进程组，超时 / 中断时可强制终止。

- 禁止递归调用 `execute_code`/`delegate_task`，避免无限循环。

### 5.3 安全扫描

脚本执行前扫描提示注入、恶意指令，拦截风险代码。

## 六、execute_code vs terminal

|特性|execute_code|terminal|
|---|---|---|
|推理能力|完整 LLM 逻辑、循环、条件|仅执行 Shell 命令，无推理|
|工具调用|支持多工具程序化调用|单次终端命令|
|适用场景|批量处理、多步骤工作流、数据过滤|简单命令、系统运维、构建|
|Token 消耗|低（仅返回最终结果）|高（返回完整输出）|

**选择建议**：需逻辑控制 / 批量处理用 `execute_code`；简单命令用 `terminal`。

## 七、常见问题排查

1. **脚本超时**：调整 `code_execution.timeout` 延长超时。

2. **工具调用超限**：优化脚本，减少无效工具调用。

3. **权限不足**：检查文件 / 目录权限，或切换 `project` 模式。

4. **依赖缺失**：`project` 模式下确保虚拟环境正确。

5. **执行失败**：查看 stderr 输出，定位脚本语法 / 逻辑错误。

## 八、总结

`execute_code` 是 Hermes Agent 批量自动化的核心工具，通过沙箱隔离、程序化工具调用，高效处理多步骤、循环、条件类复杂任务，兼顾安全与效率。合理配置资源限制、执行模式，结合安全规范，可最大化发挥批量处理价值，适配数据清洗、批量重构、多源汇总等各类场景。

### 最佳实践

- 脚本精简：聚焦核心逻辑，减少冗余工具调用。

- 模式选择：开发用 `project`，安全任务用 `strict`。

- 资源适配：简单任务缩短超时，复杂任务适当延长。

- 安全优先：避免脚本写入敏感路径，过滤密钥变量。

