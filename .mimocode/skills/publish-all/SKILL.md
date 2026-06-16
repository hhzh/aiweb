---
name: publish-all
description: 一键发布 Markdown 文章到所有平台（CSDN、掘金、InfoQ、腾讯云、51CTO、知乎、博客园、思否、阿里云）。提供 Markdown 文件路径即可自动串行发布到 9 个平台。阿里云放在最后一个发布（需手动登录）。
---

# Publish All Skill

一键发布 Markdown 文章到所有平台。提供 Markdown 文件路径，自动串行发布到 9 个平台。

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into ALL target platforms (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Input

- **Required**: Markdown file path (e.g., `/path/to/article.md`)
- **Optional**: `publishTitle` — 发布标题（优化后的标题，用于网站展示，不修改本地文件）
- If `publishTitle` is not provided, title is extracted from the first `# ` heading in the file
- Content skips YAML frontmatter automatically

## Publish Order

Publish to platforms in this fixed serial order. Problematic and session-sensitive platforms go first for early error detection:

1. 51CTO (most error-prone, handle first while attention is fresh)
2. **思否 (SegmentFault)** (session expires easily, check early)
3. CSDN
4. 掘金 (Juejin)
5. InfoQ
6. 腾讯云 (Tencent Cloud)
7. 知乎 (Zhihu)
8. 博客园 (Cnblogs)
9. 阿里云 (Aliyun) (session expires often, needs manual login — put last)

## Workflow

### Step 0: Extract Article Info & Prepare Content

Read the Markdown file to extract the title, verify the file exists, and prepare all content formats upfront:

```bash
# Extract title from first heading
originalTitle=$(grep -m1 '^# ' /path/to/article.md | sed 's/^# //')

# Verify file exists
if [ ! -f "/path/to/article.md" ]; then
  echo "Error: File not found"
  exit 1
fi

# Prepare content without frontmatter (skip YAML --- blocks)
sed -n '/^# /,$p' /path/to/article.md > /tmp/publish_content.md

# Prepare JSON-encoded content (for CodeMirror API injection - cnblogs)
python3 -c "
import json
with open('/tmp/publish_content.md', 'r') as f:
    content = f.read()
print(json.dumps(content))
" > /tmp/publish_content.json

# Prepare base64-encoded content (for CodeMirror editors - juejin, tencent)
cat /tmp/publish_content.md | base64 | tr -d '\n' > /tmp/publish_content_b64.txt

# Copy plain text content to clipboard (for paste-based editors - csdn, infoq, 51cto, segmentfault)
cat /tmp/publish_content.md | pbcopy

# Prepare inline-style HTML for Zhihu (Draft.js no longer supports Markdown)
python3 -c "
import html as h, re, sys
with open('/tmp/publish_content.md','r') as f: content = f.read()
lines = content.split('\n')
parts = ['<!DOCTYPE html>','<html lang=\"zh-CN\">','<head><meta charset=\"UTF-8\"></head><body>']
in_code = False
for line in lines:
    s = line.strip()
    if s.startswith('\`\`\`'): in_code = not in_code; continue
    if in_code or s.startswith('    '): parts.append(f'<p><code>{h.escape(line)}</code></p>'); continue
    if s.startswith('# '): parts.append(f'<p><strong>{h.escape(s[2:])}</strong></p>'); continue
    if not s: continue
    text = h.escape(s)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    parts.append(f'<p>{text}</p>')
parts.append('</body></html>')
with open('/tmp/publish_zhihu.html','w',encoding='utf-8') as f: f.write('\n'.join(parts))
print(f'Zhihu HTML prepared: {len(parts)} lines')
"

# Compile Swift clipboard tool for Zhihu HTML paste
if [ ! -f /tmp/zhihu-clipboard ]; then
  cat > /tmp/zhihu_clipboard.swift << 'SWIFT'
import AppKit; import Foundation
let path="/tmp/publish_zhihu.html"
guard let data=FileManager.default.contents(atPath: path), let html=String(data:data,encoding:.utf8) else { exit(1) }
let pb=NSPasteboard.general; pb.clearContents()
var bom=Data([0xEF,0xBB,0xBF])
if let d=html.data(using:.utf8){ bom.append(d); pb.setData(bom,forType:.html) }
pb.setString(html,forType:.string)
print("OK: \(html.count) chars")
SWIFT
  swiftc -O -o /tmp/zhihu-clipboard /tmp/zhihu_clipboard.swift
fi
```

This pre-preparation avoids re-processing the Markdown file for each platform (previously 8x `sed` + `base64` + `pbcopy`, now 1x).

### Step 0.25: 检查各平台登录态（Session Health Check）

**在各平台发布前，先快速检查所有平台的登录态**，避免发布到一半才发现 session 过期。

对于 session 容易过期的平台（思否、51CTO），使用 `playwright-cli open` 快速访问并检查是否被重定向到登录页。如果发现 session 过期，提示用户手动登录：

```bash
# 检查思否登录态
playwright-cli open --headed --persistent "https://segmentfault.com/write?freshman=1"
sleep 2
url=$(playwright-cli eval "window.location.href" | grep -o 'segmentfault.com/[^"]*')
if [[ "$url" == *"/user/login"* ]]; then
  echo "⚠️ 思否 session 已过期，请在浏览器中手动登录..."
  # 等待用户手动登录
fi
playwright-cli close
```

如果 session 可用，记录结果；如果过期，要求用户登录后再继续。

### Step 0.5: Title Optimization (Optional)

If `publishTitle` is not provided in the skill arguments, use the `title-optimizer` skill to generate optimized titles for better click-through rates on publishing platforms. This only changes the title on the website — the local Markdown file is NOT modified.

1. Invoke the `title-optimizer` skill with the original title
2. Present the 5 optimized titles to the user
3. Ask the user to select one (or keep the original)
4. Set `publishTitle` to the user's choice

**Important**: If `publishTitle` is already provided in the skill arguments, skip this step entirely and use the provided title directly.

```
# Title optimization flow
If publishTitle is NOT provided:
  → Invoke Skill: title-optimizer (pass originalTitle)
  → Present 5 optimized titles to user
  → User selects one → set publishTitle = user's choice
  → User declines → set publishTitle = originalTitle
If publishTitle IS provided:
  → Skip optimization, use publishTitle directly
```

### Step 1: Publish to 51CTO

- Ensure no leftover browser session: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `51cto-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed: `playwright-cli close`
- Record result (success/failure + error message)

### Step 2: Publish to 思否 (SegmentFault)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `segmentfault-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 3: Publish to CSDN

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `csdn-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 4: Publish to 掘金 (Juejin)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `juejin-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 5: Publish to InfoQ

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `infoq-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 6: Publish to 腾讯云 (Tencent Cloud)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `tencent-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 7: Publish to 知乎 (Zhihu)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `zhihu-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 8: Publish to 博客园 (Cnblogs)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `cnblogs-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 9: Publish to 阿里云 (Aliyun)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `aliyun-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `cnblogs-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 10: Output Summary Report

After all platforms are processed, output a summary report:

```
============================================
发布结果汇总
============================================
✅ 51CTO       - 发布成功
✅ 思否        - 发布成功
✅ CSDN        - 发布成功
✅ 掘金        - 发布成功
✅ InfoQ       - 发布成功
✅ 腾讯云      - 发布成功
✅ 知乎        - 发布成功
✅ 博客园      - 发布成功
✅ 阿里云      - 发布成功
--------------------------------------------
成功: 9/9  失败: 0/9
============================================
```

## Error Handling

### Single Platform Failure

If a platform publish fails:
1. Record the platform name and error reason
2. Ensure browser is closed: `playwright-cli close`
3. Continue to the next platform
4. Do NOT stop the entire process

### Browser Not Closed

Before starting each platform, ensure no leftover browser session:

```bash
playwright-cli close 2>/dev/null || true
```

### All Platforms Failed

If all 9 platforms fail, there may be a common issue (e.g., playwright-cli not installed, file path wrong). Output an error message suggesting the user check:
1. playwright-cli is installed globally
2. The Markdown file path is correct
3. Browser sessions are not stuck

## 强制步骤清单（MANDATORY CHECKLIST）

**这是最重要的规则：发布每个平台前，必须先创建 TaskCreate 逐项打勾，完成后逐项标记 completed。缺少任何一项都不得进入下一步。**

在加载每个平台的 publisher skill 后，**立即**根据该平台对应的强制清单创建 TaskCreate，然后在执行中逐项标记完成。

### 腾讯云强制清单
```
□ 打开浏览器 → https://cloud.tencent.com/developer/article/write-new
□ 填写标题
□ 填写内容（base64 + CodeMirror.setValue）
□ 点击"去发布"
□ 选择文章来源 → 点击"原创" radio
□ 添加标签 → 输入 "AIGC"，按 Enter
□ 添加自定义关键词 → 输入 "Claude Code"，按 Enter
□ 选择专栏 → 勾选 "小林AI实战教程" checkbox（JS eval 方式）
□ 填写摘要
□ 点击"确认发布"
□ 验证成功（URL 变化或用户确认）
□ 关闭浏览器
```

### 知乎强制清单
```
□ 编译 Swift 剪贴板工具（`swiftc -O -o /tmp/zhihu-clipboard /tmp/zhihu_clipboard.swift`）
□ 用 Swift 工具设置 HTML 剪贴板（`/tmp/zhihu-clipboard`）
□ 打开浏览器 → https://zhuanlan.zhihu.com/write
□ 关闭创作助手（Escape）
□ 填写标题
□ 点击编辑器区域 → 粘贴（Meta+v）
□ 添加话题 → 搜索 "AI" → 选择话题
□ 点击"发布"
□ 验证成功（URL 变为 /p/ 无 /edit）
□ 关闭浏览器
```

### 51CTO 强制清单
```
□ 打开浏览器 → https://blog.51cto.com/blogger/publish
□ 移除 .v-note-read-model 覆盖层
□ 填写标题
□ 填写内容（base64 + native setter）
□ 点击"发布文章"打开弹窗
□ 选择一级分类（JS eval）
□ 选择二级分类（JS eval + 验证）
□ 选择个人分类
□ 删除自动标签 → innerHTML = ''
□ 添加自定义标签（逐个 run-code 或 fill + Enter，最多5个）
□ 选择话题
□ 点击发布
□ 验证成功
□ 关闭浏览器
```

### CSDN 强制清单
```
□ 打开浏览器 → https://editor.csdn.net/md/
□ 关闭模板弹窗（如有）
□ 关闭 AI 助手面板
□ 填写标题（click 标题区域 + type，不能用 fill）
□ 填写内容（focus contenteditable + Meta+v 粘贴）
□ 点击"发布文章"打开弹窗
□ 添加标签 → fill + Enter（多个标签）
□ blur 标签面板（不能用 Escape）
□ 填写摘要
□ 选择创作活动 → 查找到含"征稿/征文/挑战/创作"的活动
□ 点击"发布文章"（btn-b-red，JS eval）
□ 验证成功
□ 关闭浏览器
```

### 掘金强制清单
```
□ 打开浏览器 → "https://juejin.cn/editor/drafts/new?v=2"
□ 填写标题
□ 填写内容（base64 + CodeMirror.setValue）
□ 点击"发布"
□ 选择分类 → 点击"人工智能"
□ 添加标签 → fill "AI编程" → sleep 1 → Enter → sleep 1
□ 添加专栏 → fill "小林AI实战教程" → sleep 1 → Enter → sleep 1
□ 添加话题 → fill "AI" → sleep 1 → Enter → sleep 1
□ 填写摘要
□ 点击"确定并发布"
□ 验证成功（URL 变为 juejin.cn/published）
□ 关闭浏览器
```

### InfoQ 强制清单
```
□ 打开浏览器 → https://xie.infoq.cn/draft/
□ 点击"立即创作"
□ 填写标题
□ 填写内容（pbcopy + ProseMirror.focus + Meta+v 粘贴）
□ 点击"发布"
□ 添加标签（fill + Enter，最多5个）
□ 填写摘要（可选）
□ 点击"确定"
□ 验证成功（URL 包含 /article/）
□ 关闭浏览器
```

### 博客园强制清单
```
□ 打开浏览器 → https://i.cnblogs.com/posts/edit
□ 填写标题
□ 填写内容（CodeMirror.setValue）
□ 选择个人分类 → 点击 nz-tree-select → 选"小林AI实战教程"
□ 勾选合集 → "小林AI实战教程" checkbox
□ 勾选投稿 → "投稿至首页候选区" checkbox
□ 选择网站分类 → "AI综合" radio（JS eval）
□ 添加标签 → 点击 nz-select → 选"AI实战教程"
□ 按 Cmd+Enter 发布
□ 点击"确定"确认弹窗
□ 验证成功（URL 含 isPublished=true）
□ 关闭浏览器
```

### 思否强制清单
```
□ 打开浏览器 → "https://segmentfault.com/write?freshman=1"
□ 填写标题
□ 填写内容（pbcopy + CodeMirror.focus + Meta+v）
□ 点击"+ 添加标签"
□ 点击 AI tab（JS eval）
□ 添加子标签：chatgpt, openai, claude（JS eval）
□ Escape 关闭标签面板
□ 确认"注明版权"已勾选
□ 确认"原创"已选中
□ 点击"提交"
□ 验证成功（URL 变为 /a/ 文章页）
□ 关闭浏览器
```

### 阿里云强制清单
```
□ 打开浏览器 → https://developer.aliyun.com/article/new#/
□ 填写标题
□ 填写内容（pbcopy + 粘贴进富文本编辑器）
□ 填写摘要（最多300字，或用 AI 生成）
□ 选择子社区 → 下拉选"千问大模型"（AI内容）
□ 点击"发布文章"
□ 确认发布弹窗 → 点击"确认"
□ 验证成功（URL 包含 /article/）
□ 关闭浏览器
```

## Implementation Notes for the Agent

When executing this skill, the main agent must:

1. **Login health check first**: Before any publishing, check session status for all platforms (Step 0.25). Prioritize platforms with easily-expired sessions (思否, 51CTO). If session expired, ask user to re-login before proceeding.
2. **Extract article info & prepare content first**: Read the Markdown file to get the original title, confirm the file exists, and prepare all content formats (plain text, base64, JSON) in `/tmp/` for reuse across platforms
3. **Optimize title if needed**: If `publishTitle` is not provided, invoke `title-optimizer` skill and let user choose; otherwise use the provided `publishTitle` directly
4. **Process platforms sequentially**: Do NOT parallelize — each platform needs its own browser session
5. **51CTO first, 思否 second**: Start with 51CTO (most error-prone), then 思否 (session-sensitive), then the rest
6. **CRITICAL — Create TaskCreate checklist before each platform**: After loading each platform's publisher skill, immediately create TaskCreate tasks from the platform's 强制清单 above. Mark each item completed as you go. Do NOT skip any item.
7. **阿里云放最后**: 阿里云 session 容易过期且需要手动登录，放到所有平台之后最后一个发布
8. **Use Skill tool for each platform**: Call the Skill tool with the appropriate publisher skill name, passing the Markdown file path AND `publishTitle` as context. Also mention the pre-prepared `/tmp/` files.
9. **Close browser between platforms**: Run `playwright-cli close` after each platform completes (success or failure)
10. **Track results**: Maintain a list of results as you go (platform, success/failure, error message)
11. **Output the summary report** at the end

For each platform, the flow is:

```
playwright-cli close 2>/dev/null || true   # Cleanup any leftover session
→ Invoke Skill: <platform>-publisher       # Execute the platform-specific skill
→ READ 强制清单 for this platform            # Review the mandatory steps
→ Create TaskCreate with all checklist items # Create todos
→ Execute each step, marking completed       # Work through checklist
→ playwright-cli close                      # Close browser after completion
→ Record result                             # Track success/failure
```

## Content Format Reference

The pre-prepared content files in `/tmp/`:

| File | Format | Used By |
|------|--------|---------|
| `/tmp/publish_content.md` | Plain text (no frontmatter) | All platforms as source |
| `/tmp/publish_content.json` | JSON-encoded string | cnblogs (CodeMirror.setValue) |
| `/tmp/publish_content_b64.txt` | Base64-encoded (UTF-8) | juejin, tencent (CodeMirror + TextDecoder) |
| `/tmp/publish_zhihu.html` | Inline-style HTML (for Draft.js) | zhihu (HTML clipboard via Swift tool) |
| Clipboard | Plain text (pbcopy) | csdn, infoq, 51cto, segmentfault (paste-based) |

## Tips

1. Each platform takes 1-3 minutes to complete — total time is approximately 18-30 minutes for all 9
2. Do NOT skip the `playwright-cli close` step between platforms — leftover sessions cause issues
3. If a platform consistently fails, the user may need to re-login to that platform manually first
4. The article content is pasted from the same Markdown file for all platforms — each platform skill handles frontmatter skipping internally
5. Tags, categories, and other platform-specific settings use the defaults defined in each individual publisher skill
