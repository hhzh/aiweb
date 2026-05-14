# Aliyun Publisher Skill

Automate publishing Markdown articles to Aliyun Developer Community using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Aliyun (persistent browser profile handles this)

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

### Security Verification

Aliyun may require a security verification (slider captcha) before publishing. This is handled automatically by the browser's persistent session.

### Content Review

After publishing, articles enter a content review state ("内容审核中，请耐心等待"). This is normal and articles will be available after review.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://developer.aliyun.com/article/new#/
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "请填写标题")
playwright-cli fill <title_ref> "Article Title Here"
```

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content.

```bash
# Skip frontmatter and copy content starting from first heading
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Click editor and paste
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"
```

The editor is a rich text editor with a preview area.

### Step 4: Fill Summary

Fill the summary field (max 300 characters):

```bash
playwright-cli fill '[placeholder="请填写摘要"]' "Article summary text..."
```

If left empty, you can click "AI生成摘要" to auto-generate.

### Step 5: Select Sub-Community

Click the sub-community dropdown and select the appropriate community:

```bash
playwright-cli snapshot
# Find the sub-community dropdown
playwright-cli click <sub_community_dropdown_ref>

# Wait for dropdown
playwright-cli snapshot
# Find and click the community option (e.g., "千问大模型")
playwright-cli click <community_option_ref>
```

Common sub-communities:
- 千问大模型 - for AI related content
- 开发者社区 - general developer content

### Step 6: Configure Article Settings (Optional)

#### Article Image
You can upload a cover image (recommended size: 200x120):
```bash
playwright-cli click <upload_image_button>
```

#### Article Reading Settings
By default, the article type is "原创" (original). You can change it if needed.

### Step 7: Click Publish Button

Click the "发布文章" button:

```bash
playwright-cli snapshot
# Find the "发布文章" button
playwright-cli click <publish_button_ref>
```

### Step 8: Confirm Publication

A confirmation dialog will appear asking "您确定发布文章？":

```bash
playwright-cli snapshot
# Find the "确认" button in the dialog
playwright-cli click <confirm_button_ref>
```

### Step 9: Security Verification (If Required)

If a security verification slider appears, it will typically complete automatically with the persistent session. If not, manual intervention may be needed.

### Step 10: Verify Success

Check the URL for success indicators:
- URL should change to article view: `https://developer.aliyun.com/article/<article_id>`
- Page title should show the article title
- Page may show "内容审核中，请耐心等待" (content under review)

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

### Sub-Community Not Selected

If sub-community dropdown doesn't open:
```bash
# Try using JavaScript evaluation
playwright-cli eval "document.querySelector('.next-select')?.click()"
```

### Security Verification Failed

If security verification keeps failing:
1. Close browser: `playwright-cli close`
2. Reopen and login again: `playwright-cli open --headed --persistent https://developer.aliyun.com/article/new#/`
3. Retry the workflow

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | Textbox with placeholder "请填写标题" |
| Content editor | Rich text editor area |
| Summary textarea | Textbox with placeholder "请填写摘要" |
| Sub-community dropdown | `.next-select` element |
| AI generate summary | Button text "AI生成摘要" |
| Upload image | Button "上传图片" |
| Publish button | Button "发布文章" |
| Confirm button | Button "确认" in dialog |
| Cancel button | Button "取消" in dialog |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://developer.aliyun.com/article/new#/

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"

# Fill summary
playwright-cli fill '[placeholder="请填写摘要"]' "Article summary text..."

# Select sub-community
playwright-cli click <sub_community_dropdown_ref>
playwright-cli snapshot
playwright-cli click <千问大模型_option_ref>

# Click publish button
playwright-cli click <publish_button_ref>

# Confirm dialog
playwright-cli snapshot
playwright-cli click <confirm_button_ref>

# Wait for verification and verify success
sleep 3
playwright-cli eval "window.location.href"
# Should contain: /article/
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Summary is limited to 300 characters
4. Sub-community selection is required for better visibility
5. Articles enter content review after publishing
6. Security verification may appear - it's usually automatic
7. Close browser when done: `playwright-cli close`
