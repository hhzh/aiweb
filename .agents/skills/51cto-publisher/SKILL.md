---
name: 51cto-publisher
description: Publish Markdown articles to 51CTO using playwright-cli automation. Use when the user wants to publish articles to 51CTO, especially when they provide a Markdown file path. Handles title, content, tags, categories, and publication settings automatically.
---

# 51CTO Publisher Skill

Automate publishing Markdown articles to 51CTO using playwright-cli browser automation.

## Title Override

If `publishTitle` is provided in the skill arguments or context, use it as the article title for publishing (instead of extracting from the Markdown file). This allows publishing with an optimized title without modifying the local Markdown file.

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into 51CTO (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Important Notes

### Markdown Frontmatter Handling

**CRITICAL**: When copying Markdown content, skip the YAML frontmatter (the section between `---` markers). The frontmatter contains metadata like title, date, and tags that should NOT be included in the published article content.

```bash
# CORRECT - skip frontmatter
sed -n '/^# /,$p' article.md | pbcopy
```

### v-note-read-model Overlay (CRITICAL)

51CTO's editor has a `.v-note-read-model` overlay that intercepts ALL pointer events. This overlay MUST be removed before interacting with the editor or any elements behind it:

```bash
# Remove the overlay FIRST before any editor interaction
playwright-cli eval "document.querySelectorAll('.v-note-read-model').forEach(el => el.remove())"
```

Without this step, `playwright-cli click` on the editor will fail with "intercepts pointer events".

### Vue.js Input Reactivity (CRITICAL)

51CTO uses Vue.js, and `playwright-cli fill` on Vue-controlled inputs may NOT trigger Vue's reactivity. Use the native value setter pattern to properly set input values and dispatch events:

```bash
# For Vue.js inputs where fill doesn't work
playwright-cli eval "(function(){var el=document.querySelector('SELECTOR');var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;nativeSetter.call(el,'VALUE');el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"
```

For the content textarea specifically, use base64 encoding with UTF-8 decoding + native setter:

```bash
# Prepare content
content=$(sed -n '/^# /,$p' /path/to/article.md | base64 | tr -d '\n')

# Inject via base64 + native setter
playwright-cli eval "(function(){var b64='${content}';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);var el=document.querySelector('textarea[placeholder=\"请输入正文\"]');if(!el){el=document.querySelector('#editor');}var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;nativeSetter.call(el,content);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"
```

### Article Category Selection

51CTO requires selecting both a primary category (一级分类) and a secondary category (二级分类). After selecting the primary category, a secondary category dropdown will appear. Both MUST be selected via JavaScript — `playwright-cli click` does NOT work reliably for these elements.

### Click Reliability

Many 51CTO UI elements cannot be clicked via `playwright-cli click` due to Vue.js rendering or overlay interception. Default to using `playwright-cli eval` with JavaScript clicks for reliability.

## Workflow

### Step 1: Open Browser

```bash
playwright-cli open --headed --persistent https://blog.51cto.com/blogger/publish
```

The `--headed` flag shows the browser UI, `--persistent` saves login state.

### Step 2: Remove Editor Overlay

**MUST do this before any editor interaction:**

```bash
playwright-cli eval "document.querySelectorAll('.v-note-read-model').forEach(el => el.remove())"
```

### Step 3: Fill Article Title

**IMPORTANT**: If `publishTitle` is provided in context, use it as the title. Otherwise, extract the title from the first `# ` heading in the Markdown file.

```bash
playwright-cli snapshot
# Find the title textbox ref
playwright-cli fill <ref> "Article Title Here"
```

The title input has placeholder "请输入标题，您可以输入100个字".

If `fill` doesn't work (Vue reactivity issue), use JS:

```bash
playwright-cli eval "(function(){var el=document.querySelector('input[placeholder=\"请输入标题，您可以输入100个字\"]');el.focus();document.execCommand('selectAll');document.execCommand('insertText',false,'Article Title Here');})()"
```

### Step 4: Fill Article Content

**IMPORTANT**: Skip YAML frontmatter. Use base64 + native setter for reliable content injection.

```bash
# Prepare content: skip frontmatter, base64 encode
content=$(sed -n '/^# /,$p' /path/to/article.md | base64 | tr -d '\n')

# Inject via base64 + native setter (handles Chinese + Vue reactivity)
playwright-cli eval "(function(){var b64='${content}';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);var el=document.querySelector('textarea[placeholder=\"请输入正文\"]');if(!el){el=document.querySelector('#editor');}var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;nativeSetter.call(el,content);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"
```

Verify content was set:

```bash
playwright-cli eval "document.querySelector('textarea[placeholder=\"请输入正文\"]')?.value?.substring(0,100)"
```

### Step 5: Click Publish Button

Click the "发布文章" button to open the publish dialog:

```bash
playwright-cli snapshot
# Find the "发布文章" button ref
playwright-cli click <publish_button_ref>
```

If click fails, use JS:

```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('发布文章'))?.click()"
```

### Step 6: Select Article Category (一级分类)

**Always use JavaScript** — `playwright-cli click` on category items is unreliable:

```bash
# Select primary category via JS
playwright-cli eval "document.querySelector('.select_item[value=\"36\"]')?.click()"
```

Common categories:
- "代码人生" - value="43"
- "人工智能" - value="36"
- "前端开发" - value="30"
- "后端开发" - value="31"

### Step 7: Select Secondary Category (二级分类)

After selecting primary category, wait for secondary options, then select via JS:

```bash
# Wait for secondary category to appear
sleep 1

# First, check available secondary categories
playwright-cli eval "document.querySelector('#twoLever')?.innerHTML"

# Then select one via JS click (NOT playwright-cli click)
playwright-cli eval "document.querySelector('.second-types-item[value=\"206\"]')?.click()"

# Verify selection — look for second-types-item-check class
playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"
```

Common secondary categories for "人工智能" (values change dynamically — always verify with `#twoLever` before selecting):
- "深度学习" - value="92"
- "机器学习" - value="155"
- "NLP" - value="150"
- "数据分析" - value="151"
- "AI IDE" - value="206" (may appear intermittently)
- "代码生成" - value="207" (may appear intermittently)

**CRITICAL**: If verification returns `undefined`, the selection failed. Retry with JS click. `playwright-cli click` on `.second-types-item` does NOT trigger the actual selection.

### Step 8: Configure Personal Category

Personal category is required. Use JS for the dropdown:

```bash
# Click the dropdown to open it
playwright-cli eval "document.querySelector('#selfType')?.click()"

# Wait for options, then select first item via JS
sleep 1
playwright-cli eval "document.querySelector('#selfType_list li')?.click()"
```

Common personal categories:
- "小林AI实战教程"

If JS click doesn't work, try from snapshot:

```bash
playwright-cli snapshot
# Find and click the personal category option (listitem)
playwright-cli click <personal_category_item_ref>
```

### Step 9: Add Tags

**CRITICAL**: 51CTO auto-generates irrelevant tags from article content (e.g., "Code", "运行测试", "搜索"). You MUST remove them first.

```bash
# Remove all auto-generated tags — use innerHTML clearing for reliability
playwright-cli eval "document.querySelector('.has-list').innerHTML = ''"

# Verify all tags are removed
playwright-cli eval "document.querySelectorAll('.has-list > span').length"
# Should be 0
```

Tags must be entered **one at a time** with Enter key. Use `playwright-cli run-code` for reliable Vue input handling:

```bash
# Add tags using run-code for proper Vue event dispatch
playwright-cli run-code "const input = page.locator('#tag-input'); await input.click(); await input.fill('AI编程'); await page.keyboard.press('Enter');"

sleep 1

playwright-cli run-code "const input = page.locator('#tag-input'); await input.click(); await input.fill('Codex'); await page.keyboard.press('Enter');"

sleep 1

# Repeat for more tags (max 5)
```

If `run-code` is unavailable, fallback to fill + Enter with snapshot refresh between each tag:

```bash
playwright-cli snapshot
playwright-cli fill <tag_input_ref> "AI编程"
playwright-cli press "Enter"
playwright-cli snapshot
playwright-cli fill <tag_input_ref> "Codex"
playwright-cli press "Enter"
```

**Important**: After 5 tags, the tag input becomes invisible — this is normal, proceed with other fields.

### Step 10: Select Topic

Topic selection is required for publishing. Use JS to interact with the dropdown:

```bash
# Click topic dropdown via JS
playwright-cli eval "document.querySelector('#subjuct')?.click()"

# Wait for options
sleep 1

# Get available topics
playwright-cli eval "document.querySelector('#listItemList')?.innerText"

# Select first topic via JS
playwright-cli eval "document.querySelector('#listItemList li')?.click()"
```

Common topics (always verify with current dropdown — topics change frequently):
- "#AI应用从工具到伙伴跨越#"
- "#我和 AI 的故事#"
- "#AI代码正在重新定义\"编程\"这件事#"
- "#这些工具让大模型用起来更顺手#"

### Step 11: Fill Summary (Optional)

```bash
playwright-cli fill "#abstractData" "Article summary text..."
```

If left empty, the first 200 characters will be used automatically.

### Step 12: Publish

Click the publish button in the dialog:

```bash
playwright-cli snapshot
# Find the final publish button in dialog
playwright-cli click <publish_button_ref>
```

If click fails, use JS:

```bash
playwright-cli eval "[...document.querySelectorAll('button')].find(b => b.textContent.includes('发布') && !b.textContent.includes('发布文章'))?.click()"
```

### Step 13: Verify Success

Check for success indicators:
- URL should change to article view page (contains `/success/` or article ID)
- Success message appears

```bash
playwright-cli eval "window.location.href"
```

## Error Handling

### Editor Click Intercepted

If `playwright-cli click` on the editor fails with "intercepts pointer events":

```bash
# Remove the overlay
playwright-cli eval "document.querySelectorAll('.v-note-read-model').forEach(el => el.remove())"
# Then retry the interaction
```

### Vue.js Fill Not Working

If `playwright-cli fill` doesn't update the input value (Vue reactivity not triggered):

```bash
# Use native setter pattern for textareas
playwright-cli eval "(function(){var el=document.querySelector('SELECTOR');var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;nativeSetter.call(el,'VALUE');el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"

# For text inputs, use HTMLInputElement.prototype
playwright-cli eval "(function(){var el=document.querySelector('SELECTOR');var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;nativeSetter.call(el,'VALUE');el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"
```

### Browser Crashed

If the browser crashes during publishing:

```bash
playwright-cli close 2>/dev/null || true
playwright-cli open --headed --persistent https://blog.51cto.com/blogger/publish
# Remove overlay, then re-fill title and content using the base64 + native setter method
```

### Category Selection Issues

**CRITICAL**: Secondary category MUST be selected via JavaScript click — `playwright-cli click` does NOT trigger the actual selection. Always use:

```bash
playwright-cli eval "document.querySelector('.second-types-item[value=\"XXX\"]')?.click()"
```

Then verify with:

```bash
playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"
```

If it returns `undefined`, the selection failed and you must retry with JS click.

### Publish Button Clicked But Page Does Not Change

If clicking "发布" doesn't redirect to a success page, check for missing required fields:
1. **Secondary category (二级分类)**: Must be selected and verified
2. **Topic (话题)**: Should be selected from the dropdown
3. **Tags**: At least one tag is required

The most common issue is that the secondary category is not actually selected. Verify with:

```bash
playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"
```

### Element Not Found

If element refs are stale:

```bash
playwright-cli snapshot
# Use new refs from snapshot
```

### Content Contains Frontmatter

If the published content shows YAML frontmatter:
1. Re-inject content using the base64 + native setter method (which skips frontmatter)

## Common Element Selectors

| Element | Selector/Description | Reliable Method |
|---------|----------|------------|
| Title input | `input[placeholder="请输入标题，您可以输入100个字"]` | fill or JS native setter |
| Content editor | `textarea[placeholder="请输入正文"]` | Base64 + native setter ONLY |
| Publish button | Button with text "发布文章" | click or JS |
| Category dropdown | `.select_item` items in `#oneLever` | JS click ONLY |
| Secondary category | `.second-types-item` in `#twoLever` | JS click ONLY |
| Personal category dropdown | `#selfType` | JS click ONLY |
| Personal category list | `#selfType_list` | JS click or snapshot ref |
| Tag input | `#tag-input` | run-code or fill + Enter |
| Topic dropdown | `#subjuct` | JS click ONLY |
| Topic list | `#listItemList` | JS click ONLY |
| Summary textarea | `#abstractData` | fill |
| Dialog publish button | Button in `.dialog-editor` | click or JS |
| Editor overlay | `.v-note-read-model` | Must remove before editor interaction |

## Complete Example

```bash
# Open browser
playwright-cli open --headed --persistent https://blog.51cto.com/blogger/publish

# Remove editor overlay FIRST
playwright-cli eval "document.querySelectorAll('.v-note-read-model').forEach(el => el.remove())"

# Fill title
playwright-cli snapshot
playwright-cli fill <title_ref> "My Article Title"

# Fill content (skip frontmatter, base64 + native setter)
content=$(sed -n '/^# /,$p' article.md | base64 | tr -d '\n')
playwright-cli eval "(function(){var b64='${content}';var bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));var content=new TextDecoder('utf-8').decode(bytes);var el=document.querySelector('textarea[placeholder=\"请输入正文\"]');var nativeSetter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;nativeSetter.call(el,content);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));})()"

# Click publish to open dialog
playwright-cli snapshot
playwright-cli click <publish_button_ref>

# Select article category "人工智能" via JS
playwright-cli eval "document.querySelector('.select_item[value=\"36\"]')?.click()"

# Select secondary category via JS
sleep 1
playwright-cli eval "document.querySelector('.second-types-item[value=\"206\"]')?.click()"

# Verify secondary category selection
playwright-cli eval "document.querySelector('.second-types-item-check')?.textContent"

# Select personal category via JS
playwright-cli eval "document.querySelector('#selfType')?.click()"
sleep 1
playwright-cli eval "document.querySelector('#selfType_list li')?.click()"

# Remove auto-generated tags, then add custom tags
playwright-cli eval "document.querySelector('.has-list').innerHTML = ''"
playwright-cli run-code "const input = page.locator('#tag-input'); await input.click(); await input.fill('AI编程'); await page.keyboard.press('Enter');"
sleep 1
playwright-cli run-code "const input = page.locator('#tag-input'); await input.click(); await input.fill('Codex'); await page.keyboard.press('Enter');"

# Select topic via JS
playwright-cli eval "document.querySelector('#subjuct')?.click()"
sleep 1
playwright-cli eval "document.querySelector('#listItemList li')?.click()"

# Click publish in dialog
playwright-cli snapshot
playwright-cli click <dialog_publish_button_ref>

# Verify - should redirect to success page
playwright-cli eval "window.location.href"
```

## Tips

1. Always remove `.v-note-read-model` overlay before interacting with the editor
2. Use base64 + native setter for content injection — regular fill/paste is unreliable
3. Use JS clicks for category, secondary category, personal category, and topic — `playwright-cli click` doesn't work for these Vue.js elements
4. Remove auto-generated tags with `innerHTML = ''` — individual close icon clicks are unreliable
5. Use `run-code` for tag input if available — it properly dispatches Vue events
6. Always verify secondary category selection with `.second-types-item-check`
7. Close browser when done: `playwright-cli close`
8. If browser crashes, reopen and re-fill title + content using the base64 method
9. After 5 tags, the tag input becomes invisible — this is normal, proceed with other fields
10. Default to `playwright-cli eval` over `playwright-cli click` for most 51CTO elements — it's more reliable
