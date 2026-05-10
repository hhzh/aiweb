# HyperFrames 视频渲染框架使用教程：从初始化到高效渲染

HyperFrames 是 HeyGen 开源的**HTML 原生视频渲染框架**，主打 AI 代理友好、零构建、确定性渲染，用 HTML+CSS+GSAP 即可快速创作、预览、导出 MP4 视频，适配自动化视频生产、AI 驱动剪辑、数据可视化视频等场景，采用 Apache 2.0 开源协议，商用无限制。

---

## 一、核心优势

- **HTML 原生**：无需 React / 专有 DSL，直接用 HTML 编写视频 composition，浏览器可直接打开预览。

- **AI 优先**：天然适配 Claude/Cursor/Gemini 等 AI 编码代理，支持自然语言生成视频，其中与 Claude（Claude Code、Claude Design）适配性最优，可通过插件或技能快速调用框架能力。

- **确定性渲染**：相同输入必产出相同视频，适合自动化流水线。

- **多动画兼容**：支持 GSAP、Lottie、Three.js、CSS 动画、WAAPI 等主流 runtime。

- **零构建成本**：无需打包，index.html 即写即看。

---

## 二、环境前置准备

1. 安装 **Node.js ≥ 22**

2. 安装 **FFmpeg**（用于视频编码）

3. 开发需安装 **Git LFS**（处理测试视频文件）

```bash
# Git LFS 安装（macOS）
brew install git-lfs
# Ubuntu/Debian
sudo apt install git-lfs
# 初始化
git lfs install
```

---

## 三、快速上手（两种方式）

### 方式 1：AI 代理驱动（官方推荐）

适合快速生成视频，无需手动写大量代码，其中配合 Claude 使用是最便捷的方式，以下为 Claude 专属操作流程

```bash
# 安装 HyperFrames 技能（供 Claude 调用）
npx skills add heygen-com/hyperframes
```

安装后在 Claude 中（优先 Claude Code、Claude Design）用指令生成，两种 Claude 版本操作差异如下：

- `/hyperframes`：创作视频 composition（所有 Claude 版本通用）

- `/hyperframes-cli`：执行 CLI 命令（所有 Claude 版本通用）

- `/gsap`/`/lottie`/`/three`：调用对应动画能力（所有 Claude 版本通用）

- Claude Design 额外支持：导入框架设计模板，快速生成视觉化视频草稿（具体步骤见第五部分实战案例）

示例提示词（适配 Claude Code，可直接复制使用）：

```text
使用 /hyperframes 生成10秒产品介绍视频，含淡入标题、背景视频、背景音乐，要求：标题为“HyperFrames 视频渲染工具”，背景视频用轻量动态粒子效果，背景音乐音量0.3，结尾添加1秒淡出效果，生成完整可直接预览的 HTML 代码和对应的 CLI 预览、渲染命令。
```

### 方式 2：手动创建项目

适合自主开发、精细调试，创建后可将项目代码复制到 Claude 中，让 AI 协助优化动画或修改结构

```bash
# 初始化项目
npx hyperframes init my-video
cd my-video
# 浏览器实时预览（热更新）
npx hyperframes preview
# 渲染输出 MP4
npx hyperframes render
```

`init` 会自动安装技能，可随时切回 AI 代理模式，将项目目录结构复制到 Claude，可提示 AI 优化代码（示例提示词：“帮我优化 my-video 项目中的 index.html，添加 GSAP 淡入淡出动画，调整图层轨道顺序，确保预览无异常”）。

---

## 四、视频编写核心规范

### 1. 基础结构（data 属性定义时间轴）

用 `data-*` 属性声明图层时间、尺寸，类似 AE 轨道管理，以下代码可直接复制到 Claude，让 AI 替换内容、调整参数：

```html
<!-- 舞台容器 -->
<div id="stage" 
  data-composition-id="my-video" 
  data-start="0" 
  data-width="1920" 
  data-height="1080">

  <!-- 视频图层：0秒开始，持续5秒，轨道0 -->
  <video id="clip-1"
    data-start="0"
    data-duration="5"
    data-track-index="0"
    src="intro.mp4"
    muted playsinline>
  </video>

  <!-- 图片叠加层：2秒开始，持续3秒，轨道1 -->
  <img id="overlay"
    class="clip"
    data-start="2"
    data-duration="3"
    data-track-index="1"
    src="logo.png">

  <!-- 音频：0秒开始，持续9秒，音量0.5，轨道2 -->
  <audio id="bg-music"
    data-start="0"
    data-duration="9"
    data-track-index="2"
    data-volume="0.5"
    src="music.wav">
  
</div>
```

**必填属性**：

- `data-start`：开始时间（秒）

- `data-duration`：持续时长（秒）

- `data-track-index`：图层轨道索引

- 带时间属性的元素需加 `class="clip"`。

### 2. 动画集成（以 GSAP 为例）

```javascript
// 创建暂停状态时间轴
const tl = gsap.timeline({ paused: true });
// 注册到全局供 HyperFrames 控制
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;

// 标题淡入动画
tl.from(".title", {
  y: 100,
  opacity: 0,
  duration: 1,
  ease: "power3.out"
}, 0.2);
```

提示：将上述代码复制到 Claude，可添加提示词“帮我修改这个 GSAP 动画，将标题淡入改为从左向右滑动， duration 调整为1.5秒，添加缓动效果”，AI 会直接输出修改后的代码，无需手动调试。

---

## 五、内置组件库与 AI 技能

### 1. 一键添加预制组件

```bash
npx hyperframes add flash-through-white      # 转场特效
npx hyperframes add instagram-follow         # 社交挂件
npx hyperframes add data-chart               # 动态图表
```

完整组件库：[hyperframes.heygen.com/catalog](https://hyperframes.heygen.com/catalog)（注：当前网页解析失败，可通过 Claude 提示词“列出 HyperFrames 所有预制组件及添加命令”获取组件清单）

### 2. 核心 AI 技能

|技能|功能|
|---|---|
|hyperframes|视频创作、字幕、TTS、转场（Claude 核心调用技能）|
|hyperframes-cli|CLI 命令（init/render/tts 等，Claude 可生成完整命令）|
|website-to-hyperframes|网页转视频（Claude 可直接生成转换命令）|
|remotion-to-hyperframes|Remotion 项目迁移（Claude 可协助转换代码）|
|gsap/lottie/three|对应动画 runtime 适配（Claude 可生成适配代码）|

### 3. 实战案例：配合 Claude 使用（核心重点）

以下案例覆盖 Claude Code、Claude Design 两种常用场景，步骤可直接实操，解决“AI 驱动视频创作”的核心需求，所有提示词可直接复制使用。

#### 案例1：Claude Code 生成完整视频（零基础，无需写代码）

1. 前置准备：已安装 Node.js、FFmpeg，执行 `npx skills add heygen-com/hyperframes` 安装技能，打开 Claude Code（网页版/客户端均可）。

2. 输入提示词（精准控制视频参数，避免 AI 输出无效代码）：
`使用 /hyperframes 生成15秒短视频，主题为“HyperFrames 框架介绍”，要求：

        1. 尺寸1080*1920（竖屏，适配抖音），帧率30fps；

        2. 开头2秒淡入标题“HyperFrames”，字体加粗、白色，背景为蓝色渐变；

        3. 中间10秒显示核心优势（HTML 原生、AI 优先、零构建），每3秒切换一个优势，配简单文字动画；

        4. 结尾3秒淡入“快速上手，高效渲染”文字，添加轻微缩放动画；

        5. 添加轻柔背景音乐，音量0.2，无杂音；

        6. 输出完整 HTML 代码（含所有依赖引入）、预览命令、渲染命令，确保代码可直接运行，无需修改。`

3. 执行操作：Claude 输出代码后，复制代码保存为 `index.html`，放在空文件夹中，执行 Claude 给出的预览命令（通常为 `npx hyperframes preview`），浏览器实时查看效果。

4. 优化调整：若对动画、文字不满意，继续向 Claude 输入提示词，例如：“将标题颜色改为白色，背景渐变改为蓝紫渐变，文字动画改为上下跳动，背景音乐音量调整为0.3”，AI 会自动修改代码，无需手动编辑。

5. 渲染导出：预览无误后，执行 Claude 给出的渲染命令（`npx hyperframes render`），等待片刻即可生成 MP4 视频文件。

#### 案例2：Claude Design 生成视觉化视频草稿（快速出图，再优化）

1. 前置准备：打开 Claude Design，访问 HyperFrames 官方仓库（https://github.com/heygen-com/hyperframes），找到 `docs/guides/claude-design-hyperframes.md` 文件，下载该文件。

2. 操作步骤：将下载的`claude-design-hyperframes.md` 文件上传到 Claude Design 聊天窗口，输入提示词：
`根据上传的 HyperFrames 设计模板，生成一个20秒的产品宣传视频草稿，主题为“AI 驱动的 HTML 视频渲染工具”，要求：视觉风格简洁大气，以白色、蓝色为主色调，包含产品 LOGO 占位、核心功能介绍文字，添加简单转场特效，输出可直接导入 HyperFrames 预览的 HTML 代码和设计说明。`

3. 后续操作：Claude Design 会生成视觉化风格的视频草稿代码，复制代码到本地，替换 LOGO 等占位资源，再通过 Claude Code 优化动画细节（例如添加 GSAP 时间轴、调整图层顺序），最后预览、渲染。

#### 案例3：Claude 协助调试代码（解决实操报错）

实操中遇到报错（如动画不生效、渲染失败），无需手动排查，可按以下步骤操作：

1. 复制报错信息（例如：“渲染失败，提示 FFmpeg 未找到”“动画不生效，控制台提示 window.\_\_timelines 未定义”）；

2. 复制自己编写的 HTML/JS 代码，一起发送给 Claude Code，输入提示词：
`我使用 HyperFrames 框架编写视频代码，出现了如下报错：[粘贴报错信息]，这是我的代码：[粘贴代码]，请帮我排查问题，修改代码并给出具体的解决步骤，确保修改后能正常预览和渲染。`

3. Claude 会快速定位问题（如路径错误、动画未注册、依赖缺失），输出修改后的代码和操作步骤，按提示修改即可解决问题。

---

## 六、HyperFrames vs Remotion 关键对比

|维度|HyperFrames|Remotion|
|---|---|---|
|编写方式|HTML+CSS+GSAP（Claude 可直接生成）|React TSX（Claude 生成后需调整适配）|
|构建步骤|无|必需打包|
|动画适配|原生支持多 runtime（Claude 可生成对应代码）|仅 React 生态|
|开源协议|Apache 2.0（完全开源）|源码可用（非 OSI 开源）|
|分布式渲染|单机|Lambda 生产级|

---

## 七、常见问题

1. **渲染报错**：检查 Node.js ≥22、FFmpeg 已安装，执行 `npx hyperframes doctor` 自检；若仍报错，复制报错信息和代码到 Claude，让 AI 排查。

2. **动画不生效**：确保动画时间轴注册到 `window.\_\_timelines`；可复制代码到 Claude，提示“检查动画不生效问题，修改代码确保动画正常显示”。

3. **Git LFS 错误**：安装 Git LFS 后重新克隆仓库；或执行 `GIT\_LFS\_SKIP\_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` 跳过 LFS 内容。

4. **AI 代理无响应**：重新执行 `npx skills add heygen-com/hyperframes`；若 Claude 无法调用技能，提示 Claude“重新加载 HyperFrames 技能，生成对应操作指令”。

5. **Claude 生成代码无法运行**：检查代码中依赖引入路径是否正确，可提示 Claude“优化代码，确保所有依赖路径正确，无需额外安装依赖即可运行”。

---

## 八、总结

HyperFrames 把**视频创作回归前端原生**，零学习成本、AI 友好、可版本管理，特别适合前端开发者、AI 自动化团队快速生产短视频、数据视频、营销视频。其中配合 Claude 使用可大幅降低开发成本，从需求描述到代码生成、调试优化，全程无需手动编写大量代码，仅需通过自然语言提示即可完成视频创作。从初始化到渲染仅需 3 行命令，配合 AI 技能可大幅提升视频生产效率。
