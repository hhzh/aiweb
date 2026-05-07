---
name: csdn-publisher
description: Publish Markdown articles to CSDN using playwright-cli automation. Use when the user wants to publish articles to their CSDN blog, especially when they provide a Markdown file path. Handles title, content, tags, summary, category, article type, and publication settings automatically.
---

# CSDN Publisher Skill

Automate publishing Markdown articles to CSDN using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into CSDN (persistent browser profile handles this)

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# Skip frontmatter and copy content starting from first heading
sed -n '/^# /,$p' /path/to/article.md | pbcopy
```

### Editor Type

CSDN has two editors:
- Rich text editor (default)
- Markdown editor

To use Markdown editor, click "使用 MD 编辑器" button in the toolbar.

### Category Column

The category column (分类专栏) must be created before use. If you don't have existing categories, use "新建分类专栏" to create one. Common categories include:
- 小林AI实战教程
- AI编程
- 技术笔记

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://mp.csdn.net/mp_blog/creation/editor
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox
playwright-cli fill '#article-title' "Article Title Here"
# Or use ref:
playwright-cli fill <title_ref> "Article Title Here"
```

Title must be 5-100 characters.

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content.

```bash
# Skip frontmatter and copy content
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Click editor and paste
playwright-cli click "iframe"
playwright-cli press "Meta+v"
```

### Step 4: Add Article Tags

1. Click "添加文章标签" button:
```bash
playwright-cli snapshot
playwright-cli click <add_tag_button_ref>
```

2. Enter tag and select from dropdown:
```bash
playwright-cli fill <tag_input_ref> "ai"
playwright-cli snapshot
# Find and click the matching tag option
playwright-cli click <tag_option_ref>
```

3. Close tag dialog:
```bash
playwright-cli press Escape
```

### Step 5: Fill Article Summary

```bash
playwright-cli snapshot
playwright-cli fill <summary_ref> "Article summary text (max 256 characters)..."
```

### Step 6: Configure Category Column

Click the category area or create a new one:
```bash
playwright-cli snapshot
playwright-cli click <category_section_ref>
# Select existing category or click "新建分类专栏"
```

**Note**: If clicking the category option fails with "intercepts pointer events" error, use JavaScript:
```bash
playwright-cli eval "document.querySelector('label.tag__option-label')?.click()"
```

Then close the category dialog:
```bash
playwright-cli click <close_button_ref>
```

### Step 7: Select Article Type

Article types: 原创 (Original), 转载 (Reprint), 翻译 (Translation)

```bash
# Default is "原创" (already selected)
# To change:
playwright-cli click <radio_ref>  # e.g., radio "转载"
```

### Step 8: Configure Creative Declaration

Default is "无声明" (No declaration). To change:
```bash
playwright-cli click <declaration_dropdown_ref>
playwright-cli snapshot
playwright-cli click <declaration_option_ref>
```

### Step 9: Configure Article Backup

To enable GitCode backup:
```bash
playwright-cli snapshot
playwright-cli click <gitcode_checkbox_ref>
```

### Step 10: Configure Visibility

Options: 全部可见 (Public), 仅我可见 (Private), 粉丝可见 (Fans only), VIP可见 (VIP only)

```bash
# Default is "全部可见" (already selected)
# To change:
playwright-cli click <visibility_radio_ref>
```

### Step 11: Configure Activity and Topic

1. Click activity dropdown:
```bash
playwright-cli snapshot
playwright-cli click <activity_dropdown_ref>
```

2. Smart activity selection logic:
   - **Priority 1**: Select the first activity containing "征文挑战"
   - **Priority 2**: If no "征文挑战" activity exists, select the second activity

```bash
playwright-cli snapshot
# From the snapshot, find all activity options
# Look for activities containing "征文挑战" in their text
# If found, click the first one (e.g., 『AI先锋杯·14天征文挑战第15期』)
# If not found, click the second activity option
playwright-cli click <selected_activity_ref>
```

3. Select topic (if available):
```bash
playwright-cli snapshot
# Check if topic dropdown is enabled (not disabled)
# If enabled, click and select the first topic
playwright-cli click <topic_dropdown_ref>
playwright-cli snapshot
playwright-cli click <first_topic_ref>
```

Note: Topic dropdown may be disabled if the selected activity has no associated topics.

### Step 12: Publish

Click the publish button:
```bash
playwright-cli snapshot
playwright-cli click <publish_button_ref>
```

### Step 13: Verify Success

Check for success indicators:
- URL changes to `/mp_blog/creation/success/<article_id>`
- Page title shows "发布成功"
- Article ID is in the URL

```bash
playwright-cli eval "window.location.href"
# Should be like: https://mp.csdn.net/mp_blog/creation/success/160869159
```

### WeChat Verification

When publishing, CSDN may show a WeChat QR code verification dialog for security:
- Message: "为保障您的账号安全，请使用您绑定的微信扫码确认"
- If WeChat is already bound and verified, it will show "校验成功" and auto-close in 2 seconds
- Wait a few seconds for the verification to complete automatically

## Error Handling

### Element Intercepted/Blocked

If clicking an element fails with "intercepts pointer events" error, use JavaScript evaluation:
```bash
# For category selection
playwright-cli eval "document.querySelector('label.tag__option-label')?.click()"

# For other elements, find the appropriate selector
playwright-cli eval "document.querySelector('<css_selector>')?.click()"
```

### Element Not Found

If element refs are stale:
```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### AI Assistant Dialog

CSDN shows an AI assistant dialog on page load. Close it if needed:
```bash
playwright-cli snapshot
# Find and click close button or press Escape
playwright-cli press Escape
```

### Tag Limit

CSDN allows up to 8 tags per article. The counter shows remaining slots.

### Session Expired

If you see login prompts or session errors:
```bash
playwright-cli close
playwright-cli open --headed --persistent https://mp.csdn.net/mp_blog/creation/editor
# Re-login manually if needed
```

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | `textbox "请输入文章标题（5～100个字）"` |
| Content editor | `iframe` in application area |
| Add tag button | `button "添加文章标签"` |
| Tag input | `textbox "文章标签*"` |
| Summary textarea | `textbox "文章摘要"` |
| Category section | `group "分类专栏"` |
| Article type radio | `radio "原创"` / `radio "转载"` / `radio "翻译"` |
| Declaration dropdown | `combobox "创作声明"` |
| GitCode checkbox | `checkbox "同时备份到GitCode"` |
| Visibility radio | `radio "全部可见"` etc. |
| Activity dropdown | First dropdown in "参与活动/话题" section |
| Topic dropdown | Second dropdown in "参与活动/话题" section |
| Publish button | `button "发布博客"` |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://mp.csdn.net/mp_blog/creation/editor

# Wait for page load and close AI dialog if needed
sleep 2
playwright-cli press Escape

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"

# Add tag
playwright-cli click <add_tag_button_ref>
playwright-cli fill <tag_input_ref> "ai"
playwright-cli snapshot
playwright-cli click <ai_tag_option_ref>
playwright-cli press Escape

# Fill summary
playwright-cli fill <summary_ref> "This is my article summary..."

# Configure backup
playwright-cli click <gitcode_checkbox_ref>

# Select activity (smart selection: prefer "征文挑战" activities)
playwright-cli click <activity_dropdown_ref>
playwright-cli snapshot
# Check activity options for "征文挑战"
# If found, click the first matching activity
# Otherwise, click the second activity
playwright-cli click <selected_activity_ref>

# Select topic (first option if available)
playwright-cli click <topic_dropdown_ref>
playwright-cli snapshot
playwright-cli click <first_topic_ref>

# Publish
playwright-cli snapshot
playwright-cli click <publish_button_ref>

# Verify
playwright-cli snapshot
# Check for success indicators
```

## Tips

1. Always take snapshots to get current element refs
2. Use `--depth` parameter for partial snapshots when full snapshot is too large
3. Skip YAML frontmatter when copying Markdown content
4. Title must be 5-100 characters
5. Summary is limited to 256 characters
6. Maximum 8 tags per article
7. Close browser when done: `playwright-cli close`
8. The AI assistant dialog may appear - close it with Escape
9. Use JavaScript evaluation when elements are blocked by overlays
10. WeChat verification may appear during publish - wait for auto-verification if already bound
