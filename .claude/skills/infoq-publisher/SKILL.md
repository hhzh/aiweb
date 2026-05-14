# InfoQ Publisher Skill

Automate publishing Markdown articles to InfoQ writing community using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into InfoQ (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# WRONG - includes frontmatter
cat article.md | pbcopy

# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md | pbcopy  # Start from first heading
```

### Tag Limits

InfoQ allows a maximum of 5 tags per article. Tags are created by typing and pressing Enter.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://xie.infoq.cn/draft/
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Click Create Button

Click the "立即创作" button to create a new article:

```bash
playwright-cli snapshot
# Find the "立即创作" button ref
playwright-cli click <create_button_ref>
```

This will create a new draft and navigate to the editor page.

### Step 3: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "请输入标题")
playwright-cli fill <title_ref> "Article Title Here"
```

### Step 4: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content.

```bash
# Skip frontmatter and copy content starting from first heading
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Focus the ProseMirror editor and paste
playwright-cli eval "document.querySelector('.ProseMirror')?.focus()"
playwright-cli press "Meta+v"
playwright-cli press "Meta+v"
```

The editor area shows a preview of the content with headings.

### Step 5: Click Publish Button

Click the "发布" button in the header to open the publish dialog:

```bash
playwright-cli snapshot
# Find the "发布" button ref in header
playwright-cli click <publish_button_ref>
```

### Step 6: Add Tags

In the publish dialog, add tags by typing and pressing Enter:

```bash
# Fill tag input
playwright-cli fill <tag_input_ref> "AI"
playwright-cli press "Enter"

# Add more tags
playwright-cli fill <tag_input_ref> "AI教程"
playwright-cli press "Enter"

playwright-cli fill <tag_input_ref> "AI 编程"
playwright-cli press "Enter"

playwright-cli fill <tag_input_ref> "月更"
playwright-cli press "Enter"
```

The tag input has placeholder "输入标签，回车创建". Maximum 5 tags allowed.

### Step 7: Configure Summary (Optional)

The summary is auto-generated from the first paragraph (max 120 characters). You can edit it if needed:

```bash
playwright-cli fill <summary_ref> "Custom summary text..."
```

### Step 8: Configure Copyright (Optional)

By default, copyright is set to "不声明" (no declaration). You can change it if needed.

### Step 9: Confirm Publish

Click the "确定" button to publish:

```bash
playwright-cli snapshot
# Find the "确定" button ref
playwright-cli click <confirm_button_ref>
```

### Step 10: Verify Success

Check the URL for success indicators:
- URL should change to article view: `https://xie.infoq.cn/article/<article_id>`
- Page title should show the article title

```bash
playwright-cli eval "window.location.href"
# Should contain: /article/
```

## Error Handling

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

### Tag Not Created

If tags don't appear after pressing Enter:
```bash
# Wait a moment and try again
sleep 0.5
playwright-cli snapshot
```

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Create button | Text "立即创作" in header |
| Title input | Textbox with placeholder "请输入标题" |
| Content editor | ProseMirror `.ProseMirror` element, focus via JS |
| Publish button | Text "发布" in header |
| Tag input | Textbox with placeholder "输入标签，回车创建" |
| Summary textarea | Textbox with placeholder about 120 characters limit |
| Confirm button | Text "确定" in dialog |
| Cancel button | Text "取消" in dialog |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://xie.infoq.cn/draft/

# Get initial snapshot
playwright-cli snapshot

# Click create button
playwright-cli click <create_button_ref>

# Wait for editor to load
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli eval "document.querySelector('.ProseMirror')?.focus()"
playwright-cli press "Meta+v"

# Click publish button
playwright-cli click <publish_button_ref>

# Wait for dialog
playwright-cli snapshot

# Add tags
playwright-cli fill <tag_input_ref> "AI"
playwright-cli press "Enter"
playwright-cli fill <tag_input_ref> "AI教程"
playwright-cli press "Enter"
playwright-cli fill <tag_input_ref> "AI 编程"
playwright-cli press "Enter"

# Click confirm
playwright-cli click <confirm_button_ref>

# Verify
playwright-cli eval "window.location.href"
# Should contain: /article/
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Maximum 5 tags allowed per article
4. Tags must be created by pressing Enter after typing
5. Summary is auto-generated but can be customized (max 120 chars)
6. Close browser when done: `playwright-cli close`
7. InfoQ uses a ProseMirror rich text editor — focus it via JS: `document.querySelector('.ProseMirror')?.focus()`, then paste with `Meta+v`
8. The "编辑" button in the editor may be outside the viewport — use JS click instead: `document.querySelector('._3DSA44lQ')?.click()`
