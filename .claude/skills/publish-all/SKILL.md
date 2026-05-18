---
name: publish-all
description: 一键发布 Markdown 文章到所有平台（CSDN、掘金、InfoQ、腾讯云、51CTO、知乎、博客园、思否）。提供 Markdown 文件路径即可自动串行发布到 8 个平台。
---

# Publish All Skill

一键发布 Markdown 文章到所有平台。提供 Markdown 文件路径，自动串行发布到 8 个平台。

## Prerequisites

- playwright-cli must be installed globally
- User must be logged into ALL target platforms (persistent browser profile handles this)

## Self-Optimization

**发布过程中如果遇到问题，就优化这个 skill。** When issues are encountered during publishing (e.g., elements not found, UI changes, workflow errors), update this skill's SKILL.md to fix the problem so it won't recur in future runs.

## Input

- **Required**: Markdown file path (e.g., `/path/to/article.md`)
- **Optional**: `publishTitle` — 发布标题（优化后的标题，用于网站展示，不修改本地文件）
- If `publishTitle` is not provided, title is extracted from the first `# ` heading in the file
- Content skips YAML frontmatter automatically

## Publish Order

Publish to platforms in this fixed serial order (problematic platforms first for early error detection):

1. 51CTO (most error-prone, handle first while attention is fresh)
2. CSDN
3. 掘金 (Juejin)
4. InfoQ
5. 腾讯云 (Tencent Cloud)
6. 知乎 (Zhihu)
7. 博客园 (Cnblogs)
8. 思否 (SegmentFault)

## Workflow

### Step 0: Extract Article Info & Prepare Content

Read the Markdown file to extract the title, verify the file exists, and prepare all content formats upfront:

```bash
# Extract title from first heading
originalTitle=$(grep -m1 '^# ' /path/to/article.md | sed 's/^# //')

# Verify file exists
if [ ! -f "/path/to/article.md" ]; then
  echo "Error: File not found"
  exit 1
fi

# Prepare content without frontmatter (skip YAML --- blocks)
sed -n '/^# /,$p' /path/to/article.md > /tmp/publish_content.md

# Prepare JSON-encoded content (for CodeMirror API injection - cnblogs)
python3 -c "
import json
with open('/tmp/publish_content.md', 'r') as f:
    content = f.read()
print(json.dumps(content))
" > /tmp/publish_content.json

# Prepare base64-encoded content (for CodeMirror editors - juejin, tencent)
cat /tmp/publish_content.md | base64 | tr -d '\n' > /tmp/publish_content_b64.txt

# Copy plain text content to clipboard (for paste-based editors - csdn, infoq, zhihu, 51cto, segmentfault)
cat /tmp/publish_content.md | pbcopy
```

This pre-preparation avoids re-processing the Markdown file for each platform (previously 8x `sed` + `base64` + `pbcopy`, now 1x).

### Step 0.5: Title Optimization (Optional)

If `publishTitle` is not provided in the skill arguments, use the `title-optimizer` skill to generate optimized titles for better click-through rates on publishing platforms. This only changes the title on the website — the local Markdown file is NOT modified.

1. Invoke the `title-optimizer` skill with the original title
2. Present the 5 optimized titles to the user
3. Ask the user to select one (or keep the original)
4. Set `publishTitle` to the user's choice

**Important**: If `publishTitle` is already provided in the skill arguments, skip this step entirely and use the provided title directly.

```
# Title optimization flow
If publishTitle is NOT provided:
  → Invoke Skill: title-optimizer (pass originalTitle)
  → Present 5 optimized titles to user
  → User selects one → set publishTitle = user's choice
  → User declines → set publishTitle = originalTitle
If publishTitle IS provided:
  → Skip optimization, use publishTitle directly
```

### Step 1: Publish to 51CTO

- Ensure no leftover browser session: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `51cto-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed: `playwright-cli close`
- Record result (success/failure + error message)

### Step 2: Publish to CSDN

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `csdn-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 3: Publish to 掘金 (Juejin)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `juejin-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 4: Publish to InfoQ

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `infoq-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 5: Publish to 腾讯云 (Tencent Cloud)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `tencent-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 6: Publish to 知乎 (Zhihu)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `zhihu-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 7: Publish to 博客园 (Cnblogs)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `cnblogs-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 8: Publish to 思否 (SegmentFault)

- Ensure browser closed: `playwright-cli close 2>/dev/null || true`
- Call Skill tool with `segmentfault-publisher`
- Pass the Markdown file path AND `publishTitle` as context
- Wait for completion, ensure browser closed
- Record result

### Step 9: Output Summary Report

After all platforms are processed, output a summary report:

```
============================================
发布结果汇总
============================================
✅ 51CTO       - 发布成功
✅ CSDN        - 发布成功
✅ 掘金        - 发布成功
❌ InfoQ       - 失败: element not found
✅ 腾讯云      - 发布成功
✅ 知乎        - 发布成功
✅ 博客园      - 发布成功
✅ 思否        - 发布成功
--------------------------------------------
成功: 7/8  失败: 1/8
失败平台: InfoQ
============================================
```

## Error Handling

### Single Platform Failure

If a platform publish fails:
1. Record the platform name and error reason
2. Ensure browser is closed: `playwright-cli close`
3. Continue to the next platform
4. Do NOT stop the entire process

### Browser Not Closed

Before starting each platform, ensure no leftover browser session:

```bash
playwright-cli close 2>/dev/null || true
```

### All Platforms Failed

If all 8 platforms fail, there may be a common issue (e.g., playwright-cli not installed, file path wrong). Output an error message suggesting the user check:
1. playwright-cli is installed globally
2. The Markdown file path is correct
3. Browser sessions are not stuck

## Implementation Notes for the Agent

When executing this skill, the main agent should:

1. **Extract article info & prepare content first**: Read the Markdown file to get the original title, confirm the file exists, and prepare all content formats (plain text, base64, JSON) in `/tmp/` for reuse across platforms
2. **Optimize title if needed**: If `publishTitle` is not provided, invoke `title-optimizer` skill and let user choose; otherwise use the provided `publishTitle` directly
3. **Process platforms sequentially**: Do NOT parallelize — each platform needs its own browser session
4. **51CTO first**: Start with 51CTO as it's the most error-prone platform — handle it while attention is fresh
5. **Use Skill tool for each platform**: Call the Skill tool with the appropriate publisher skill name, passing the Markdown file path AND `publishTitle` as context
6. **Close browser between platforms**: Run `playwright-cli close` after each platform completes (success or failure)
7. **Track results**: Maintain a list of results as you go (platform, success/failure, error message)
8. **Output the summary report** at the end

For each platform, the flow is:

```
playwright-cli close 2>/dev/null || true   # Cleanup any leftover session
→ Invoke Skill: <platform>-publisher       # Execute the platform-specific skill
→ playwright-cli close                      # Close browser after completion
→ Record result                             # Track success/failure
```

## Content Format Reference

The pre-prepared content files in `/tmp/`:

| File | Format | Used By |
|------|--------|---------|
| `/tmp/publish_content.md` | Plain text (no frontmatter) | All platforms as source |
| `/tmp/publish_content.json` | JSON-encoded string | cnblogs (CodeMirror.setValue) |
| `/tmp/publish_content_b64.txt` | Base64-encoded (UTF-8) | juejin, tencent (CodeMirror + TextDecoder) |
| Clipboard | Plain text (pbcopy) | csdn, infoq, zhihu, 51cto, segmentfault (paste-based) |

## Tips

1. Each platform takes 1-3 minutes to complete — total time is approximately 15-25 minutes for all 8
2. Do NOT skip the `playwright-cli close` step between platforms — leftover sessions cause issues
3. If a platform consistently fails, the user may need to re-login to that platform manually first
4. The article content is pasted from the same Markdown file for all platforms — each platform skill handles frontmatter skipping internally
5. Tags, categories, and other platform-specific settings use the defaults defined in each individual publisher skill
