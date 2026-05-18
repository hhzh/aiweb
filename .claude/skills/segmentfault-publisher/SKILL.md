---
name: segmentfault-publisher
description: Publish Markdown articles to SegmentFault (思否) using playwright-cli automation. Use when the user wants to publish articles to their SegmentFault blog, especially when they provide a Markdown file path. Handles title, content, tags, copyright declaration, and publication settings automatically.
---

# SegmentFault Publisher Skill

Automate publishing Markdown articles to SegmentFault using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into SegmentFault (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# Skip frontmatter and copy content starting from first heading
sed -n '/^# /,$p' /path/to/article.md | pbcopy
```

### Editor Type (CodeMirror)

SegmentFault uses a **CodeMirror** editor that supports Markdown syntax. The editor has:
- Edit mode (编辑)
- Preview mode (预览)
- Fullscreen mode (全屏)

**CRITICAL**: The CodeMirror display layer intercepts pointer events, so `playwright-cli click` on the editor textbox will FAIL. You MUST use the CodeMirror API to focus the editor before pasting content:

```bash
# Focus the CodeMirror editor via its API
playwright-cli eval "document.querySelector('.CodeMirror').CodeMirror.focus()"

# Then paste
playwright-cli press "Meta+v"
```

Do NOT try `playwright-cli click <editor_ref>` — it will fail with "intercepts pointer events" or paste content into the title field instead.

### Tag Limit

SegmentFault allows up to 5 tags per article. The counter shows remaining slots.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent "https://segmentfault.com/write?freshman=1"
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli snapshot
# Find the title textbox
playwright-cli fill <title_ref> "Article Title Here"
```

Title input: `textbox "标题"`

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content. The CodeMirror editor requires special focus handling.

```bash
# Skip frontmatter and copy content
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Focus CodeMirror editor via API (do NOT use playwright-cli click)
playwright-cli eval "document.querySelector('.CodeMirror').CodeMirror.focus()"

# Paste content
playwright-cli press "Meta+v"
```

**Why not click?** The CodeMirror display layer (`CodeMirror-lines`, `CodeMirror-scroll`) intercepts pointer events, causing `playwright-cli click` to fail. Clicking may also accidentally focus the title field instead, pasting all content into the title.

To verify content was pasted correctly:
```bash
playwright-cli eval "document.querySelector('.CodeMirror')?.CodeMirror?.getValue()?.substring(0, 100)"
```

### Step 4: Add Tags

1. Click "+ 添加标签" button:
```bash
playwright-cli snapshot
playwright-cli click <add_tag_button_ref>
```

2. Click "AI" tab to show AI-related tags:
```bash
playwright-cli click <ai_tab_ref>  # tab "AI"
```

3. Select tags from the AI category:
```bash
playwright-cli snapshot
# Click on each desired tag
playwright-cli click <tag_ref>  # e.g., link "人工智能"
playwright-cli click <tag_ref>  # e.g., link "chatgpt"
playwright-cli click <tag_ref>  # e.g., link "openai"
playwright-cli click <tag_ref>  # e.g., link "prompt"
playwright-cli click <tag_ref>  # e.g., link "claude"
```

4. Close tag panel:
```bash
playwright-cli press Escape
```

### Step 5: Configure Copyright Declaration

Check "注明版权" checkbox:
```bash
playwright-cli snapshot
playwright-cli click <copyright_checkbox_ref>
```

### Step 6: Configure Article Type

Article types: 原创 (Original), 转载 (Reprint), 翻译 (Translation)

```bash
# Default is "原创" (already selected)
# To change:
playwright-cli click <radio_ref>  # e.g., radio "转载"
```

### Step 7: Configure Publication Target

Select where to publish:
```bash
playwright-cli click <publish_target_combobox_ref>
playwright-cli snapshot
# Select: 个人文章 or 创建博客
playwright-cli click <option_ref>
```

### Step 8: Publish

Click the "提交" button:
```bash
playwright-cli snapshot
# Note: Button is disabled until title and content are filled
playwright-cli click <submit_button_ref>
```

### Step 9: Verify Success

After clicking "提交", the page may briefly show a 404 or redirect to the homepage. This is normal — the article takes a few seconds to propagate.

Check for success indicators:
- Wait 3-5 seconds, then check the URL
- The article URL format is: `https://segmentfault.com/a/<article_id>`
- Page title should contain the article title and blog name (e.g., "Claude Code 指南 - 小林学AI - SegmentFault 思否")
- If redirected to homepage, navigate directly to the article URL to verify

```bash
# Wait for propagation
sleep 3
# Check current URL
playwright-cli eval "window.location.href"
# If on homepage, check article URL directly
playwright-cli eval "window.location.href = 'https://segmentfault.com/a/<article_id>'"
```

## AI Tags Reference

Common AI-related tags in the "AI" tab:

| Tag | Description |
|-----|-------------|
| 人工智能 | Artificial Intelligence |
| 机器学习 | Machine Learning |
| 深度学习 | Deep Learning |
| chatgpt | ChatGPT |
| openai | OpenAI |
| prompt | Prompt Engineering |
| claude | Claude AI |
| llm | Large Language Model |
| llama | LLaMA |
| generative-ai | Generative AI |

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

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Session Expired

If you see login prompts or session errors:
```bash
playwright-cli close
playwright-cli open --headed --persistent "https://segmentfault.com/write?freshman=1"
# Re-login manually if needed
```

### Content Contains Frontmatter

If the published content shows YAML frontmatter (`---` at the beginning):
1. Clear the editor
2. Copy content without frontmatter: `sed -n '/^# /,$p' article.md | pbcopy`
3. Paste again: `playwright-cli press "Meta+v"`

### CodeMirror Editor Not Receiving Paste

If pasting results in content appearing in the title field instead of the editor:
1. Clear the title field: `playwright-cli fill <title_ref> "Correct Title Only"`
2. Focus CodeMirror via API: `playwright-cli eval "document.querySelector('.CodeMirror').CodeMirror.focus()"`
3. Re-paste: `playwright-cli press "Meta+v"`
4. Verify: `playwright-cli eval "document.querySelector('.CodeMirror')?.CodeMirror?.getValue()?.substring(0, 100)"`

### Beforeunload Dialog on Submit

After clicking "提交", a `beforeunload` dialog may appear. Accept it:
```bash
playwright-cli dialog-accept
```

### Article Under Review Prompt

SegmentFault may show a dialog: "你有被拒绝的文章等待编辑，通过之后才能继续撰写文章". This means the article was submitted but needs review. The article URL can be found in the "查看详情" link within the dialog. Accept the dialog to continue:
```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('确定'))?.click()"
```

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | `textbox "标题"` |
| Content editor | CodeMirror — use `CodeMirror.focus()` API, do NOT click |
| Add tag button | `button "+ 添加标签"` |
| AI tab | `tab "AI"` |
| Copyright checkbox | `checkbox "注明版权"` |
| Article type radio | `radio "原创"` / `radio "转载"` / `radio "翻译"` |
| Publish target | `combobox "发布到"` |
| Submit button | `button "提交"` |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent "https://segmentfault.com/write?freshman=1"

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy

# CRITICAL: Use CodeMirror API to focus, NOT playwright-cli click
playwright-cli eval "document.querySelector('.CodeMirror').CodeMirror.focus()"
playwright-cli press "Meta+v"

# Verify content was pasted correctly (optional)
playwright-cli eval "document.querySelector('.CodeMirror')?.CodeMirror?.getValue()?.substring(0, 100)"

# Add tags (AI category)
playwright-cli click <add_tag_button_ref>
playwright-cli click <ai_tab_ref>
playwright-cli snapshot
playwright-cli click <tag_人工智能_ref>
playwright-cli click <tag_chatgpt_ref>
playwright-cli click <tag_openai_ref>
playwright-cli click <tag_prompt_ref>
playwright-cli click <tag_claude_ref>
playwright-cli press Escape

# Configure copyright
playwright-cli click <copyright_checkbox_ref>

# Publish
playwright-cli snapshot
playwright-cli click <submit_button_ref>

# Handle beforeunload dialog if it appears
playwright-cli dialog-accept

# Handle review prompt dialog if it appears
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('确定'))?.click()"
```

## Tips

1. Always take snapshots to get current element refs
2. Use `--depth` parameter for partial snapshots when full snapshot is too large
3. Skip YAML frontmatter when copying Markdown content
4. Maximum 5 tags per article
5. Close browser when done: `playwright-cli close`
6. The tag panel shows remaining slots available
7. After submitting, the article may briefly show 404 — wait a few seconds then navigate directly to the article URL to verify
8. The article ID appears in the redirect URL right after submit (e.g., `/a/1190000047761971`) — capture it for verification
