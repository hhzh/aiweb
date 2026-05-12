# 51CTO Publisher Skill

Automate publishing Markdown articles to 51CTO using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into 51CTO (persistent browser profile handles this)

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# WRONG - includes frontmatter
cat article.md | pbcopy

# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md | pbcopy  # Start from first heading
```

### Article Category Selection

51CTO requires selecting both a primary category (一级分类) and a secondary category (二级分类). After selecting the primary category, a secondary category dropdown will appear.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://blog.51cto.com/blogger/publish
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox ref
playwright-cli fill <ref> "Article Title Here"
```

The title input has placeholder "请输入标题，您可以输入100个字".

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content.

```bash
# Skip frontmatter and copy content starting from first heading
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Click editor and paste
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"
```

The content editor has placeholder "请输入正文".

### Step 4: Click Publish Button

Click the "发布文章" button to open the publish dialog:

```bash
playwright-cli snapshot
# Find the "发布文章" button ref
playwright-cli click <publish_button_ref>
```

This will open a dialog with category and tag settings.

### Step 5: Select Article Category (一级分类)

In the publish dialog, select the primary category:

```bash
playwright-cli snapshot
# Find the category item and click it
playwright-cli click <category_ref>
```

Common categories:
- "代码人生" - value="43"
- "人工智能" - value="36"
- "前端开发" - value="30"
- "后端开发" - value="31"

### Step 6: Select Secondary Category (二级分类)

After selecting primary category, secondary category options appear but may NOT be visible in the snapshot as clickable elements. Use JavaScript to click them:

```bash
# First, find available secondary categories
playwright-cli eval "document.querySelector('#twoLever')?.innerHTML"

# Then select one by its value attribute (via JS click)
playwright-cli eval "document.querySelector('.second-types-item[value=\"206\"]')?.click()"
```

Common secondary categories for "人工智能" (values may change — always verify with `#twoLever`):
- "深度学习" - value="92"
- "机器学习" - value="155"
- "NLP" - value="150"
- "计算机视觉" - value="148"
- "数据分析" - value="151"
- "数据挖掘" - value="152"
- "神经网络" - value="153"
- "数据可视化" - value="154"
- "PyTorch" - value="149"
- "数据结构与算法" - value="147"

**Important**: The secondary category items (`.second-types-item`) often cannot be clicked via `playwright-cli click` because they are not rendered as standard interactive elements. Use `playwright-cli eval` with JavaScript click instead. To verify selection, check for `second-types-item-check` class (NOT `.active`):
```bash
playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"
```

### Step 7: Configure Personal Category

The personal category field is a **readonly dropdown** — `playwright-cli fill` will NOT work. Click the dropdown first, then select from options:

```bash
# Click the dropdown to open it (readonly input, cannot fill)
playwright-cli eval "document.querySelector('#selfType')?.click()"

# Wait for options to appear
sleep 1
playwright-cli snapshot
# Find and click the personal category option (listitem)
playwright-cli click <personal_category_item_ref>
```
playwright-cli snapshot
playwright-cli click <personal_category_item_ref>
```

The personal category list is in `#selfType_list`.

### Step 8: Add Tags

**CRITICAL**: 51CTO auto-generates tags from article content. These auto-tags are often irrelevant (e.g., "Code", "运行测试", "搜索"). You MUST remove them first before adding your own tags.

```bash
# Remove all auto-generated tags
playwright-cli eval "document.querySelectorAll('.has-list .iconeditor').forEach(el => el.click())"

# Verify all tags are removed
playwright-cli eval "document.querySelectorAll('.has-list > span').length"
# Should be 0
```

Tags must be entered **one at a time** with Enter key after each. Do NOT use comma-separated input:

```bash
# Add tags one by one
playwright-cli fill <tag_input_ref> "AI编程"
playwright-cli press "Enter"

playwright-cli snapshot  # Get fresh ref after each tag
playwright-cli fill <tag_input_ref> "Claude"
playwright-cli press "Enter"

# Repeat for more tags (max 5)
```

**Important**: After each tag is added, the input ref may change. Take a snapshot to get the fresh ref before adding the next tag. Comma-separated input does NOT work as expected.

### Step 9: Select Topic

Click the topic input to show dropdown, then select from the list:

```bash
# Click the topic input to show dropdown
playwright-cli click <topic_input_ref>

# Wait for options to appear
sleep 1
playwright-cli snapshot
# Click on the desired topic (listitem)
playwright-cli click <topic_ref>
```

Topic selection is important for 51CTO — articles without a topic may fail to publish.

Common topics:
- "#我和 AI 的故事#" - value="32"
- "#ChatGPT初体验#" - value="15"
- "#AIGC二三事#" - value="20"

### Step 10: Fill Summary (Optional)

```bash
playwright-cli fill "#abstractData" "Article summary text..."
```

If left empty, the first 200 characters will be used automatically.

### Step 11: Publish

Click the publish button in the dialog:

```bash
playwright-cli snapshot
# Find the final publish button in dialog
playwright-cli click <publish_button_ref>
```

### Step 12: Verify Success

Check for success indicators:
- URL should change to article view page
- Success message appears

## Error Handling

### Dialog Not Appearing

If the publish dialog doesn't appear:
```bash
playwright-cli snapshot
# Ensure title and content are filled
# Try clicking publish button again
```

### Category Selection Issues

If secondary category doesn't appear after selecting primary category:
```bash
# Wait a moment and take snapshot again
sleep 1
playwright-cli snapshot
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

### Publish Button Clicked But Page Does Not Change

If clicking "发布" doesn't redirect to a success page, check for missing required fields:
1. **Secondary category (二级分类)**: Must be selected — use JS: `playwright-cli eval "document.querySelector('.second-types-item[value=\"206\"]')?.click()"`
2. **Topic (话题)**: Should be selected from the dropdown
3. **Tags**: At least one tag is required

The most common issue is that the secondary category is not actually selected, even though the UI looks like it was clicked. Verify with: `playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"`

## Common Element Selectors

| Element | Selector/Description |
|---------|----------|
| Title input | Textbox with placeholder "请输入标题，您可以输入100个字" |
| Content editor | Textbox with placeholder "请输入正文" |
| Publish button | Button with text "发布文章" |
| Category dropdown | `.select_item` items in `#oneLever` |
| Secondary category | Items in `#twoLever` |
| Personal category dropdown | `#selfType` |
| Personal category list | `#selfType_list` |
| Tag input | `#tag-input` |
| Topic dropdown | `#subjuct` |
| Topic list | `#listItemList` |
| Summary textarea | `#abstractData` |
| Dialog publish button | Button in `.dialog-editor` |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://blog.51cto.com/blogger/publish

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"

# Click publish to open dialog
playwright-cli click <publish_button_ref>

# Wait for dialog
playwright-cli snapshot

# Select article category "人工智能"
playwright-cli eval "document.querySelector('.select_item[value=\"36\"]')?.click()"

# Wait for secondary category to appear, then select via JS
sleep 1
playwright-cli eval "document.querySelector('.second-types-item[value=\"206\"]')?.click()"

# Select personal category (readonly dropdown, click then select)
playwright-cli eval "document.querySelector('#selfType')?.click()"
sleep 1
playwright-cli snapshot
playwright-cli click <personal_category_item_ref>

# Add tags one by one
playwright-cli fill <tag_input_ref> "AI"
playwright-cli press "Enter"
playwright-cli snapshot
playwright-cli fill <tag_input_ref> "Claude Code"
playwright-cli press "Enter"

# Select topic from dropdown
playwright-cli click <topic_input_ref>
sleep 1
playwright-cli snapshot
playwright-cli click <topic_ref>  # e.g., "#ChatGPT初体验#"

# Click publish in dialog
playwright-cli snapshot
playwright-cli click <dialog_publish_button_ref>

# Verify - should redirect to success page
playwright-cli eval "window.location.href"
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Primary category selection triggers secondary category dropdown
4. Tags can be entered directly without dropdown selection
5. Topics are optional but recommended for better visibility
6. Close browser when done: `playwright-cli close`
7. 51CTO auto-generates irrelevant tags from content — always remove them first with `document.querySelectorAll('.has-list .iconeditor').forEach(el => el.click())`
8. After 5 tags, the tag input becomes invisible (`element is not visible` error) — this is normal, just proceed with other fields
9. Secondary category uses `second-types-item-check` class (not `.active`) — verify with `document.querySelector('.second-types-item-check')?.textContent`
10. Topic options can be accessed via `#listItemList` after clicking `#subjuct` — use JS click to select
