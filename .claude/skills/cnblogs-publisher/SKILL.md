---
name: cnblogs-publisher
description: Publish Markdown articles to cnblogs (博客园) using playwright-cli automation. Use when the user wants to publish articles to their cnblogs blog, especially when they provide a Markdown file path. Handles title, content, category, collection, tags, and submission settings automatically.
---

# Cnblogs Publisher Skill

Automate publishing Markdown articles to cnblogs using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into cnblogs (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://i.cnblogs.com/posts/edit
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli snapshot
# Find the title textbox ref (usually labeled "标题")
playwright-cli fill <ref> "Article Title Here"
```

### Step 3: Fill Article Content

Copy content to clipboard, then paste into editor:

```bash
cat /path/to/article.md | pbcopy
playwright-cli click ".CodeMirror-code"
playwright-cli press "Meta+v"
```

### Step 4: Configure Personal Category

1. Click on category dropdown:
```bash
playwright-cli click ".cnb-tree-category-select__container"
```

2. Wait for dropdown, then select the category:
```bash
playwright-cli snapshot --depth=1
# Find the category item ref
playwright-cli click <category_ref>
```

### Step 5: Configure Collection

Check the collection checkbox:
```bash
playwright-cli click 'input[id="<collection_id>"]'
# Or use role-based selector:
playwright-cli getByRole('checkbox', { name: 'Collection Name' }).click()
```

### Step 6: Configure Submission Option

Check the submission checkbox (e.g., "投稿至首页候选区"):
```bash
playwright-cli click 'input[id="isToHomeCandidate"]'
```

### Step 7: Select Site Category

Select the site category radio button (e.g., "小林AI实战教程"):
```bash
playwright-cli eval "document.querySelector('input#Java[type=\"radio\"]')?.click()"
```

### Step 8: Add Tags

1. Click tag dropdown:
```bash
playwright-cli click "nz-select"
```

2. Select tag from dropdown:
```bash
playwright-cli snapshot --depth=1
# Find and click the tag
playwright-cli click <tag_ref>
```

3. Close dropdown:
```bash
playwright-cli press Escape
```

### Step 9: Fill Summary

```bash
playwright-cli fill "#summary" "Article summary text..."
```

### Step 10: Publish

Click the publish button:
```bash
playwright-cli click 'button:has-text("发布")'
```

If a confirmation dialog appears:
```bash
playwright-cli snapshot
# Find confirm button
playwright-cli click <confirm_button_ref>
```

### Step 11: Verify Success

Check the URL for success indicators:
- URL should contain `edit-done`
- URL contains `postId=<id>`
- URL contains `isPublished=true`

## Error Handling

### Session Validation Error

If you see "会话校验失败" (session validation failed):

```bash
playwright-cli close
playwright-cli open --headed --persistent https://i.cnblogs.com/posts/edit
# Retry the workflow
```

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### 400 Bad Request

This usually means:
1. Session expired - refresh browser
2. Required field missing - check category, tags, summary
3. Content too long - may need to split

## Common Element Selectors

| Element | Selector |
|---------|----------|
| Title input | `#post-title` or `textbox "标题"` |
| Content editor | `.CodeMirror-code` |
| Category dropdown | `.cnb-tree-category-select__container` |
| Collection checkbox | `input[id="<collection_id>"]` |
| Submission checkbox | `input[id="isToHomeCandidate"]` |
| Site category radio | `input#<category_name>[type="radio"]` |
| Tag dropdown | `nz-select` |
| Summary textarea | `#summary` |
| Publish button | `button:has-text("发布")` |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://i.cnblogs.com/posts/edit

# Fill title
playwright-cli fill '#post-title' "My Article Title"

# Fill content
cat article.md | pbcopy
playwright-cli click ".CodeMirror-code"
playwright-cli press "Meta+v"

# Configure settings
playwright-cli click ".cnb-tree-category-select__container"
playwright-cli click '[title="小林AI实战教程"]'
playwright-cli click 'input[id="38977"]'
playwright-cli click 'input[id="isToHomeCandidate"]'
playwright-cli eval "document.querySelector('input#Java[type=\"radio\"]')?.click()"

# Add tag
playwright-cli click "nz-select"
playwright-cli click '[title="Java"]'
playwright-cli press Escape

# Fill summary
playwright-cli fill "#summary" "Article summary..."

# Publish
playwright-cli click 'button:has-text("发布")'

# Verify
playwright-cli snapshot --depth=2
# Check URL contains edit-done;postId=...;isPublished=true
```

## Tips

1. Always take snapshots to get current element refs
2. Use `--depth` parameter for partial snapshots when full snapshot is too large
3. JavaScript evaluation (`playwright-cli eval`) is useful for hard-to-click elements
4. Close browser when done: `playwright-cli close`
