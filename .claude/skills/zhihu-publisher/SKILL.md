# Zhihu Publisher Skill

Automate publishing Markdown articles to Zhihu Zhuanlan (知乎专栏) using playwright-cli browser automation.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into Zhihu (persistent browser profile handles this)

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# WRONG - includes frontmatter
cat article.md | pbcopy

# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md | pbcopy  # Start from first heading
```

### Special Format Detection

When pasting Markdown content, Zhihu may detect special formats and show a dialog asking to confirm parsing. Click "确认并解析" to continue.

### Topics Limit

Zhihu allows selecting multiple topics for an article. Topics help with article discovery.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Fill Article Title

```bash
playwright-cli snapshot
# Find the title textbox (placeholder: "请输入标题（最多 100 个字）")
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

The editor is a rich text editor that supports Markdown syntax.

### Step 4: Confirm Markdown Parsing

If a dialog appears with "识别到特殊格式，请确认是否将 Markdown 解析为正确格式":

```bash
playwright-cli snapshot
# Find the "确认并解析" button
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('确认并解析'))?.click()"
```

### Step 5: Configure Contribute to Question (Optional)

To contribute the article to a related question, you must click the **combobox** below the "投稿至问题" button (NOT the button itself). The combobox shows "未选择" by default:

```bash
playwright-cli snapshot
# Find the combobox that shows "未选择" (below the "投稿至问题" text)
# It is a combobox element, NOT the button labeled "投稿至问题"
playwright-cli click <combobox_ref>
```

After clicking the combobox, a question search dialog will appear with recommended questions. You can either search or directly select from recommendations:

```bash
# Option A: Search for a specific question
playwright-cli fill <search_combobox_ref> "search keyword"
playwright-cli click <search_button_ref>

# Option B: Directly select from recommended questions (no search needed)
# Click on the first question's "选择" button
playwright-cli snapshot
playwright-cli click <first_select_button_ref>

# Confirm selection by clicking "确定"
playwright-cli click <confirm_button_ref>
```

**Important**: The "投稿至问题" button itself only toggles the section visibility. To actually open the question picker dialog, you must click the combobox (showing "未选择") underneath it.

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

### Step 8: Verify Success

Check the URL for success indicators:
- URL should change to article view: `https://zhuanlan.zhihu.com/p/<article_id>`
- Page title should show the article title

```bash
playwright-cli eval "window.location.href"
# Should contain: /p/ and NOT contain /edit
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

## Common Element Selectors

| Element | Description |
|---------|-------------|
| Title input | Textbox with placeholder "请输入标题（最多 100 个字）" |
| Content editor | Textbox for article body |
| Confirm parse button | Button with text "确认并解析" |
| Contribute to question button | Button "投稿至问题" (toggles section visibility) |
| Contribute to question combobox | Combobox showing "未选择" (opens question picker dialog) |
| Question search input | Combobox "搜索" in question picker dialog |
| Question select button | Button "选择" in question list |
| Confirm button | Button "确定" in dialogs |
| Add topic button | Button "添加话题" |
| Topic search input | Textbox with placeholder "搜索话题..." |
| Topic button | Button with topic name (e.g., "AI", "AI技术") |
| Publish button | Button "发布" |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://zhuanlan.zhihu.com/write

# Get initial snapshot
playwright-cli snapshot

# Fill title
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli click <editor_ref>
playwright-cli press "Meta+v"

# Confirm Markdown parsing if dialog appears
playwright-cli eval "[...document.querySelectorAll('button')].find(btn => btn.textContent.includes('确认并解析'))?.click()"

# Wait for parsing
sleep 2

# Contribute to question (optional)
# IMPORTANT: Click the combobox (showing "未选择"), NOT the "投稿至问题" button
playwright-cli snapshot
playwright-cli click <combobox_ref>  # Combobox showing "未选择"
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

# Verify
playwright-cli eval "window.location.href"
# Should contain: /p/ and NOT /edit
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Title is limited to 100 characters
4. Use JavaScript evaluation for elements that are hard to click
5. Topics help with article discovery
6. Close browser when done: `playwright-cli close`
