---
name: csdn-publisher
description: Publish Markdown articles to CSDN using playwright-cli automation. Use when the user wants to publish articles to their CSDN blog, especially when they provide a Markdown file path. Handles title, content, tags, summary, category, article type, and publication settings automatically.
---

# CSDN Publisher Skill

Automate publishing Markdown articles to CSDN using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into CSDN (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

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
playwright-cli open --headed --persistent https://editor.csdn.net/md/
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

**Note**: Use `https://editor.csdn.net/md/` to open the Markdown editor directly. The old URL `https://mp.csdn.net/mp_blog/creation/editor` opens the rich text editor which requires an extra step to switch.

### Step 1.1: Handle Template Dialog

CSDN may show a template selection dialog ("插入模版(MarkDown)") on first load. If it appears:

```bash
playwright-cli snapshot
# Find the "取消" button in the dialog
playwright-cli click <cancel_button_ref>
```

The dialog contains templates like "学习计划模板示例", "系列文章模板" etc. Click "取消" to dismiss it.

### Step 1.2: Close AI Assistant Panel

CSDN shows an AI assistant panel on the right side. Close it to free up space:

```bash
playwright-cli snapshot
# Find the "关闭" button at the top of the AI assistant panel
playwright-cli click <close_button_ref>
```

### Step 2: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

**IMPORTANT**: `playwright-cli fill '#article-title'` does NOT work on CSDN's Markdown editor — the CSS selector doesn't match any element. Use one of these methods instead:

**Method 1: Click + type (recommended)**
```bash
playwright-cli snapshot
# The title area shows a generic element (e.g., ref=e10) with text "【无标题】"
# Click it to activate the input, then type the title
playwright-cli click <title_area_ref>
playwright-cli press "Meta+a"
playwright-cli type "Article Title Here"
```

**Method 2: JavaScript `execCommand`**
```bash
playwright-cli eval "(function(){var el=document.querySelector('.article-bar__title');if(el){el.focus();el.select();document.execCommand('selectAll');document.execCommand('insertText',false,'Article Title Here');}})()"
```

**Note**: If the title shows "【无标题】" prefix after typing, use Method 1 with `Meta+a` to select all existing text first, then type the correct title to overwrite it.

Title must be 5-100 characters.

### Step 3: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter when copying content.

For the Markdown editor (`https://editor.csdn.net/md/`):

```bash
# Skip frontmatter and copy content
sed -n '/^# /,$p' /path/to/article.md | pbcopy

# Focus the CodeMirror editor area
playwright-cli eval "document.querySelector('[contenteditable=true]')?.focus()"

# Select any existing content and paste
playwright-cli press "Meta+a"
playwright-cli press "Meta+v"
```

The Markdown editor uses CodeMirror, which doesn't have a traditional textbox. Use `contenteditable` focus + keyboard paste instead of clicking an iframe.

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

3. Close tag panel:
```bash
# Blur the tag input to close the tag panel
playwright-cli eval "document.querySelector('.tag__box')?.blur()"
```

**WARNING**: Do NOT use `Escape` to close the tag panel — it will close the entire publish dialog and lose all filled data (tags, summary, etc.).

### Step 5: Fill Article Summary

```bash
playwright-cli snapshot
playwright-cli fill <summary_ref> "Article summary text (max 256 characters)..."
```

### Step 6: Configure Category Column

**Category is optional** — if no existing categories match, you can skip this step entirely and proceed to publish.

If you have existing categories, select one:
```bash
playwright-cli snapshot
# Look for category labels in the dialog
playwright-cli click <category_label_ref>
```

If clicking the category option fails with "intercepts pointer events" error, use JavaScript:
```bash
playwright-cli eval "document.querySelector('label.tag__option-label')?.click()"
```

To create a new category, click "新建分类专栏":
```bash
playwright-cli eval "document.querySelectorAll('button.tag__btn-tag')[0]?.click()"
# If a dialog appears, fill in the category name and confirm
# If no dialog appears (common issue), skip category and publish without it
```

**Note**: The "新建分类专栏" button is often blocked by overlay elements. If JS click doesn't trigger a dialog, skip the category — it's not required for publishing.

Close the category dialog if one appeared:
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
# If click fails with "intercepts pointer events" error, use JS:
playwright-cli eval "document.querySelector('input[placeholder=\"请选择创作活动\"]')?.click()"
```

2. Smart activity selection logic:
   - **Priority 1**: Select the first activity containing "征稿", "征文", "挑战", or "创作" keywords
   - **Priority 2**: If no matching activity exists, select the second activity

```bash
playwright-cli snapshot
# From the snapshot, find all activity options
# Look for activities containing "征稿", "征文", "挑战", or "创作" in their text
# If found, click the first matching one
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

Click the publish button in the dialog:
```bash
playwright-cli snapshot
# Find the "发布文章" button in the dialog (not the toolbar one)
playwright-cli click <publish_dialog_button_ref>
```

**Note**: If click fails with "intercepts pointer events" error (common in the publish dialog), use JavaScript:
```bash
playwright-cli eval "document.querySelector('button.btn-b-red')?.click()"
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

### Click Fallback Pattern

When `playwright-cli click` fails (e.g., "intercepts pointer events", "element not visible", "element is not attached"), automatically fall back to JavaScript evaluation:

```bash
# Instead of: playwright-cli click <ref>
# Use: playwright-cli eval "document.querySelector('CSS_SELECTOR')?.click()"
```

For elements identified by ref (not CSS selector), use text-based JS click:

```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('BUTTON_TEXT'))?.click()"
```

Common CSDN overlays that block clicks: `mark-mask-box-div`, `.tag__box` combobox panel.

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

### AI Assistant Panel

CSDN shows an AI assistant panel on the right side of the editor. Close it by clicking the "关闭" button:
```bash
playwright-cli snapshot
# Find the "关闭" button at the top of the AI assistant panel
playwright-cli click <close_button_ref>
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

| Element | Selector / Description | Reliable Method |
|---------|----------------------|----------------|
| Title input | Generic element showing "【无标题】", click it then type (do NOT use `fill '#article-title'`) | click + type (NOT fill) |
| Content editor (MD) | `contenteditable` element, focus via JS | JS focus + paste |
| Template cancel | "取消" button in template dialog | click |
| AI assistant close | "关闭" button at top of AI panel | click |
| Add tag button | `button "添加文章标签"` | click |
| Tag input | `textbox "请输入文字搜索，Enter键入可添加自定义标签"` | fill + Enter |
| Summary textarea | `textbox "本内容会在各展现列表中展示..."` | fill |
| Category section | `button "新建分类专栏"` | JS click (overlay) |
| Category label | `label.tag__option-label` | JS click (overlay) |
| Article type | `generic` with text "原创"/"转载"/"翻译" | click |
| Declaration dropdown | `textbox "无声明"` | click |
| GitCode checkbox | `checkbox "同时备份到GitCode"` | click |
| Visibility options | `generic` with text "全部可见"/"仅我可见" etc. | click |
| Activity dropdown | `textbox "请选择创作活动"` | JS click (overlay) |
| Topic dropdown | `textbox "请选择创作话题"` | click |
| Publish button (toolbar) | `button "发布文章"` (first one) | click |
| Publish button (dialog) | `button "发布文章"` with class `btn-b-red` | JS click (overlay) |
| Tag combobox | `.tag__box` | blur to close (NOT Escape) |

## Complete Example

```bash
# Open Markdown editor
playwright-cli open --headed --persistent https://editor.csdn.net/md/

# Handle template dialog if it appears
playwright-cli snapshot
# Find and click "取消" to dismiss template dialog
playwright-cli click <cancel_button_ref>

# Close AI assistant panel
playwright-cli snapshot
playwright-cli click <close_ai_panel_ref>

# Fill title (click title area + type, NOT fill)
playwright-cli snapshot
playwright-cli click <title_area_ref>
playwright-cli press "Meta+a"
playwright-cli type "My Article Title"

# Fill content (skip frontmatter)
sed -n '/^# /,$p' article.md | pbcopy
playwright-cli eval "document.querySelector('[contenteditable=true]')?.focus()"
playwright-cli press "Meta+a"
playwright-cli press "Meta+v"

# Click publish button in toolbar to open dialog
playwright-cli snapshot
playwright-cli click <toolbar_publish_ref>

# Add tags in publish dialog
playwright-cli snapshot
playwright-cli click <add_tag_button_ref>
playwright-cli fill <tag_input_ref> "AI编程"
playwright-cli press "Enter"
playwright-cli fill <tag_input_ref> "Claude"
playwright-cli press "Enter"
playwright-cli fill <tag_input_ref> "AI工具"
playwright-cli press "Enter"
playwright-cli eval "document.querySelector('.tag__box')?.blur()"

# Fill summary
playwright-cli snapshot
playwright-cli fill <summary_ref> "Article summary text..."

# Select activity (use JS to bypass overlay)
playwright-cli eval "document.querySelector('input[placeholder=\"请选择创作活动\"]')?.click()"
playwright-cli snapshot
# Find activity containing "征稿", "征文", "挑战", or "创作" and click it
playwright-cli click <selected_activity_ref>

# Publish (use JS to bypass overlay)
playwright-cli eval "document.querySelector('button.btn-b-red')?.click()"

# Verify
playwright-cli eval "window.location.href"
# Should be like: https://mp.csdn.net/mp_blog/creation/success/160990174
```

## Tips

1. Always take snapshots to get current element refs
2. Skip YAML frontmatter when copying Markdown content
3. Title must be 5-100 characters
4. Summary is limited to 256 characters
5. Maximum 8 tags per article
6. Close browser when done: `playwright-cli close`
7. Use JavaScript evaluation when elements are blocked by `mark-mask-box-div` overlays — this is very common in the publish dialog
8. Do NOT use `Escape` to close the tag input panel — it will close the entire publish dialog and lose all data. Use `.tag__box` blur instead
9. WeChat verification may appear during publish — wait for auto-verification if already bound
10. Tags are entered by typing and pressing Enter — they are added as custom tags, no need to select from dropdown
11. The Markdown editor URL (`https://editor.csdn.net/md/`) is preferred over the rich text editor URL
12. Category column (分类专栏) is optional — if you can't create/select one, skip it and publish without
13. After filling tags, always blur the tag combobox (`.tag__box` blur) before interacting with other dialog elements, otherwise the tag panel may interfere
14. The publish dialog's "发布文章" button (class `btn-b-red`) is almost always blocked by overlays — always use `document.querySelector('button.btn-b-red')?.click()` JS method
