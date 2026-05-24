# Zhihu Publisher Skill

Automate publishing Markdown articles to Zhihu Zhuanlan (知乎专栏) using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Zhihu (persistent browser profile handles this)

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

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# WRONG - includes frontmatter
cat article.md | pbcopy

# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md | pbcopy  # Start from first heading
```

### Content Preparation（优先使用 /tmp/ 预准备文件）

如果 `/tmp/publish_content.md` 存在（由 publish-all 预准备），直接读取它而不是重新解析源文件：

```bash
# BEST — use pre-prepared content
cat /tmp/publish_content.md | cat - <(echo -e "\n---\n\n> 本文作者：小林学AI...") | pbcopy
```

```bash
# FALLBACK — parse from source file
sed -n '/^# /,$p' /path/to/article.md | cat - <(echo -e "\n---\n\n> 本文作者：小林学AI...") | pbcopy
```

### 点击编辑器会创建草稿，元素 ref 会失效（CRITICAL）

当点击内容编辑器时，知乎会自动创建草稿并跳转到 `/p/xxx/edit` 页面。**跳转后所有之前的元素 ref 都会失效**，必须在跳转后重新 `playwright-cli snapshot` 获取新的 ref。

工作流修正：
1. 点击编辑器触发草稿创建 → 页面跳转
2. **立即 `playwright-cli snapshot` 刷新 ref**
3. 使用新的 ref 继续后续操作（粘贴内容等）

### Special Format Detection

When pasting Markdown content, Zhihu may detect special formats and show a dialog asking to confirm parsing. Click "确认并解析" to continue.

### Creation Assistant Panel

Zhihu shows a "创作助手" (creation assistant) panel on the right side of the editor. Close it to free up space:

```bash
playwright-cli snapshot
# Find the "关闭创作助手" button at the top of the panel
playwright-cli click <close_assistant_ref>
```

### Topics Limit

Zhihu allows selecting multiple topics for an article. Topics help with article discovery.

### "投稿至问题" Info Dialog

When opening the question picker for the first time, Zhihu may show an info dialog explaining the rules (e.g., "含好物卡片的文章不支持投稿至问题"). Click "我知道了" to dismiss it before proceeding.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 1.1: Close Creation Assistant Panel

Close the creation assistant panel if it's open:

```bash
playwright-cli snapshot
# Find the "关闭创作助手" button
playwright-cli click <close_assistant_ref>
```

### Step 2: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "请输入标题（最多 100 个字）")
playwright-cli fill <title_ref> "Article Title Here"
```

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content. Append a promotional footer for the "小林学AI" site to the article content (on the web only, NOT in the local markdown file).

```bash
# Skip frontmatter, append promotional footer, then copy to clipboard
cat /tmp/publish_content.md 2>/dev/null || sed -n '/^# /,$p' /path/to/article.md | cat - <(echo -e "\n---\n\n> 本文作者：小林学AI，更多AI实战教程干货持续更新中，欢迎访问官网地址 [小林学AI](https://xiaolinxueai.com) 获取更多内容。") | pbcopy

# Click editor — THIS WILL CREATE A DRAFT and NAVIGATE to /p/xxx/edit
playwright-cli click <editor_ref>

# CRITICAL: Page navigation invalidated all refs — take a fresh snapshot
playwright-cli snapshot

# Find the editor ref in the NEW page and paste
playwright-cli click <new_editor_ref>
playwright-cli press "Meta+v"
```

The editor is a rich text editor that supports Markdown syntax. After clicking the editor for the first time, Zhihu creates a draft and navigates — always re-snapshot after this step.

### Step 4: Confirm Markdown Parsing

If a dialog appears with "识别到特殊格式，请确认是否将 Markdown 解析为正确格式":

```bash
# Use JS click — the button may be outside the viewport and regular click will timeout
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('确认并解析'))?.click()"
```

Wait for parsing to complete:

```bash
sleep 3
```

### Step 5: Configure Contribute to Question (Optional)

To contribute the article to a related question, you must click the **combobox** below the "投稿至问题" button (NOT the button itself). The combobox shows "未选择" by default:

```bash
playwright-cli snapshot
# Find the combobox that shows "未选择" (below the "投稿至问题" text)
# It is a combobox element, NOT the button labeled "投稿至问题"
```

If clicking the combobox directly fails with "intercepts pointer events" (Modal backdrop may block the click), use JS:

```bash
playwright-cli eval "document.querySelector('#Popover6-toggle')?.click()"
```

#### Handle Info Dialog

When opening the question picker for the first time, an info dialog may appear with rules about contributing to questions. Click "我知道了" to dismiss:

```bash
playwright-cli snapshot
# Find the "我知道了" button
playwright-cli click <dismiss_button_ref>
```

#### Select a Question

After the dialog is dismissed, click the combobox again to open the question picker. Recommended questions are usually shown by default. If recommended questions are already displayed, directly select the first one (no need to search):

```bash
playwright-cli snapshot
# If recommended questions are shown (look for "推荐问题" heading and "选择" buttons)
# Click the "选择" button for the first recommended question
playwright-cli click <first_select_button_ref>

# If no recommendations shown, search for a question:
playwright-cli fill <search_combobox_ref> "search keyword"
playwright-cli press "Enter"

# Confirm selection by clicking "确定"
playwright-cli click <confirm_button_ref>
```

**Important**:
- The "投稿至问题" button itself only toggles the section visibility. To actually open the question picker dialog, you must click the combobox (showing "未选择") underneath it.
- If recommended questions are already displayed, select directly without searching.
- The combobox click may be blocked by a Modal backdrop — use JS click as a fallback.

### Step 6: Add Topics

Click "添加话题" button to add topics:

```bash
playwright-cli snapshot
# Click "添加话题" button
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('添加话题'))?.click()"
```

Search and select topics:

```bash
# Wait for topic dialog
playwright-cli snapshot
# Find the topic search input
playwright-cli fill <topic_search_ref> "AI"

# Press Enter to search
playwright-cli press "Enter"

# Wait for results and click on topic
playwright-cli snapshot
playwright-cli click <ai_topic_ref>
```

Common topics:
- AI
- AI技术
- AI教程
- 人工智能

### Step 7: Click Publish

Click the "发布" button to publish:

```bash
playwright-cli snapshot
# Find the "发布" button
playwright-cli click <publish_button_ref>
```

After clicking, the button may change to "发布中..." (publishing). A "确认" button may also appear. If a confirmation dialog or element appears outside the viewport, use JS:

```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent === '确认')?.click()"
```

Wait for the page to navigate to the article view.

### Step 8: Verify Success

Check the URL for success indicators:
- URL should change to article view: `https://zhuanlan.zhihu.com/p/<article_id>`
- Page title should show the article title

```bash
playwright-cli eval "window.location.href"
# Should contain: /p/ and NOT contain /edit
```

### Click Fallback Pattern

When `playwright-cli click` fails (e.g., "intercepts pointer events", "element not visible"), automatically fall back to JavaScript evaluation:

```bash
# Instead of: playwright-cli click <ref>
# Use: playwright-cli eval "document.querySelector('CSS_SELECTOR')?.click()"
```

For elements identified by ref (not CSS selector), use text-based JS click:

```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('BUTTON_TEXT'))?.click()"
```

## Error Handling

### Element Intercepted/Blocked

If clicking an element fails with "intercepts pointer events":
```bash
# Use JavaScript evaluation instead
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('Button Text'))?.click()"
```

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Content Contains Frontmatter

If the published content shows YAML frontmatter:
1. Clear the editor
2. Copy content without frontmatter: `sed -n '/^# /,$p' article.md | pbcopy`
3. Paste again

### Topic Dialog Not Opening

If topic dialog doesn't open:
```bash
# Try clicking via JavaScript
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('添加话题'))?.click()"
```

### Question Picker Not Opening

If clicking the "投稿至问题" button doesn't open the question picker dialog:
```bash
# The button only toggles section visibility. You must click the combobox below it.
# Look for a combobox showing "未选择" in the snapshot
playwright-cli snapshot
# Find and click the combobox (not the button)
playwright-cli click <combobox_ref>
```

If the combobox click is blocked by a Modal backdrop:
```bash
playwright-cli eval "document.querySelector('#Popover6-toggle')?.click()"
```

### "投稿至问题" Info Dialog

When opening the question picker for the first time, an info dialog with rules may appear. Dismiss it by clicking "我知道了" before proceeding with question selection.

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | Textbox with placeholder "请输入标题（最多 100 个字）" |
| Content editor | Textbox for article body |
| Confirm parse button | Button with text "确认并解析" |
| Contribute to question button | Button "投稿至问题" (toggles section visibility) |
| Contribute to question combobox | Combobox showing "未选择" (opens question picker dialog, use JS click if blocked) |
| Question info dialog dismiss | Button "我知道了" (first-time info dialog) |
| Question search input | Combobox "搜索" in question picker dialog |
| Question select button | Button "选择" in question list |
| Confirm button | Button "确定" in dialogs |
| Add topic button | Button "添加话题" |
| Topic search input | Textbox with placeholder "搜索话题..." |
| Topic button | Button with topic name (e.g., "AI", "AI技术") |
| Close creation assistant | Button "关闭创作助手" |
| Publish button | Button "发布" |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write

# Get initial snapshot
playwright-cli snapshot

# Close creation assistant panel
playwright-cli click <close_assistant_ref>

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter, append promotional footer)
cat /tmp/publish_content.md 2>/dev/null || sed -n '/^# /,$p' article.md | cat - <(echo -e "\n---\n\n> 本文作者：小林学AI，更多AI实战教程干货持续更新中，欢迎访问官网地址 [小林学AI](https://xiaolinxueai.com) 获取更多内容。") | pbcopy
playwright-cli click <editor_ref>
playwright-cli snapshot  # Re-snapshot after page navigation
playwright-cli press "Meta+v"

# Confirm Markdown parsing if dialog appears
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('确认并解析'))?.click()"
sleep 3

# Contribute to question (optional)
# IMPORTANT: Click the combobox (showing "未选择"), NOT the "投稿至问题" button
# If direct click fails (Modal backdrop blocks), use JS:
playwright-cli eval "document.querySelector('#Popover6-toggle')?.click()"

# Dismiss info dialog if shown ("我知道了" button)
playwright-cli snapshot
playwright-cli click <dismiss_button_ref>

# Click combobox again to open question picker
playwright-cli eval "document.querySelector('#Popover6-toggle')?.click()"

# Select first recommended question (no need to search if recommendations shown)
playwright-cli snapshot
playwright-cli click <first_select_button_ref>  # "选择" button for first question
playwright-cli click <confirm_button_ref>  # "确定" button

# Add topics
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('添加话题'))?.click()"
playwright-cli snapshot
playwright-cli fill <topic_search_ref> "AI"
playwright-cli press "Enter"
playwright-cli snapshot
playwright-cli click <ai_topic_ref>

# Publish
playwright-cli snapshot
playwright-cli click <publish_button_ref>

# If confirmation appears outside viewport, use JS
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent === '确认')?.click()"

# Verify
playwright-cli eval "window.location.href"
# Should contain: /p/ and NOT /edit
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Title is limited to 100 characters
4. Use JavaScript evaluation for elements that are hard to click (outside viewport, blocked by overlays)
5. Topics help with article discovery
6. Close browser when done: `playwright-cli close`
7. Close the creation assistant panel at the start to free up space
8. When contributing to questions, if recommended questions are already shown, select the first one directly without searching
9. The combobox for "投稿至问题" may be blocked by a Modal backdrop — use JS click as fallback
10. The "确认并解析" button may be outside the viewport — use JS click instead of regular click
11. Always append the "小林学AI" promotional footer to the article content before pasting — this goes on the web only, never modify the local markdown source file
