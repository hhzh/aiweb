# OpenClaw 模型选择指南

OpenClaw 模型体系是智能体的**推理核心引擎**，支持数十家主流 LLM 提供商、本地模型与兼容代理，提供**主备降级、认证轮转、会话热切换、白名单管控、图像模型分离、故障自动转移**六大企业级能力。本文基于官方全套模型文档，完整覆盖模型标识规范、提供商配置、选择逻辑、故障转移、CLI 操作、自定义扩展与场景化最佳实践，做到一站式落地、无死角配置。

---

## 一、模型体系核心设计与基础概念

### 1.1 核心定位

OpenClaw 不绑定单一模型，通过标准化适配层打通所有主流 LLM，实现：

- 一次配置，多模型自由切换
- 主模型故障，备用模型自动接管
- 文本 / 图像模型分离，最优能力匹配
- 多认证密钥轮转，避免限流中断
- 会话级热切换，无需重启网关

### 1.2 模型标识规范（必知）

所有模型统一使用 **`提供商/模型名`** 格式，全局唯一：

```text
anthropic/claude-opus-4-6
openai/gpt-4o
moonshot/kimi-k2.5
ollama/llama3.3
```

- 提供商名标准化：`z.ai` → `zai`、`google-gemini` → `google`
- 模型名区分大小写，以官方注册为准
- 含多级路径模型（如 OpenRouter）：`openrouter/moonshotai/kimi-k2`

### 1.3 模型选择优先级（执行顺序）

OpenClaw 按固定顺序选择模型，确保确定性：

1. 会话级覆盖（`/model` 指令）
2. 智能体专属配置（`agents.list[].model`）
3. 全局主模型（`agents.defaults.model.primary`）
4. 全局备用模型列表（`agents.defaults.model.fallbacks`）
5. 提供商内认证 Profile 轮转

### 1.4 三大模型分工

1. **主模型**：默认推理模型，处理文本 / 工具 / 长上下文
2. **备用模型**：主模型故障时降级，数组顺序生效
3. **图像模型**：主模型不支持视觉时，专用处理图片 / 截图

---

## 二、全局核心配置（openclaw.json）

所有模型配置集中在全局配置文件，支持 JSON5 格式，路径：`~/.openclaw/openclaw.json`

### 2.1 基础模型配置（推荐模板）

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": [
          "openai/gpt-4o",
          "moonshot/kimi-k2.5",
          "ollama/llama3.3"
        ]
      },
      "imageModel": {
        "primary": "google/gemini-2.0-flash",
        "fallbacks": ["openai/gpt-4o"]
      },
      "models": {
        "anthropic/claude-opus-4-6": {"alias": "Opus"},
        "openai/gpt-4o": {"alias": "GPT4o"},
        "moonshot/kimi-k2.5": {"alias": "Kimi"}
      }
    }
  }
}
```

### 2.2 配置项说明

- `primary`：全局主模型，必填
- `fallbacks`：备用模型数组，按顺序降级
- `imageModel`：视觉任务专用模型，可选
- `models`：模型白名单 + 别名，限制可使用模型，提升安全性

---

## 三、模型认证体系：API Key 与 OAuth

OpenClaw 支持两种认证方式，密钥存储在安全文件，不硬编码主配置：

- 认证存储路径：`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- 支持多 Profile 轮转，同一提供商多个密钥 / 账号自动切换

### 3.1 API Key 认证（通用）

绝大多数提供商使用环境变量或配置注入：

| 提供商 | 环境变量 | 配置方式 |
| --- | --- | --- |
| Anthropic | `ANTHROPIC_API_KEY` | `openclaw onboard --auth-choice token` |
| OpenAI | `OPENAI_API_KEY` | `openclaw onboard --auth-choice openai-api-key` |
| Moonshot | `MOONSHOT_API_KEY` | 自定义提供商配置 |
| Z.AI | `ZAI_API_KEY` | `openclaw onboard --auth-choice zai-api-key` |

### 3.2 OAuth 认证（订阅 / 账号登录）

适合 ChatGPT Code、Gemini、Qwen 等订阅服务：

```bash
# OpenAI Codex 登录
openclaw models auth login --provider openai-codex --set-default
# Google Gemini CLI 登录
openclaw plugins enable google-gemini-cli-auth
openclaw models auth login --provider google-gemini-cli --set-default
# Qwen OAuth 登录
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

### 3.3 快速初始化向导

无需手动改配置，一键完成认证 + 模型设置：

```bash
openclaw onboard
```

---

## 四、内置主流提供商全配置

OpenClaw 内置支持数十家提供商，无需自定义配置，仅需认证 + 指定模型。

### 4.1 头部厂商配置

#### （1）Anthropic（推荐工具 / 长文本）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "anthropic/claude-opus-4-6"}
    }
  }
}
```

认证：`ANTHROPIC_API_KEY` 或 `claude setup-token` 粘贴

#### （2）OpenAI（通用 / 代码）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "openai/gpt-4o"}
    }
  }
}
```

认证：`OPENAI_API_KEY`

#### （3）Google Gemini（视觉 / 多模态）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "google/gemini-2.0-pro"}
    }
  }
}
```

认证：`GEMINI_API_KEY`

#### （4）Moonshot Kimi（中文 / 长上下文）

自定义提供商配置（OpenAI 兼容）：

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "moonshot/kimi-k2.5"}
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.ai/v1",
        "apiKey": "${MOONSHOT_API_KEY}",
        "api": "openai-completions",
        "models": [{"id": "kimi-k2.5", "name": "Kimi K2.5"}]
      }
    }
  }
}
```

### 4.2 本地模型

#### （1）Ollama（本地一键运行）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "ollama/llama3.3"}
    }
  }
}
```

前置：安装 Ollama → `ollama pull llama3.3`

#### （2）vLLM（本地高性能）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "vllm/your-model-id"}
    }
  }
}
```

认证：`export VLLM_API_KEY="vllm-local"`

### 4.3 统一网关

#### OpenRouter（聚合多模型）

```json
{
  "agents": {
    "defaults": {
      "model": {"primary": "openrouter/anthropic/claude-sonnet-4-5"}
    }
  }
}
```

认证：`OPENROUTER_API_KEY`

---

## 五、自定义模型提供商（兼容代理）

支持接入任意 OpenAI/Anthropic 兼容接口，如本地代理、中转服务：

### 5.1 配置模板

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "custom-proxy": {
        "baseUrl": "https://your-proxy.com/v1",
        "apiKey": "${PROXY_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "custom-model",
            "name": "自定义模型",
            "contextWindow": 128000,
            "maxTokens": 4096,
            "input": ["text", "image"]
          }
        ]
      }
    }
  }
}
```

### 5.2 协议类型

- `openai-completions`：OpenAI 兼容协议
- `anthropic-messages`：Anthropic 兼容协议
- `openai-embeddings`：向量模型专用

---

## 六、模型切换与管理（CLI + 聊天指令）

### 6.1 CLI 全命令集

```bash
# 查看当前模型状态（主模型+备用+认证）
openclaw models status
openclaw models status --check # 自动化校验，异常退出码

# 列出模型（默认已配置，--all=全量）
openclaw models list
openclaw models list --all --provider anthropic

# 设置全局主模型
openclaw models set anthropic/claude-opus-4-6
# 设置全局图像模型
openclaw models set-image google/gemini-2.0-flash

# 别名管理
openclaw models aliases add Opus anthropic/claude-opus-4-6
openclaw models aliases list

# 备用模型管理
openclaw models fallbacks add openai/gpt-4o
openclaw models fallbacks list
openclaw models fallbacks clear

# OpenRouter 免费模型扫描
openclaw models scan --provider openrouter --set-default
```

### 6.2 聊天内热切换（/model 指令）

无需重启网关，当前会话立即生效：

```bash
# 打开模型选择器
/model
# 列出所有可用模型
/model list
# 按序号选择
/model 2
# 按模型名选择
/model openai/gpt-4o
# 查看当前模型详情
/model status
```

### 6.3 模型白名单管控

配置 `agents.defaults.models` 后，仅允许列表内模型：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-opus-4-6": {"alias": "Opus"},
        "openai/gpt-4o": {"alias": "GPT4o"}
      }
    }
  }
}
```

违规选择提示：`Model is not allowed`

---

## 七、故障转移与自动降级（高可用核心）

OpenClaw 实现**两级故障转移**，确保服务不中断：

1. 提供商内：多认证 Profile 轮转
2. 提供商间：备用模型列表降级

### 7.1 认证 Profile 轮转

同一提供商多个密钥 / 账号，自动按顺序切换：

- 轮转顺序：`auth.order` 配置 > 存储 Profile 列表
- 排序规则：OAuth > API Key，最久未使用优先
- 会话粘性：同一会话固定 Profile，提升缓存命中率

### 7.2 冷却策略

失败 Profile 自动冷却，避免频繁重试：

- 冷却指数退避：1min → 5min → 25min → 1h（上限）
- 冷却状态存储：`auth-profiles.json` → `usageStats`
- 计费失败（余额不足）：禁用 5h→24h，而非短时冷却

### 7.3 模型降级规则

仅以下故障触发降级：

- 认证失败 / 密钥过期
- 限流 429 错误
- 网关超时

**无效请求（参数错误）不降级**

### 7.4 高可用配置示例

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["openai/gpt-4o", "moonshot/kimi-k2.5"]
      }
    }
  },
  "auth": {
    "order": {
      "anthropic": ["anthropic:key1", "anthropic:key2"],
      "openai": ["openai:account1", "openai:account2"]
    }
  }
}
```

---

## 八、图像模型专用体系

视觉任务（图片理解、截图分析）使用独立模型，不占用主模型配额：

### 8.1 启用配置

```json
{
  "agents": {
    "defaults": {
      "imageModel": {
        "primary": "google/gemini-2.0-flash",
        "fallbacks": ["openai/gpt-4o"]
      }
    }
  }
}
```

### 8.2 触发逻辑

- 消息含图片 / 截图 → 自动路由至图像模型
- 图像模型故障 → 回退至主模型（支持视觉）
- 主模型无视觉能力 → 提示无法处理

---

## 九、高级能力：模型扫描与注册表

### 9.1 OpenRouter 免费模型扫描

自动发现、探测、设置免费模型：

```bash
openclaw models scan \
  --provider openrouter \
  --min-params 7 \
  --max-age-days 30 \
  --set-default
```

探测维度：图像支持、工具调用、上下文长度、延迟

### 9.2 模型注册表（models.json）

自定义提供商存储路径：`~/.openclaw/agents/<agentId>/models.json`

- 合并模式（默认）：自定义 + 内置提供商
- 替换模式：仅使用自定义配置

---

## 十、多智能体模型隔离

多智能体场景下，每个智能体可独立配置模型，完全隔离：

```json
{
  "agents": {
    "list": [
      {
        "id": "work",
        "model": {"primary": "anthropic/claude-sonnet-4-5"}
      },
      {
        "id": "personal",
        "model": {"primary": "moonshot/kimi-k2.5"}
      }
    ]
  }
}
```

---

## 十一、场景化最佳实践

### 11.1 企业生产（高可用）

- 主模型：Anthropic Opus
- 备用：GPT-4o + Kimi
- 图像模型：Gemini 2.0
- 开启多密钥轮转 + 冷却策略

### 11.2 个人助理（平衡成本）

- 主模型：Claude Sonnet
- 备用：GPT-4o mini
- 本地兜底：Ollama llama3
- 图像模型：GPT-4o

### 11.3 代码开发（工具优先）

- 主模型：OpenAI GPT-4o / Anthropic Opus
- 专用 Codex：openai-codex/gpt-5.3-codex
- 开启工具调用白名单

### 11.4 本地隐私（无外网）

- 主模型：Ollama qwen2.5
- 禁用云端模型
- 所有认证本地完成

---

## 十二、常见问题排查

### 12.1 Model is not allowed

- 原因：模型不在白名单 `agents.defaults.models`
- 解决：添加模型至白名单或删除白名单配置

### 12.2 所有模型认证失败

- 原因：密钥过期 / 限流 / 网络故障
- 解决：`openclaw models status` 检查认证，更新密钥

### 12.3 本地模型不生效

- 原因：Ollama 未启动 / 模型未拉取
- 解决：`ollama list` 校验，重启 Ollama 服务

### 12.4 降级不触发

- 原因：错误为无效请求，非可降级故障
- 解决：检查请求参数，确认错误类型

---

## 总结

OpenClaw 模型体系以**多提供商兼容、两级故障转移、会话热切换、权限白名单**为核心，构建了企业级高可用推理引擎。从云端头部模型到本地私有部署，从通用对话到专业代码 / 视觉任务，均可通过标准化配置实现最优匹配。遵循**主备兜底、密钥轮转、模型隔离**三大原则，即可搭建稳定、安全、高效的智能体推理底座。
