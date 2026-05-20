# Llama\.cpp 快速入门教程：从安装到核心用法

# llama\.cpp 快速入门教程

## 一、工具概述

llama\.cpp 是一款**纯 C/C\+\+ 开发的轻量级大语言模型（LLM）本地推理框架**，由 ggml\-org 团队维护，核心目标是**低依赖、高性能、跨硬件**，让普通电脑、嵌入式设备都能流畅运行主流大模型，无需云端服务。

它独创 GGUF 模型格式，支持 1\.5\~8 位极致量化，兼顾速度、效果与内存占用，是本地部署大模型的**行业标杆工具**，开源仓库地址：[https://github\.com/ggml\-org/llama\.cpp](https://github.com/ggml-org/llama.cpp)。

### 核心优势

- **极简无依赖**：纯 C/C\+\+ 编写，无 Python、Java 等重型依赖，编译后体积仅数 MB，适配低端设备；

- **极致量化**：支持 1\.5/2/3/4/5/6/8 位整数量化，模型体积最高压缩 75%，4GB 内存即可运行 7B 级模型；

- **全平台兼容**：适配 Windows/macOS/Linux，支持 x86、ARM、RISC\-V 架构，覆盖桌面、笔记本、树莓派、嵌入式 NPU；

- **全硬件加速**：原生支持 Apple Metal、NVIDIA CUDA、AMD HIP、Vulkan、Intel SYCL、华为 CANN 等，CPU 也有深度优化；

- **格式通用**：独创 GGUF 格式，加载快、兼容性强，已成为本地部署标准格式；

- **工具链完整**：内置对话、生成、API 服务、性能测试、模型转换、多模态推理等全套工具；

- **生态丰富**：支持数百款主流模型，配套 WebUI、开发框架绑定，社区插件完善。

## 二、安装指南（4 种方式，新手优先）

### 方式 1：预编译包（零编译，新手首选）

无需配置环境，直接下载解压即用，适配全系统全硬件。

1. 打开官方发布页：[https://github\.com/ggml\-org/llama\.cpp/releases](https://github.com/ggml-org/llama.cpp/releases)；

2. 找到最新稳定版（如 b9222），进入 Assets 列表；

3. 按**系统 \+ 硬件**匹配压缩包：

    - Windows：CPU 选 `llama\-bxxxx\-bin\-win\-cpu\-x64\.zip`，NVIDIA 选 `cuda` 版；

    - macOS：Apple Silicon（M1/M2/M3）选 `macos\-arm64`，Intel 选 `macos\-x64`；

    - Linux：CPU 选 `linux\-x64`，NVIDIA 选 `cuda` 版；

    - 嵌入式：Android、openEuler 等系统对应包；

4. 解压到**纯英文路径**（无中文、空格、特殊字符），解压后 `build/bin` 目录即为可执行文件。

### 方式 2：包管理器（一行命令，快速安装）

主流系统支持包管理器一键安装，自动更新，无需手动下载：

- **Windows（winget）**

```bash
winget install llama.cpp
```

- **macOS/Linux（Homebrew）**

```bash
brew install llama.cpp
```

- **macOS（MacPorts）**

```bash
sudo port install llama.cpp
```

- **Linux（Nix）**

```bash
# flake 模式
nix profile install nixpkgs#llama-cpp
# 传统模式
nix-env --file '<nixpk>' --install --attr llama-cpp
```

### 方式 3：Docker 容器（隔离环境，推荐进阶）

通过 Docker 快速部署，不污染本地环境，支持跨平台：

```bash
# 基础版（CPU）
docker run -p 8080:8080 -v /本地模型目录:/models ghcr.io/ggml-org/llama.cpp:server

# NVIDIA GPU版（需nvidia-docker）
docker run -p 8080:8080 -v /本地模型目录:/models --gpus all ghcr.io/ggml-org/llama.cpp:server-cuda
```

### 方式 4：源码编译（自定义配置，进阶）

适合需要开启特殊加速、自定义功能的用户。

#### 1\. 环境依赖

- macOS：安装 Xcode 命令行工具

```bash
xcode-select --install
```

- Linux（Ubuntu/Debian）：安装编译工具链

```bash
sudo apt update && sudo apt install build-essential git cmake
```

- Windows：安装 Visual Studio（勾选 C\+\+ 桌面开发）、CMake、Git

#### 2\. 编译命令

```bash
# 1. 克隆仓库
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# 2. 基础编译（CPU版，全平台通用）
cmake -B build
cmake --build build --config Release

# 3. 硬件加速编译（按需选择）
# Apple Silicon（Metal加速）
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release

# NVIDIA CUDA加速
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

# AMD HIP加速
cmake -B build -DGGML_HIP=ON
cmake --build build --config Release
```

编译完成后，可执行文件输出到 `build/bin` 目录。

#### 3\. 编译常见问题

- 编译失败：检查依赖是否完整，CMake 版本≥3\.16；

- CUDA 编译报错：确认显卡驱动、CUDA Toolkit 版本匹配；

- 路径错误：避免中文、空格路径，终端切换到英文模式。

## 三、获取 GGUF 模型

llama\.cpp 仅支持 **GGUF 格式模型**，优先选择 \\*\\4\-bit（Q4\_K\_M）\\\\* 量化版，平衡速度、效果、内存。

### 方式 1：Hugging Face 下载（主流首选）

1. 访问 GGUF 模型专区：[https://huggingface\.co/models?search=llama\+gguf](https://huggingface.co/models?search=llama+gguf)；

2. 热门模型推荐（中文友好）：

    - 轻量（1B\~3B）：gemma\-3\-1b\-it、Qwen\-2\.5\-1\.5B、MiniCPM；

    - 均衡（7B\~9B）：Qwen3\-8B、Llama 3\.1\-8B、ChatGLM4\-9B；

    - 高性能（13B\+）：Llama 3\-70B、Deepseek\-V2；

    - 多模态：Qwen2\-VL、LLaVA、Mini CPM；

3. 选择**量化版本**（推荐 Q4\_K\_M，兼顾速度与效果），下载 `\.gguf` 文件。

### 方式 2：命令直接下载（无需手动找）

通过 `\-hf` 参数，一键下载并运行 Hugging Face 模型：

```bash
# 下载并运行 gemma-3-1b-it 模型（默认Q4_K_M量化）
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF

# 指定量化版本（如Q2_K，极致省内存）
llama-cli -hf qwen/Qwen3-8B-GGUF:Q2_K
```

### 方式 3：模型转换（自定义模型）

将 Hugging Face 原生模型转为 GGUF 格式，仓库自带转换脚本：

```bash
# 基础转换（PyTorch→GGUF）
python convert_hf_to_gguf.py 原生模型目录 --out 输出模型.gguf

# 带量化转换（转为4-bit）
python convert_hf_to_gguf.py 原生模型目录 --out 输出模型.gguf --q4_k_m
```

## 四、核心用法（4 大场景，从入门到进阶）

### 1\. 本地对话（llama\-cli）

交互式聊天，支持上下文记忆、自定义对话模板。

#### 基础对话

```bash
# CPU运行，上下文4096
llama-cli -m 模型路径.gguf -c 4096

# GPU加速（卸载所有层到显卡）
llama-cli -m qwen3-8b-q4_k_m.gguf -ngl all -c 8192

# 指定中文对话模板
llama-cli -m chatglm4-9b.gguf --chat-template chatglm4
```

#### 常用核心参数

```bash
# 基础参数
-m：模型路径（必填）
-ngl N：GPU卸载层数（0=纯CPU，all=全卸载）
-c N：上下文窗口（默认2048，越大支持越长对话）
-t N：CPU线程数（建议等于物理核心数）

# 生成参数
-p：直接输入提示词（非交互式）
-n N：最大生成token数（默认-1，无限）
--temp N：温度（0=严谨，1=随机，默认0.8）
--repeat-penalty：重复惩罚（避免内容重复）

# 高级参数
--json-schema：输出JSON格式
--grammar：自定义输出语法规则
```

#### 示例：非交互式生成

```bash
# 生成3点总结，输出200字
llama-cli -m qwen3-8b-q4_k_m.gguf -p "用3点总结llama.cpp的核心优势" -n 200 --temp 0.5
```

### 2\. 多模态推理（图文理解）

支持 LLaVA、Qwen2\-VL、Mini CPM 等多模态模型，图文问答：

```bash
# 图文对话（加载模型+图片）
llama-cli -m qwen2-vl-7b-q4_k_m.gguf --mmproj 投影文件.gguf --image 图片.jpg -p "描述这张图片"
```

### 3\. 启动 API 服务（llama\-server）

搭建 OpenAI 兼容 API，支持多并发、WebUI、嵌入 / 重排序功能。

#### 基础服务（默认 8080 端口）

```bash
llama-server -m qwen3-8b-q4_k_m.gguf -ngl all
# 浏览器访问：http://localhost:8080，打开WebUI聊天
```

#### 进阶配置

```bash
# 自定义端口+4并发+上下文8192
llama-server -m qwen3-8b-q4_k_m.gguf -port 8000 -np 4 -c 8192

# 启动嵌入服务（用于知识库）
llama-server -m 嵌入模型.gguf --embedding

# 启用JSON输出+多模态
llama-server -m qwen2-vl-7b.gguf --json-schema '{"type":"object"}'
```

#### API 调用示例（curl）

```bash
curl http://localhost:8080/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
"model": "qwen3-8b",
"messages": [{"role":"user","content":"什么是llama.cpp"}]
}'
```

### 4\. 性能测试（llama\-bench）

测试模型推理速度，对比硬件性能：

```bash
# 基础测速
llama-bench -m qwen3-8b-q4_k_m.gguf

# 输出：模型大小、推理速度（t/s）、硬件信息
```

## 五、支持的模型与硬件

### 主流支持模型

- **中文文本**：Qwen、ChatGLM、Llama 3 中文微调、Baichuan、Yi；

- **英文文本**：Llama 2/3、Mistral、Gemma、Phi、Deepseek；

- **多模态**：LLaVA、Qwen2\-VL、Mini CPM、Moondream、LLaVA 1\.5/1\.6；

- **代码模型**：Deepseek\-Coder、StarCoder、CodeLlama。

### 支持硬件

- 苹果：M1/M2/M3 系列（Metal 加速，性能最优）；

- NVIDIA：RTX 20/30/40 系列、Quadro；

- AMD：RX 6000/7000 系列（HIP/Vulkan）；

- 英特尔：CPU、Arc 显卡（SYCL）；

- 国产：华为昇腾 NPU、摩尔线程 GPU；

- 嵌入式：树莓派、Android、openEuler、Hexagon 处理器。

## 六、常见问题

1. **模型加载失败**：路径含中文 / 空格、非 GGUF 格式、模型损坏，重新下载或换路径；

2. **GPU 不生效**：编译未开启对应加速、`\-ngl 0`、显卡驱动过低；

3. **内存不足**：选 Q2\_K/Q3\_K 低量化、减小 `\-c`、关闭后台程序；

4. **推理速度慢**：开启 GPU、增加 `\-t`、关闭杀毒 / 后台占用；

5. **输出乱码**：模型不支持中文、未指定中文模板，换中文模型。

## 七、总结

llama\.cpp 是本地部署大模型的**全能工具**，轻量无依赖、跨硬件、高性能，新手用预编译包 \+ 4\-bit 量化模型即可快速上手，进阶可自定义加速、多模态、API 服务，覆盖个人聊天、开发测试、嵌入式部署等全场景。

关注官方仓库：[https://github\.com/ggml\-org/llama\.cpp](https://github.com/ggml-org/llama.cpp)，获取多模态、投机解码、函数调用等最新功能。

要不要我把文中的核心命令整理成一份**可直接复制的速查表**，方便你快速查阅？
