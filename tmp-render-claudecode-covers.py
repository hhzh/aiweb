from pathlib import Path
import math
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path("/Users/yideng/Documents/workspace/aiweb")
SRC = ROOT / "src/claudecode"
OUT_DIR = ROOT / "src/img"
W, H = 1600, 900

FONT_CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"


def font(path, size):
    return ImageFont.truetype(path, size=size)


F_SMALL = font(FONT_CN_BOLD, 28)
F_TITLE = font(FONT_CN_BOLD, 96)
F_TITLE_SMALL = font(FONT_CN_BOLD, 82)
F_SUB = font(FONT_CN, 34)
F_CHIP = font(FONT_CN_BOLD, 23)
F_PANEL = font(FONT_CN_BOLD, 27)
F_BODY = font(FONT_CN, 23)
F_MONO = font(FONT_MONO, 24)
F_NO = font(FONT_MONO, 40)


ARTICLES = {
    "03-claude-permission-modes": {
        "title": "权限模式完全指南",
        "eyebrow": "Claude Code · Permission Modes",
        "subtitle": "从默认确认到计划模式，按风险选择最合适的执行权限。",
        "theme": "shield",
        "chips": ["默认模式", "自动编辑", "计划模式", "沙箱隔离"],
        "terminal": ["mode: plan", "ask before shell", "allow safe edits", "deny risky ops"],
        "palette": ((9, 24, 36), (30, 64, 175), (20, 184, 166), (250, 204, 21)),
    },
    "04-claude-common-workflows": {
        "title": "常见工作流",
        "eyebrow": "Claude Code · Engineering Workflows",
        "subtitle": "把探索、开发、验证串成闭环，让 AI 真正参与工程任务。",
        "theme": "workflow",
        "chips": ["代码库探索", "Bug 修复", "重构迁移", "测试验证"],
        "terminal": ["inspect repo", "trace failure", "edit files", "run checks"],
        "palette": ((8, 24, 42), (14, 116, 144), (99, 102, 241), (34, 197, 94)),
    },
    "05-claude-commands-guide": {
        "title": "斜杠命令实战",
        "eyebrow": "Claude Code · Slash Commands",
        "subtitle": "用一行命令完成会话管理、诊断、配置与上下文控制。",
        "theme": "commands",
        "chips": ["/clear", "/help", "/model", "/doctor"],
        "terminal": ["/init", "/context", "/agents", "/permissions"],
        "palette": ((13, 21, 38), (124, 58, 237), (6, 182, 212), (244, 114, 182)),
    },
    "06-claude-hooks-tutorial": {
        "title": "Hooks 实战教程",
        "eyebrow": "Claude Code · Automation Hooks",
        "subtitle": "监听工具调用与会话事件，把安全拦截和流程自动化前置。",
        "theme": "hooks",
        "chips": ["PreToolUse", "PostToolUse", "SessionStart", "Stop"],
        "terminal": ["event received", "run policy check", "format code", "continue flow"],
        "palette": ((20, 22, 36), (190, 24, 93), (249, 115, 22), (45, 212, 191)),
    },
    "07-claude-mcp-guide": {
        "title": "MCP 使用教程",
        "eyebrow": "Claude Code · Model Context Protocol",
        "subtitle": "连接 GitHub、数据库、设计工具与外部服务，打通工作流边界。",
        "theme": "mcp",
        "chips": ["GitHub", "PostgreSQL", "Figma", "Sentry"],
        "terminal": ["connect server", "list tools", "call resource", "sync result"],
        "palette": ((5, 25, 47), (37, 99, 235), (16, 185, 129), (168, 85, 247)),
    },
    "08-claude-skills-guide": {
        "title": "Skills 使用教程",
        "eyebrow": "Claude Code · Reusable Skills",
        "subtitle": "把高频提示、团队规范和专项流程封装成可复用技能。",
        "theme": "skills",
        "chips": ["技能描述", "按需加载", "团队规范", "复用流程"],
        "terminal": ["load skill card", "read instructions", "execute workflow", "save pattern"],
        "palette": ((10, 31, 34), (5, 150, 105), (14, 165, 233), (250, 204, 21)),
    },
    "09-claude-subagent-guide": {
        "title": "子代理使用指南",
        "eyebrow": "Claude Code · Subagents",
        "subtitle": "用独立上下文拆分复杂任务，让审查、调试和实现并行推进。",
        "theme": "subagents",
        "chips": ["主代理", "代码审查", "调试专家", "结果汇总"],
        "terminal": ["spawn reviewer", "spawn debugger", "merge findings", "ship patch"],
        "palette": ((12, 23, 45), (79, 70, 229), (34, 211, 238), (132, 204, 22)),
    },
    "10-claude-memory-configuration": {
        "title": "内存配置文档",
        "eyebrow": "Claude Code · Memory Configuration",
        "subtitle": "用 CLAUDE.md 与自动记忆沉淀项目经验，跨会话保持一致。",
        "theme": "memory",
        "chips": ["CLAUDE.md", "自动记忆", "项目规范", "会话启动"],
        "terminal": ["load project notes", "remember workflow", "apply convention", "reduce repeat"],
        "palette": ((18, 26, 43), (147, 51, 234), (20, 184, 166), (251, 191, 36)),
    },
    "11-claude-directory-configuration": {
        "title": ".claude 目录配置",
        "eyebrow": "Claude Code · Directory Configuration",
        "subtitle": "理清 settings、skills、agents、commands 的位置与优先级。",
        "theme": "directory",
        "chips": ["settings.json", "CLAUDE.md", "skills/", "agents/"],
        "terminal": [".claude/", "  settings.json", "  commands/", "  skills/"],
        "palette": ((10, 25, 48), (2, 132, 199), (34, 197, 94), (251, 146, 60)),
    },
    "12-claude-extensions-guide": {
        "title": "扩展选型与配置",
        "eyebrow": "Claude Code · Extensions",
        "subtitle": "在 Skills、Subagents、MCP、Hooks 与 Plugins 之间做正确取舍。",
        "theme": "extensions",
        "chips": ["Skills", "Subagents", "MCP", "Plugins"],
        "terminal": ["choose extension", "control context", "compose workflow", "avoid conflict"],
        "palette": ((13, 25, 41), (8, 145, 178), (168, 85, 247), (34, 197, 94)),
    },
    "13-claude-plugins-guide": {
        "title": "插件使用教程",
        "eyebrow": "Claude Code · Plugins",
        "subtitle": "把命令、技能、代理和工具打包成可安装的扩展单元。",
        "theme": "plugins",
        "chips": ["Commands", "Skills", "Agents", "Hooks"],
        "terminal": ["install plugin", "enable package", "load components", "share workflow"],
        "palette": ((20, 23, 39), (217, 70, 239), (14, 165, 233), (245, 158, 11)),
    },
    "14-claude-best-practices": {
        "title": "最佳实践",
        "eyebrow": "Claude Code · Best Practices",
        "subtitle": "围绕上下文、提示、权限和验证，建立高效安全的 AI 开发习惯。",
        "theme": "best",
        "chips": ["精准上下文", "先计划", "小步验证", "权限可控"],
        "terminal": ["reference files", "write a plan", "test each step", "review changes"],
        "palette": ((13, 25, 37), (22, 163, 74), (59, 130, 246), (250, 204, 21)),
    },
}


def lerp(a, b, t):
    return int(a + (b - a) * t)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def rounded_layer(base, xy, radius, fill, outline=None, shadow=True):
    if shadow:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(layer)
        x1, y1, x2, y2 = xy
        sd.rounded_rectangle((x1, y1 + 18, x2, y2 + 18), radius=radius, fill=(0, 0, 0, 82))
        base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=1)
    return d


def make_background(palette):
    c1, c2, c3, c4 = palette
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        ty = y / (H - 1)
        for x in range(W):
            tx = x / (W - 1)
            t = ty * 0.62 + tx * 0.38
            if t < 0.55:
                k = t / 0.55
                col = tuple(lerp(c1[i], c2[i], k) for i in range(3))
            else:
                k = (t - 0.55) / 0.45
                col = tuple(lerp(c2[i], c1[i], k * 0.55) for i in range(3))
            px[x, y] = col
    img = img.convert("RGBA")
    for cx, cy, r, color in [(230, 110, 430, c2), (1380, 170, 360, c3), (1180, 820, 340, c4)]:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for rr in range(r, 0, -10):
            a = int(62 * (1 - rr / r) ** 1.8)
            gd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(*color, a))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 50):
        d.line((x, 0, x, H), fill=(255, 255, 255, 18), width=1)
    for y in range(0, H, 50):
        d.line((0, y, W, y), fill=(255, 255, 255, 18), width=1)
    return img


def draw_top(draw, no, meta, palette):
    draw.rounded_rectangle((88, 76, 146, 134), radius=16, fill=(8, 20, 39, 190), outline=(*palette[2], 120), width=1)
    draw.text((105, 86), ">", font=F_NO, fill=(*palette[2], 255))
    draw.text((164, 90), meta["eyebrow"], font=F_SMALL, fill=(210, 235, 255, 255))
    draw.text((1394, 88), f"#{no}", font=F_NO, fill=(255, 255, 255, 150))


def wrap_title(title):
    if len(title) <= 8:
        return [title]
    if "与" in title and len(title) > 9:
        left, right = title.split("与", 1)
        return [left, "与" + right]
    for key in ["使用", "配置", "实战", "完全"]:
        idx = title.find(key)
        if idx > 1:
            return [title[:idx], title[idx:]]
    mid = len(title) // 2
    return [title[:mid], title[mid:]]


def draw_title(draw, meta):
    draw.text((88, 206), "Claude Code", font=F_TITLE, fill=(139, 233, 253, 255))
    lines = wrap_title(meta["title"])
    y = 326
    fnt = F_TITLE if max(len(x) for x in lines) <= 9 else F_TITLE_SMALL
    for line in lines:
        draw.text((88, y), line, font=fnt, fill=(248, 251, 255, 255))
        y += 110 if fnt == F_TITLE else 96
    draw.text((92, 592), meta["subtitle"][:21], font=F_SUB, fill=(217, 233, 246, 255))
    draw.text((92, 642), meta["subtitle"][21:], font=F_SUB, fill=(217, 233, 246, 255))


def draw_terminal(img, meta, palette):
    d = rounded_layer(img, (948, 122, 1508, 620), 8, (4, 11, 22, 224), (148, 214, 255, 65))
    d.rounded_rectangle((948, 122, 1508, 170), radius=8, fill=(255, 255, 255, 20))
    d.rectangle((948, 154, 1508, 170), fill=(255, 255, 255, 20))
    for i, c in enumerate([(251, 113, 133), (250, 204, 21), (52, 211, 153)]):
        d.ellipse((966 + i * 24, 140, 979 + i * 24, 153), fill=c)
    y = 210
    d.text((980, y), "$", font=F_MONO, fill=(*palette[2], 255))
    d.text((1006, y), "claude", font=F_MONO, fill=(248, 250, 252, 255))
    y += 52
    for line in meta["terminal"]:
        d.text((980, y), "OK", font=F_MONO, fill=(134, 239, 172, 255))
        d.text((1022, y), line, font=F_MONO, fill=(210, 231, 244, 255))
        y += 45
    y += 18
    d.text((980, y), "status", font=F_MONO, fill=(*palette[2], 255))
    d.text((1074, y), "ready for workflow", font=F_MONO, fill=(147, 169, 186, 255))


def draw_chips(img, meta, palette):
    d = rounded_layer(img, (1018, 686, 1488, 832), 8, (9, 23, 39, 188), (255, 255, 255, 42))
    d.text((1048, 714), "核心能力地图", font=F_PANEL, fill=(224, 242, 254, 255))
    for idx, chip in enumerate(meta["chips"]):
        x = 1048 + (idx % 2) * 220
        y = 764 + (idx // 2) * 48
        d.rounded_rectangle((x, y, x + 186, y + 38), radius=8, fill=(*palette[1], 45), outline=(*palette[2], 80), width=1)
        tw, _ = text_size(d, chip, F_CHIP)
        d.text((x + (186 - tw) / 2, y + 6), chip, font=F_CHIP, fill=(231, 255, 255, 255))


def draw_theme_icon(img, meta, palette):
    d = ImageDraw.Draw(img)
    cx, cy = 730, 770
    color = (*palette[2], 230)
    faint = (*palette[2], 70)
    if meta["theme"] == "shield":
        pts = [(cx, cy - 70), (cx + 82, cy - 36), (cx + 66, cy + 56), (cx, cy + 96), (cx - 66, cy + 56), (cx - 82, cy - 36)]
        d.polygon(pts, outline=color, fill=(*palette[1], 45))
        d.line((cx, cy - 38, cx, cy + 56), fill=color, width=5)
        d.line((cx - 34, cy + 8, cx - 8, cy + 34, cx + 42, cy - 24), fill=(134, 239, 172, 240), width=7)
    elif meta["theme"] == "workflow":
        for i, label in enumerate(["理解", "行动", "验证"]):
            x = cx - 190 + i * 160
            d.rounded_rectangle((x, cy - 34, x + 118, cy + 34), radius=8, outline=color, fill=(*palette[1], 45), width=2)
            tw, _ = text_size(d, label, F_CHIP)
            d.text((x + (118 - tw) / 2, cy - 15), label, font=F_CHIP, fill=(232, 255, 255, 255))
            if i < 2:
                d.line((x + 122, cy, x + 154, cy), fill=color, width=5)
                d.polygon([(x + 154, cy), (x + 140, cy - 10), (x + 140, cy + 10)], fill=color)
    elif meta["theme"] == "commands":
        for i, cmd in enumerate(["/clear", "/help", "/doctor"]):
            y = cy - 68 + i * 52
            d.text((cx - 150, y), cmd, font=F_MONO, fill=(248, 250, 252, 230))
            d.line((cx + 10, y + 18, cx + 150, y + 18), fill=faint, width=4)
    elif meta["theme"] == "hooks":
        for a in range(0, 360, 60):
            r = math.radians(a)
            x = cx + math.cos(r) * 90
            y = cy + math.sin(r) * 72
            d.line((cx, cy, x, y), fill=faint, width=3)
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=color)
        d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), outline=color, width=5)
    elif meta["theme"] == "mcp":
        for i in range(4):
            ang = math.radians(45 + i * 90)
            x = cx + math.cos(ang) * 110
            y = cy + math.sin(ang) * 82
            d.line((cx, cy, x, y), fill=faint, width=4)
            d.rounded_rectangle((x - 42, y - 28, x + 42, y + 28), radius=8, outline=color, fill=(*palette[1], 45), width=2)
        d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=color, width=5)
    elif meta["theme"] == "skills":
        for i in range(3):
            d.rounded_rectangle((cx - 110 + i * 58, cy - 64 + i * 26, cx + 80 + i * 58, cy + 12 + i * 26), radius=8, outline=color, fill=(*palette[1], 35), width=2)
        d.text((cx - 58, cy - 18), "SKILL", font=F_MONO, fill=(248, 250, 252, 230))
    elif meta["theme"] == "subagents":
        d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), outline=color, width=5)
        for i, label in enumerate(["A", "B", "C"]):
            x = cx - 150 + i * 150
            y = cy + 96
            d.line((cx, cy + 40, x, y - 20), fill=faint, width=4)
            d.ellipse((x - 30, y - 30, x + 30, y + 30), outline=color, width=4)
            d.text((x - 9, y - 18), label, font=F_NO, fill=(248, 250, 252, 230))
    elif meta["theme"] == "memory":
        for i in range(5):
            y = cy - 82 + i * 38
            d.rounded_rectangle((cx - 140, y, cx + 140, y + 24), radius=12, outline=faint, fill=(*palette[1], 30), width=2)
        d.text((cx - 74, cy - 18), "MEMORY", font=F_MONO, fill=(248, 250, 252, 230))
    elif meta["theme"] == "directory":
        d.text((cx - 128, cy - 94), ".claude/", font=F_MONO, fill=(248, 250, 252, 230))
        for i, name in enumerate(["settings.json", "skills/", "agents/", "commands/"]):
            y = cy - 42 + i * 38
            d.line((cx - 108, y + 15, cx - 70, y + 15), fill=faint, width=3)
            d.text((cx - 62, y), name, font=F_BODY, fill=(218, 236, 247, 240))
    elif meta["theme"] == "extensions":
        for i in range(6):
            a = math.radians(i * 60)
            x = cx + math.cos(a) * 110
            y = cy + math.sin(a) * 86
            d.ellipse((x - 24, y - 24, x + 24, y + 24), outline=color, width=3)
            d.line((cx, cy, x, y), fill=faint, width=3)
        d.rounded_rectangle((cx - 48, cy - 32, cx + 48, cy + 32), radius=12, outline=color, fill=(*palette[1], 45), width=3)
    elif meta["theme"] == "plugins":
        for x, y in [(cx - 70, cy - 54), (cx + 14, cy - 54), (cx - 70, cy + 30), (cx + 14, cy + 30)]:
            d.rounded_rectangle((x, y, x + 70, y + 70), radius=10, outline=color, fill=(*palette[1], 45), width=3)
        d.line((cx, cy - 18, cx, cy + 28), fill=faint, width=4)
        d.line((cx - 28, cy + 10, cx + 42, cy + 10), fill=faint, width=4)
    else:
        for i, label in enumerate(["Context", "Prompt", "Verify"]):
            y = cy - 68 + i * 58
            d.rounded_rectangle((cx - 150, y, cx + 150, y + 38), radius=8, outline=color, fill=(*palette[1], 42), width=2)
            d.text((cx - 120, y + 6), label, font=F_CHIP, fill=(248, 250, 252, 230))


def render(slug, meta):
    no = slug.split("-", 1)[0]
    img = make_background(meta["palette"])
    d = ImageDraw.Draw(img)
    draw_top(d, no, meta, meta["palette"])
    draw_title(d, meta)
    draw_theme_icon(img, meta, meta["palette"])
    draw_terminal(img, meta, meta["palette"])
    draw_chips(img, meta, meta["palette"])
    edge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.rectangle((0, 0, W, H), outline=(0, 0, 0, 58), width=34)
    img.alpha_composite(edge.filter(ImageFilter.GaussianBlur(30)))
    out = OUT_DIR / f"{slug}.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for md in sorted(SRC.glob("[0-9][0-9]-*.md")):
        slug = md.stem
        if slug in ARTICLES:
            written.append(render(slug, ARTICLES[slug]))
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
