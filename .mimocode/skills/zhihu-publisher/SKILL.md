# Zhihu Publisher Skill

Automate publishing Markdown articles to Zhihu Zhuanlan (知乎专栏) using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Zhihu (persistent browser profile handles this)
- Swift compiler (`swiftc`) must be available (pre-installed on macOS)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Important Notes

### playwright-cli eval 语法限制（CRITICAL）

`playwright-cli eval` wraps code as `() => (CODE)`. This means:
- **No** `var`, `let`, `const` at top level — use `(function(){...})()` IIFE
- **No** semicolons (`;`) at top level — use comma operator or IIFE
- **No** multi-line statements — write everything on one line or use IIFE

```bash
# WRONG — will throw SyntaxError
playwright-cli eval "var x = 1; return x;"

# CORRECT — use IIFE
playwright-cli eval "(function(){var x = 1; return x;})()"
```

### 知乎不再支持 Markdown 格式（CRITICAL）

**知乎编辑器已不支持直接粘贴 Markdown 格式。** 需要先将 Markdown 转换为内联样式 HTML（类似微信公众号排版），然后通过剪贴板以 HTML 富文本格式粘贴。

转换 + 粘贴流程：
1. 用 `wechat-md-converter` 样式将 Markdown 转换为带内联样式的 HTML
2. 使用 Swift 工具将 HTML 设置到系统剪贴板（带 BOM，确保中文编码正确）
3. 在知乎编辑器中直接粘贴（Cmd+V）

### Swift 剪贴板工具（编译一次，永久使用）

需要先编译一个 Swift 剪贴板工具，用于将 HTML 富文本设置到系统剪贴板：

```bash
# 检查是否已编译
if [ ! -f /tmp/zhihu-clipboard ]; then
  cat > /tmp/zhihu_clipboard.swift << 'SWIFT'
import AppKit
import Foundation

let path = "/tmp/publish_zhihu.html"
guard let data = FileManager.default.contents(atPath: path),
      let html = String(data: data, encoding: .utf8) else {
    print("Failed to read file"); exit(1)
}

let pb = NSPasteboard.general
pb.clearContents()

// Add UTF-8 BOM then HTML data (critical for correct Chinese encoding)
var bom = Data([0xEF, 0xBB, 0xBF])
if let htmlData = html.data(using: .utf8) {
    bom.append(htmlData)
    pb.setData(bom, forType: .html)
}
pb.setString(html, forType: .string)
print("OK: \(html.count) chars")
SWIFT
  swiftc -o /tmp/zhihu-clipboard /tmp/zhihu_clipboard.swift
  echo "Swift clipboard tool compiled"
fi
```

### HTML 内容格式要求

为了在 Draft.js 编辑器中保留最多格式，HTML 必须遵守以下规则：

**Draft.js 只保留的格式：**
- `font-weight: bold`（加粗）— 使用 `<strong>` 或 `<b>` 标签
- `font-family: monospace`（等宽字体）— 使用 `<code>` 标签
- `background-color` / `background`（背景色）— 代码块灰色背景可保留

**Draft.js 丢弃的格式：**
- `font-size`（字号）— 标题不会比正文大
- 列表结构的块级类型（ol/ul → Draft.js list blocks）
- `<blockquote>` 块级引用
- `<h2>`/`<h3>` 块级标题
- 表格结构

**内容结构建议（每行代码独立成段）：**
```html
<p><strong>标题文字（加粗）</strong></p>
<p>普通正文段落</p>
<p><code>每行代码独立成段</code></p>
<p><code>第二行代码</code></p>
```

### 渲染预览（可选）

在粘贴到知乎前，先在浏览器中预览 HTML 渲染效果：

```bash
# 保存 HTML 并通过 HTTP 服务预览
open /tmp/publish_zhihu.html
```

### 点击编辑器会创建草稿，元素 ref 会失效（CRITICAL）

当点击内容编辑器时，知乎会自动创建草稿并跳转到 `/p/xxx/edit` 页面。**跳转后所有之前的元素 ref 都会失效**，必须在跳转后重新 `playwright-cli snapshot` 获取新的 ref。

工作流修正：
1. 点击编辑器触发草稿创建 → 页面跳转
2. **立即 `playwright-cli snapshot` 刷新 ref**
3. 使用新的 ref 继续后续操作

### Creation Assistant Panel

Zhihu shows a "创作助手" (creation assistant) panel on the right side of the editor. Close it to free up space.

### Topics Limit

Zhihu allows selecting multiple topics for an article. Topics help with article discovery.

## Workflow

### Step 0: Convert Markdown to Inline-Style HTML

**THIS IS THE KEY STEP** — convert Markdown to inline-style HTML for Zhihu's Draft.js editor:

```bash
# Read Markdown content (skip YAML frontmatter)
CONTENT=$(cat /tmp/publish_content.md 2>/dev/null || sed -n '/^# /,$p' /path/to/article.md)

# Generate inline-style HTML
python3 -c "
import html as h
content = '''$CONTENT'''

# Convert to inline-style HTML compatible with Zhihu Draft.js
# Style rules:
# - H1 title: <strong> bold (Draft.js preserves font-weight: bold)
# - H2/H3: <strong> bold  
# - Normal text: <p> with inline styles
# - Code: <code> each line as separate <p> (preserves monospace font-family)
# - Lists: each item as separate <p> (Draft.js strips list blocks)
# - Blockquotes: <p> with italic (best effort)

lines = content.split('\n')
html_parts = ['<!DOCTYPE html>', '<html lang=\"zh-CN\">', '<head><meta charset=\"UTF-8\"></head><body>']

in_code_block = False
for line in lines:
    stripped = line.strip()
    
    # Handle code blocks (``` fences)
    if stripped.startswith('\`\`\`'):
        in_code_block = not in_code_block
        continue
    
    if in_code_block or stripped.startswith('    ') or stripped.startswith('\t'):
        # Code line — each line as separate <p><code>
        html_parts.append(f'<p><code>{h.escape(line)}</code></p>')
        continue
    
    # Skip YAML frontmatter
    if stripped == '---':
        continue
    
    # Headings → bold paragraphs
    if stripped.startswith('# '):
        html_parts.append(f'<p><strong>{h.escape(stripped[2:])}</strong></p>')
        continue
    
    # Empty lines
    if not stripped:
        continue
    
    # Regular paragraphs + inline formatting
    # Bold (**text**)
    import re
    text = h.escape(stripped)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    html_parts.append(f'<p>{text}</p>')

html_parts.append('</body></html>')
result = '\n'.join(html_parts)

with open('/tmp/publish_zhihu.html', 'w', encoding='utf-8') as f:
    f.write(result)
print(f'HTML generated: {len(result)} chars')
"
```

### Step 1: Set Clipboard with HTML（关键步骤）

**使用 Swift 工具将 HTML 设置到系统剪贴板（带 UTF-8 BOM）：**

```bash
# 编译 Swift 剪贴板工具（仅首次需要）
if [ ! -f /tmp/zhihu-clipboard ]; then
  swiftc -o /tmp/zhihu-clipboard /tmp/zhihu_clipboard.swift
fi

# 设置剪贴板为 HTML 格式（带 BOM，确保中文正确）
/tmp/zhihu-clipboard
```

### Step 2: Open Browser

```bash
playwright-cli close 2>/dev/null || true
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 3: Close Creation Assistant Panel

Close the creation assistant panel if it's open. The close button has ref in snapshot, or use Escape:

```bash
playwright-cli press "Escape"
sleep 1
```

### Step 4: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "请输入标题（最多 100 个字）")
# Use the placeholder selector
playwright-cli fill '[placeholder*="标题"]' "Article Title Here"
```

### Step 5: Paste Article Content

**内容已通过 Swift 工具设置为 HTML 格式在剪贴板中，直接粘贴即可：**

```bash
# Click the editor content area to focus
# Use textbox selector from snapshot — it's after the title input
playwright-cli click '[contenteditable]'
sleep 1

# Paste HTML content from clipboard
playwright-cli press "Meta+v"
sleep 4

# Content should appear with: bold headings, monospace code, gray code backgrounds
```

**注意：** 不再需要 Markdown 确认解析弹窗。因为内容已经是 HTML 格式。

### Step 6: Add Topics (Optional)

Click "添加话题" button to add topics:

```bash
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText.indexOf('添加话题')>=0})[0].click()"
sleep 1

# Type topic name
playwright-cli fill '[placeholder="搜索话题..."]' "AI"
sleep 1

# Select the first topic result (press Enter)
playwright-cli press "Enter"
```

Common topics: AI, AI技术, AI教程, 人工智能

### Step 7: Click Publish

```bash
# Click the "发布" button via JS eval
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText==='发布'}).map(function(b){b.click();return 'clicked'})"
sleep 3
```

After clicking, the page should navigate from `/edit` to the article view (`/p/<id>`).

### Step 8: Verify Success

Check the URL for success indicators:
- URL should change to article view: `https://zhuanlan.zhihu.com/p/<article_id>`
- URL should NOT contain `/edit`

```bash
playwright-cli eval "window.location.href"
```

### Click Fallback Pattern

When `playwright-cli click` fails (e.g., "intercepts pointer events", "element not visible"), automatically fall back to JavaScript evaluation:

```bash
# Instead of: playwright-cli click <ref>
# Use: playwright-cli eval "document.querySelector('CSS_SELECTOR')?.click()"
```

For elements identified by ref (not CSS selector), use text-based JS click:

```bash
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText.indexOf('BUTTON_TEXT')>=0})[0].click()"
```

## Error Handling

### Element Intercepted/Blocked

If clicking an element fails with "intercepts pointer events":
```bash
# Use JavaScript evaluation instead
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText.indexOf('Button Text')>=0})[0].click()"
```

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Chinese Characters Garbled

If pasted content shows garbled Chinese text (like `浠ｇ爜`):
```bash
# Re-generate HTML and re-compile the Swift tool
# Make sure the HTML file has <meta charset="UTF-8">
# Then re-run the clipboard tool
/tmp/zhihu-clipboard
playwright-cli press "Meta+v"
```

### Topic Dialog Not Opening

If topic dialog doesn't open:
```bash
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText.indexOf('添加话题')>=0})[0].click()"
```

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | `[placeholder*="标题"]` |
| Content editor | `[contenteditable]` |
| Add topic button | Button with text "添加话题" |
| Topic search input | `[placeholder="搜索话题..."]` |
| Publish button | Button with text "发布" |

## Complete Example

```bash
# Step 0: Generate HTML
CONTENT=$(cat /tmp/publish_content.md 2>/dev/null || sed -n '/^# /,$p' article.md)
python3 -c "
import html as h, re
content = '''$CONTENT'''
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
"

# Step 1: Set clipboard with HTML (BOM)
/tmp/zhihu-clipboard

# Step 2: Open Zhihu editor
playwright-cli close 2>/dev/null || true
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write
sleep 3

# Step 3: Close creation assistant
playwright-cli press "Escape"

# Step 4: Fill title
playwright-cli fill '[placeholder*="标题"]' "Article Title"

# Step 5: Paste content
playwright-cli click '[contenteditable]'
sleep 1
playwright-cli press "Meta+v"
sleep 4

# Step 6: Add topic
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText.indexOf('添加话题')>=0})[0].click()"
sleep 1
playwright-cli fill '[placeholder="搜索话题..."]' "AI"
sleep 1
playwright-cli press "Enter"

# Step 7: Publish
playwright-cli eval "[].slice.call(document.querySelectorAll('button')).filter(function(b){return b.innerText==='发布'}).map(function(b){b.click();return 'clicked'})"
sleep 3

# Step 8: Verify
playwright-cli eval "window.location.href"
playwright-cli close
```

## Tips

1. Always compile the Swift clipboard tool first time: `swiftc -o /tmp/zhihu-clipboard /tmp/zhihu_clipboard.swift`
2. The HTML file must have `<meta charset="UTF-8">` and the BOM is critical for correct Chinese encoding
3. Use `<code>` tag for monospace font — DO NOT use `<span style="font-family: monospace">` (textutil doesn't handle it)
4. Each code line should be its own `<p><code>line</code></p>` to prevent line merging
5. Skip YAML frontmatter when reading Markdown content
6. Title is limited to 100 characters
7. Use JavaScript evaluation for elements that are hard to click (outside viewport, blocked by overlays)
8. Close browser when done: `playwright-cli close`
9. The "确认并解析" Markdown dialog no longer appears (we paste HTML, not Markdown)
