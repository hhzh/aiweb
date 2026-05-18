# Tencent Cloud Publisher Skill

Automate publishing Markdown articles to Tencent Cloud Developer Community (腾讯云开发者社区) using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Tencent Cloud (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Important Notes

### Title Input Selector

The title input is a **textarea** with class `cdc-article-editor__title-input`:

```bash
playwright-cli fill "textarea.cdc-article-editor__title-input" "Article Title"
```

### Content Editor (CodeMirror)

The content editor uses CodeMirror. For Chinese content, use base64 encoding with UTF-8 decoding to avoid garbled characters:

```bash
# Encode content as base64
content=$(sed -n '/^# /,$p' article.md | base64)

# Set content via JavaScript with UTF-8 decoding
playwright-cli eval "(function(){var b64='$content';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"
```

### Publish Dialog Interception

The publish dialog (`.cdc-modal`) intercepts pointer events. Use JavaScript evaluation to click buttons:

```bash
# Click confirm publish button
playwright-cli eval "document.querySelectorAll('button.cdc-btn--primary')[1]?.click()"
```

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md
```

### Author Signature (作者签名)

No author signature or promotional footer should be appended to the article content. Publish the article content as-is, without any additional marketing text.

### Article Source Selection

Tencent Cloud requires selecting the article source (原创/转载/翻译). Use JavaScript for radio buttons:

```bash
playwright-cli eval "document.querySelector('input[value=\"1\"][type=\"radio\"]')?.click()"
```

### Tag Input

Tags are entered by typing and pressing Enter. Tags may show dropdown suggestions.

### Column Selection

Column checkbox needs JavaScript click due to element interception:

```bash
playwright-cli eval "document.querySelector('input[value=\"COLUMN_ID\"][type=\"checkbox\"]')?.click()"
```

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://cloud.tencent.com/developer/article/write-new
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli fill "textarea.cdc-article-editor__title-input" "Article Title Here"
```

### Step 3: Fill Article Content

Use base64 encoding for proper UTF-8 handling:

```bash
# Prepare content: skip frontmatter
content=$(sed -n '/^# /,$p' /path/to/article.md)

# Base64 encode
encoded=$(echo -n "$content" | base64 | tr -d '\n')

# Set content via JavaScript
playwright-cli eval "(function(){var b64='${encoded}';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"
```

### Step 4: Click "去发布" Button

```bash
playwright-cli eval "document.querySelector('button.cdc-btn--primary')?.click()"
```

This will open a dialog with publication settings.

### Step 5: Select Article Source (文章来源)

Select "原创" (original) for the article source:

```bash
playwright-cli eval "document.querySelector('input[value=\"1\"][type=\"radio\"]')?.click()"
```

### Step 6: Add Tags (文章标签)

Add tags by typing and pressing Enter:

```bash
playwright-cli snapshot
# Find tag input ref
playwright-cli fill <tag_input_ref> "AIGC"
playwright-cli press "Enter"

playwright-cli fill <tag_input_ref> "腾讯混元大模型"
playwright-cli press "Enter"
```

Common tags:
- AIGC
- 腾讯混元大模型
- 腾讯混元大模型AIGC
- chatgpt
- 玩转腾讯混元大模型A

### Step 7: Add Custom Keywords (自定义关键字)

```bash
playwright-cli fill <keyword_input_ref> "AI教程"
playwright-cli press "Enter"
```

### Step 8: Select Column (专栏)

Use JavaScript to click the column checkbox:

```bash
playwright-cli eval "document.querySelector('input[value=\"COLUMN_ID\"][type=\"checkbox\"]')?.click()"
```

Common columns:
- 小林AI实战教程 (value: 107616)

### Step 9: Fill Summary (文章摘要)

```bash
playwright-cli fill <summary_ref> "Article summary text..."
```

### Step 10: Confirm Publish

Use JavaScript to click the confirm button:

```bash
playwright-cli eval "document.querySelectorAll('button.cdc-btn--primary')[1]?.click()"
```

### Step 11: Verify Success

After successful publish, a success message appears:

```bash
playwright-cli snapshot 2>&1 | grep "发布成功"
# Should show: "发布成功！"
```

The message includes:
- "发布成功！" (Publish successful)
- "文章正在审核中，审核通过后前仅自己可见。" (Article is under review)
- Link to article: `https://cloud.tencent.com/developer/article/<article_id>`

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
playwright-cli eval "document.querySelector('SELECTOR')?.click()"
```

### Content Shows Garbled Characters

If Chinese content appears garbled:
1. Use base64 encoding with UTF-8 TextDecoder as shown in Step 3
2. Do NOT use simple base64 decode (atob) - it returns Latin-1, not UTF-8

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Title Has Extra Content

If title field contains article content:
1. Clear and re-fill using the selector: `textarea.cdc-article-editor__title-input`
2. The title should only contain the article title, not the full content

## Common Element Selectors

| Element | Selector/Description |
|---------|----------|
| Title input | `textarea.cdc-article-editor__title-input` |
| Content editor | `.CodeMirror` (use CodeMirror.setValue) |
| "去发布" button | `button.cdc-btn--primary` |
| Article source 原创 | `input[value="1"][type="radio"]` |
| Article source 转载 | `input[value="2"][type="radio"]` |
| Article source 翻译 | `input[value="3"][type="radio"]` |
| Tag input | Textbox in 文章标签 section |
| Keyword input | Textbox in 自定义关键词 section |
| Column checkbox | `input[value="<column_id>"][type="checkbox"]` |
| Summary textarea | Textbox with placeholder "请输入文章摘要" |
| Confirm publish button | Second `button.cdc-btn--primary` |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://cloud.tencent.com/developer/article/write-new

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill "textarea.cdc-article-editor__title-input" "My Article Title"

# Fill content with proper UTF-8 encoding
content=$(sed -n '/^# /,$p' article.md)
encoded=$(echo -n "$content" | base64 | tr -d '\n')
playwright-cli eval "(function(){var b64='${encoded}';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"

# Click "去发布"
playwright-cli eval "document.querySelector('button.cdc-btn--primary')?.click()"

# Wait for dialog
sleep 1
playwright-cli snapshot

# Select "原创"
playwright-cli eval "document.querySelector('input[value=\"1\"][type=\"radio\"]')?.click()"

# Add tags
playwright-cli fill <tag_input_ref> "AIGC"
playwright-cli press "Enter"
playwright-cli fill <tag_input_ref> "腾讯混元大模型"
playwright-cli press "Enter"

# Add custom keyword
playwright-cli fill <keyword_input_ref> "AI教程"
playwright-cli press "Enter"

# Select column
playwright-cli eval "document.querySelector('input[value=\"107616\"][type=\"checkbox\"]')?.click()"

# Fill summary
playwright-cli fill <summary_ref> "Article summary text..."

# Confirm publish
playwright-cli eval "document.querySelectorAll('button.cdc-btn--primary')[1]?.click()"

# Verify success
sleep 2
playwright-cli snapshot 2>&1 | grep "发布成功"
```

## Tips

1. Always use JavaScript evaluation for buttons in the publish dialog
2. Use base64 + TextDecoder for Chinese content to avoid encoding issues
3. Title selector: `textarea.cdc-article-editor__title-input`
4. Tags and keywords require pressing Enter after typing
5. Column checkbox needs JavaScript click
6. After publish, look for "发布成功！" success message
7. Article goes into review mode after publishing
8. Close browser when done: `playwright-cli close`
