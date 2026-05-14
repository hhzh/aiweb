# Juejin Publisher Skill

Automate publishing Markdown articles to Juejin (稀土掘金) using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Juejin (persistent browser profile handles this)

## Important Notes

### URL with Query Parameters

The URL has query parameters, so quote it properly:

```bash
playwright-cli open --headed --persistent "https://juejin.cn/editor/drafts/new?v=2"
```

### Title Input

The title input has class `.title-input`:

```bash
playwright-cli fill <title_ref> "Article Title"
```

### Content Editor (CodeMirror)

The content editor uses CodeMirror. For Chinese content, use base64 encoding with UTF-8 decoding:

```bash
# Encode content as base64
content=$(sed -n '/^# /,$p' article.md | base64 | tr -d '\n')

# Set content via JavaScript with UTF-8 decoding
playwright-cli eval "(function(){var b64='$content';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"
```

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers):

```bash
# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md
```

### Category Selection

Categories are displayed as clickable items in the publish dialog. Just click on the category name directly.

### Tag/Column/Topic Input

Tags, columns, and topics use searchable inputs. **IMPORTANT**: Do NOT press Enter after typing - it will select the first dropdown option instead of your intended choice. Instead:

1. Type the search term
2. Wait for the dropdown to appear
3. Click directly on the desired option button

```bash
# CORRECT - type, wait, then click the option button
playwright-cli fill <tag_input_ref> "人工智能"
sleep 1
playwright-cli snapshot  # Find the option button ref
playwright-cli click <option_button_ref>

# WRONG - pressing Enter selects the first dropdown option
playwright-cli fill <tag_input_ref> "人工智能"
playwright-cli press "Enter"  # This will select wrong option!
```

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent "https://juejin.cn/editor/drafts/new?v=2"
```

### Step 2: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "输入文章标题...")
playwright-cli fill <title_ref> "Article Title Here"
```

### Step 3: Fill Article Content

Use base64 encoding for proper UTF-8 handling:

```bash
content=$(sed -n '/^# /,$p' /path/to/article.md | base64 | tr -d '\n')
playwright-cli eval "(function(){var b64='$content';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"
```

### Step 4: Click "发布" Button

```bash
playwright-cli snapshot
# Find the "发布" button
playwright-cli click <publish_button_ref>
```

This opens the publish dialog with settings.

### Step 5: Select Category (分类)

Categories are listed directly - just click on the category name:

```bash
playwright-cli snapshot
# Find and click "人工智能" category item
playwright-cli click <ai_category_ref>
```

Available categories: 后端, 前端, Android, iOS, 人工智能, 开发工具, 代码人生, 阅读

### Step 6: Add Tags (添加标签)

Type in the tag input and press Enter. **IMPORTANT**: Add `sleep 1` after pressing Enter to allow the tag to register before proceeding:

```bash
playwright-cli snapshot
# Find tag textbox
playwright-cli fill <tag_input_ref> "人工智能"
sleep 1
playwright-cli press "Enter"
sleep 1
```

Common tags: AI编程, 人工智能, Claude, AI工具

### Step 7: Select Column (收录至专栏)

Search and add column. Add `sleep 1` after pressing Enter:

```bash
playwright-cli snapshot
# Find column textbox
playwright-cli fill <column_input_ref> "小林AI实战教程"
sleep 1
playwright-cli press "Enter"
sleep 1
```

Common columns: 小林AI实战教程

### Step 8: Select Topic (创作话题)

Search and add topic. Add `sleep 1` after pressing Enter:

```bash
playwright-cli snapshot
# Find topic textbox
playwright-cli fill <topic_input_ref> "AI"
sleep 1
playwright-cli press "Enter"
sleep 1
```

Common topics: AI 编程

### Step 9: Fill Summary (摘要)

```bash
playwright-cli fill <summary_ref> "Article summary text..."
```

Summary is auto-generated but can be customized.

### Step 10: Confirm Publish (确定并发布)

```bash
playwright-cli snapshot
# Find the "确定并发布" button
playwright-cli click <confirm_publish_ref>
```

### Step 11: Verify Success

After successful publish:
- URL changes to `https://juejin.cn/published`
- Page shows "发布成功"

```bash
playwright-cli eval "window.location.href"
# Should be: https://juejin.cn/published
```

The article URL will be shown in the success page (format: `/spost/<article_id>`).

## Error Handling

### Editor Intercepted

If clicking the editor fails with "intercepts pointer events":
- Use the CodeMirror setValue approach via JavaScript (shown in Step 3)

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Content Contains Frontmatter

If the title field contains article content:
1. Set title using the correct selector
2. Set content via CodeMirror.setValue

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | Textbox with placeholder "输入文章标题..." |
| Content editor | `.CodeMirror` (use CodeMirror.setValue) |
| "发布" button | Button to open publish dialog |
| Category items | Clickable category names (e.g., "人工智能") |
| Tag input | Textbox for searching/adding tags |
| Column input | Textbox for searching/adding columns |
| Topic input | Textbox for searching/adding topics |
| Summary textarea | Textarea for article summary |
| "确定并发布" button | Button to confirm and publish |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent "https://juejin.cn/editor/drafts/new?v=2"

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content with UTF-8 encoding
content=$(sed -n '/^# /,$p' article.md | base64 | tr -d '\n')
playwright-cli eval "(function(){var b64='$content';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);document.querySelector('.CodeMirror').CodeMirror.setValue(content);})()"

# Click "发布"
playwright-cli click <publish_button_ref>

# Wait for dialog
sleep 1
playwright-cli snapshot

# Select category "人工智能"
playwright-cli click <ai_category_ref>

# Add tag "AI编程" (wait between fill and Enter)
playwright-cli fill <tag_input_ref> "AI编程"
sleep 1
playwright-cli press "Enter"
sleep 1

# Add column "小林AI实战教程"
playwright-cli fill <column_input_ref> "小林AI实战教程"
sleep 1
playwright-cli press "Enter"
sleep 1

# Add topic "AI"
playwright-cli fill <topic_input_ref> "AI"
sleep 1
playwright-cli press "Enter"
sleep 1

# Fill summary
playwright-cli fill <summary_ref> "Article summary text..."

# Confirm publish
playwright-cli click <confirm_publish_ref>

# Verify success
sleep 2
playwright-cli eval "window.location.href"
# Should be: https://juejin.cn/published
```

## Tips

1. Quote the URL with query parameters: `"https://juejin.cn/editor/drafts/new?v=2"`
2. Use base64 + TextDecoder for Chinese content in CodeMirror
3. Categories are clicked directly, not from a dropdown
4. Tags/columns/topics use searchable inputs - type, wait for dropdown, then press Enter. Add `sleep 1` between fill and Enter, and after Enter, to ensure items register properly
5. Summary is auto-generated but can be customized
6. After publish, look for "发布成功" on the published page
7. Close browser when done: `playwright-cli close`
8. **CRITICAL**: Fill all dialog fields (category, tags, column, topic, summary) in one pass without taking intermediate snapshots that could refresh the dialog. Verify all items are present before clicking "确定并发布". If items appear missing after a dialog refresh, re-fill them.
9. The article URL format on success page is `/spost/<article_id>`
