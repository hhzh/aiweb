import markdownit from 'markdown-it'
import fs from 'fs'

function esc(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
}

const input = fs.readFileSync('/tmp/publish_content.md', 'utf-8')

const md = markdownit({ html: false, breaks: false })

// Headings → <p><strong>...</strong></p>
md.renderer.rules.heading_open = () => '<p><strong>'
md.renderer.rules.heading_close = () => '</strong></p>\n'

// Paragraph
md.renderer.rules.paragraph_open = () => '<p>'
md.renderer.rules.paragraph_close = () => '</p>\n'

// Code fences → one <p><code> per line
md.renderer.rules.fence = (t, i) => {
  const lines = t[i].content.split('\n')
  return lines.map(l => `<p><code>${esc(l)}</code></p>\n`).join('')
}

// Indented code block
md.renderer.rules.code_block = (t, i) => {
  const lines = t[i].content.split('\n')
  return lines.map(l => `<p><code>${esc(l)}</code></p>\n`).join('')
}

// Lists – suppress wrapper, emit list items only
md.renderer.rules.bullet_list_open   = () => ''
md.renderer.rules.bullet_list_close  = () => ''
md.renderer.rules.ordered_list_open  = () => ''
md.renderer.rules.ordered_list_close = () => ''
md.renderer.rules.list_item_open     = () => ''
md.renderer.rules.list_item_close    = () => '\n'

// Blockquotes – suppress
md.renderer.rules.blockquote_open  = () => ''
md.renderer.rules.blockquote_close = () => '\n'

// Horizontal rule
md.renderer.rules.hr = () => '<p>——</p>\n'

// Soft/hard break → space
md.renderer.rules.softbreak  = () => ' '
md.renderer.rules.hardbreak  = () => ' '

// Image → alt text only
md.renderer.rules.image = (t, i) => t[i].alt || ''

// Link → keep text, strip href
md.renderer.rules.link_open  = () => ''
md.renderer.rules.link_close = () => ''

// Tables → flatten
md.renderer.rules.table_open   = () => ''
md.renderer.rules.table_close  = () => '\n'
md.renderer.rules.thead_open   = () => ''
md.renderer.rules.thead_close  = () => ''
md.renderer.rules.tbody_open   = () => ''
md.renderer.rules.tbody_close  = () => ''
md.renderer.rules.tr_open      = () => ''
md.renderer.rules.tr_close     = () => '\n'
md.renderer.rules.th_open      = () => ''
md.renderer.rules.th_close     = () => ' '
md.renderer.rules.td_open      = () => ''
md.renderer.rules.td_close     = () => ' '

// ── Render ──
let html = md.render(input)
html = html.replace(/\n{3,}/g, '\n\n')

const output = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head><meta charset="UTF-8"></head>\n<body>\n' + html + '</body>\n</html>'

fs.writeFileSync('/tmp/publish_zhihu.html', output)
console.log(`HTML generated: ${output.length} chars`)
