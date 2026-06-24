---
title: OpenCode 切换模型使用教程
order: 6
---

# OpenCode 切换模型使用教程

OpenCode **支持 75+ 主流大模型提供商**，兼容公有云商用模型、本地离线模型、官方订阅模型等多种类型，并提供了模型变体、参数精细化调控等能力，可适配代码编写、重构、Bug 修复、复杂逻辑分析等不同开发场景。

模型切换与配置是使用 OpenCode 的核心操作，无论是临时更换模型、固定项目默认模型，还是对接本地私有化模型、官方专属模型服务，都有对应的标准化流程。本文将从零开始，全面讲解 OpenCode 模型切换、配置、管理与故障排查的全流程，兼顾新手快速上手与高阶个性化配置需求。

## 二、核心基础概念

在学习模型切换前，先明确 OpenCode 中与模型相关的核心术语和官方服务，避免后续操作出现概念混淆。

### 2.1 核心术语

1. **提供商（Provider）**
即大模型服务提供方，如 OpenAI、Anthropic、Ollama、Azure OpenAI 等。所有模型都归属对应提供商，**必须先完成提供商授权**（配置 API 密钥、云服务凭证等），才能使用旗下模型。提供商凭据默认存储在 `~/.local/share/opencode/auth.json` 文件中。

2. **模型 ID**
模型的唯一标识，标准格式为 `provider_id/model_id`，是切换模型、配置默认模型的核心依据，不同提供商的模型 ID 命名规则独立。

3. **模型变体（Variant）**
同一模型的多套参数组合，可针对推理强度、思考 Token 预算、输出风格等进行区分。无需重复新增模型，通过变体即可快速适配简单调试、复杂开发等不同场景。

### 2.2 官方专属模型服务

OpenCode 推出两款官方模型服务，也是主流使用选择：

1. **OpenCode Zen**
处于测试阶段的精选模型网关，整合了 GPT、Claude、Gemini、Kimi、通义千问等多款经过基准测试的优质模型，采用**按量付费**模式，同时提供多款永久免费模型，适配绝大多数编码场景。

2. **OpenCode Go**
Beta 阶段的低成本订阅服务，主打开源编程大模型，定价为首月 5 美元、后续每月 10 美元，设有固定调用额度限制，适合长期使用开源模型的开发者。

## 三、基础操作：终端命令即时切换模型

若仅需**临时切换模型**（单次会话、临时测试），无需修改配置文件，使用 OpenCode 内置终端命令即可快速完成，这也是日常最常用的切换方式。

### 3.1 前置条件

已通过 `/connect` 命令完成目标提供商的授权，确保该提供商的 API 密钥、云服务凭证等配置正常生效。

### 3.2 可视化切换：/models 命令

该命令会加载所有已授权的提供商及旗下全部可用模型，支持可视化选择切换，操作步骤如下：

1. 打开终端，执行指令启动 OpenCode 终端交互界面（TUI）：

```bash
opencode
```

2. 在交互界面中输入核心切换命令并回车：

```bash
/models
```

3. 终端会列出所有可用提供商、模型名称与简要信息，通过上下方向键选中目标模型，按下回车键即可完成切换。当前会话会立即生效，全程无需重启程序。

### 3.3 启动指定模型：命令行参数临时指定

如果希望**启动 OpenCode 时直接加载目标模型**，可使用 `--model`（简写 `-m`）命令行参数，格式严格遵循 `provider_id/model_id`：

```bash
# 完整参数写法
opencode --model anthropic/claude-sonnet-4-5

# 简写写法（推荐）
opencode -m opencode/gpt-5.4-mini
```

该方式仅对**当前启动的单次会话**生效，不会修改全局或项目的默认模型配置。

## 四、持久化配置：设置全局 / 项目默认模型

针对长期固定使用某款模型的场景，推荐通过 `opencode.json` 或 `opencode.jsonc`（支持代码注释）配置文件设置默认模型。OpenCode 采用**配置合并、高优先级覆盖低优先级**的规则，可区分全局用户配置与项目独立配置。

### 4.1 配置文件加载优先级

配置文件按以下顺序加载，后方配置优先级更高，会覆盖前方冲突项（非冲突配置会全部保留）：

1. 远程组织配置（`.well-known/opencode`，组织统一默认配置）；

2. 全局用户配置（`~/.config/opencode/opencode.json`，当前用户所有项目生效）；

3. 自定义配置（`OPENCODE_CONFIG` 环境变量指定的配置文件）；

4. 项目级配置（项目根目录 `opencode.json`，仅当前项目生效，优先级最高）；

5. 运行时内联配置（`OPENCODE_CONFIG_CONTENT` 环境变量，临时运行时覆盖）。

### 4.2 全局默认模型（全项目生效）

全局配置作用于当前系统登录用户的所有 OpenCode 会话，配置文件固定路径为 `~/.config/opencode/opencode.json`。

1. 新建 / 编辑全局配置文件，写入基础配置：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // 主默认模型（代码开发、逻辑分析主力模型）
  "model": "anthropic/claude-haiku-4-5",
  // 轻量任务专用小模型（生成会话标题、简短文本解析等）
  "small_model": "opencode/gpt-5-nano"
}
```

2. 保存文件后，重启 OpenCode，所有新项目、已有项目都会默认使用该套模型配置。

### 4.3 项目级默认模型（单项目生效）

不同项目可能需要匹配不同能力的模型（如大型项目用强推理模型、小型脚本用轻量模型），可在**项目根目录**创建 `opencode.json`，该配置优先级高于全局配置，还可提交至 Git 实现团队统一规范。
示例（适配 OpenCode Zen 模型）：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/kimi-k2.5",
  "small_model": "opencode/minimax-m2.5-free"
}
```

## 五、进阶玩法：模型变体配置与切换

GPT、Claude、Gemini 等主流模型支持**模型变体**功能，针对推理强度、思考 Token 预算、输出格式划分多套参数方案，无需重复添加模型，即可快速适配不同开发场景。

### 5.1 主流提供商内置变体

OpenCode 为头部 AI 提供商预设了通用变体，开箱即用：

1. **Anthropic（Claude 系列）**

    - `high`：高思考 Token 预算（默认变体），适配常规代码开发；

    - `max`：最大思考预算，适合大型项目架构分析、复杂代码重构。

2. **OpenAI（GPT 系列）**
按推理强度分级：`none`（无推理，极速响应）、`minimal`、`low`、`medium`、`high`、`xhigh`（超高推理，复杂逻辑专用）。

3. **Google（Gemini 系列）**

    - `low`：低推理预算，适合简单 Bug 修复；

    - `high`：高推理预算，适配多文件联动开发。

### 5.2 自定义模型变体

可在配置文件中为指定模型新增个性化变体，自定义推理、输出等参数，示例如下：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "opencode": {
      "models": {
        "gpt-5": {
          "variants": {
            // 复杂重构专用变体：高推理、精简输出
            "high-rebuild": {
              "reasoningEffort": "high",
              "textVerbosity": "low"
            },
            // 快速调试专用变体：低推理、极速响应
            "fast-debug": {
              "reasoningEffort": "low"
            }
          }
        }
      }
    }
  }
}
```

### 5.3 快捷键快速切换变体

配置变体后，无需修改配置文件，使用内置快捷键 `variant_cycle` 即可在当前模型的所有变体之间**循环切换**，大幅提升操作效率。

## 六、全场景实战：不同类型提供商模型接入与切换

OpenCode 支持商用云模型、本地离线模型、自定义兼容接口、官方 Zen/Go 四大类模型，不同类型的接入、授权、切换流程存在差异，本节分场景逐一讲解。

### 6.1 主流商用云模型（OpenAI/Anthropic/Azure/Amazon Bedrock）

这类模型为公有云在线服务，需提前在对应平台申请 API 密钥或配置云服务凭证。

#### 通用接入流程

1. 终端执行 `/connect`，在提供商列表中选中目标服务商（如 OpenAI、Amazon Bedrock）；

2. 根据终端指引完成授权：粘贴 API 密钥、配置云平台环境变量或本地凭证文件；

3. 授权完成后执行 `/models`，选中模型即可切换使用。

#### 典型示例：Amazon Bedrock 专属配置

Amazon Bedrock 支持 AWS 区域、配置文件、VPC 端点等个性化配置，可写入 `opencode.json` 持久化：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "amazon-bedrock": {
      "options": {
        "region": "us-east-1",
        "profile": "my-aws-profile"
      }
    }
  }
}
```

> 补充说明：Amazon Bedrock 认证存在优先级，`AWS_BEARER_TOKEN_BEDROCK` 令牌优先级高于 AWS 密钥、本地配置文件等其他认证方式。
> 
> 

### 6.2 本地离线模型（Ollama/LM Studio/llama.cpp）

适用于隐私敏感、断网、内网隔离等场景，需**先启动本地模型服务**，再配置 OpenCode 对接本地端口。

#### 示例 1：Ollama 本地模型配置

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (本地模型)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "llama2": {
          "name": "Llama 2 本地编码模型"
        }
      }
    }
  }
}
```

> 补充说明：若出现工具调用异常，建议调大 Ollama 的 `num_ctx` 参数，推荐设置为 16k~32k 提升上下文承载能力。
> 
> 

#### 示例 2：LM Studio 本地模型配置

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (本地模型)",
      "options": {
        "baseURL": "http://127.0.0.1:1234/v1"
      }
    }
  }
}
```

配置完成后执行 `/models`，即可选择本地模型完成切换。

### 6.3 自定义 OpenAI 兼容提供商

市面上多数第三方 AI 接口兼容 OpenAI API 协议，可通过 OpenCode 的 `Other` 选项自定义接入：

1. 启动 OpenCode，执行 `/connect`，下滑选择列表底部的 `Other`；

2. 输入自定义提供商 ID（自定义名称，后续配置需保持一致）；

3. 粘贴第三方接口的 API 密钥，完成临时授权；

4. 在配置文件中补充接口地址、模型参数：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "my-custom-api": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "自定义兼容接口",
      "options": {
        "baseURL": "https://api.example.com/v1"
      },
      "models": {
        "code-model": {
          "name": "第三方编码模型",
          "limit": {
            "context": 200000,
            "output": 65536
          }
        }
      }
    }
  }
}
```

5. 保存配置后，执行 `/models` 即可选择自定义模型。

### 6.4 OpenCode Zen 官方精选模型

Zen 是新手入门首选，整合免费、付费两类模型，接入与切换流程如下：

1. 执行 `/connect`，在列表中选择 `opencode`（OpenCode Zen）；

2. 根据指引跳转至 `opencode.ai/auth` 页面，登录账号、补充账单信息，复制生成的 API 密钥并粘贴到终端；

3. 执行 `/models` 查看全部 Zen 模型，**模型 ID 统一使用 ****`opencode/原始模型ID`**** 格式**。

Zen 提供多款永久免费模型（MiniMax M2.5 Free、Qwen3.6 Plus Free 等），可零成本体验；付费模型按 Token 阶梯计费，也可访问 `https://opencode.ai/zen/v1/models` 获取完整模型元数据与定价表。

### 6.5 OpenCode Go 低成本订阅模型

OpenCode Go 专注开源编程模型，采用订阅制并设有调用额度限制：

1. 登录 OpenCode Zen 控制台，完成 OpenCode Go 订阅；

2. 执行 `/connect`，选择 `OpenCode Go`，粘贴订阅对应的 API 密钥；

3. 模型 ID 格式为 `opencode-go/原始模型ID`，执行 `/models` 即可选择切换。

> 补充说明：OpenCode Go 存在 5 小时、每周、每月三层美元额度限制，超出限制后可切换 Zen 免费模型继续使用。
> 
> 

## 七、高阶配置：模型精细化参数调控

针对网关路由、Token 限制、LLM 监控等专业场景，可对模型进行精细化参数配置，进一步适配生产环境需求。

### 7.1 上下文与输出 Token 限制

通过 `limit` 字段限制模型最大输入、输出 Token，避免超长上下文溢出：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llama.cpp": {
      "models": {
        "qwen3-coder:a3b": {
          "limit": {
            "context": 128000,
            "output": 65536
          }
        }
      }
    }
  }
}
```

### 7.2 多网关路由策略

对接 Vercel AI Gateway、Cloudflare AI Gateway 等聚合网关时，可配置提供商优先级、访问限制：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "vercel": {
      "models": {
        "anthropic/claude-sonnet-4": {
          "options": {
            "order": ["anthropic", "vertex"], // 提供商尝试顺序
            "only": ["anthropic"] // 仅允许指定提供商
          }
        }
      }
    }
  }
}
```

### 7.3 自定义请求头（监控 / 缓存场景）

对接 Helicone 等 LLM 监控平台时，可添加自定义请求头实现会话跟踪、响应缓存：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "helicone": {
      "options": {
        "baseURL": "https://ai-gateway.helicone.ai",
        "headers": {
          "Helicone-Cache-Enabled": "true",
          "Helicone-User-Id": "dev-01"
        }
      }
    }
  }
}
```

## 八、提供商全局管理：启用与禁用规则

当系统中存在多个提供商时，可通过黑白名单限制可用服务，精简模型列表、规避误操作。

### 8.1 禁用指定提供商（黑名单）

使用 `disabled_providers` 字段，彻底禁用目标提供商（即使存在有效密钥也无法使用）：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "disabled_providers": ["openai", "gemini"]
}
```

### 8.2 仅启用指定提供商（白名单）

使用 `enabled_providers` 字段，仅允许列表内的提供商生效：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "enabled_providers": ["anthropic", "opencode"]
}
```

> 补充说明：`disabled_providers` 优先级高于 `enabled_providers`，若同一提供商同时出现在两个列表中，以禁用规则为准。
> 
> 

### 8.3 查看已授权提供商

执行以下命令，快速查看当前系统所有已完成授权的提供商与凭据状态：

```bash
opencode auth list
```

## 九、常见问题与故障排查

1. **执行 ****`/models`**** 看不到目标模型**
排查方向：检查对应提供商 API 密钥是否过期，重新执行 `/connect` 授权；核对配置文件中 `provider_id` 与授权时填写的 ID 完全一致；本地模型需确认本地服务正常启动、端口与 `baseURL` 匹配。

2. **Ollama 本地模型工具调用失效**
解决方案：调大 Ollama `num_ctx` 参数，推荐取值 16384~32768，提升上下文承载能力。

3. **OpenCode Zen/Go 模型调用失败**
排查方向：登录 Zen 控制台检查账户余额、订阅状态；核对是否超出 OpenCode Go 额度限制；切换免费模型测试网络连通性。

4. **模型变体配置不生效**
排查方向：检查变体名称拼写是否错误；确认代理配置未覆盖全局模型变体；重启 OpenCode 重载配置文件。

5. **Amazon Bedrock 认证异常**
解决方案：遵循认证优先级，优先检查 `AWS_BEARER_TOKEN_BEDROCK` 环境变量；使用配置文件时，核对 AWS 区域、profile 名称是否正确。

## 十、通用使用注意事项

1. 模型 ID 必须严格遵循 `provider_id/model_id` 格式，Zen 模型前缀为 `opencode/`、Go 模型前缀为 `opencode-go/`，字符拼写、大小写错误会直接导致模型加载失败。

2. 部署本地模型时，需保证本地服务端口、配置文件中 `baseURL` 完全一致，防火墙、端口占用会造成连接失败。

3. 对接 AWS、Azure 等云服务商时，优先使用配置文件持久化凭证，避免临时环境变量导致认证丢失。

4. 自定义 OpenAI 兼容接口时，需区分接口协议：`/v1/chat/completions` 使用 `@ai-sdk/openai-compatible`，`/v1/responses` 使用 `@ai-sdk/openai`。

5. 团队协作场景中，项目级 `opencode.json` 建议统一模型配置，保证全体成员开发环境一致。

6. OpenCode Go 有固定调用额度，高频使用需合理规划调用量，超出额度后建议切换 Zen 免费模型。

## 十一、总结

OpenCode 的模型切换体系分为**临时切换**与**持久化配置**两大模式，可根据使用场景灵活选择：单次测试、临时调试优先使用 `/models` 命令可视化切换；长期开发、团队协作推荐配置全局 / 项目默认模型。

场景选择参考：新手入门、通用编码优先使用 OpenCode Zen；追求低成本开源模型选择 OpenCode Go；隐私隔离、内网环境使用 Ollama、LM Studio 等本地模型；企业私有化部署可对接自定义 OpenAI 兼容接口。

配合模型变体、参数精细化配置、提供商黑白名单等能力，可充分发挥不同大模型的优势，适配从个人开发到企业团队的全场景需求。日常使用中定期检查提供商授权、账户额度，可有效规避绝大多数使用故障。
